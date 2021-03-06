import os
from tests.config_test import BaseTestCase
from app.actions import multiplayer
from sqlalchemy.orm.exc import NoResultFound
from app.constants import US_TIMEZONES, Statuses
from app.models import AppUser, Team, TeamMember

class TestMultiplayer(BaseTestCase):
    inviter_number = os.environ.get('TEST_FROM_NUMBER')
    secondary_number = os.environ.get('TEST_TO_NUMBER')

    def setUp(self):
        super().setUp()

        self.mitch = AppUser(
            phone_number=self.inviter_number, 
            username='mitch',
            timezone=US_TIMEZONES['b'])
        self.db.session.add(self.mitch)

        self.billy = AppUser(
            phone_number=self.secondary_number, 
            username='billy',
            timezone=US_TIMEZONES['b'])
        self.db.session.add(self.billy)

        self.team = Team(
            founder = self.mitch,
            name = 'The Cherrys')
        self.db.session.add(self.team)

        self.mitch_member = TeamMember(
            user = self.mitch,
            team = self.team,
            inviter = self.mitch,
            status = Statuses.ACTIVE)       
        self.db.session.add(self.mitch_member)

        self.billy_member = TeamMember(
            user = self.billy,
            team = self.team,
            inviter = self.mitch,
            status = Statuses.PENDING)       
        self.db.session.add(self.billy_member)

        self.db.session.commit()

        self.mitch = self.mitch.to_dict()
        self.billy = self.billy.to_dict()
        self.team = self.team.to_dict()
    
    def test_leave_team(self):
        valid_inbound = self.team['id']
        invalid_inbound = '999'
        # test correct team id, and incorrect team id
        multiplayer.leave_team(self.mitch, valid_inbound)

        self.assertRaises(
            NoResultFound,
            multiplayer.leave_team,
            self.mitch, 
            invalid_inbound)

    def test_join_team_existing_user(self):
        '''Test the ability to join a team as an existing user'''
        member = multiplayer.respond_to_invite(self.billy, 'yes')

        assert member.status == Statuses.ACTIVE


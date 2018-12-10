from datetime import datetime as dt
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import postgresql
from app import db


class Base:
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=func.now(), server_default=func.now())
    updated = db.Column(db.DateTime, nullable=False, default=func.now(), server_default=func.now(), onupdate=func.current_timestamp())

Base = declarative_base(cls=Base)


class AppUser(db.Model, Base):
    username = db.Column(db.String(64), default='NEW_USER')
    phone_number = db.Column(db.String(32), unique=True, nullable=False)
    timezone = db.Column(db.String(32))

    def to_dict(self):
        return dict(
            id = self.id, 
            username = self.username,
            phone_number = self.phone_number,
            timezone = self.timezone,
            created = self.created
        )

    def __repr__(self):
        return '<AppUser %r>' % self.phone_number


class Notification(db.Model, Base):
    router_id = db.Column(db.String(32), nullable=False)
    body = db.Column(db.Text, nullable=False)
    day_of_week = db.Column(db.String(32)) 
    hour = db.Column(db.Integer, nullable=False)
    minute = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'),
        nullable=False)
    user = db.relationship('AppUser',
        backref=db.backref('notifications', lazy=True))

    # def to_cron(self):
    #     '''return only values needed for cron job'''
    #     return dict(
    #         day_of_week = self.day_of_week, 
    #         hour = self.hour,
    #         minute = self.minute,
    #         jitter = self.jitter,
    #         end_date = self.end_date,
    #         timezone = self.timezone
    #     )
    
    def to_dict(self):
        return dict(
            router_id = self.router_id,
            body = self.body,
            day_of_week = self.day_of_week, 
            hour = self.hour,
            minute = self.minute,
            active = self.active)


    def __repr__(self):
        return '<Notification %r>' % self.router_id


class Exchange(db.Model, Base):
    router = db.Column(db.String(32), nullable=False)
    outbound = db.Column(db.String(612))
    inbound = db.Column(db.String(612))
    confirmation = db.Column(db.String(64))
    next_router = db.Column(db.String(32))
    next_exchange_id = db.Column(db.Integer) # this needs to be nullable because it is not known when an exchange is first created

    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'),
        nullable=False)
    user = db.relationship('AppUser',
        backref=db.backref('exchanges', lazy=True))
    
    def to_dict(self):
        return dict(
            id = self.id,
            router = self.router, 
            outbound = self.outbound,
            inbound = self.inbound,
            confirmation = self.confirmation,
            next_router = self.next_router,
            next_exchange_id = self.next_exchange_id,
            user_id = self.user_id,
            created = self.created,
            updated = sel.updated
        )
    
    def __repr__(self):
        return '<Exchange %r>' % self.router
    

class Point(db.Model, Base):
    value = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'),
        nullable=False)
    user = db.relationship('AppUser',
        backref=db.backref('points', lazy=True))
    
    def __repr__(self):
        return f'<Point user={self.user_id}; value={self.value} >'


class Task(db.Model, Base):
    description = db.Column(db.String(612), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    exchange_id = db.Column(db.Integer, db.ForeignKey('exchange.id'), nullable=False)
    exchange = db.relationship('Exchange', backref=db.backref('tasks', lazy=True))

    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    user = db.relationship('AppUser', backref=db.backref('tasks', lazy=True))
    
    def __repr__(self):
        return f'<Task {self.description[10]} >'

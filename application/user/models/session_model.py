import binascii
import os
from application.database import db


class Session(db.Model):
    __tablename__ = 'session'

    user_id = db.Column(db.Float, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship("User", back_populates="session")
    token = db.Column(db.String())
    expiration = db.Column(db.Date())

    def __init__(self, user_id_, expiration):
        self.user_id = user_id_
        self.expiration = expiration
        self.token = self.__generate_key__()

    def __repr__(self):
        return '<token {}>'.format(self.token)

    def serialize(self):
        return {'token': self.token}

    @staticmethod
    def __generate_key__():
        return binascii.hexlify(os.urandom(20)).decode()

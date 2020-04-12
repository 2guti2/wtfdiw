from application.database import db


class Session(db.Model):
    __tablename__ = 'session'

    user_id = db.Column(db.Float, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship("User", back_populates="session")
    token = db.Column(db.String())
    expiration = db.Column(db.Date())

    def __init__(self, user_id_, token, expiration):
        self.user_id = user_id_
        self.token = token
        self.expiration = expiration

    def __repr__(self):
        return '<token {}>'.format(self.token)

    def serialize(self):
        return {'token': self.token}

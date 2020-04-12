from application.database import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Float, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    profile_pic = db.Column(db.String())
    session = db.relationship("Session", uselist=False, back_populates="user")

    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.session = None

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'profile_pic': self.profile_pic
        }

class UserService:
    def __init__(self, db, User):
        self.db = db
        self.User = User

    def create_or_update(self, user_data):
        unique_id, users_name, users_email, picture = user_data
        user_ins = self.User(
            id_=unique_id, name=users_name, email=users_email, profile_pic=picture
        )

        exists = self.User.query.filter_by(id=unique_id).first() is not None
        if not exists:
            self.db.session.add(user_ins)
            self.db.session.commit()
        else:
            # TODO: this is not right
            self.User.query.filter_by(id=unique_id).update(user_ins.serialize())
            self.db.session.commit()

        return user_ins

    def get_all(self):
        return self.User.query.all()

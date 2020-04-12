class UserService:

    @staticmethod
    def create_or_update(db, User, user_data):
        unique_id, users_name, users_email, picture = user_data
        user_ins = User(
            id_=unique_id, name=users_name, email=users_email, profile_pic=picture
        )

        exists = User.query.filter_by(id=unique_id).first() is not None
        if not exists:
            db.session.add(user_ins)
            db.session.commit()
        else:
            User.query.filter_by(id=unique_id).update(user_ins.serialize())
            db.session.commit()

        return user_ins

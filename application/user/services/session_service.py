class SessionService:

    @staticmethod
    def new_session(code, args):
        app, json, db, Session, User, OauthService, UserService, oauth, request, requests = args
        unique_id, users_name, users_email, picture = \
            OauthService.get_user_info_from_google(code, (app, json, oauth, request, requests))

        user_ins = UserService.create_or_update(db, User, (
            unique_id, users_name, users_email, picture
        ))
        session_ins = SessionService.create_or_update(db, Session, unique_id)

        return {**user_ins.serialize(), **session_ins.serialize()}

    @staticmethod
    def create_or_update(db, Session, user_id):
        session_ins = Session.query.filter_by(user_id=user_id).first()
        exists = session_ins is not None
        if not exists:
            session_ins = Session(user_id_=user_id, expiration=None)
            db.session.add(session_ins)
            db.session.commit()
        return session_ins

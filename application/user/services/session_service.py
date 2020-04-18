class SessionService:
    def __init__(self, db, Session, User, google_service, user_service):
        self.db = db
        self.Session = Session
        self.User = User
        self.google_service = google_service
        self.user_service = user_service

    def new_session(self, code, request_info):
        unique_id, users_name, users_email, picture = \
            self.google_service.get_user_info(code, request_info)

        user_ins = self.user_service.create_or_update((
            unique_id, users_name, users_email, picture
        ))
        session_ins = self.create_or_update(unique_id)

        return {**user_ins.json_serialize(), **session_ins.serialize()}

    def create_or_update(self, user_id):
        session_ins = self.Session.query.filter_by(user_id=user_id).first()
        exists = session_ins is not None
        if not exists:
            session_ins = self.Session(user_id_=user_id, expiration=None)
            self.db.session.add(session_ins)
            self.db.session.commit()
        return session_ins

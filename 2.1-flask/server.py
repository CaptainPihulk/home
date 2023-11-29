from app import get_app
from flask import request, jsonify
from flask.views import MethodView
from db import User, Ad, Token, Session
from auth import check_password, hash_password, check_auth
from schema import RegisterUser, LoginUser, UserData, CreateAd, validate, AdData
from sqlalchemy.exc import IntegrityError
from errors import HttpError

app = get_app()


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    http_response = jsonify({'status': 'error', 'description': error.message})
    http_response.status_code = error.status_code
    return http_response


def get_user(user_id: int, session: Session):
    user = session.query(User).get(user_id)
    if user is None:
        raise HttpError(404, 'user not found')
    return user


def user_register():
    json_data = validate(RegisterUser, request.json)
    json_data['password'] = hash_password(json_data['password'])
    with Session() as session:
        new_user = User(**json_data)
        session.add(new_user)
        try:
            session.commit()
        except IntegrityError:
            raise HttpError(409, 'User already exists!')
        return jsonify(
            {'id': new_user.id}
        )


def login():
    login_data = validate(LoginUser, request.json)
    with Session() as session:
        user = session.query(User).filter(User.email_address == login_data["email_address"]).first()
        if user is None or not check_password(user.password, login_data["password"]):
            raise HttpError(401, "Invalid user or password")

        token = Token(user=user)
        session.add(token)
        session.commit()
        return jsonify({"token": token.id})


class UserView(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            return jsonify({'id': user.id, 'user name': user.name,
                            'ads headers': [ad.ad_header for ad in user.ads]})

    def delete(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            token = check_auth(session)
            if token.user_id != user.id:
                raise HttpError(403, "You need to log in to delete")
            session.delete(user)
            session.commit()
            return jsonify({'status': 'User and all his ads are deleted'})

    def patch(self, user_id: int):
        with Session() as session:
            data_to_change = validate(UserData, request.json)
            if 'password' in data_to_change:
                data_to_change['password'] = hash_password(data_to_change['password'])
            token = check_auth(session)
            user = get_user(user_id, session)
            if token.user_id != user.id:
                raise HttpError(403, "You need to log in to chage any data")
            for field, value in data_to_change.items():
                setattr(user, field, value)
            session.add(user)
            session.commit()
        return jsonify({'status': 'fields successfully changed'})


app.add_url_rule('/register', view_func=user_register, methods=['POST'])
app.add_url_rule('/login', view_func=login, methods=['POST'])
app.add_url_rule('/user/<int:user_id>', view_func=UserView.as_view('user_by_id'), methods=['GET', 'DELETE', 'PATCH'])


def get_ad(ad_id: int, session: Session):
    ad = session.query(Ad).get(ad_id)
    if ad is None:
        raise HttpError(404, f'ad with id {ad_id} not found')
    return ad


class AdView(MethodView):

    def get(self, ad_id: int):
        with Session() as session:
            ad = get_ad(ad_id, session)
            return jsonify({'ad id': ad.id, 'ad header': ad.ad_header, 'creation date': ad.creation_date,
                            'user name': ad.user.name})

    def post(self):
        json_data = validate(CreateAd, request.json)
        with Session() as session:
            new_ad = Ad(**json_data)
            token = check_auth(session)
            if token.user_id != new_ad.owner_id:
                raise HttpError(403, "You must be logged in to post an ad.")
            session.add(new_ad)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'ad with the same header or description already exists!')
            return jsonify(
                {'id': new_ad.id, 'adv_header': new_ad.ad_header,
                 'creation_date': new_ad.creation_date.isoformat(),
                 'owner_id': new_ad.owner_id}
            )

    def patch(self, ad_id: int):
        json_data = validate(AdData, request.json)
        with Session() as session:
            token = check_auth(session)
            ad = get_ad(ad_id, session)
            if token.user_id != ad.owner_id:
                raise HttpError(403, "You need to be owner to chage the add")
            for field, value in json_data.items():
                setattr(ad, field, value)
            session.add(ad)
            session.commit()
        return jsonify({'status': 'fields successfully changed'})

    def delete(self, ad_id: int):
        with Session() as session:
            token = check_auth(session)
            ad = get_ad(ad_id, session)
            if token.user_id != ad.owner_id:
                raise HttpError(403, "You need to be owner to chage the add")
            session.delete(ad)
            session.commit()
            return jsonify({'status': f'ad with id {ad_id} is deleted'})


app.add_url_rule('/ads/<int:ad_id>', view_func=AdView.as_view('ad_by_id'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/ads', view_func=AdView.as_view('new_ad'), methods=['POST'])

app.run(port=5000)

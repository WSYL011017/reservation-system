from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv
from app.models.users import User


load_dotenv()
bp = Blueprint('main', __name__)

WEIXIN_APPID = os.getenv('WEIXIN_APPID')
WEIXIN_APPSECRET = os.getenv('WEIXIN_APPSECRET')


@bp.route('/')
def index():
    return 'Hello, World!'

@bp.route('/getcode', methods=['POST'])
def getcode():
    data = request.get_json()
    print(data)
    code = data['code']
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid={WEIXIN_APPID}&secret={WEIXIN_APPSECRET}&js_code={code}&grant_type=authorization_code'
    response = requests.get(url)
    print(response.json())
    session_key = response.json()['session_key']
    openid = response.json()['openid']

    user = User.query.filter_by(openid=openid).one_or_none()
    if user is None:
        User.create_user()
        



    return jsonify(response.json())



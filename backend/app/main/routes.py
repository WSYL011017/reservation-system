from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv
from requests.api import head
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
    getaccess_token = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WEIXIN_APPID}&secret={WEIXIN_APPSECRET}'
    res = requests.get(url=getaccess_token)
    resbody = response.json()
    resbody.update(res.json())
    return jsonify(resbody)



@bp.route('/getPhoneNumber', methods=['POST'])
def getPhoneNumber():
    body = request.get_json()
    ACCESS_TOKEN = body['token']['access_token']
    url = f'https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token={ACCESS_TOKEN}'
    print(url)
    data = {
        "code": body['code']
    }
    print(data)
    res = requests.post(url=url, json=data,headers={'Content-Type': 'application/json'})
    print(res.json())
    return jsonify(res.json())



from flask import Blueprint, request, jsonify

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return 'Hello, World!'

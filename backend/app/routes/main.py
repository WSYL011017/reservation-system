from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.before_request
def before_request():
    print('Before request')

@bp.after_request
def after_request(response):
    print('After request')
    return response

@bp.teardown_request
def teardown_request(exception):
    print('Teardown request')

@bp.route('/status')
def status():
    return 'Everything is OK', 200

@bp.errorhandler(404)
def not_found(error):
    return 'Page not found', 404
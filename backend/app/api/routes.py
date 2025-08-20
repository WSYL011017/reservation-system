from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db

bp = Blueprint('api', __name__)

@bp.route('/posts', methods=['GET'])
def get_posts():
    """获取所有文章"""
    pass

@bp.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    """获取单篇文章"""
    pass

@bp.route('/posts', methods=['POST'])
@login_required
def create_post():
    """创建新文章"""
    data = request.get_json()
    
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': '标题和内容不能为空'}), 400
    
    db.session.commit()
    
    return jsonify(), 201

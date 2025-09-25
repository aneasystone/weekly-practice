from flask import Blueprint

# 创建 Blueprint
user_bp = Blueprint('user', __name__, url_prefix='/user')

# 定义路由
@user_bp.route('/profile')
def profile():
    return 'user profile'

@user_bp.route('/settings')
def settings():
    return 'user settings'

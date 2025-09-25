from flask import Blueprint
from flask_restx import Api, Namespace, Resource, fields

# 创建 Blueprint 和 API
bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(bp, doc='/docs')  # 启用 Swagger UI

# 创建命名空间
user_ns = Namespace('users', description='用户管理相关操作')

# 定义数据模型
user_model = user_ns.model('User', {
    'id': fields.Integer(description='用户ID'),
    'name': fields.String(required=True, description='用户名')
})

# 定义 API 资源
@user_ns.route('/')
class UserList(Resource):
    @user_ns.doc('get_users')
    @user_ns.marshal_list_with(user_model)
    def get(self):
        """获取用户列表"""
        return []

    @user_ns.doc('create_user')
    @user_ns.expect(user_model)
    def post(self):
        """创建新用户"""
        return {"message": "用户创建成功"}, 201

# 注册命名空间
api.add_namespace(user_ns, path='/users')

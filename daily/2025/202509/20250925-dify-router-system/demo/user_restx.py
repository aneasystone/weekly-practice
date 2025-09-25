from flask import Blueprint
from flask_restx import Api, Resource

# 创建 Blueprint 和 API
bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(bp, doc='/docs')  # 启用 Swagger UI

# 定义 API 资源
class UserResource(Resource):

    def get(self):
        """获取用户列表"""
        return []

    def post(self):
        """创建新用户"""
        return {"message": "用户创建成功"}, 201

# 注册资源
api.add_resource(UserResource, '/users')

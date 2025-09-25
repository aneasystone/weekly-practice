# 创建应用
from flask import Flask
app = Flask(__name__)

# 注册 Blueprint
from user_restx import bp
app.register_blueprint(bp)

# print(app.url_map)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6001)

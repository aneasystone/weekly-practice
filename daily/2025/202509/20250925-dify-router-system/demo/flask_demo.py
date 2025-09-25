# 创建应用
from flask import Flask
app = Flask(__name__)

# 注册路由
@app.route('/user/profile')
def user_profile():
    return 'user profile'

@app.route('/user/settings')
def user_settings():
    return 'user settings'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6001)
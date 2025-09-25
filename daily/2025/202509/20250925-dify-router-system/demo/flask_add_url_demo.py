# 创建应用
from flask import Flask
app = Flask(__name__)

def user_profile():
    return 'user profile'

def user_settings():
    return 'user settings'

# 手动注册路由
app.add_url_rule('/user/prifile', 'user_profile', user_profile)
app.add_url_rule('/user/settings', 'user_settings', user_settings)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6001)
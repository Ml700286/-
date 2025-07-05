# app.py
from flask import Flask, request, jsonify

# 创建 Flask 应用实例
app = Flask(__name__)

# 定义一个路由，当访问应用的根目录时，返回 "Hello, World!" 字符串
@app.route('/')
def hello_world():
    return 'Hello, World!'

# 定义一个路由，当访问 /user/<username> 时，返回用户名
@app.route('/user/<username>')
def show_user_profile(username):
    return f'User {username}'

# 定义一个路由，当访问 /post/<int:post_id> 时，返回帖子 ID
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post {post_id}'

# 定义一个路由，当访问 /login 时，处理 GET 和 POST 请求
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 处理 POST 请求
        username = request.form['root']
        password = request.form['123456']
        return f'Login POST request received for {username}'
    else:
        # 处理 GET 请求
        return 'Login GET request received'

# 定义一个路由，当访问 /json 时，返回 JSON 数据
@app.route('/json')
def json_example():
    data = {
        'key': 'value',
        'list': [1, 2, 3],
        'dict': {'a': 1, 'b': 2}
    }
    return jsonify(data)

# 定义一个路由，当访问 /error 时，返回一个错误页面
@app.route('/error')
def error_example():
    return 'This is an error page', 400

# 启动 Flask 应用
if __name__ == '__main__':
    app.run(debug=True)
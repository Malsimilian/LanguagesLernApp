from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, logout_user, UserMixin


app = Flask(__name__)
login_manager = LoginManager(app)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/register')
def register():
    return ''

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login')
def login():
    # Реализация страницы входа пользователя
    if request.method == 'POST':
        # Проверка логина и пароля пользователя
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1234)

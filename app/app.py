from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from data import db_session
from data.users import User
from data.lessons import Lesson
from data.courses import Course
from forms.login import LoginForm
from forms.user import RegisterForm
from forms.course import CourseForm
from forms.lesson import LessonForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            is_author=form.role.data == 'teacher' or form.role.data == 'Teacher'
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Course).filter(Course.name == form.name.data).first():
            return render_template('create_course.html', title='create_course',
                                   form=form,
                                   message="Такой курс уже есть")
        course = Course(
            name=form.name.data,
            language=form.language.data,
            author_id=current_user.id
        )
        db_sess.add(course)
        db_sess.commit()
        return redirect('/my_courses')
    return render_template('create_course.html', title='create_course', form=form)


@login_required
@app.route('/my_courses')
def my_courses():
    db_sess = db_session.create_session()
    courses = db_sess.query(Course).filter(Course.author_id == current_user.id)
    return render_template("my_courses.html", courses=courses)


@login_required
@app.route('/my_course/<int:id>')
def my_course(id):
    db_sess = db_session.create_session()
    course = db_sess.query(Course).filter(Course.id == id).first()
    lessons = db_sess.query(Lesson).filter(Lesson.course_id == id)
    return render_template("my_course.html", course=course, lessons=lessons)


@login_required
@app.route('/add_lesson/<int:course_id>', methods=['GET', 'POST'])
def add_lesson(course_id):
    form = LessonForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Course).filter(Course.name == form.name.data).first():
            return render_template('add_lesson.html', title='add_lesson',
                                   form=form,
                                   message="Такой урок уже есть")
        lesson = Lesson(
            name=form.name.data,
            text_material=form.text.data,
            video_material=form.video.data,
            course_id=course_id

        )
        db_sess.add(lesson)
        db_sess.commit()
        return redirect('/my_courses')
    return render_template('add_lesson.html', title='add_lesson', form=form)

@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == "__main__":
    db_session.global_init("db/bs.db")
    app.run(host='0.0.0.0', port=1234)

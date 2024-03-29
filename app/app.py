from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from sqlalchemy import and_, or_

from data import db_session
from data.users import User
from data.lessons import Lesson
from data.courses import Course
from data.questions import Question
from forms.login import LoginForm
from forms.user import RegisterForm
from forms.course import CourseForm
from forms.lesson import LessonForm
from forms.search import SearchForm
from forms.test import TestForm
from another_classes.boolconverter import BoolConverter


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.url_map.converters['bool'] = BoolConverter
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
            is_author=form.role.data == 'teacher'
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
            difficulty=form.difficulty.data,
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
        if db_sess.query(Lesson).filter(Lesson.name == form.name.data).first():
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
        return redirect(f'/my_course/{course_id}')
    return render_template('add_lesson.html', title='add_lesson', form=form)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/search_courses', methods=['GET', 'POST'])
def search_courses():
    form = SearchForm()
    if form.validate_on_submit():
        name = form.name.data
        language = form.language.data
        difficulty = form.difficulty.data
        db_sess = db_session.create_session()
        if difficulty == '' and language == '':
            courses = db_sess.query(Course).all()
        elif difficulty == '':
            courses = db_sess.query(Course).filter(Course.language == language).all()
        elif language == '':
            courses = db_sess.query(Course).filter(Course.difficulty == difficulty).all()
        else:
            courses = db_sess.query(Course).filter(and_(Course.difficulty == difficulty,
                                                        Course.language == language)).all()
        dels = []
        for course in courses:
            if name not in course.name:
                dels.append(course)
        for d in dels:
            courses.remove(d)
        return render_template('search_result.html', courses=courses)
    return render_template("search_courses.html", form=form)


@app.route('/course/<int:id>')
def course(id):
    db_sess = db_session.create_session()
    course = db_sess.query(Course).filter(Course.id == id).first()
    lessons = db_sess.query(Lesson).filter(Lesson.course_id == id)
    return render_template("course.html", course=course, lessons=lessons)


@app.route('/lesson/<int:id>')
def lesson(id):
    db_sess = db_session.create_session()
    lesson = db_sess.query(Lesson).filter(Lesson.id == id).first()
    return render_template('lesson.html', lesson=lesson)


@login_required
@app.route('/my_lesson/<int:id>')
def my_lesson(id):
    db_sess = db_session.create_session()
    lesson = db_sess.query(Lesson).filter(Lesson.id == id).first()
    return render_template('my_lesson.html', lesson=lesson)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            db_sess.close()
            return redirect("/")
        db_sess.close()
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_required
@app.route('/favorite/<string:url>/<int:course_id>', methods=['GET', 'POST'])
def add_or_exclude_course_to_favorite(url, course_id):
    db_sess = db_session.create_session()
    course = db_sess.query(Course).filter(Course.id == course_id).first()
    if course in current_user.favorite_courses:
        current_user.favorite_courses.remove(course)
    else:
        current_user.favorite_courses.append(course)
    db_sess.commit()
    db_sess.close()
    return redirect(f'/{url}')


@login_required
@app.route('/favorite_courses', methods=['GET', 'POST'])
def favorite_courses():
    db_sess = db_session.create_session()
    courses = db_sess.query(Course)
    db_sess.close()
    return render_template("favorite_courses.html", courses=courses)


@login_required
@app.route('/delete_course/<int:id>')
def delete_course(id):
    db_sess = db_session.create_session()
    course = db_sess.query(Course).filter(Course.id == id).first()
    user = db_sess.query(User).filter(User.id == course.author_id).first()
    if current_user == user:
        lessons = db_sess.query(Lesson).filter(Lesson.course_id == id).all()
        for lesson in lessons:
            db_sess.delete(lesson)
        db_sess.delete(course)
        db_sess.commit()
    db_sess.close()
    return redirect('/my_courses')


@login_required
@app.route('/delete_lesson/<int:id>')
def delete_lesson(id):
    db_sess = db_session.create_session()
    lesson = db_sess.query(Lesson).filter(Lesson.id == id).first()
    course_id = lesson.course_id
    course = db_sess.query(Course).filter(Course.id == course_id).first()
    user = db_sess.query(User).filter(User.id == course.author_id).first()
    if current_user == user:
        db_sess.delete(lesson)
        db_sess.commit()
    db_sess.close()
    return redirect(f'/my_course/{course_id}')


@app.route('/add_test/<bool:more>/<int:lesson_id>', methods=['GET', 'POST'])
def add_test(more, lesson_id):
    form = TestForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        lesson = db_sess.query(Lesson).filter(Lesson.id == lesson_id).first()
        course = db_sess.query(Course).filter(Course.id == lesson.course_id).first()
        user = db_sess.query(User).filter(User.id == course.author_id).first()
        if current_user == user:
            question = Question(
            question=form.question.data,
            answer1=form.answer1.data,
            answer2=form.answer2.data,
            answer3=form.answer3.data,
            answer4=form.answer4.data,
            lesson_id=lesson_id
            )
            db_sess.add(question)
            db_sess.commit()
            db_sess.close()
        if more:
            return render_template('add_test.html', form=TestForm())
        return redirect(f'/my_lesson/{lesson_id}')
    return render_template('add_test.html', form=form)


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

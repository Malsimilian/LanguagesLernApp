import telebot
from telebot import types
import os

from sqlalchemy.ext.declarative import declarative_base

from data.courses import Course
from data.lessons import Lesson
from data.users import User
from data import db_session


Base = declarative_base()


def get_courses():
    db_sess = db_session.create_session()
    courses = db_sess.query(Course)
    db_sess.close()
    if courses:
        return [course.name for course in courses]
    return False


def get_lessons():
    db_sess = db_session.create_session()
    lessons = db_sess.query(Lesson)
    db_sess.close()
    if lessons:
        return [lesson.name for lesson in lessons]
    return False


def f(message):
    return message.text in get_courses()


def ff(message):
    return message.text in get_lessons()


def set_status_for_login_user():
    user_state = {}
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.tg_chat_id is not None).all()
    for user in users:
        user_state[user.tg_chat_id] = 'login'
    return user_state

def set_status_for_new_user(message):
    if message.chat.id not in user_state:
        user_state[message.chat.id] = 'logout'
    elif user_state[message.chat.id] != 'login':
        user_state[message.chat.id] = 'logout'

db_session.global_init("db/bs.db")

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

user_state = set_status_for_login_user()
user_info = {}


@bot.message_handler(func=lambda message: message.chat.id not in user_state)
def set_logout_status(message):
    user_state[message.chat.id] = 'logout'

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет, нажмите /help")
    set_status_for_new_user(message)


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id,'''
/start
/help
/check_status
/login
/logout
/courses
/favorite_courses
    ''')


@bot.message_handler(commands=['courses'])
def handle_courses(message):
    set_status_for_new_user(message)
    if get_courses():
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for item in get_courses():
            markup.add(item)
        bot.send_message(message.chat.id, "Выберите курс:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'На данный момент нет доступных курсов.')


@bot.message_handler(commands=['check_status'])
def handle_check_status(message):
    set_status_for_new_user(message)
    bot.send_message(message.chat.id, user_state[message.chat.id])

@bot.message_handler(func=lambda message: f(message))
def handle_lessons(message):
    db_sess = db_session.create_session()
    course = db_sess.query(Course).filter(Course.name == message.text).first()
    lessons = db_sess.query(Lesson).filter(Lesson.course_id == course.id).all()
    if lessons:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for lesson in [lesson.name for lesson in lessons]:
            markup.add(lesson)
        bot.send_message(message.chat.id, "Выберите урок:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'В этом курсе еще нет уроков.')
    db_sess.close()


@bot.message_handler(func=lambda message: ff(message))
def handle_lesson(message):
    db_sess = db_session.create_session()
    lesson = db_sess.query(Lesson).filter(Lesson.name == message.text).first()
    bot.send_message(message.chat.id, lesson.video_material)
    bot.send_message(message.chat.id, lesson.text_material)
    db_sess.close()


@bot.message_handler(commands=['login'])
def handle_please_email(message):
    set_status_for_new_user(message)
    if user_state[message.chat.id] == 'logout':
        bot.send_message(message.chat.id, 'Введите please почту')
        user_state[message.chat.id] = "waiting_email"
    else:
        bot.send_message(message.chat.id, 'Вы уже вошли в аккаунт')


@bot.message_handler(func=lambda message: user_state[message.chat.id] == 'waiting_email')
def handle_please_password(message):
    user_info[message.chat.id] = message.text
    user_state[message.chat.id] = 'waiting_password'
    bot.send_message(message.chat.id, 'Введите please password')


@bot.message_handler(func=lambda message: user_state[message.chat.id] == 'waiting_password')
def handle_login(message):
    password = message.text
    email = user_info[message.chat.id]
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first()
    if user and user.check_password(password):
        user.tg_chat_id = message.chat.id
        db_sess.commit()
        user_state[message.chat.id] = 'login'
        bot.send_message(message.chat.id, f'Вы успешно вошли в аккаунт {user.name}')
        db_sess.close()
    else:
        bot.send_message(message.chat.id, 'Неверный логин или пароль. Можете попробовать еще раз /login')


@bot.message_handler(commands=['logout'])
def handle_logout(message):
    set_status_for_new_user(message)
    if user_state[message.chat.id] == 'login':
        user_state[message.chat.id] = 'logout'
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.tg_chat_id == message.chat.id).first()
        user.tg_chat_id = None
        db_sess.commit()
        db_sess.close()
        'Вы успешно вышли из всоего аккаунта'
    else:
        'Вы не вошли в аккаунт'


@bot.message_handler(commands=['favorite_courses'])
def handle_favorite_courses(message):
    set_status_for_new_user(message)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.tg_chat_id == message.chat.id).first()
    lessons = user.favorite_courses
    if lessons:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for lesson in [lesson.name for lesson in lessons]:
            markup.add(lesson)
        bot.send_message(message.chat.id, "Выберите курс:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'У вас нет избранных курсов.')
    db_sess.close()


bot.polling()



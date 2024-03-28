import telebot
from telebot import types
import os

from sqlalchemy.ext.declarative import declarative_base

from data.courses import Course
from data.lessons import Lesson
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



db_session.global_init("db/bs.db")

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет, нажмите /courses чтобы выбрать курс")


@bot.message_handler(commands=['courses'])
def handle_courses(message):
    if get_courses():
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for item in get_courses():
            markup.add(item)
        bot.send_message(message.chat.id, "Выберите курс:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'На данный момент нет доступных курсов.')


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
        bot.send_message(message.chat.id, 'На данный момент нет доступных уроков.')
    db_sess.close()


@bot.message_handler(func=lambda message: ff(message))
def handle_lesson(message):
    db_sess = db_session.create_session()
    lesson = db_sess.query(Lesson).filter(Lesson.name == message.text).first()
    bot.send_message(message.chat.id, lesson.video_material)
    bot.send_message(message.chat.id, lesson.text_material)
    db_sess.close()


bot.polling()



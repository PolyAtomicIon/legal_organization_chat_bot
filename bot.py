from flask import Flask,request
import telebot
from telebot import types
import sys, time
import pickle
import os.path
import gspread
from oauth2client.service_account import ServiceAccountCredentials

token = '896203315:AAHGOl_c4-RzAU36sW7n843jzpI8Y8UNyCw'
secret = 'gfdgf4454'
url = 'https://altaiabitelegrambot.pythonanywhere.com/' + secret

bot = telebot.TeleBot(token, threaded = False)

bot.remove_webhook()
bot.set_webhook(url = url)

app = Flask(__name__)
@app.route('/' + secret, methods = ['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

#Google SpreadSheets

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

#gc = gspread.authorize(credentials)

DB_1 = 'DB_1'
DB_2 = 'DB_2'
DB_3 = 'DB_3'

db_1 = {}
db_2 = {}
db_3 = {}

##Google SpreadSheets

def start_btn(chatId):
    kb = types.ReplyKeyboardMarkup(row_width = 1,resize_keyboard = True, one_time_keyboard = False)
    btn = ['Авторлық шарт', 'Лицензиялық шарт', 'Іздеудегі құқық иеленушілер']
    kb.add(*btn)

    bot.send_message(chatId, 'Құрметті қолданушы! Қажетті функционалды таңдаңыз!', reply_markup = kb)

def getDataFromDB():

    global db_1, db_2, db_3
    gc = gspread.authorize(credentials)

    #First Sheet
    wkc = gc.open(DB_1)
    db_sheet_1 = wkc.worksheets()

    index = 0

    for sheet in db_sheet_1:

        all_data = sheet.get_all_values()

        for row in all_data:
            db_1[row[1]] = row[1].lower()

    #Second Sheet
    wkc = gc.open(DB_2)
    db_sheet_2 = wkc.worksheets()

    index = 0

    for sheet in db_sheet_2:

        all_data = sheet.get_all_values()

        for row in all_data:
            db_2[row[0]] = row[1].lower()

    #Third Sheet
    wkc = gc.open(DB_3)
    db_sheet_3 = wkc.worksheets()

    index = 0

    for sheet in db_sheet_3:

        all_data = sheet.get_all_values()

        for row in all_data:
            db_3[row[0]] = row[1].lower()

def find_db_1(msg):

    global db_1
    txt = msg.text.lower()

    for key, value in db_1.items():
        cnt = value.count(txt)
        print(cnt, txt)
        if cnt == 1:
            bot.send_message(msg.chat.id, key)
            return
        elif cnt > 1:
            bot.send_message(msg.chat.id, 'Біз осындай есімді {} әнші таптық. Нақтырақ жазыңыз!'.format(cnt) )
            first_func(msg.chat.id)
            return

    bot.send_message(msg.chat.id, 'Табылмады!')

def first_func(chatId):
    new_msg = bot.send_message(chatId, 'Бұл функционал авторлық және сабақтас құқық иелерінің қай ұжымдық басқару ұйымымен шарт жасасқандығын көрсетеді. Автордың атын жазыңыз, мысалы Жігіттер, сол кезде автордың кіммен шарт жасасқаны шығады.')
    bot.register_next_step_handler(new_msg, lambda msg: find_db_1(msg))

def find_db_2(msg):

    global db_2
    txt = msg.text.lower()

    for key, value in db_2.items():
        cnt = value.count(txt)
        print(cnt, txt)
        if cnt == 1:
            bot.send_message(msg.chat.id, key)
            return
        elif cnt > 1:
            bot.send_message(msg.chat.id, 'Біз осындай есімді {} әнші таптық. Нақтырақ жазыңыз!'.format(cnt) )
            second_func(msg.chat.id)
            return

    bot.send_message(msg.chat.id, 'Табылмады!')

def second_func(chatId):
    new_msg = bot.send_message(chatId, 'Авторлық және сабақтас құқық туындыларын пайдаланушылардың қандай ұйыммен лицензиялық шарт жасасқанын табуға жәрдемдеседі. Пайдаланушының атын жазыңыз, мысалы караоке Terraline дегенде оның қандай ұйыммен шарт жасағаны шығады.​')
    bot.register_next_step_handler(new_msg, lambda msg: find_db_2(msg))

def find_db_3(msg):

    global db_3
    txt = msg.text.lower()

    for key, value in db_3.items():
        cnt = value.count(txt)
        print(cnt, txt)
        if cnt == 1:
            bot.send_message(msg.chat.id, key)
            return
        elif cnt > 1:
            bot.send_message(msg.chat.id, 'Біз осындай есімді {} әнші таптық. Нақтырақ жазыңыз!'.format(cnt) )
            third_func(msg.chat.id)
            return

    bot.send_message(msg.chat.id, 'Табылмады! Қатесіз жазыңыз!')

def third_func(chatId):
    new_msg = bot.send_message(chatId, 'Авторлық және сабақтас құқықты ұжымдық басқару ұйымдарымен сыйақысын беру үшін іздеудегі құқық иеленушілерді табуға жәрдемдеседі. Автордың атын жазыңыз, мысалы Жігіттер квартеті дегенде оны қандай ұйым іздеп жатқаны шығады​.')
    bot.register_next_step_handler(new_msg, lambda msg: find_db_3(msg))

getDataFromDB()

#testing..

@bot.message_handler(commands = ['start'])
def start(m):
    start_btn(m.chat.id)

@bot.message_handler(func=lambda msg: msg.text == 'Авторлық шарт')
def handler(msg):
    first_func(msg.chat.id)

@bot.message_handler(func=lambda msg: msg.text == 'Лицензиялық шарт')
def handler(msg):
    second_func(msg.chat.id)

@bot.message_handler(func=lambda msg: msg.text == 'Іздеудегі құқық иеленушілер')
def handler(msg):
    third_func(msg.chat.id)

if __name__ == '__main__':
    bot.polling(none_stop=True)

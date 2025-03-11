import telebot
from telebot import types
import speech_recognition as sr
from pydub import AudioSegment
import os
import requests
import time
from icrawler.builtin import GoogleImageCrawler
import csv
from datetime import datetime, timedelta
import random

token = 

bot = telebot.TeleBot(token)

rec = sr.Recognizer()

with open("data.csv") as file:
    filereader = csv.reader(file)
    mass = [line for line in filereader if line != []][1:]
    for i in range(len(mass)):
        mass[i][0] = int(mass[i][0])
    slovar = dict(mass)
    print(slovar)

AudioSegment.converter = os.getcwd() + "\\bin\\ffmpeg.exe"
AudioSegment.ffprobe = os.getcwd() + "\\bin\\ffprobe.exe"
bot.mass = [[],[]]


    

@bot.message_handler(commands=["start"])
def start(message):
    markup1 = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("Что ты можешь?", callback_data="q_1")
    btn2 = types.InlineKeyboardButton("Возникли проблемы с ботом или нашли баг?", callback_data="q_2")
    markup1.add(btn1, btn2)
    bot.send_message(
        message.chat.id, text="Привет, {0.first_name}! Меня зовут TPB.".format(message.from_user), reply_markup=markup1
    )

@bot.message_handler(commands=["help"])
def help(message):
    markup2 = types.InlineKeyboardMarkup(row_width=2)
    btn3 = types.InlineKeyboardButton("Руководство /start", callback_data="q_3")
    btn4 = types.InlineKeyboardButton("Руководство /pic", callback_data="q_4")
    btn5 = types.InlineKeyboardButton("Руководство /all", callback_data="q_5")
    btn6 = types.InlineKeyboardButton("Руководство /mute", callback_data="q_6")
    markup2.add(btn3, btn4, btn5, btn6)
    bot.send_message(
        message.chat.id,
        text="Я умею расшифровывать голосовые сообщения, а так же обладаю рядом команд.\nРуководство по командам:",
        reply_markup=markup2,
    )


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == "q_1":
            bot.send_message(
                call.message.chat.id,
                text="Для того, чтоeбы полностью узнать мой функционал напиши команду '/help'!",
            )
        if call.data == "q_2":
            bot.send_message(
                call.message.chat.id,
                text="Если возникли проблемы напишите сюда: @aftersg",
            )
        if call.data == "q_3":
            bot.send_message(
                call.message.chat.id,
                text='/start:\n   Команда "/start" перезапускает бота.',
            )
        if call.data == "q_4":
            bot.send_message(
                call.message.chat.id,
                text=(
                    '/pic:\n   Команда "/pic слово N" присылает N фоток по запросу "слово"\n   Пример  "/pic слон 3" -'
                    " выведет 3 фотки по запросу слон"
                ),
            )
        if call.data == "q_5":
            bot.send_message(
                call.message.chat.id,
                text=(
                    '/all:\n   Команда "/all" уведомляет участников чата\n   Команда "/all" обладает рядом методов:\n  '
                    '   "new"- если используете "/all" в первый раз, следует указать данный метод и одним сообщением'
                    ' через пробел указать теги всех участников вашего чата.\n   "add"- если в чате появился'
                    " новый участник, с помощью данного метода можно легко"
                    ' добавить его тег к остальным.\n     "del"- если ваш чат покинул участник вы можете удалить его'
                    " тег. "
                ),
            )
        if call.data == "q_6":
            bot.send_message(
                call.message.chat.id,
                text=(
                    '/mute:\n   Команда "/mute" мьютит участника чата, на сообщение которого вы отвечаете, на заданное'
                    ' количество секунд.\n     Пример: "/mute 60" - мьютит пользователя на 1 минуту.'
                ),
            )


@bot.message_handler(commands=["all"])
def all(message):
    try:
        if len(message.text.split()) == 1:
            if message.chat.id not in slovar.keys():
                bot.send_message(message.chat.id, text="Вы не добавили участников группы")
            else:
                bot.send_message(message.chat.id, text=slovar[message.chat.id])
        else:
            if message.text.split()[1] == "add":
                slovar[message.chat.id] += " "
                slovar[message.chat.id] += " ".join(message.text.split()[2:])
                bot.send_message(
                    message.chat.id,
                    text='Вы успешно добавили участника(ов) с тегом(ами):\n"{}"'.format(
                        " ".join(message.text.split()[2:])
                    ),
                )

            if message.text.split()[1] == "new":
                slovar[message.chat.id] = " ".join(message.text.split()[2:])
                bot.send_message(
                    message.chat.id,
                    text='Вы успешно изменили тег(и). Состав вашей группы:\n"{}"'.format(slovar[message.chat.id]),
                )

            if message.text.split()[1] == "del":
                for user in message.text.split()[2:]:
                    if user in slovar[message.chat.id]:
                        slovar[message.chat.id] = " ".join(slovar[message.chat.id].split()).strip().replace(user, "")
                bot.send_message(
                    message.chat.id,
                    text='Вы успешно удалили участника(ов) с тегом(ами):\n"{}"'.format(
                        " ".join(message.text.split()[2:])
                    ),
                )

        with open("data.csv", "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["id", "members"])
            for key, value in slovar.items():
                writer.writerow([int(key), value])

    except ValueError:
        bot.send_message(message.chat.id, text="Ты доспустил ошибку, будь внимательнее")


@bot.message_handler(commands=["pic"])
def pic(message):
    for f in os.listdir("pictures"):
        os.remove(os.path.join("pictures", f))

    def find_pic(message):
        try:
            peremen = message.text.replace("/pic ", "").split()
            try:
                numb = int(peremen.pop(-1))
                if numb < 20 and numb > 0:
                    request = " ".join(peremen)
                    google = GoogleImageCrawler(storage={"root_dir": "pictures"})
                    google.crawl(keyword=request, max_num=numb)

                    for f in os.listdir("pictures"):
                        photo = open(os.path.join("pictures", f), "rb")
                        bot.send_photo(message.chat.id, photo)
                else:
                    bot.send_message(message.chat.id, text="Иди нахуй ")
            except TypeError:
                bot.send_message(message.chat.id, text="Дура тупая смотри что вводишь")
        except ValueError:
            bot.send_message(message.chat.id, text="Дура тупая смотри что вводишь")

    find_pic(message)


@bot.message_handler(commands=["mute"])
def mute(message):
    time_out = int(message.text.split()[1])
    if time_out <= 40 or time_out >= 900000:
        bot.send_message(
            reply_to_message_id=message.id,
            chat_id=message.chat.id,
            text="Слишком слабое или слишком ебейшее наказание!",
        )
        return
    try:
        bot.restrict_chat_member(
            message.chat.id,
            message.reply_to_message.from_user.id,
            until_date=datetime.now() + timedelta(seconds=time_out),
        )
        bot.send_message(
            reply_to_message_id=message.id, chat_id=message.chat.id, text=f"Пользователь замьючен на {time_out} секунд."
        )
    except AttributeError:
        bot.send_message(reply_to_message_id=message.id, chat_id=message.chat.id, text="Вы не выбрали кого замьютить!")


@bot.message_handler(content_types=["voice"])
def bot_messages(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get(
        "https://api.telegram.org/file/bot{0}/{1}".format(token, file_info.file_path)
    )  # запрос и скачивание файла с сервера
    src = file_info.file_path[:6] + "oga" + file_info.file_path[5:]
    dst = file_info.file_path[:6] + "wav" + file_info.file_path[5:-3] + "wav"
    with open(src, "wb") as f:
        f.write(file.content)
    sound = AudioSegment.from_file(src, "ogg")
    sound.export(dst, format="wav")
    del sound
    with sr.WavFile(dst) as source:
        audio = rec.record(source)
        rec.adjust_for_ambient_noise(source)
    text = rec.recognize_google(audio, language="ru-RU").lower()
    bot.send_message(message.chat.id, text=text)

    os.remove(src)
    os.remove(dst)



@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    ran = random.randint(0,100000)
    print(ran)
    if  "BUF" in message.text:
        bot.mass[0].append(message.from_user.username)
        bot.mass[1].append(message.from_user.id)
    if ran == 0 and bot.flag:
        print(bot.mass)
        chat = message.chat.id
        bot.flag = False
        bot.send_message(chat, "Йой, йоу, йоу! Внезапный бaтл буферов!\nУ тебя есть время пока не истечет таймер чтобы отправить свой буфер обмена, у кого он будет самый смешной тот и выиграет!\nРешать не мне, решаете вы!\n Пришли свой буфекр обмена, эт оможет быть что угодно, фотка, гс, видео. Главное чтобы твое сообщение содержала слово 'BUF'.\nВремя на батл: 1 минута")
        message = bot.send_message(chat, "Осталось времени: 1:00")
        idd = message.message_id
        timeend = datetime.now() + timedelta(seconds=60)
        while timeend - datetime.now() > timedelta(seconds=5):
            time.sleep(4)
            end = datetime.strptime(str(timeend - datetime.now()), '%H:%M:%S.%f')
            bot.edit_message_text("Осталось времени: " + end.strftime("%M:%S"), chat, idd)
        bot.send_message(chat, "Время вышло!")
        message = bot.send_poll(chat, "Чей буфер обмена самый смешной?", bot.mass[0], is_anonymous=False, allows_multiple_answers=True, open_period = 60)
        time.sleep(59)
        poll = bot.stop_poll(chat, message.message_id)
        for i in poll.options: 
            if i.voter_count == max([i.voter_count for i in poll.options]):
                bot.send_message(chat, f"Победил @{i.text} !")
                bot.restrict_chat_member(
                    chat,
                    bot.mass[1][bot.mass[0].index(i.text)],
                    until_date=datetime.now() + timedelta(seconds=600),
                )
                bot.send_message(chat, f"... а еще он заблокирован на 10 минут!")
                bot.flag = True
                bot.mass = [[],[]]
                break



if __name__ == "__main__":
    bot.flag = True
    bot.infinity_polling()

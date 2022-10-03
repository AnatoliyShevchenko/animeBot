from email.message import Message
from typing import Text
from telebot import types
import telebot
import urllib.request
import json
import random
import config
import requests
from requests.models import Response


bot = telebot.TeleBot(token=config.TOKEN)


url = "https://gogoanime.herokuapp.com/recent-release"
r: Response = requests.get(url)
# print(r.status_code)
data = r.json()
serialurl = ''
# print(type(data))
list_of_anime = []
for element in data:
    # with open("{0}.png".format(element.get('animeTitle')), "wb") as f:
    #     img = requests.get(element.get('animeImg'))
    #     f.write(img.content)
        
    list_of_anime.append(element.get('animeTitle'))


@bot.callback_query_handler(func=lambda call: True)
def btn_handle(call: telebot.types.CallbackQuery):
    global data, serialurl
    for element in data:
        if str(call.data) == element.get('animeTitle'):
            markup = types.InlineKeyboardMarkup()
            buttonA = types.InlineKeyboardButton('доступен эпизод ' + element.get('episodeNum'), callback_data='episodeNum')
            markup.row(buttonA)
            serialurl = element.get('episodeUrl')
            with open("poster.png".format(element.get('animeTitle')), "wb") as f:
                img = requests.get(element.get('animeImg'))
                f.write(img.content)
            img = open('poster.png', 'rb')
            bot.send_photo(call.message.chat.id, img)
            img.close()
            bot.send_message(call.message.chat.id, 'вы выбрали аниме '+ element.get('animeTitle'), reply_markup=markup)
    
    if str(call.data) == 'episodeNum':
        bot.send_message(call.message.chat.id, 'держи ссылку: ' + serialurl)

    bot.answer_callback_query(call.id)

    
@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonAnime = types.KeyboardButton('/get_anime')
    markup.row(buttonAnime)
    bot.send_message(message.chat.id, 'нажмите кнопку /get_anime или введите команду чтобы продолжить', reply_markup=markup)

@bot.message_handler(commands=['get_anime'])
def get_anime(message: telebot.types.Message):
    global list_of_anime
    markup = types.InlineKeyboardMarkup()
    button_list = []
    button_list = [types.InlineKeyboardButton(text=i, callback_data=i) for i in list_of_anime]        
    markup.add(*button_list)
    bot.send_message(message.chat.id, 'ANIME', reply_markup=markup)



bot.polling(non_stop=True)

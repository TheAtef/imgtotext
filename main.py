import os
import time
import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import ocrspace
import random
from datetime import datetime
from server import server

API_KEY = os.getenv('API_KEY')
API_KEYY = os.getenv('API_KEYY')
CHATID = os.getenv('CHATID')
 
bot = AsyncTeleBot(API_KEY)

server()

eng_button = types.InlineKeyboardButton(text='English', callback_data='eng')
ar_button = types.InlineKeyboardButton(text='Arabic عربي', callback_data='ar')
close = types.InlineKeyboardButton(text='Close', callback_data='close')
markup = types.InlineKeyboardMarkup([[eng_button], [ar_button], [close]])

@bot.message_handler(commands=['start'])
async def start(message):
    await bot.send_chat_action(message.chat.id, action='typing')
    smsg = "ImgToText is up!\nSend me an image and I will extract the text from it."
    await bot.reply_to(message, smsg)

@bot.message_handler(func=lambda m: True, content_types=['photo'])
async def get_broadcast_picture(message):
    global m
    m = message
    await bot.send_chat_action(message.chat.id, action='typing')
    await bot.reply_to(message, "What's the text language?", reply_markup=markup)
    file__path = await bot.get_file(message.photo[-1].file_id)
    file = await bot.download_file(file__path.file_path)
    global n
    n = str(random.randint(0,19))
    with open("pic"+n+".jpg", "wb") as code:
        code.write(file)
    
    userId = message.chat.id
    nameUser = str(message.chat.first_name) + ' ' + str(message.chat.last_name)
    username = message.chat.username
    text = message.text
    date = datetime.now()
    data = f'User id: {userId}\nUsermae: @{username}\nName: {nameUser}\nText: {text}\nDate: {date}'
    await bot.send_message(chat_id=CHATID, text=data)

@bot.callback_query_handler(func=lambda call: True)
async def callback_data(call):
    if call.message:
        if call.data == 'close':
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=m.message_id)
        if call.data == 'eng':
            await bot.send_chat_action(call.message.chat.id, action='typing')
            api = ocrspace.API(api_key=API_KEYY)
            text = api.ocr_file("pic"+n+".jpg")
            if text == "":
                text = "Sorry, couldn't read."
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.reply_to(m, text)

        if call.data == 'ar':
            await bot.send_chat_action(call.message.chat.id, action='typing')
            api = ocrspace.API(api_key=API_KEYY, language=ocrspace.Language.Arabic)
            text = api.ocr_file("pic"+n+".jpg")
            if text == "":
                text = "Sorry, couldn't read."
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.reply_to(m, text)

print('Bot is running...')
import asyncio
while True:
    try:
        asyncio.run(bot.infinity_polling())
    except:
        time.sleep(10)
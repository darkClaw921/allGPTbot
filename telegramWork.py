
import telebot
from telebot import types
from chat import GPT
from workRedis import *
import os 
from dotenv import load_dotenv
from loguru import logger
load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN'))
# bot = telebot.TeleBot('TOKEN')
gpt = GPT()
GPT.set_key(os.getenv('KEY_AI'))
USERS = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, я бот, который отвечает на вопросы. Напиши мне что-нибудь. Сейчас вы работаете с OPEN_AI. чтобы переключится на других ботов введите /help')
    USERS[message.chat.id] = 'OPEN_AI'
    clear_history(message.chat.id)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Список ботов: /OPEN_AI, \n/YANDEX, \n/GIGA_CHAT. Чтобы переключится на другого бота введите /имя_бота')

@bot.message_handler(commands=['OPEN_AI'])
def openai(message):
    bot.send_message(message.chat.id, 'Вы переключились на OPEN_AI')
    USERS[message.chat.id] = 'OPEN_AI'

@bot.message_handler(commands=['YANDEX'])
def yandex(message):
    bot.send_message(message.chat.id, 'Вы переключились на YANDEX')
    USERS[message.chat.id] = 'YANDEX'

@bot.message_handler(commands=['GIGA_CHAT'])
def gigachat(message):
    bot.send_message(message.chat.id, 'Вы переключились на GIGA_CHAT')
    USERS[message.chat.id] = 'GIGA_CHAT'



@bot.message_handler(content_types=['text'])
@logger.catch
def send_text(message):
    model = USERS[message.chat.id]
    add_message_to_history(message.chat.id, 'user', message.text)
    history = get_history(message.chat.id)
    
    # if history is None:
    #     history = []

    answer = gpt.answer(message.text, history, 1, MODEL=model)[0]
    bot.send_message(message.chat.id, answer)

   
    add_message_to_history(message.chat.id, 'assistant', answer)


       



print('bot started')
bot.infinity_polling()
    


# if __name__ == '__main__':
    # main()
# a = gpt.answer('Какие факторы влияют на стоимость страховки на дом?',[],1,MODEL='GIGA_CHAT')
# a = gpt.answer('Какие факторы влияют на стоимость страховки на дом?',[],1,MODEL='YANDEX')
# print(a)





import telebot
from telebot import types
from chat import GPT
from workRedis import *
import os 
from dotenv import load_dotenv
from loguru import logger
from pprint import pprint
load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN'))
# bot = telebot.TeleBot('TOKEN')
gpt = GPT()
GPT.set_key(os.getenv('KEY_AI'))
USERS = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, я бот, который отвечает на вопросы. Напиши мне что-нибудь. Сейчас вы работаете с gpt. чтобы переключится на других ботов введите /help')
    USERS[message.chat.id] = 'gpt'
    clear_history(message.chat.id)

@bot.message_handler(commands=['help'])
def help(message):
    # bot.send_message(message.chat.id, 'Подключенные нейросети: \n/gpt, \n/yandex, \n/giga. \n/start - начать все заново(сбросить контекст) Чтобы переключится на другого бота введите /имя_бота')
    bot.send_message(message.chat.id, 'Подключенные нейросети: \n/gpt \n/yandex \n/giga \n/start - начать новый диалог (сбросить контекст)')

@bot.message_handler(commands=['gpt'])
def openai(message):
    bot.send_message(message.chat.id, 'Вы переключились на gpt')
    USERS[message.chat.id] = 'gpt'

@bot.message_handler(commands=['yandex'])
def yandex(message):
    bot.send_message(message.chat.id, 'Вы переключились на yandex')
    USERS[message.chat.id] = 'yandex'

@bot.message_handler(commands=['giga'])
def gigachat(message):
    bot.send_message(message.chat.id, 'Вы переключились на giga')
    USERS[message.chat.id] = 'giga'



@bot.message_handler(content_types=['text'])
@logger.catch
def send_text(message):
    model = USERS[message.chat.id]
    add_message_to_history(message.chat.id, 'user', message.text)
    history = get_history(message.chat.id)
    pprint(history)
    # if history is None:
    #     history = []
    promt = 'Ты бот-помошник, который помогает пользователю решить его проблемы.'
    answer = gpt.answer(promt, history, 1, MODEL=model)[0]
    bot.send_message(message.chat.id, answer)

   
    add_message_to_history(message.chat.id, 'assistant', answer)


       



print('bot started')
bot.infinity_polling()
    


# if __name__ == '__main__':
    # main()
# a = gpt.answer('Какие факторы влияют на стоимость страховки на дом?',[],1,MODEL='giga')
# a = gpt.answer('Какие факторы влияют на стоимость страховки на дом?',[],1,MODEL='yandex')
# print(a)




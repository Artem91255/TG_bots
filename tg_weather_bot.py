
import csv
import tokens
import telebot
from telebot import types
from pyowm.utils import timestamps
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config


bot = telebot.TeleBot(tokens.bot_TOKEN, parse_mode=None)
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM(tokens.owm_TOKEN, config_dict)
@bot.message_handler(commands=['start'])
def send_welcome(message):

	markup = types.InlineKeyboardMarkup()
	btn1 = types.InlineKeyboardButton(text="Выбрать город", callback_data='get_town')
	markup.add(btn1)
	bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот. В данный момент я могу показать тебе прогноз погоды в конкретном городе.".format(message.from_user), reply_markup=markup)

@bot.callback_query_handler(func = lambda call:True)
def answer(call):
	if call.data =='get_town':
		mesg = bot.send_message(call.from_user.id, 'Погода в каком городе тебя интересует?')
	
@bot.message_handler(content_types=['text'])
def message_reply(message):
		try:
			bot.send_message(message.chat.id, text="Ищу информацию о погоде искомом городе")
			id_list = message.from_user.id
			town = message.text
			enter_the_log(id_list, town)

			mgr = owm.weather_manager()
			observation = mgr.weather_at_place(message.text)
			w = observation.weather
			temperature = w.temperature('celsius')["temp"]
			ws = w.wind()['speed']
			fl = w.temperature('celsius')['feels_like']

			answer = 'В городе ' + message.text + ' сейчас ' + w.detailed_status + '\n'
			answer += 'Температура сейчас в районе ' + str(temperature) + '°С'+'\n'
			answer += 'Ощущяется как ' + str(fl) + '°С' + '\n'
			answer += 'Скорость ветра ' + str(ws) + ' м\сек' + '\n'
			markup = types.InlineKeyboardMarkup()
			
			button_choose_place = types.InlineKeyboardButton(text='Выбрать город', callback_data='get_town')
			markup.add(button_choose_place)
			bot.send_message(message.chat.id, answer, reply_markup = markup)
		except:
			bot.send_message(message.chat.id, "К сожалению я не могу найти населенный пункт с таким названием. Возможно его название написано неверно.")


def enter_the_log(get_id, get_town):
	personal_list = []
	personal_list.append(get_id)
	personal_list.append(get_town)
	write_in_csv(personal_list)


def write_in_csv(some_list):
    with open('logger.csv', 'a', encoding='utf=8') as pb:
        writer = csv.writer(pb, lineterminator="\r")
        writer.writerow(some_list)

bot.infinity_polling()
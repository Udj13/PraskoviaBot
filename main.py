import telebot
import locarus
from check_user import security
from check_user import check_user
from conf import vk_api
from human_func import answer

bot = telebot.TeleBot(vk_api)



@bot.message_handler(commands=['help'])
def send_help(message):
	chat_id = str(message.chat.id)
	user_id = message.from_user.id

	replay_text = 'Привет, я Прасковья и я умею в Локарус. Спроси меня что-нибудь про приборчики.\n' \
				  'Вводи команду с имей прибора через пробел \n' \
				  '/info - полная информация по приборчику \n' \
				  'Коротенькие /devinfo, /client, /lastactiv \n' \
				  '/loc - получить положение \n' \
				  '/abonentka - параметры через пробел - месяц, год, клиент. Например /abonentka 10 2020 Stroiregion \n'

	replay_text = security(user_id, replay_text)
	bot.send_message(chat_id, replay_text)




@bot.message_handler(commands=['devinfo', 'client', 'lastactiv'])
def send_info(message):
	user_id = message.from_user.id
	s = message.text.split()
	command = s[0]
	try:
		imei = s[1]
	except IndexError:
		replay_text = 'ты забыл номер локаруса'
	else:
		if command == '/devinfo':
			replay_text = locarus.GetDeviceInfo(imei)
		elif command == '/client':
			replay_text = locarus.GetClientDeviceInfo(imei)
		elif command == '/lastactiv':
			replay_text = locarus.GetActivityDeviceInfo(imei)

	replay_text = security(user_id, replay_text)
	bot.reply_to(message, replay_text)


@bot.message_handler(commands=['info'])
def send_fullinfo(message):
	s = message.text.split()
	command = s[0]
	chat_id = str(message.chat.id)
	user_id = message.from_user.id

	try:
		imei = s[1]
	except IndexError:
		replay_text = 'ты забыл номер локаруса'
		replay_text = security(user_id, replay_text)
		bot.reply_to(message, replay_text)
	else:
		reply_texts = locarus.GetFullDeviceInfo(imei)
		for string in reply_texts:
			string = security(user_id, string)
			bot.send_message(chat_id, string)




@bot.message_handler(commands=['loc'])
def send_location(message):
	s = message.text.split()
	command = s[0]
	chat_id = str(message.chat.id)
	user_id = message.from_user.id

	try:
		imei = s[1]
	except IndexError:
		replay_text = 'ты забыл номер локаруса'
		replay_text = security(user_id, replay_text)
		bot.reply_to(message, replay_text)
	else:
		reply_texts = locarus.GetLastPosition(imei)
		for string in reply_texts:
			string = security(user_id, string)
			bot.send_message(chat_id, string)
		if check_user(user_id):
			try:
				lon = reply_texts[7]
				lat = reply_texts[9]
			except IndexError:
				replay_text = 'Не могу показать карту'
				replay_text = security(user_id, replay_text)
				bot.reply_to(message, replay_text)
			else:
				bot.send_location(chat_id, lat, lon)





@bot.message_handler(commands=['abonentka'])
def send_location(message):

	s = message.text.split()
	command = s[0]
	chat_id = str(message.chat.id)
	user_id = message.from_user.id

	try:
		month = int(s[1])
		year = int(s[2])
		client = s[3]
	except IndexError:
		replay_text = 'не тупи, ты забыл параметры, месяц год и название клиента в базе'
		replay_text = security(user_id, replay_text)
		bot.reply_to(message, replay_text)
	except ValueError:
		replay_text = 'БЕСИШЬ! Я же сказала: месяц год и название клиента в базе'
		replay_text = security(user_id, replay_text)
		bot.reply_to(message, replay_text)
	else:
		replay_texts = locarus.GetActiveDevicesList(month, year, client)
		for string in replay_texts:
			secure_string = security(user_id, string)
			bot.send_message(chat_id, secure_string)




@bot.message_handler(commands=['userinfo'])
def send_userinfo(message):
	chat_id = str(message.chat.id)
	user_id = message.from_user.id
	bot.send_message(chat_id, user_id)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	if answer(message.text):
		bot.reply_to(message, answer(message.text))
#	bot.send_message(str(message.chat.id), "just text to chat")



if __name__ == '__main__':
	bot.polling()

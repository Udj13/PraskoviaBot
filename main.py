import telebot
import locarus
from conf import vk_api

bot = telebot.TeleBot(vk_api)


@bot.message_handler(commands=['info', 'client', 'lastactiv'])
def send_info(message):
	s = message.text.split()
	command = s[0]
	try:
		imei = s[1]
	except IndexError:
		replay_text = 'ты забыл номер локаруса'
	else:
		if command == '/info':
			replay_text = locarus.GetDeviceInfo(imei)
		elif command == '/client':
			replay_text = locarus.GetClientDeviceInfo(imei)
		elif command == '/lastactiv':
			replay_text = locarus.GetActivityDeviceInfo(imei)
	bot.reply_to(message, replay_text)


@bot.message_handler(commands=['fullinfo'])
def send_info(message):
	s = message.text.split()
	command = s[0]
	imei = s[1]


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)
#	bot.send_message(message.chat, "just text to chat")


bot.polling()

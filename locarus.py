import conf
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime


def GetTestInfo(imei):
    return ('test' + imei)


def GetFullDeviceInfo(imei):
    r_json = Request(conf.urlGetInfo + imei, conf.main_user, conf.main_pwd)

    if r_json == '':
        return ['недоступна информация для геопозиции', 'пустой ответ сервера']

    if(r_json['result'] == 'error'):
        return [r_json['description']]


    text = [r_json['result'][0]['imei'] + '\t' + 'Прописан как: ' + r_json['result'][0]['type'],
            'госномер: ' + r_json['result'][0]['number'] + '\t модель: ' + r_json['result'][0]['model'],
            'комментарий:' + r_json['result'][0]['comment'] + '\t примечание:' + r_json['result'][0]['remark'],
            'клиент: ' + str(r_json['result'][0]['clientID']),
            'Черная дата: ' + ConvertTZTime(r_json['result'][0]['blackDate']),
            'Активность UTC:' + ConvertTZTime(r_json['result'][0]['lastActivity']),
            'Свежий пакет UTC:' + ConvertTZTime(r_json['result'][0]['lastPacketTime'])
            ]
    return text


# Getting device info
def GetDeviceInfo(imei):
    r_json = Request(conf.urlGetInfo + imei, conf.main_user, conf.main_pwd)

    if r_json == '':
        return 'недоступна информация, пустой ответ сервера'

    if(r_json['result'] == 'error'):
        return r_json['description']

    return (r_json['result'][0]['imei'] + '\t' + 'Прописан как: ' + r_json['result'][0]['type'] +
            '\n госномер: ' + r_json['result'][0]['number'] + '\t модель: ' + r_json['result'][0]['model'] +
            '\n комментарий:' + r_json['result'][0]['comment'] + '\t примечание:' + r_json['result'][0]['remark']
            )


def GetClientDeviceInfo(imei):
    r_json = Request(conf.urlGetInfo + imei, conf.main_user, conf.main_pwd)

    if r_json == '':
        return 'недоступна информация, пустой ответ сервера'

    if(r_json['result'] == 'error'):
        return r_json['description']


    return (r_json['result'][0]['imei'] + '\t' + 'Прописан как:' + r_json['result'][0]['type'] +
            '\n госномер: ' + r_json['result'][0]['number'] +
            '\t модель: ' + r_json['result'][0]['model'] +
            '\t клиент: ' + str(r_json['result'][0]['clientID'])
            )


def GetActivityDeviceInfo(imei):
    r_json = Request(conf.urlGetInfo + imei, conf.main_user, conf.main_pwd)

    if r_json == '':
        return 'недоступна информация, пустой ответ сервера'

    if(r_json['result'] == 'error'):
        return r_json['description']

    return (r_json['result'][0]['imei'] + '\t' + 'Прописан как:' + r_json['result'][0]['type'] +
            '\n Черная дата: ' + ConvertTZTime(r_json['result'][0]['blackDate']) +
            '\n Активность UTC:' + ConvertTZTime(r_json['result'][0]['lastActivity']) +
            '\t Свежий пакет UTC:' + ConvertTZTime(r_json['result'][0]['lastPacketTime'])
            )


# PRINT LAST POSITION
def GetLastPosition(imei):
    r_json = Request(conf.urlGetPosition + imei, conf.main_user, conf.main_pwd)
    if r_json == '':
        return ['недоступна информация для геопозиции', 'пустой ответ сервера']

    if(r_json['result'] == 'error'):
        return [r_json['description']]


    if (r_json['result'] == 'error'):
        exit(0)

    reply_text = [
        'IMEI: ' + r_json['result']['objectID'],
        PrintDeltaTime(r_json['result']['time']),
        'Тип: ' + r_json['result']['objectType'],
        'Напряжение: ' + str(r_json['result']['voltage']),
        'Датчики: ' + str(r_json['result']['analogIn']),
        '----------------НАВИГАЦИЯ-----------------',
        'Широта: ', str(r_json['result']['Coords']['lon']),
        'Долгота: ', str(r_json['result']['Coords']['lat']),
        'Скорость: ' + str(r_json['result']['Coords']['speed']),
        'Валидность: ' + str(r_json['result']['Coords']['valid']),
        'Спутники: ' + str(r_json['result']['Satellites']['count']),
        'Спутники ГЛОНАСС: ' + str(r_json['result']['Satellites']['countGlonass'])
    ]
    return reply_text




def GetActiveDevicesList(month, year, client):

    r_json = Request(conf.urlGetUser, client, client)
    if r_json == '':
        return ['недоступна информация по пользователю']

    if(r_json['result'] == 'error'):
        return r_json['description']


    imei_list = r_json['result']['devices']

    reply_text = ['Активность машин ' + client + ' за '+month_name(month)+' '+str(year)]

    counter_all = 0
    counter_active = 0

    for imei in imei_list:
        counter_all += 1
        isActive = False
        reply_str = TableDeviceDuration(imei, month, year, client)
        reply_text.append(reply_str)
        if reply_str[0] == '+':
            counter_active += 1

    reply_text.append('Ездило '+ str(counter_active) + ' машин из ' + str(counter_all))

    return reply_text



def TableDeviceDuration(imei, month, year, client):
    next_month = month + 1
    year2 = year
    if next_month > 12:
        next_month = 1
        year2 = year + 1

    date_from = str(year)+'-'+str(month)+'-01T00:00:00.000Z'
    date_to = str(year2)+'-'+str(next_month)+'-01T00:00:00.000Z'
    param = '&from='+date_from+'&to='+date_to+'&vars=DurationText,MovingTimeText,Distance'

    r_json = Request(conf.urlGetDuration + imei + param, client, client)
    if r_json == '':
        return ('недоступна информация по машинке' + imei)


    if(r_json['result'] == 'error'):
        print(r_json['description'])
        return False

    printed_imei = r_json['result']['values'][0]['imei']
    durationText = r_json['result']['values'][0]['vars'][0]['varValue']
    movingTimeText = r_json['result']['values'][0]['vars'][1]['varValue']
    distanceText = r_json['result']['values'][0]['vars'][2]['varValue']

    device_is_active = False

    result = GetDeviceModelNumber(imei, client)
    model = result[0]
    number = result[1]

    duration = durationText_to_integer(durationText)
    movingTime = durationText_to_integer(movingTimeText)
    try:
        distance = float(distanceText)
    except ValueError:
        distance = 0

    if (distance > 500)or(duration > 10)or(movingTime > 10):
        device_is_active = True

    reply_text = PlusOrMinus(device_is_active) +'\t'+ printed_imei+'\t'+ str(model)+'\t'+ str(number)+'\t'+ str(duration)+'д\t' + str(movingTime)+'д\t' + str(distance)+'км\t'

    return reply_text




def GetDeviceModelNumber(imei, client):
    r_json = Request(conf.urlGetInfo + imei, client, client)
    if r_json == '':
        return ['недоступна информация', 'чот случилось']

    model = r_json['result'][0]['model']
    number = r_json['result'][0]['number']
    return [model, number]










# UNIVERSAL REQUEST FUNCTION
def Request(url, user, pwd):
    response = requests.get(url, auth=HTTPBasicAuth(user, pwd))
    if not response:
        return ''
    return response.json()


def ConvertTZTime(time):
    f = "%Y-%m-%dT%H:%M:%S.%fZ"
    dt = datetime.strptime(time, f)
    return dt.strftime("%d.%m.%Y-%H:%M")


# Print time from last activity
def PrintDeltaTime(time_old_withTZ):
    f = "%Y-%m-%dT%H:%M:%S.%fZ"
    time_old = datetime.strptime(time_old_withTZ, f)

    time_now = datetime.utcnow()
    time_delta = time_now - time_old

    days = time_delta.days
    seconds = time_delta.seconds
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    if days > 0:
        if days > 30:
            return "Нет свежих данных"
        else:
            return ("Был в сети" + str(days) + "дней назад")
    else:
        if (h == 0) & (m < 2):
            return "В СЕТИ, время UTC:" + str(time_old) + (", прошло: %d ч %02d мин" % (h, m))
        else:
            return ("Был в сети сегодня, прошло: %d ч %02d мин" % (h, m))


def month_name(n):
    if (n >= 1) & (n <= 12):
        return ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сеетябрь', 'октябрь', 'ноябрь',
                'декабрь'][n - 1]
    else:
        return 'неправильный номер месяца'


# convert text '9 д 23 ч 45 мин' to integer days count
def durationText_to_integer(durationText):
    position_d = durationText.find('д')
    if position_d > 0:
        durationText = durationText[:position_d]
        durationText.strip
        return int(durationText)
    else:
        return 0


def PlusOrMinus(isActive):
    if isActive:
        return '+'
    else:
        return '-'

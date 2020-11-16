import conf
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime



def GetTestInfo(imei):
    return ('test'+imei)

# Getting device info
def GetDeviceInfo(imei):

    r_json = Request(conf.urlGetInfo + imei, conf.main_user, conf.main_pwd)

    return  (r_json['result'][0]['imei']+'\t'+'Прописан как: ' + r_json['result'][0]['type']+
             '\n госномер: ' + r_json['result'][0]['number'] +'\t модель: ' + r_json['result'][0]['model'] +
             '\n комментарий:' + r_json['result'][0]['comment'] + '\t примечание:' + r_json['result'][0]['remark']
             )


def GetClientDeviceInfo(imei):

    r_json = Request(conf.urlGetInfo + imei, conf.main_user, conf.main_pwd)

    return  (r_json['result'][0]['imei']+'\t'+'Прописан как:' + r_json['result'][0]['type']+
             '\n госномер: ' + r_json['result'][0]['number'] +
             '\t модель: ' + r_json['result'][0]['model'] +
             '\t клиент: ' + str(r_json['result'][0]['clientID'])
             )



def GetActivityDeviceInfo(imei):

    r_json = Request(conf.urlGetInfo + imei, conf.main_user, conf.main_pwd)

    return  (r_json['result'][0]['imei']+'\t'+'Прописан как:' + r_json['result'][0]['type']+
             '\n Черная дата: ' + ConvertTZTime(r_json['result'][0]['blackDate']) +
             '\n Активность UTC:' + ConvertTZTime(r_json['result'][0]['lastActivity']) +
             '\t Свежий пакет UTC:' + ConvertTZTime(r_json['result'][0]['lastPacketTime'])
             )






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
            return "Был в сети %s дней назад" %(days)
    else:
        if (h == 0)&(m<2):
            return "В СЕТИ, время UTC:", time_old
        else:
            return "Был в сети сегодня, прошло: %d ч %02d мин" % (h, m)






def month_name(n):
    if (n>=1) & (n<=12):
        return ['январь','февраль','март','апрель','май','июнь','июль','август','сеетябрь','октябрь','ноябрь','декабрь'][n-1]
    else:
        return 'неправильный номер месяца'



#convert text '9 д 23 ч 45 мин' to integer days count
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

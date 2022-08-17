from datetime import date, datetime
import math
import calendar
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now().strftime('%Y-%m-%d')

#format year-month-days
start_date = os.environ['START_DATE']

city = os.environ['CITY']

#format month-days
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = datetime.today() - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - datetime.today()).days

 def last_business_day_in_month(year: int, month: int) -> int:
   return max(calendar.monthcalendar(year, month)[-1:][0][:5])

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()

last_wd = last_business_day_in_month(date.today().year,date.today().month)
cur_mon = datetime.strptime(str(date.today().year) + "-" + str(date.today().month) + "-" + str(last_wd), "%Y-%m-%d")
salary_days_diff = (cur_mon - datetime.today()).days
data = {"weather":{"value":wea, 
                 "color":get_random_color()},
        "temperature":{"value":temperature, 
                 "color":get_random_color()},
        "salary_day"{"value":salary_days_diff, 
                 "color":get_random_color()},
        "love_days":{"value":get_count(), 
                 "color":get_random_color()},
        "birthday_left":{"value":get_birthday(), 
                 "color":get_random_color()},
        "words":{"value":get_words(), 
                 "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)

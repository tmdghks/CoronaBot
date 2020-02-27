import discord
import requests
from bs4 import BeautifulSoup
import re
import time

token = 'token'

def get_comfirmed_number():
    res = requests.get('https://www.coronanow.kr/')
    soup = BeautifulSoup(res.content, 'html.parser')
    tmp = soup.select('#layoutSidenav_content > main > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div > div.card-body2')[0].get_text()
    tmp = tmp.replace(",","")
    comfirmed_number = re.findall("\d+", tmp)
    if len(comfirmed_number) == 1:
        comfirmed_number.append(str(0))
    return comfirmed_number

def get_deaths_number():
    res = requests.get('https://www.coronanow.kr/')
    soup = BeautifulSoup(res.content, 'html.parser')
    tmp = soup.select('#layoutSidenav_content > main > div:nth-child(2) > div:nth-child(2) > div:nth-child(4) > div > div.card-body2')[0].get_text()
    tmp = tmp.replace(",","")
    deaths_number = re.findall("\d+", tmp)
    if len(deaths_number) == 1:
        deaths_number.append(str(0))
    return deaths_number

def get_recoveries_number():
    res = requests.get('https://www.coronanow.kr/')
    soup = BeautifulSoup(res.content, 'html.parser')
    tmp = soup.select('#layoutSidenav_content > main > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div > div.card-body2')[0].get_text()
    tmp = tmp.replace(",","")
    recoveries_number = re.findall("\d+", tmp)
    if len(recoveries_number) == 1:
        recoveries_number.append(str(0))
    return recoveries_number

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        #don't response to ourselves
        if message.author == self.user:
            return
        
        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content == '!확진자':
            now = time.localtime()
            embeded = discord.Embed(
                title = "대한민국 코로나 확진자 수",
                description = get_comfirmed_number()[0] + "명",
                color = 0xFFFF00
            )
            embeded.add_field(name = "전일대비", value = get_comfirmed_number()[1] + "명 증가")
            embeded.set_footer(text = "%04d년 %02d월 %02d일 %02d시 %02d분 %02d초 기준\nhttps://coronanow.kr/에서 데이터를 가져왔습니다." % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
            await message.channel.send(embed = embeded)
        
        if message.content == '!사망자':
            now = time.localtime()
            embeded = discord.Embed(
                title = "대한민국 코로나 사망자 수",
                description = get_deaths_number()[0] + "명",
                color = 0xFF0000
            )
            embeded.add_field(name = "전일대비", value = get_deaths_number()[1] + "명 증가")
            embeded.set_footer(text = "%04d년 %02d월 %02d일 %02d시 %02d분 %02d초 기준\nhttps://coronanow.kr/에서 데이터를 가져왔습니다." % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
            await message.channel.send(embed = embeded)

        if message.content == '!완치자':
            now = time.localtime()
            embeded = discord.Embed(
                title = "대한민국 코로나 완치자 수",
                description = get_recoveries_number()[0] + "명",
                color = 0x00FF00
            )
            embeded.add_field(name = "전일대비", value = get_recoveries_number()[1] + "명 증가")
            embeded.set_footer(text = "%04d년 %02d월 %02d일 %02d시 %02d분 %02d초 기준\nhttps://coronanow.kr/에서 데이터를 가져왔습니다." % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
            await message.channel.send(embed = embeded)

client = MyClient()
client.run(token)
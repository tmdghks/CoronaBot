import discord
import requests
from bs4 import BeautifulSoup
import re

token = 'token'

def get_patient_number():
    res = requests.get('https://www.coronanow.kr/')
    soup = BeautifulSoup(res.content, 'html.parser')
    tmp = soup.select('#layoutSidenav_content > main > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div > div.card-body2')[0].get_text()
    tmp = tmp.replace(",","")
    patient_number = re.findall("\d+", tmp)
    return patient_number

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        #don't response to ourselves
        if message.author == self.user:
            return
        
        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content == '!corona':
            await message.channel.send("현재 확진자: " + get_patient_number()[0] + "명")
            await message.channel.send("전일 대비: +" + get_patient_number()[1] + "명")

client = MyClient()
client.run(token)
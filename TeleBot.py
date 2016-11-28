import os
import re
import logging
import telebot
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup as bs

bot = telebot.TeleBot('265431846:AAGobX591NC5o4PTeqMj8wei1YOprQKyDlU')



@bot.message_handler(commands=['start'])
def SendInfo(message):
    bot.send_message(message.chat.id, 'Привет я БОТ')


@bot.message_handler(commands=['text'])
def SendInfo(message):
    args = message.text.split(' ')
    if len(args)== 4 :
        if len(args[2].split('*'))!=2 :
            spl = args[2].split('*')
            width = spl[0]
            height = spl[1]
            images = SearchGoogleImages(args[1], message.chat.id, width=width, height=height)
        else:
            spl = args[2].split('*')
            width = spl[0]
            height = spl[1]
            images = SearchGoogleImages(args[1], message.chat.id, width=width, height=height, cnt=args[3])
    elif len(args)== 3 :
        if len(args[2].split('*'))!=2 :
            images = SearchGoogleImages(query=args[1], id=message.chat.id,cnt=args[2])
        else:
            spl = args[2].split('*')
            width = spl[0]
            height = spl[1]
            images = SearchGoogleImages(args[1], message.chat.id, width=width, height=height)
    else:
        images = SearchGoogleImages(query=args[1], id=message.chat.id)

    for image in images:
        bot.send_photo(message.chat.id, open(image, 'rb'))


def SearchGoogleImages(query, id ,width=320,height=320,cnt=5):
    path = os.path.abspath(os.curdir)
    path = os.path.join(path, str(id))
    print('path=' + path)

    if not os.path.exists(path):
        os.makedirs(path)

    url = 'https://www.google.ru/search?q=' + query + '&newwindow=1&tbm=isch'
    request = requests.get(url, headers={
        'User-Agent': 'Mozilla/50.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, Chrome/43.0.2357.134 Safari/537.36'})
    print('query='+query)
    print(url)
    soup = bs(request.content, "html.parser")
    # images = soup.find_all('img')
    images = soup.find_all('div', attrs={'class': re.compile("rg_meta")})
    atr = str(images[0])[str(images[0]).find('ou":"') + 5:]
    atr = atr[:atr.find('"')]

    imagesPaths = []

    for count, image in enumerate(images[0:int(cnt)]):
        '''print(image.get('src')+'\n')
        img = requests.get(image.get('src'))
        image = Image.open(BytesIO(img.content))
        imgpath=os.path.join(path, str(count)+'.'+image.format)
        image.save(imgpath)
        print(imgpath)
        imagesPaths.append(imgpath)'''

        print(str(image) + '\n')
        atr = str(image)[str(image).find('ou":"') + 5:]
        atr = atr[:atr.find('"')]
        img = requests.get(atr)
        if width==320 and height==320 :
            image = Image.open(BytesIO(img.content))
        else:
            image = Image.open(BytesIO(img.content)).resize((int(width),int(height)))
        imgpath = os.path.join(path, str(count) + '.jpg')
        image.save(imgpath)
        print(imgpath)
        imagesPaths.append(imgpath)

    return imagesPaths


if __name__ == '__main__':
    logging.basicConfig(filename='botlog.log',format='%(filename)s[LINE:%(lineno)d]# %(levelname) -8s [%(asctime)s] %(message)s',level=logging.DEBUG)
    logging.info('Bot started!')

try:
    bot.polling(none_stop=True)
except Exception:
    logging.critical('ERROR...')
finally:
    bot.polling(none_stop=True)

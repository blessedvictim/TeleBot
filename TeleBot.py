import os
import re
import logging
import telebot
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup as bs
import cherrypy

# Наш вебхук-сервер
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)

WEBHOOK_HOST = '172.31.22.9'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = 'cert/webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = 'cert/webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % ('265431846:AAGobX591NC5o4PTeqMj8wei1YOprQKyDlU')

bot = telebot.TeleBot('265431846:AAGobX591NC5o4PTeqMj8wei1YOprQKyDlU')

bot.remove_webhook()

 # Ставим заново вебхук
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Указываем настройки сервера CherryPy
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

 # Собственно, запуск!
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})

'''
@bot.message_handler(commands=['start'])
def SendInfo(message):
    bot.send_message(message.chat.id, 'Привет я БОООООТ')


@bot.message_handler(commands=['text'])
def SendInfo(message):
    images = SearchGoogleImages(message.text, message.chat.id)
    for image in images:
        bot.send_photo(message.chat.id, open(image, 'rb'))'''

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


def SearchGoogleImages(query, id):
    path = os.path.abspath(os.curdir)
    path = os.path.join(path, str(id))
    print('path=' + path)

    if not os.path.exists(path):
        os.makedirs(path)

    url = 'https://www.google.ru/search?q=' + query[6:] + '&newwindow=1&tbm=isch'
    request = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, Chrome/43.0.2357.134 Safari/537.36'})
    print(query[6:])
    print(url)
    soup = bs(request.content, "html.parser")
    # images = soup.find_all('img')
    images = soup.find_all('div', attrs={'class': re.compile("rg_meta")})
    print(str(images) + '\n\n\n')
    atr = str(images[0])[str(images[0]).find('ou":"') + 5:]
    atr = atr[:atr.find('"')]
    print(atr)
    # print(request.text)

    imagesPaths = []

    for count, image in enumerate(images[0:1]):
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
        image = Image.open(BytesIO(img.content))
        imgpath = os.path.join(path, str(count) + '.' + image.format)
        image.save(imgpath)
        print(imgpath)
        imagesPaths.append(imgpath)

    return imagesPaths


'''if __name__ == '__main__':
    logging.basicConfig(filename='botlog.log',format='%(filename)s[LINE:%(lineno)d]# %(levelname) -8s [%(asctime)s] %(message)s',level=logging.DEBUG)
    logging.info('Bot started!')'''
'''
try:
    bot.polling(none_stop=True)
except Exception:
    logging.critical('ERROR...')
finally:
    bot.polling(none_stop=True)'''

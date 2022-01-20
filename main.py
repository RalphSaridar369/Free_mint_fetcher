import requests
import shelve
from bs4 import BeautifulSoup
import telegram.ext
from telegram import *

ShelfFile = shelve.open('shelf')
ShelfFile['hash'] = ''
ShelfFile.close()

bot_api = '5293722053:AAHtIAGP1F9E2R9ul-rt1J9-lkx7UjCUYqA'

updater = telegram.ext.Updater(bot_api)
disp = updater.dispatcher

def Mints(update,context):
    if(update.message.text == "/mints"):
        update.message.reply_text("Please number of pages to fetch ")
    else:
        pages = int(update.message.text.split(' ')[1])
        for i in range(pages):
            reponse = requests.get('https://polygonscan.com/txs?p={}'.format(i+1))
            soup = BeautifulSoup(reponse.content, 'html.parser')
            table = soup.find('table',class_='table')
            rows = table.find('tbody').find_all('tr')
            message = "Page: {}\n\n".format(str(i+1))
            for j in rows:
                all_tds = j.find_all('td') 
                ShelfFile = shelve.open('shelf')
                if (all_tds[2].text == "Mint" and (all_tds[8].text not in ShelfFile['hash'])):
                    print(all_tds[8].text)
                    message +='https://polygonscan.com/address/{}'.format(all_tds[8].text[1::]) +"\n"#'<a href={}>{}</a>'.format(('https://polygonscan.com/address/{}'.format((all_tds[8].text))),all_tds[8].text)
                    print("TSSSSSSSSST")
                    ShelfFile['hash'] += all_tds[8].text+"-"
                    ShelfFile.close()
            if('https' in message):
                update.message.reply_text(message)
        update.message.reply_text("All done!")
        message=""

disp.add_handler(telegram.ext.CommandHandler("mints",Mints))

updater.start_polling()
updater.idle()
import logging
import settings
import ephem
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


VERSION = '0.4.2'
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


def greet_user(update, context):
    update.message.reply_text('Привет! Ты вызвал команду /start', )


def talk_to_me(update, context):
    user_text = update.message.text
    update.message.reply_text(user_text)


def my_version(update, context):
    update.message.reply_text(f'Привет! Это версия бота № {VERSION}')    


def find_constellation(update, context):
    planets = {
        'mercury' : ephem.Mercury,
        'venus' : ephem.Venus,
        'moon' : ephem.Moon,
        'mars' : ephem.Mars,
        'jupiter' : ephem.Jupiter,
        'saturn' : ephem.Saturn,
        'uranus' : ephem.Uranus,
        'neptune' : ephem.Neptune,
        'pluto' : ephem.Pluto,
        'sun' : ephem.Sun,
    }
    my_planet = update.message.text.split()[1].lower()
    now = datetime.datetime.now()
    if my_planet in planets:
        head = f'{my_planet.capitalize()} is currently in the constellation of '
        my_constellation = ephem.constellation(planets[my_planet](now))[1]
        update.message.reply_text(f'{head}{my_constellation}')
    else:
        update.message.reply_text("Sorry, I don't know this planet") 


# Реализуйте в боте команду /wordcount которая считает слова в присланной фразе
def count_words(update, context):
    sentence = update.message.text.split()
    if len(sentence) == 1:
        update.message.reply_text(f"There's no words")
    else:    
        update.message.reply_text(f'{len(sentence[1:])} word(s)')


# Реализуйте в боте команду, которая отвечает на вопрос "Когда ближайшее полнолуние?"
def when_full_moon(update, context):
    user_input = update.message.text.split()
    dt = datetime.datetime
    if len(user_input) == 1:
        user_date = datetime.date.today()
        prefix = ''
    else:
        try:
            user_date = dt.strptime(user_input[1], '%Y-%m-%d')
        except ValueError:
            update.message.reply_text('Incorrect date. Proper date format is YYYY-MM-DD')
        prefix =  ' after the date you input'
    next_full_moon = dt.strftime(ephem.next_full_moon(user_date).datetime(), '%d-%m-%Y')
    update.message.reply_text(f'Next full moon date{prefix}: {next_full_moon}')


def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('version', my_version))
    dp.add_handler(CommandHandler('planet', find_constellation))
    dp.add_handler(CommandHandler('wordcount', count_words))
    dp.add_handler(CommandHandler('next_full_moon', when_full_moon))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info(f'{datetime.datetime.now()}: Bot has started')
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()

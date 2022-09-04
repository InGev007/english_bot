from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button1 = KeyboardButton('Учить слова')
button2 = KeyboardButton('Учить правила*(в разработке)')
button3 = KeyboardButton('Переводчик')

button4=KeyboardButton('Англо-Русский')
button5=KeyboardButton('Руско-Английский')
button6=KeyboardButton('Назад')

startmenu = ReplyKeyboardMarkup().add(
    button1).add(button2).add(button3)

perevodmenu0=ReplyKeyboardMarkup(one_time_keyboard=True).add(
    button4).add(button5).add(button6)

def learnword(word):
    b1=KeyboardButton(word[0])
    b2=KeyboardButton(word[1])
    b3=KeyboardButton(word[2])
    b4=KeyboardButton(word[3])
    under=KeyboardButton('Назад')
    return ReplyKeyboardMarkup().add(b1).add(b2).add(b3).add(b4).add(under)
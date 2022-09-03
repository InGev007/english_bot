from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button1 = KeyboardButton('Учить слова')
button2 = KeyboardButton('Учить правила*')
button3 = KeyboardButton('Переводчик')

button4=KeyboardButton('Англо-Русский')
button4=KeyboardButton('Руско-Английский')

startmenu = ReplyKeyboardMarkup().add(
    button1).add(button2).add(button3)

perevodmenu0=ReplyKeyboardMarkup().add(
    button1).add(button2)

def learnword(word):
    b1=KeyboardButton(word[0])
    b2=KeyboardButton(word[1])
    b3=KeyboardButton(word[2])
    b4=KeyboardButton(word[3])
    under=KeyboardButton('Назад')
    return ReplyKeyboardMarkup().add(b1).add(b2).add(b3).add(b4).add(under)
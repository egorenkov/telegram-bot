import telebot # type: ignore
import text
import sqlite3
import os 

bot = telebot.TeleBot('token')

"""
- Как проходят занятия
- Контакты 
- Цены 
- Телеграмм канал 
- Информация о преподавателе 
- оставить отзыв
"""

@bot.message_handler(commands = ['start'])
def start(message):

    markup = telebot.types.ReplyKeyboardMarkup()
    
    bt1 = telebot.types.KeyboardButton(text.bt_coast)
    bt2 = telebot.types.KeyboardButton(text.bt_contact)
    bt3 = telebot.types.KeyboardButton(text.bt_channel)
    bt4 = telebot.types.KeyboardButton(text.bt_site)
    bt5 = telebot.types.KeyboardButton(text.bt_lesson)
    bt6 = telebot.types.KeyboardButton(text.bt_review)

    markup.row(bt1,bt2)
    markup.row(bt3,bt4)
    markup.row(bt5,bt6)


    bot.send_message(message.chat.id, text.start, reply_markup = markup)
    #bot.send_photo(message.chat.id, photo = img, caption = "Привет ЗДЕСЬ ИМЯ ... ")

  
@bot.message_handler(commands = ['help'])
def help(message):
    bot.send_message(message.chat.id ,text.help)



@bot.message_handler(commands = ['look_at_my_commments'])
def look_comm(message):
    s = text.list_of_comment + '\n'
    
    if not(os.path.exists('newdb.sql')):
         s += text.unfortunately
         bot.send_message(message.chat.id, s)
         return 

    conn = sqlite3.connect('newdb.sql')
    c = conn.cursor()

    c.execute("""SELECT comm FROM comment
                    WHERE user_id = '%d' ;""" % (message.from_user.id))
    tx = c.fetchall()
    c.close()
    conn.close()
   
    if len(tx) == 0:
         s += text.unfortunately
         bot.send_message(message.chat.id,s)
         return 
    
    for i in tx:
        s += '— ' + i[0] + '\n'
    bot.send_message(message.chat.id,s)
   


@bot.message_handler()
def main(message):
    img = telebot.types.InputFile('post.png')
    
    if message.text == text.bt_coast:
        bot.send_message(message.chat.id, text.coast)
    
    
    elif message.text == text.bt_contact:
        bot.send_message(message.chat.id, text.contact)
    
    
    elif message.text == text.bt_review:
        bot.send_message(message.chat.id, text.review)
        bot.register_next_step_handler(message, review)
    
    elif message.text == text.bt_channel:
        mk = telebot.types.InlineKeyboardMarkup()
        mk.add(telebot.types.InlineKeyboardButton('Телеграмм канал', url = "https://t.me/importEGE" ))
        bot.send_photo(message.chat.id,img, caption = text.channel, reply_markup = mk)
        
    elif message.text == text.bt_site:
        mk = telebot.types.InlineKeyboardMarkup()
        mk.add(telebot.types.InlineKeyboardButton('Мой сайт', url = "https://egorenkov.github.io/" ))
        bot.send_message(message.chat.id, text.site, reply_markup = mk)
    
    
    elif message.text == text.bt_lesson:
        bot.send_message(message.chat.id, text.question)
    
    else:
        bot.send_message(message.chat.id, text.wrong)
        
    
def review(mes):
    
    conn = sqlite3.connect('newdb.sql')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS comment (
                    user_id INTEGER,
                    first_name VARCHAR(45),
                    second_name VARCHAR(45),
                    comm VARCHAR(45)
                )""")

    

    cur.execute("""INSERT INTO 
                comment (user_id, first_name, second_name, comm) 
                VALUES('%d','%s','%s','%s')""" % (mes.from_user.id, mes.from_user.first_name, 
                                                  mes.from_user.last_name, mes.text))
    
    cur.execute('SELECT * FROM comment;')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(mes.chat.id, text.after_comment)



bot.polling(none_stop= True)








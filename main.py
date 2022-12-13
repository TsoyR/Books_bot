import telebot
from telebot import types
import sqlite3 as sq
import config

bot = telebot.TeleBot(config.TOKEN)

name_b = ''
author_b = ''
style_b = ''
section_b = ''

search_a = ''
search_n = ''
search_s = ''
search_sec = ''



@bot.message_handler(commands=['start'])
def start(message):
    with sq.connect('book_bot.db') as con:
        cur = con.cursor()
        cur.execute(
        '''CREATE TABLE IF NOT EXISTS books (
            book_id integer primary key autoincrement,
            name text,
            author text,
            style text,
            section text)''')
    con.commit()
    bot.send_message(message.chat.id, 'Добро пожаловать!')

@bot.message_handler(commands=['view'])
def view(message):
    with sq.connect('book_bot.db') as con:
        cur = con.cursor()
        cur.execute('''SELECT * FROM books''')
        rows = cur.fetchall()
        for i in rows:
            bot.send_message(message.chat.id,f'{";".join(map(str,i))}')
        
@bot.message_handler(commands=['delete'])
def delete_rec(message):
    del_id = bot.send_message(message.chat.id,'Введите id ')
    bot.register_next_step_handler(del_id,del_rec)
def del_rec(message):
    id = int(message.text)
    with sq.connect('book_bot.db') as con:
        cur = con.cursor()
        cur.execute('''DELETE FROM books WHERE book_id=?''',(id,))

@bot.message_handler(commands=['search'])
def search(message):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn_1 = types.InlineKeyboardButton(text="Название",callback_data='btn1')
    btn_2 = types.InlineKeyboardButton(text="Автор",callback_data='btn2')
    btn_3 = types.InlineKeyboardButton(text="Жанр",callback_data='btn3')
    btn_4 = types.InlineKeyboardButton(text="Секция",callback_data='btn4')
    btn_5 = types.InlineKeyboardButton(text="Поиск",callback_data='btn5')
    kb.add(btn_1,btn_2,btn_3,btn_4,btn_5)
    
    bot.send_message(message.chat.id,"Где будем искать?",reply_markup=kb)

@bot.callback_query_handler(func=lambda callback:callback.data)
def check_calback_data(callback):
    if callback.data == 'btn1':
        name_book = bot.send_message(callback.message.chat.id,"Напишите название книги")
        bot.register_next_step_handler(name_book,search_name)


    elif callback.data == 'btn2':
        author_book = bot.send_message(callback.message.chat.id,"Напишите автора книги")
        bot.register_next_step_handler(author_book,search_author)
      
    elif callback.data == 'btn3':
        style_book = bot.send_message(callback.message.chat.id,"Напишите жанр книги")
        bot.register_next_step_handler(style_book,search_style)
        
    elif callback.data == 'btn4':
        section_book = bot.send_message(callback.message.chat.id,"Напишите секцию")
        bot.register_next_step_handler(section_book,search_section)
    elif callback.data == 'btn5':
        with sq.connect('book_bot.db') as con:
            cur = con.cursor()
            cur.execute(
            '''SELECT * FROM books WHERE name=? OR author=? OR style=? OR section=?''',
            (search_n,search_a,search_s,search_sec))
            rows = cur.fetchall()
            for i in rows:
                bot.send_message(callback.message.chat.id,f'{";".join(map(str,i))}')
      
    
def search_name(message):
    global search_n
    search_n = message.text
def search_author(message):
    global search_a
    search_a = message.text
    print(search_a)

def search_style(message):
    global search_s
    search_s = message.text    

def search_section(message):
    global search_sec
    search_sec = message.text

@bot.message_handler(commands=['update'])         
def update(message):
    id_update = bot.send_message(message.chat.id,"Введите id")
    bot.register_next_step_handler(id_update,update_id)
    

def update_id(message):
    global updateid
    updateid = int(message.text)
    name_update = bot.send_message(message.chat.id,"Напишите название книги")
    bot.register_next_step_handler(name_update,update_name)

def update_name(message):
    global update_n
    update_n = message.text
    print(update_n)
    author_update = bot.send_message(message.chat.id,"Напишите автора книги")
    bot.register_next_step_handler(author_update,update_author)

def update_author(message):
    global update_a
    update_a = message.text
    style_update = bot.send_message(message.chat.id,"Напишите жанр книги")
    bot.register_next_step_handler(style_update,update_style)

def update_style(message):
    global update_s
    update_s = message.text
    section_update = bot.send_message(message.chat.id,"Напишите сектор книги")
    bot.register_next_step_handler(section_update,update_section)

def update_section(message):
    global update_sec
    update_sec = message.text
    with sq.connect('book_bot.db') as con:
        cur = con.cursor()
        cur.execute(
            '''UPDATE books SET name=?, author=?, style=?, section=? WHERE book_id=?''',
            (update_n,update_a,update_s,update_sec,updateid))
        rows = cur.fetchall()
        for i in rows:
            bot.send_message(message.chat.id,f'{";".join(map(str,i))}')
        view(message)



@bot.message_handler(content_types=['text'])
def get_text(message):
    name = bot.send_message(message.chat.id,'Введите пожалуйста название книги')
    bot.register_next_step_handler(name,add_name)
    
  
  
def add_name(message):
    global name_b
    name_b = message.text
    author = bot.send_message(message.chat.id, 'Введите пожалуйста автора книги')
    bot.register_next_step_handler(author,add_author)
  
def add_author(message):
    global author_b
    author_b = message.text
    style = bot.send_message(message.chat.id, 'Введите пожалуйста жанр книги')
    bot.register_next_step_handler(style,add_style)

def add_style(message):
    global style_b
    style_b = message.text
    section = bot.send_message(message.chat.id, 'Введите пожалуйста секцию')
    bot.register_next_step_handler(section,add_section)

def add_section(message):
    global section_b
    section_b = message.text
    bot.send_message(message.chat.id, 'Данные успешно добавлены!')
    with sq.connect('book_bot.db') as con:
        cur = con.cursor()
        cur.execute(
        "INSERT INTO books ('name','author','style','section') VALUES (?,?,?,?)",
        (name_b,
        author_b,
        style_b,
        section_b))


bot.polling()  


    





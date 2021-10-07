# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# v.1.4
import telebot
import datetime
import numbers
import pathlib

from telebot import types
from loguru import logger
from time import sleep

import db
import config


bot = telebot.TeleBot(config.TOKEN, threaded=False)

global len_urls, id_edit_message_add_urls

log_dir = pathlib.Path.home().joinpath('logs')
log_dir.mkdir(parents=True, exist_ok=True)

logger.add(log_dir.joinpath('bot-olga-service.log'),
           format='{time} [{level}] {module} {name} {function} - {message}',
           level='DEBUG', compression='zip', rotation='30 MB')


#######################################################################################################################

#db.init_db(FORCE_SAVES=True)
#db.init_db(FORCE_CATALOGS=True)
#db.init_db(FORCE_USERS=True)

#######################################################################################################################
def get_datetime():
    from datetime import datetime, timezone
    return str(datetime.now(timezone.utc))



def save_user_message(message):
    try:
        str_logs = get_datetime() + " -- message_from_id_user: " + str(message.chat.id) + "\n"
        str_logs += " + message_id: " + str(message.message_id) + "\n"
        str_logs += " + message.chat.type: " + str(message.chat.type) + "\n"
        str_logs += " + content_type: " + str(message.content_type) + "\n"
        str_logs += " + from_user.first_name: " + str(message.from_user.first_name) + "\n"
        str_logs += " + from_user.last_name: " + str(message.from_user.last_name) + "\n"
        str_logs += " + from_user.username: " + str(message.from_user.username) + "\n"

        smiles = u""
        str_logs_with_smiles = str_logs + u"smiles" + repr(smiles)  + "\n"  + "\n"

        str_logs += " + message.text: " + str(message.text) + "\n"
        str_logs += "\n"

        try:
            logger.info(str_logs)
            print(str_logs)
        except:
            logger.info(str_logs_with_smiles)
            print(str_logs_with_smiles)
    except Exception as e:
        logger.error(str(e))
        print(repr(e))


def save_bot_message(message, text: str):
    try:
        str_logs = get_datetime() + " -- BOT SEND in message.chat.id: " + str(message.chat.id) + "\n"
        str_logs += " + message_id: " + str(message.message_id) + "\n"
        str_logs += " + message.chat.type: " + str(message.chat.type) + "\n"
        str_logs += " + content_type: " + str(message.content_type) + "\n"
        str_logs += " + from_user.first_name: " + str(message.from_user.first_name) + "\n"
        str_logs += " + from_user.last_name: " + str(message.from_user.last_name) + "\n"
        str_logs += " + from_user.username: " + str(message.from_user.username) + "\n"
        str_logs += " + message.text: " + str(text) + "\n"
        str_logs += "\n"

        logger.info(str_logs)
        print(str_logs)
    except Exception as e:
        logger.error(str(e))
        print(repr(e))

def save_bot_admins_message(id: int, text: str):
    str_logs = get_datetime() + " -- BOT SEND in message.chat.id: " + str(id) + "\n"
    str_logs += " + text: " + text + "\n"
    str_logs += "\n"

    logger.info(str_logs)(str_logs)
    print(str_logs)


def save_other_message(message):
    try:
        str_logs = get_datetime() + " -- message_from_id_user: " + str(message.chat.id) + "\n"
        str_logs += " + message_id: " + str(message.message_id) + "\n"
        str_logs += " + content_type: " + str(message.content_type) + "\n"
        str_logs += " + message.chat.type: " + str(message.chat.type) + "\n"
        str_logs += " + from_user.first_name: " + str(message.from_user.first_name) + "\n"
        str_logs += " + from_user.last_name: " + str(message.from_user.last_name) + "\n"
        str_logs += " + from_user.username: " + str(message.from_user.username) + "\n"
        str_logs += "\n"

        logger.info(str_logs)
        print(str_logs)
    except Exception as e:
        logger.error(str(e))
        print(repr(e))

#######################################################################################################################

@bot.message_handler(content_types=['sticker', 'photo', 'audio', 'document', 'video', 'video_note', 'voice', 'location',
                                    'contact', 'new_chat_members', 'left_chat_member', 'new_chat_title',
                                    'new_chat_photo', 'delete_chat_photo', 'group_chat_created',
                                    'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id',
                                    'migrate_from_chat_id', 'pinned_message'])
def save_all_others_message(message):
    save_other_message(message)

#######################################################################################################################

# обработчик команды /start
@bot.message_handler(commands = ['start'])
def welcome(message):

    save_user_message(message)

    global len_urls
    try:
        perm = db.check_perm_user(USER_ID=message.from_user.id)

        if int(perm[0]) == 1:
            in_kb = types.InlineKeyboardMarkup(row_width=1)
            saves = types.InlineKeyboardButton(text="Сохранёнки 🎈", callback_data='select_catalog_for_users')
            in_kb.add(saves)

            if str(message.chat.id) in config.admins:
                admins = types.InlineKeyboardButton(text="Админка 🛠", callback_data='admins')
                in_kb.add(admins)

            text = "Добро пожаловать в Визуальный Рай!" + "\n" + "\n" + "\n" + "Жми скорей кнопку!"
            bot.send_message(message.chat.id, text, reply_markup=in_kb)

            len_urls = 1

            try:
                status_page = db.check_id_user(USER_ID=message.from_user.id)
                if int(status_page[0]) > 0:
                    db.up_page_user(PAGE="1", USER_ID=message.from_user.id)
            except Exception as e:
                if str(message.chat.id) in config.admin_2:
                    bot.reply_to(message, "Ooops!" + '\n' + '\n' + "Exception [00]:" + '\n' + repr(e))

            save_bot_message(message, text)

    except Exception as e:
        if str(message.chat.id) in config.admin_2:
            bot.reply_to(message, "Ooops!" + '\n' + '\n' + "Exception [01]:" + '\n' + repr(e))

#######################################################################################################################

# обработчик нажатий клавиш по клавиатуре
@bot.callback_query_handler(func = lambda message: True)
def menu(call):
    global ls, spisok, next_, len_urls, id_edit_message_add_urls

    spisok = []

    # отвечает за количество отображаемых категорий на странице
    pack_catalogs = 10
    try:
        sheet = db.get_catalogs()
        count = 0
        lengh = len(sheet)
        while count <= lengh:
            if count <= lengh:
                spisok.append(sheet[0 + count:pack_catalogs + count])
                count += pack_catalogs
            else:
                count = lengh - count
                spisok.append(sheet[0 + count:pack_catalogs + count])

        if call.message:
            if call.data == 'menu':
                in_kb = types.InlineKeyboardMarkup(row_width=1)
                saves = types.InlineKeyboardButton(text="Сохранёнки 🎈", callback_data='select_catalog_for_users')
                in_kb.add(saves)

                if str(call.message.chat.id) in config.admins:
                    admins = types.InlineKeyboardButton(text="Админка 🛠", callback_data='admins')
                    in_kb.add(admins)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Добро пожаловать в Визуальный Рай! 😍" + '\n' +
                                 '\n' + '\n' + "Жми скорей кнопку! 👇", reply_markup=in_kb)

            if call.data == 'saves':
                in_kb = types.InlineKeyboardMarkup(row_width=1)
                saves = types.InlineKeyboardButton(text="Категории 🎁", callback_data='select_catalog_for_users')
                in_kb.add(saves)
                if str(call.message.chat.id) in config.admins:
                    in_kb.add(types.InlineKeyboardButton(text="🎈️ В меню", callback_data='menu'))


                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Выберите интересующую Вас категорию:" + '\n' + '\n' +
                                           "❤️", reply_markup=in_kb)

            if call.data == 'admins':
                in_kb = types.InlineKeyboardMarkup(row_width=1)
                create_catalog = types.InlineKeyboardButton(text="Создать категорию 💎", callback_data='create_catalog')
                select_catalog = types.InlineKeyboardButton(text="Выбрать категорию 🎁", callback_data='select_catalog')
                delete_users = types.InlineKeyboardButton(text="Очистить пользователей 👻",
                                                          callback_data='delete_users')
                in_kb.add(create_catalog)
                in_kb.add(select_catalog)
                in_kb.add(delete_users)
                if str(call.message.chat.id) in config.admins:
                    in_kb.add(types.InlineKeyboardButton(text="🛠 В меню", callback_data='menu'))

                try:
                    kol_vo = db.get_count_catalogs()
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Количество существующих категорий:" + '\n' + '\n' + str(kol_vo[0]),
                                          reply_markup=in_kb)
                except Exception as e:
                    if str(call.message.chat.id) in config.admin_2:
                        bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [02]:" + '\n' + repr(e))

            if call.data == 'create_catalog':

                text = "Введите название категории:"
                send = bot.send_message(call.message.chat.id, text)
                save_bot_message(call.message, text)

                bot.register_next_step_handler(send, ins_cat)

            if call.data == 'select_catalog_for_users':
                in_kb = types.InlineKeyboardMarkup(row_width=2)

                y = 0
                while y < len_urls and len_urls - y > 1:
                    bot.delete_message(call.message.chat.id, call.message.message_id-y)
                    y += 1

                try:
                    next_ = db.check_page_user(USER_ID=call.from_user.id)
                    page = int(next_[0])

                    for i in spisok[page-1]:
                        in_kb.add(types.InlineKeyboardButton(text=i[0][0:], callback_data=f"name_user_{i}"))

                    if page == 1:
                        in_kb.add(types.InlineKeyboardButton(text="Вперёд ⏩", callback_data='next_for_users'))
                    elif page == len(spisok):
                        in_kb.add(types.InlineKeyboardButton(text="⏪ Назад", callback_data='back_for_users'))
                    else:
                        in_kb.add(types.InlineKeyboardButton(text="⏪ Назад", callback_data='back_for_users'),
                                  types.InlineKeyboardButton(text="Вперёд ⏩", callback_data='next_for_users'))
                    try:
                        db.up_page_user(PAGE=str(page), USER_ID=call.from_user.id)
                    except Exception as e:
                        if str(call.message.chat.id) in config.admin_2:
                            bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [03]:" + '\n' + repr(e))

                except Exception as e:
                    if str(call.message.chat.id) in config.admin_2:
                        bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [04]:" + '\n' + repr(e))

                if str(call.message.chat.id) in config.admins:
                    in_kb.add(types.InlineKeyboardButton(text="🎈️ В меню", callback_data='menu'))

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id-y,
                                      text="Выберите интересующую Вас категорию:" + '\n' + '\n' + "❤️",
                                      reply_markup=in_kb)

            if call.data == 'next_for_users':
                in_kb = types.InlineKeyboardMarkup(row_width=2)
                try:
                    next_ = db.check_page_user(USER_ID=call.from_user.id)
                    if int(next_[0]) + 1 <= len(spisok):
                        page = int(next_[0]) + 1

                        for i in spisok[page-1]:
                            in_kb.add(types.InlineKeyboardButton(text=i[0][0:], callback_data=f"name_user_{i}"))

                        if page == 1:
                            in_kb.add(types.InlineKeyboardButton(text="Вперёд ⏩", callback_data='next_for_users'))
                        elif page == len(spisok):
                            in_kb.add(types.InlineKeyboardButton(text="⏪ Назад", callback_data='back_for_users'))
                        else:
                            in_kb.add(types.InlineKeyboardButton(text="⏪ Назад", callback_data='back_for_users'),
                                      types.InlineKeyboardButton(text="Вперёд ⏩", callback_data='next_for_users'))
                        try:
                            db.up_page_user(PAGE=str(page), USER_ID=call.from_user.id)
                        except Exception as e:
                            if str(call.message.chat.id) in config.admin_2:
                                bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [05]:" + '\n' + repr(e))

                except Exception as e:
                    if str(call.message.chat.id) in config.admin_2:
                        bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [06]:" + '\n' + repr(e))

                if str(call.message.chat.id) in config.admins:
                    in_kb.add(types.InlineKeyboardButton(text="🎈️ В меню", callback_data='menu'))

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Выберите интересующую Вас категорию:" + '\n' + '\n' + "❤️",
                                      reply_markup=in_kb)

            if call.data == 'back_for_users':
                in_kb = types.InlineKeyboardMarkup(row_width=2)
                try:
                    next_ = db.check_page_user(USER_ID=call.from_user.id)
                    if int(next_[0]) - 1 <= len(spisok):
                        page = int(next_[0]) - 1

                        for i in spisok[page-1]:
                            in_kb.add(types.InlineKeyboardButton(text=i[0][0:], callback_data=f"name_user_{i}"))

                        if page == 1:
                            in_kb.add(types.InlineKeyboardButton(text="Вперёд ⏩", callback_data='next_for_users'))
                        elif page == len(spisok):
                            in_kb.add(types.InlineKeyboardButton(text="⏪ Назад", callback_data='back_for_users'))
                        else:
                            in_kb.add(types.InlineKeyboardButton(text="⏪ Назад", callback_data='back_for_users'),
                                      types.InlineKeyboardButton(text="Вперёд ⏩", callback_data='next_for_users'))
                        try:
                            db.up_page_user(PAGE=str(page), USER_ID=call.from_user.id)
                        except Exception as e:
                            if str(call.message.chat.id) in config.admin_2:
                                bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [07]:" + '\n' + repr(e))

                except Exception as e:
                    if str(call.message.chat.id) in config.admin_2:
                        bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [08]:" + '\n' + repr(e))

                if str(call.message.chat.id) in config.admins:
                    in_kb.add(types.InlineKeyboardButton(text="🎈️ В меню", callback_data='menu'))

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Выберите интересующую Вас категорию:" + '\n' + '\n' + "❤️",
                                      reply_markup=in_kb)

            if call.data == 'select_catalog':
                in_kb = types.InlineKeyboardMarkup(row_width=2)

                y = 0
                while y < len_urls and len_urls - y > 1:
                    bot.delete_message(call.message.chat.id, call.message.message_id-y)
                    y += 1

                try:
                    next_ = db.check_page_user(USER_ID=call.from_user.id)
                    page = int(next_[0])

                    for i in spisok[page - 1]:
                        in_kb.add(types.InlineKeyboardButton(text=i[0][0:], callback_data=f"name_admin_{i}"))

                    if page == 1:
                        in_kb.add(types.InlineKeyboardButton(text="Вперёд ⏩", callback_data='next'))
                    elif page == len(spisok):
                        in_kb.add(types.InlineKeyboardButton(text="⏪ Назад", callback_data='back'))
                    else:
                        in_kb.add(types.InlineKeyboardButton(text="⏪ Назад", callback_data='back'),
                                  types.InlineKeyboardButton(text="Вперёд ⏩", callback_data='next'))
                    try:
                        db.up_page_user(PAGE=str(page), USER_ID=call.from_user.id)
                    except Exception as e:
                        if str(call.message.chat.id) in config.admin_2:
                            bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [09]:" + '\n' + repr(e))

                except Exception as e:
                    if str(call.message.chat.id) in config.admin_2:
                        bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [10]:" + '\n' + repr(e))

                in_kb.add(types.InlineKeyboardButton(text="🎁 К категориям", callback_data='admins'))

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Выберите интересующую Вас категорию:" + '\n' + '\n' + "❤️",
                                      reply_markup=in_kb)

            if call.data == 'next':
                in_kb = types.InlineKeyboardMarkup(row_width=2)
                try:
                    next_ = db.check_page_user(USER_ID=call.from_user.id)
                    if int(next_[0]) + 1 <= len(spisok):
                        page = int(next_[0]) + 1

                        for i in spisok[page-1]:
                            in_kb.add(types.InlineKeyboardButton(text=i[0][0:], callback_data=f"name_admin_{i}"))

                        if page == 1:
                            in_kb.add(types.InlineKeyboardButton(text="Вперёд ⏩", callback_data='next'))
                        elif page == len(spisok):
                            in_kb.add(types.InlineKeyboardButton(text="⏪ Назад", callback_data='back'))
                        else:
                            in_kb.add(types.InlineKeyboardButton(text="⏪ Назад", callback_data='back'),
                                      types.InlineKeyboardButton(text="Вперёд ⏩", callback_data='next'))
                        try:
                            db.up_page_user(PAGE=str(page), USER_ID=call.from_user.id)
                        except Exception as e:
                            if str(call.message.chat.id) in config.admin_2:
                                bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [11]:" + '\n' + repr(e))

                except Exception as e:
                    if str(call.message.chat.id) in config.admin_2:
                        bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [12]:" + '\n' + repr(e))


                in_kb.add(types.InlineKeyboardButton(text="🎁 К категориям", callback_data='admins'))

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Выберите интересующую Вас категорию:" + '\n' + '\n' + "❤️",
                                      reply_markup=in_kb)

            if call.data == 'back':
                in_kb = types.InlineKeyboardMarkup(row_width=2)
                try:
                    next_ = db.check_page_user(USER_ID=call.from_user.id)
                    if int(next_[0]) - 1 >= 0:
                        page = int(next_[0]) - 1

                        for i in spisok[page-1]:
                            in_kb.add(types.InlineKeyboardButton(text=i[0][0:], callback_data=f"name_admin_{i}"))

                        if page == 1:
                            in_kb.add(types.InlineKeyboardButton(text="Вперёд ⏩", callback_data='next'))
                        elif page == len(spisok):
                            in_kb.add(types.InlineKeyboardButton(text="⏪ Назад", callback_data='back'))
                        else:
                            in_kb.add(types.InlineKeyboardButton(text="⏪ Назад", callback_data='back'),
                                      types.InlineKeyboardButton(text="Вперёд ⏩", callback_data='next'))
                        try:
                            db.up_page_user(PAGE=str(page), USER_ID=call.from_user.id)
                        except Exception as e:
                            if str(call.message.chat.id) in config.admin_2:
                                bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [13]:" + '\n' + repr(e))

                except Exception as e:
                    if str(call.message.chat.id) in config.admin_2:
                        bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [14]:" + '\n' + repr(e))

                in_kb.add(types.InlineKeyboardButton(text="🎁 К категориям", callback_data='admins'))

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Выберите интересующую Вас категорию:" + '\n' + '\n' + "❤️",
                                      reply_markup=in_kb)

            if "name_admin" in call.data:
                in_kb = types.InlineKeyboardMarkup(row_width=1)
                ls = call.data
                ls = ls.replace("name_admin_('",'')
                ls = ls.replace("',)", '')

                if str(call.message.chat.id) in config.admins:
                    change_catalog = types.InlineKeyboardButton(text="Переименовать категорию",
                                                                callback_data='change_catalog')
                    delete_catalog = types.InlineKeyboardButton(text="Удалить категорию",
                                                                callback_data='delete_catalog')
                    add_saves = types.InlineKeyboardButton(text="Пополнить коллекцию",
                                                                callback_data='add_saves')
                    in_kb.add(change_catalog)
                    in_kb.add(delete_catalog)
                    in_kb.add(add_saves)

                in_kb.add(types.InlineKeyboardButton(text="⬅️ Назад", callback_data='select_catalog'))

                id_edit_message_add_urls = call.message.message_id

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Редактирование категории:' + '\n' + '\n' + ls, reply_markup=in_kb)


            if "name_user" in call.data:
                in_kb = types.InlineKeyboardMarkup(row_width=1)
                ls = call.data
                ls = ls.replace("name_user_('",'')
                ls = ls.replace("',)", '')

                name = ls
                try:
                    id_ = db.check_id_catalog(NAME=name)

                    try:
                        urls = db.list_urls(CATALOG_ID=id_[0])
                        in_kb.add(types.InlineKeyboardButton(text="Закрыть", callback_data='select_catalog_for_users'))

                        len_urls = len(urls)
                        bot.delete_message(call.message.chat.id, call.message.message_id)

                        y = 1
                        for i in urls:
                            l_user = ""
                            if y < len(urls):
                                l_user = l_user + str(i[0]) + '\n' + '\n'
                                bot.send_message(chat_id=call.message.chat.id,
                                                 text=l_user)
                                save_bot_message(call.message, l_user)
                            else:
                                l_user = l_user + str(i[0]) + '\n' + '\n'
                                bot.send_message(chat_id=call.message.chat.id,
                                            text=l_user, reply_markup=in_kb)
                                save_bot_message(call.message, l_user)
                            y += 1

                    except Exception as e:
                        if str(call.message.chat.id) in config.admin_2:
                            bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [16]:" + '\n' + repr(e))

                except Exception as e:
                    if str(call.message.chat.id) in config.admin_2:
                        bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [17]:" + '\n' + repr(e))

            if call.data == 'add_saves':
                ls = call.message.text
                ls = ls.replace('Редактирование категории:' + '\n' + '\n', '')
                ls = ls.replace('\n' + '\n' + 'Запись добавлена!', '')
                try:
                    ls = db.check_id_catalog(NAME=ls)
                except Exception as e:
                    if str(call.message.chat.id) in config.admin_2:
                        bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [18]:" + '\n' + repr(e))

                text = "Введите ссылку:"
                send = bot.send_message(call.message.chat.id, text)
                save_bot_message(call.message, text)

                bot.register_next_step_handler(send, add_save)

            # Добавление прав пользователю
            if call.data == 'add_user':
                add_user = call.message.text
                idd = add_user.split('\n')[0][10:]
                text_sms = add_user.split('~')[0][10:]

                try:
                    db.add_perm(USER_ID=idd)
                    kill_perm = types.InlineKeyboardMarkup(row_width=2)
                    kill_user = types.InlineKeyboardButton(text="🪓 Изъять доступ!", callback_data='kill_user')
                    kill_perm.add(kill_user)

                    text = "Ура! Вам предоставлен доступ к боту.\n" + "Чтобы начать работу, нажмите на ссылку -> /start"
                    bot.send_message(chat_id=idd, text=text)
                    save_bot_message(idd, text)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="USER ID = " + text_sms + "~" + '\n' + '\n' + "✅ Доступ предоставлен!",
                                          reply_markup=kill_perm)
                except Exception as e:
                    if str(call.message.chat.id) in config.admin_2:
                        bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [19]:" + '\n' + repr(e))

            # Изъятие прав у пользователя
            if call.data == 'kill_user':
                kill_user = call.message.text
                idd = kill_user.split('\n')[0][10:]
                text_sms = kill_user.split('~')[0][10:]

                try:
                    db.kill_perm(USER_ID=idd)

                    add_perm = types.InlineKeyboardMarkup(row_width=2)
                    add_user = types.InlineKeyboardButton(text="Добавить пользователя", callback_data='add_user')
                    add_perm.add(add_user)

                    text = "Доступ закрыт!"
                    bot.send_message(chat_id=idd, text=text)
                    save_bot_message(idd, text)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="USER ID = " + text_sms + "~" + '\n' + '\n' + "❌ Доступ закрыт!",
                                          reply_markup=add_perm)
                except Exception as e:
                    if str(call.message.chat.id) in config.admin_2:
                        bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [20]:" + '\n' + repr(e))

            # Удаление всех пользователей не имеющих прав на доступ к боту (PERMISSIONS = 0)
            if call.data == 'delete_users':
                try:
                    db.delete_users()
                except Exception as e:
                    if str(call.message.chat.id) in config.admin_2:
                        bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [21]:" + '\n' + repr(e))

            if call.data == 'change_catalog':
                text = call.message.text
                name_catalog = text.replace("Редактирование категории:\n\n", "")
                try:
                    id_catalog = db.check_id_catalog(NAME=name_catalog)

                    text = "Введите название категории:"
                    send = bot.send_message(call.message.chat.id, text)
                    save_bot_message(idd, text)

                    bot.register_next_step_handler(send, change_name_catalog, id_catalog[0])
                except Exception as e:
                    if str(call.message.chat.id) in config.admin_2:
                        bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [22]:" + '\n' + repr(e))

            if call.data == 'delete_catalog':
                text = call.message.text
                name_catalog = text.replace("Редактирование категории:\n\n", "")
                try:
                    id_catalog = db.check_id_catalog(NAME=name_catalog)
                    db.delete_saves(ID=id_catalog[0])
                    db.delete_catalog(ID=id_catalog[0])

                    in_kb = types.InlineKeyboardMarkup(row_width=2)
                    try:
                        spisok = []
                        sheet = db.get_catalogs()
                        count = 0
                        lengh = len(sheet)
                        while count <= lengh:
                            if count <= lengh:
                                spisok.append(sheet[0 + count:pack_catalogs + count])
                                count += pack_catalogs
                            else:
                                count = lengh - count
                                spisok.append(sheet[0 + count:pack_catalogs + count])
                        next_ = db.check_page_user(USER_ID=call.from_user.id)

                        for i in spisok[int(next_[0]) - 1]:
                            in_kb.add(types.InlineKeyboardButton(text=i[0][0:], callback_data=f"name_admin_{i}"))

                        if int(next_[0]) == 1:
                            in_kb.add(types.InlineKeyboardButton(text="Вперёд ⏩", callback_data='next'))
                        elif int(next_[0]) == len(spisok):
                            in_kb.add(types.InlineKeyboardButton(text="⏪ Назад", callback_data='back'))
                        else:
                            in_kb.add(types.InlineKeyboardButton(text="⏪ Назад", callback_data='back'),
                                      types.InlineKeyboardButton(text="Вперёд ⏩", callback_data='next'))

                    except Exception as e:
                        if str(call.message.chat.id) in config.admin_2:
                            bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [23]:" + '\n' + repr(e))


                    in_kb.add(types.InlineKeyboardButton(text="🎁 К категориям", callback_data='admins'))

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Выберите интересующую Вас категорию:" + '\n' + '\n' + "❤️",
                                          reply_markup=in_kb)

                except Exception as e:
                    if str(call.message.chat.id) in config.admin_2:
                        bot.reply_to(call.message, "Ooops!" + '\n' + '\n' + "Exception [24]:" + '\n' + repr(e))

    except Exception as e:
        print(repr(e))

#######################################################################################################################

# обработчик текстовых сообщейни отправленных боту
@bot.message_handler(content_types=['text'])
# регистрация нового пользователя
def text_from_user(message):

    save_user_message(message)

    try:
        security = types.InlineKeyboardMarkup(row_width=2)
        add_user = types.InlineKeyboardButton(text="Добавить пользователя", callback_data='add_user')
        security.add(add_user)

        user = db.check_id_user(USER_ID=message.from_user.id)
        if user[0] == 0:
            try:
                # функция которая записывает USER ID в БД
                db.ins_users(USER_ID=message.from_user.id,
                             FIRST_NAME=message.from_user.first_name,
                             LAST_NAME=message.from_user.last_name,
                             USER_NAME=message.from_user.username,
                             PERMISSIONS="0",
                             PAGE="1")

                # рассылка Ольге -- добавить пользователя
                text = "USER ID = " + \
                str(message.from_user.id) + "\n" + "\n" + \
                str(message.from_user.first_name) + " " + \
                str(message.from_user.last_name) + " @" + \
                str(message.from_user.username) + "\n" + "\n" + \
                "Сообщение: "  + message.text + "~"
                bot.send_message(441039920, text=text, reply_markup=security)
                save_bot_admins_message(441039920, text)

                # рассылка мне -- добавить пользователя
                text = "USER ID = " + \
                str(message.from_user.id) + "\n" + "\n" + \
                str(message.from_user.first_name) + " " + \
                str(message.from_user.last_name) + " @" + \
                str(message.from_user.username) + "\n" + "\n" + \
                "Сообщение: "  + message.text + "~"
                bot.send_message(370314854, text=text, reply_markup=security)
                save_bot_admins_message(370314854, text)


            except Exception as e:
                if str(message.chat.id) in config.admin_2:
                    bot.reply_to(message, "Ooops!" + '\n' + '\n' + "Exception [25]:" + '\n' + repr(e))

    except Exception as e:
        if str(message.chat.id) in config.admin_2:
            bot.reply_to(message, "Ooops!" + '\n' + '\n' + "Exception [26]:" + '\n' + repr(e))

    if message.content_type == 'text' and (message.text == "Введите название категории:" or
                                           message.from_user.is_bot == True) and str(message.chat.id) in config.admins:
        text = "Введите название категории:"
        send = bot.send_message(message.chat.id, text)
        save_bot_message(message, text)

        bot.register_next_step_handler(send, ins_cat)

    if message.content_type == 'text' and (message.text == "Введите ссылку:" or
                                           message.from_user.is_bot == True) and str(message.chat.id) in config.admins:
        text = "Введите ссылку:"
        send = bot.send_message(message.chat.id, text)
        save_bot_message(message, text)

        bot.register_next_step_handler(send, add_save)

# создание новой категории
def ins_cat(message):
    in_kb = types.InlineKeyboardMarkup(row_width=1)
    create_catalog = types.InlineKeyboardButton(text="Создать категорию 💎", callback_data='create_catalog')
    select_catalog = types.InlineKeyboardButton(text="Выбрать категорию 🎁", callback_data='select_catalog')
    delete_users = types.InlineKeyboardButton(text="Очистить пользователей 👻", callback_data='delete_users')
    in_kb.add(create_catalog)
    in_kb.add(select_catalog)
    in_kb.add(delete_users)
    if str(message.chat.id) in config.admins:
        in_kb.add(types.InlineKeyboardButton(text="🛠️ Назад", callback_data='menu'))

    # опрашиваем БД на наличие данного каталога
    try:
        count_catalog = db.check_catalog(NAME=message.text)

        if count_catalog[0] == 0:
            # создаём новую, уникальную категорию
            try:
                db.ins_cat(NAME=message.text)
                try:
                    kol_vo = db.get_count_catalogs()

                    bot.delete_message(message.chat.id, message.message_id)
                    bot.delete_message(message.chat.id, message.message_id - 1)
                    bot.delete_message(message.chat.id, message.message_id - 2)

                    text = "Количество существующих категорий:" + "\n" + "\n" + str(kol_vo[0])
                    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=in_kb)
                    save_bot_message(message, text)

                except Exception as e:
                    if str(message.chat.id) in config.admin_2:
                        bot.reply_to(message, "Ooops!" + '\n' + '\n' + "Exception [27]:" + '\n' + repr(e))

            except Exception as e:
                if str(message.chat.id) in config.admin_2:
                    bot.reply_to(message, "Ooops!" + '\n' + '\n' + "Exception [28]:" + '\n' + repr(e))
        else:
            # отправляем сообщение с введённой категорией
            try:
                kol_vo = db.get_count_catalogs()

                text = "Количество существующих категорий:" + "\n" + "\n" + str(kol_vo[0])
                bot.send_message(chat_id=message.chat.id, text=text, reply_markup=in_kb)
                save_bot_message(message, text)

                save_bot_message(message, text)
            except Exception as e:
                if str(message.chat.id) in config.admin_2:
                    bot.reply_to(message, "Ooops!" + '\n' + '\n' + "Exception [29]:" + '\n' + repr(e))

    except Exception as e:
        # отправляем сообщение с введённой категорией
        try:
            kol_vo = db.get_count_catalogs()

            text = "Количество существующих категорий:" + "\n" + "\n" + str(kol_vo[0])
            bot.send_message(chat_id=message.chat.id, text=text, reply_markup=in_kb)
            save_bot_message(message, text)

        except Exception as ee:
            if str(message.chat.id) in config.admin_2:
                bot.reply_to(message, "Ooops!" + '\n' + '\n' + "Exception [30]:" + '\n' + repr(ee))

        if str(message.chat.id) in config.admin_2:
            bot.reply_to(message, "Ooops!" + '\n' + '\n' + "Exception [31]:" + '\n' + repr(e))

# переименование категории
def change_name_catalog(message, id_catalog: int):
    text = message.text
    name_catalog = text.replace("Редактирование категории:\n\n", "")

    try:
        db.up_name_catalog(NAME=name_catalog, ID=id_catalog)
        in_kb = types.InlineKeyboardMarkup(row_width=1)

        if str(message.chat.id) in config.admins:
            change_catalog = types.InlineKeyboardButton(text="Переименовать категорию",
                                                        callback_data='change_catalog')
            delete_catalog = types.InlineKeyboardButton(text="Удалить категорию",
                                                        callback_data='delete_catalog')
            add_saves = types.InlineKeyboardButton(text="Пополнить коллекцию",
                                                   callback_data='add_saves')
            in_kb.add(change_catalog)
            in_kb.add(delete_catalog)
            in_kb.add(add_saves)

        in_kb.add(types.InlineKeyboardButton(text="⬅️ Назад", callback_data='select_catalog'))

        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)

        text = 'Редактирование категории:' + '\n' + '\n' + name_catalog
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=in_kb)
        save_bot_message(message, text)

    except Exception as e:
        if str(message.chat.id) in config.admin_2:
            bot.reply_to(message, "Ooops!" + '\n' + '\n' + "Exception [32]:" + '\n' + repr(e))

# добавляет сохранёнки в каталог
def add_save(message):
    global id_edit_message_add_urls
    try:
        db.ins_saves(CATALOG_ID=int(ls[0]),URL=message.text)
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id-1)

        if str(message.chat.id) in config.admins:
            in_kb = types.InlineKeyboardMarkup(row_width=1)
            change_catalog = types.InlineKeyboardButton(text="Переименовать категорию",
                                                        callback_data='change_catalog')
            delete_catalog = types.InlineKeyboardButton(text="Удалить категорию",
                                                        callback_data='delete_catalog')
            add_saves = types.InlineKeyboardButton(text="Пополнить коллекцию",
                                                   callback_data='add_saves')
            in_kb.add(change_catalog)
            in_kb.add(delete_catalog)
            in_kb.add(add_saves)

            in_kb.add(types.InlineKeyboardButton(text="⬅️ Назад", callback_data='select_catalog'))

            name_catalog = db.check_name_catalog(ID=ls[0])
            delta = message.message_id - id_edit_message_add_urls

            try:
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id-int(delta),
                                  text='Редактирование категории:' + '\n' + '\n' + name_catalog[0] + '\n' + '\n' +
                                       'Запись добавлена!' + '\n', reply_markup=in_kb)
            except Exception as ee:
                print(repr(ee))

    except Exception as e:
        if str(message.chat.id) in config.admin_2:
            bot.reply_to(message, "Ooops!" + '\n' + '\n' + "Exception [33]:" + '\n' + repr(e))

#######################################################################################################################

while True:
    try:
        bot.polling(none_stop=True, timeout=120)
    except Exception as e:
        print(repr(e))
        logger.error(str(e))
        sleep(5)














































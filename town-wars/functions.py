# -*- coding: utf-8 -*-
from constants import *
import sys
import time
import random
import sqlite3
import telebot
import traceback



def after_restart():
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM WorkStatus")
    mas = cursor.fetchall()
    for i in mas:
        id = i[0]
        if i[1] != 0:
            cursor.execute("UPDATE WorkStatus SET Status = 0 WHERE ID = '{0}'".format(id))
            cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(id))
            cursor.execute(
                "UPDATE Players SET Status = '{1}' WHERE ID = '{0}'".format(id, "\U0001F6CCТы сейчас отдыхаешь"))
            connection.commit()


after_restart()


def excepter(message):
    error_class = sys.exc_info()[0]
    error = sys.exc_info()[1]
    line = sys.exc_info()[2].tb_lineno
    
    mas_time = time.asctime().split()
    string_time = mas_time[2] + " " + mas_time[1] + " " + mas_time[4] + " | " + mas_time[3]
    
    file_name = "Error"
    file = open('{0}.txt'.format(file_name), 'w')
    file.write('Filename: ' + 'Main bot file' + '\n')
    file.write('Line: ' + str(line) + '\n')
    file.write('Error class: ' + str(error_class) + '\n')
    file.write('Error: ' + str(error) + '\n')
    file.write('Time: ' + str(string_time) + '\n')
    file.write('\n')
    if message != '':
        file.write('USER:' + '\n')
        file.write('id: ' + str(message.from_user.id) + '\n')
        file.write('is_bot: ' + str(message.from_user.is_bot) + '\n')
        file.write('username: ' + str(message.from_user.username) + '\n')
        file.write('first_name: ' + str(message.from_user.first_name) + '\n')
        file.write('last_name: ' + str(message.from_user.last_name) + '\n')
        file.write('language_code: ' + str(message.from_user.language_code) + '\n')
        file.write('\n')
    file.write('System traceback:' + '\n')
    for sys_string in traceback.format_tb(sys.exc_info()[2]):
        file.write(str(sys_string))
    file.close()
    
    file_to_send = open('{0}.txt'.format(file_name), 'r')
    bot.send_document(287352001, file_to_send)
    bot.send_message(message.from_user.id, "<b>Software error has occurred. Report already has been sent to developers. Sorry.</b>", parse_mode = 'HTML')  


def player_information(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Inventory_on WHERE ID = '{0}'".format(message.from_user.id))
    mas_inventory_on = cursor.fetchone()
    cursor.execute("SELECT * FROM Players WHERE ID = '{0}'".format(message.from_user.id))
    mas_player = cursor.fetchone()

    str1 = ""

    if mas_player[6] >= int(((1.3 * mas_player[3]) ** 3 + 5)):
        str1 += "\U0001F31FУ тебя новый уровень!\U0001F31F \n"
        str1 += "Жми /level_up \n"
        str1 += "\n"

    now_time = list(time.gmtime())
    now_time[3] += 3
    hours = 4 - now_time[3] % 4 - 1
    minutes = 60 - now_time[4] - 1
    seconds = 60 - now_time[5] - 1

    if hours == 0:
        hours_name = "часов"
    elif hours == 1:
        hours_name = "час"
    elif hours == 2 or hours == 3:
        hours_name = "часа"

    if minutes in [11, 12, 13, 14]:
        minutes_name = "минут"
    elif minutes % 10 == 1:
        minutes_name = "минуту"
    elif minutes % 10 in [2, 3, 4]:
        minutes_name = "минуты"
    elif minutes % 10 in [5, 6, 7, 8, 9, 0]:
        minutes_name = "минут"

    if seconds in [11, 12, 13, 14]:
        seconds_name = "секунд"
    elif seconds % 10 == 1:
        seconds_name = "секунду"
    elif seconds % 10 in [2, 3, 4]:
        seconds_name = "секунды"
    elif seconds % 10 in [5, 6, 7, 8, 9, 0]:
        seconds_name = "секунд"

    str1 += "\U0000231AСледующая битва через "
    if hours != 0:
        str1 += "<b>{0} {1}</b> ".format(hours, hours_name)
    if minutes != 0:
        str1 += "<b>{0} {1}</b> ".format(minutes, minutes_name)
    if seconds != 0:
        str1 += "<b>{0} {1}</b> ".format(seconds, seconds_name)
    str1 += "\n"
    str1 += "\n"

    str1 += "\U0001F3C2<b>{0}</b>\n".format(mas_player[2])
    str1 += "{0}\n".format(mas_player[1])
    str1 += "\U0001F4A5Уровень: {0} \n".format(mas_player[3])
    str1 += "\U0001F5E1Атака: {0}  \U0001F6E1Защита: {1} \n".format(mas_player[4], mas_player[5])
    str1 += "\U0001F31FОпыт: {0}/{1}\n".format(mas_player[6], int(((1.3 * mas_player[3]) ** 3 + 5)))
    str1 += "\U0001F4B0Банковский счет: {0}$ \n".format(mas_player[7])
    str1 += "\U0001F50BВыносливость: {0} из {1} \n".format(mas_player[8], mas_player[9])

    set_attack, set_defence = set_check(mas_inventory_on)

    sum_attack = dict_inventory[mas_inventory_on[1]][2] + dict_inventory[mas_inventory_on[2]][2] + dict_inventory[mas_inventory_on[4]][2]
    sum_attack += dict_inventory[mas_inventory_on[5]][2] + dict_inventory[mas_inventory_on[6]][2] + dict_inventory[mas_inventory_on[7]][2]
    sum_attack += dict_inventory[mas_inventory_on[8]][2] + set_attack

    sum_defence = dict_inventory[mas_inventory_on[1]][3] + dict_inventory[mas_inventory_on[2]][3] + dict_inventory[mas_inventory_on[4]][3]
    sum_defence += dict_inventory[mas_inventory_on[5]][3] + dict_inventory[mas_inventory_on[6]][3] + dict_inventory[mas_inventory_on[7]][3]
    sum_defence += dict_inventory[mas_inventory_on[8]][3] + set_defence

    str1 += "\U0001F392Снаряжение: +{0}\U0001F5E1 +{1}\U0001F6E1 \n".format(sum_attack, sum_defence)
    str1 += "\n"
    str1 += "\U0001F530<b>Состояние</b>: \n"
    str1 += "{0}".format(mas_player[10])

    bot.send_message(message.from_user.id, str1, reply_markup=show_keyboard_main, parse_mode="html")


def equipment_check(mas, str1):
    for i in range(len(mas)):
        if str1 == mas[i]:
            return(i)
    return(-1)


def set_check(mas_inventory_on):
    helmet_set = dict_inventory[mas_inventory_on[4]][1]
    armor_set = dict_inventory[mas_inventory_on[5]][1]
    gloves_set = dict_inventory[mas_inventory_on[6]][1]
    pants_set = dict_inventory[mas_inventory_on[7]][1]
    boots_set = dict_inventory[mas_inventory_on[8]][1]
    if helmet_set == armor_set == gloves_set == pants_set == boots_set:
        if helmet_set == "Комфорт":
            return 1, 1
        elif helmet_set == "Вызов":
            return 2, 2
        elif helmet_set == "Статус":
            return 3, 3
        elif helmet_set == "Страж":
            return 4, 4
        elif helmet_set == "Дельта":
            return 5, 5
        elif helmet_set == "Шилд":
            return 0, 10
        elif helmet_set == "Шкура дракона":
            return 10, 0
        elif helmet_set == "Пусто":
            return 0, 0
    else:
        return 0, 0


def horse_maker(horse, game_length):
    str1 = "_" * (game_length - horse)
    str1 += "\U0001F3C7"
    str1 += "_" * (horse - 1)
    return str1


# ------------------------------------------------------


def technical_work(message):
    bot.send_message(message.from_user.id, "Сейчас идут технические работы!", reply_markup=show_keyboard_stop_bot)


def the_battle_is(message):
    bot.send_message(message.from_user.id, "Сейчас идет битва!", reply_markup=show_keyboard_main)


def registration_1(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Players WHERE ID = '{0}'".format(message.from_user.id))
    cursor.execute("DELETE FROM WorkStatus WHERE ID = '{0}'".format(message.from_user.id))
    cursor.execute("DELETE FROM Inventory_on WHERE ID = '{0}'".format(message.from_user.id))
    cursor.execute("DELETE FROM Inventory_off WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    bot.send_message(message.from_user.id, "Я тебя пока что не знаю! Как мне тебя называть?")
    cursor.execute("INSERT INTO WorkStatus VALUES(?, ?, ?)",
                   (message.from_user.id, 1, 0))
    cursor.execute("INSERT INTO Players VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (message.from_user.id, 0, "NoNickName", 1, 1, 1, 0, 0, 5, 5, "\U0001F6CCТы сейчас отдыхаешь!", 0, 0))
    cursor.execute("INSERT INTO Inventory_on VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (message.from_user.id, "Пусто", "Пусто", "Пусто", "Пусто", "Пусто", "Пусто", "Пусто", "Пусто", "Нет",
                    "Пусто"))
    cursor.execute("INSERT INTO Inventory_off VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (message.from_user.id, "Пусто", "Пусто", "Пусто", "Пусто", "Пусто", "Пусто", "Пусто",
                    "Пусто", "Пусто", "Пусто", "Пусто", "Пусто", "Пусто", "Пусто", "Пусто", "Пусто"))
    connection.commit()
    connection.close()


def registration_2(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM WorkStatus WHERE ID = '{0}'".format(message.from_user.id))
    mas_workstatus = cursor.fetchone()

    if mas_workstatus[1] == 1:
        if len(message.text) > 20:
            bot.send_message(message.from_user.id, "Имя не может быть длиннее 20 символов")
        else:
            bot.send_message(message.from_user.id, "А за кого ты хочешь играть?", reply_markup=show_keyboard_clan)
            cursor.execute("UPDATE WorkStatus SET Status = 2 WHERE ID = '{0}'".format(message.from_user.id))
            cursor.execute(
                "UPDATE Players SET Nickname = '{1}' WHERE ID = '{0}'".format(message.from_user.id, message.text))
            connection.commit()
            connection.close()
    elif mas_workstatus[1] == 2:
        if message.text in ["\U0001F004Мафия", "\U0001F694Спецназ", "\U0001F5E1Наёмники", "\U0001F44AМародёры"]:
            bot.send_message(message.from_user.id, "Прекрасный выбор!")
            cursor.execute("UPDATE WorkStatus SET Status = 0 WHERE ID = {0}".format(message.from_user.id))
            cursor.execute("UPDATE Players SET Clan = '{1}' WHERE ID = {0}".format(message.from_user.id, message.text))
            connection.commit()
            connection.close()
            player_information(message)
        else:
            bot.send_message(message.from_user.id, "Нет такого клана!")


def the_adventure_is(message):
    if message.text == "\U0001F3C2Боец":
        warrior(message)
    elif message.text == "\U0001F4DCОтчет" or message.text == "/report":
        report(message)
    elif message.text == "\U00002139F.A.Q.":
        faq(message)
    elif message.text == "\U00002B05Назад":
        back(message)
    else:
        bot.send_message(message.from_user.id, "Ты сейчас занят приключением!")


def the_cards(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Players WHERE ID = '{0}'".format(message.from_user.id))
    mas_player = cursor.fetchone()
    cursor.execute("SELECT * FROM WorkStatus WHERE ID = '{0}'".format(message.from_user.id))
    mas_workstatus = cursor.fetchone()

    cursor.execute("UPDATE Workstatus SET Status = 24 WHERE ID = {0}".format(message.from_user.id))
    connection.commit()
    connection.close()

    try:
        bet = int(message.text)
        bot.send_message(message.from_user.id, "Твоя ставка - {0}$!".format(bet), reply_markup=show_keyboard_bar)
        index_cards = random.randint(1, 100)
        if mas_player[7] >= bet:
            connection = sqlite3.connect("database", check_same_thread=False)
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE Players SET Money = {1} WHERE ID = {0}".format(message.from_user.id, mas_player[7] - bet))
            connection.commit()
            connection.close()
            time.sleep(10)
            connection = sqlite3.connect("database", check_same_thread=False)
            cursor = connection.cursor()
            if mas_workstatus[1] == 21:
                if index_cards > 30:
                    cursor.execute("UPDATE Players SET Money = {1} WHERE ID = {0}".format(message.from_user.id,
                                                                                          mas_player[
                                                                                              7] + 1.3 * bet // 1 + 1))
                    connection.commit()
                    bot.send_message(message.from_user.id,
                                     "Поздравляю, ты обыграл пьяницу без особых усилий и заработал {0}$! "
                                     "Может сыграешь с девушкой, которая сидит рядом с тобой?"
                                     .format(int(1.3 * bet // 1 + 1)),
                                     reply_markup=show_keyboard_bar)
                else:
                    bot.send_message(message.from_user.id,
                                     "К сожалению, ты проиграл пьянице. Может в другой раз повезет?",
                                     reply_markup=show_keyboard_bar)

            elif mas_workstatus[1] == 22:
                if index_cards > 70:
                    cursor.execute("UPDATE Players SET Money = {1} WHERE ID = {0}".format(message.from_user.id,
                                                                                          mas_player[
                                                                                              7] + 2 * bet // 1 + 1))
                    connection.commit()
                    bot.send_message(message.from_user.id, "Поздравляю, ты обыграл девушку и заработал {0}$! "
                                                           "Может стоит попробовать сыграть с мастером?"
                                     .format(int(2 * bet // 1 + 1)),
                                     reply_markup=show_keyboard_bar)
                else:
                    bot.send_message(message.from_user.id,
                                     "К сожалению, ты проиграл девушке. Может в другой раз повезет?",
                                     reply_markup=show_keyboard_bar)

            elif mas_workstatus[1] == 23:
                if index_cards > 90:
                    cursor.execute("UPDATE Players SET Money = {1} WHERE ID = {0}".format(message.from_user.id,
                                                                                          mas_player[
                                                                                              7] + 5 * bet // 1 + 1))
                    connection.commit()
                    bot.send_message(message.from_user.id,
                                     "Поздравляю, у тебя получилось обыграть мастера и ты заработал {0}$! "
                                     "Похоже, что ты профессионал!"
                                     .format(int(5 * bet // 1 + 1)),
                                     reply_markup=show_keyboard_bar)
                else:
                    bot.send_message(message.from_user.id,
                                     "Как и ожидалось, ты проиграл мастеру. Может в другой раз повезет?",
                                     reply_markup=show_keyboard_bar)

        else:
            bot.send_message(message.from_user.id,
                             "Ты попытался обмануть, но тебя разоблачили и выкинули из бара! У тебя недостаточно денег для такой ставки!",
                             reply_markup=show_keyboard_main)

    except:
        if message.text == "\U00002B05Назад":
            bar(message)
        else:
            bot.send_message(message.from_user.id, "Прикольная ставка, но тут принимаются только $!",
                             reply_markup=show_keyboard_bar)

    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("UPDATE Workstatus SET Status = 0 WHERE ID = {0}".format(message.from_user.id))
    connection.commit()
    connection.close()


def the_cards_is(message):
    bot.send_message(message.from_user.id, "Ты сейчас играешь в карты!", reply_markup=show_keyboard_bar)


def changing_smth(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM WorkStatus WHERE ID = '{0}'".format(message.from_user.id))
    mas_workstatus = cursor.fetchone()

    if mas_workstatus[1] == 31:
        cursor.execute("UPDATE WorkStatus SET Status = 0 WHERE ID = '{0}'".format(message.from_user.id))
        connection.commit()
        connection.close()
        bot.send_message(message.from_user.id, "Ха, обманул. Фракцию нельзя поменять.", reply_markup=show_keyboard_main)

    elif mas_workstatus[1] == 32:
        if len(message.text) > 20:
            bot.send_message(message.from_user.id, "Имя не может быть длиннее 20 символов")
        else:
            cursor.execute("UPDATE WorkStatus SET Status = 0 WHERE ID = '{0}'".format(message.from_user.id))
            cursor.execute(
                "UPDATE Players SET Nickname = '{1}' WHERE ID = '{0}'".format(message.from_user.id, message.text))
            connection.commit()
            connection.close()
            bot.send_message(message.from_user.id, "Ты сменил свой ник")


def the_horses(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Players WHERE ID = '{0}'".format(message.from_user.id))
    mas_player = cursor.fetchone()
    cursor.execute("SELECT * FROM WorkStatus WHERE ID = '{0}'".format(message.from_user.id))
    mas_workstatus = cursor.fetchone()

    if mas_workstatus[1] == 41:
        cursor.execute("UPDATE WorkStatus SET Status = 45 WHERE ID = '{0}'".format(message.from_user.id))
    elif mas_workstatus[1] == 42:
        cursor.execute("UPDATE WorkStatus SET Status = 46 WHERE ID = '{0}'".format(message.from_user.id))
    elif mas_workstatus[1] == 43:
        cursor.execute("UPDATE WorkStatus SET Status = 47 WHERE ID = '{0}'".format(message.from_user.id))
    elif mas_workstatus[1] == 44:
        cursor.execute("UPDATE WorkStatus SET Status = 48 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()

    cursor.execute("SELECT * FROM WorkStatus WHERE ID = '{0}'".format(message.from_user.id))
    mas_workstatus = cursor.fetchone()

    try:
        bet = int(message.text)
        bot.send_message(message.from_user.id, "Твоя ставка - {0}$!".format(bet), reply_markup=show_keyboard_bar)
        if mas_player[7] >= bet:
            horse_1 = 1
            horse_2 = 1
            horse_3 = 1
            horse_4 = 1
            game_length = 30
            str1 = "01/30" + "  \U0001F3C1" + horse_maker(horse_1, game_length) + "\n"
            str1 += "01/30" + "  \U0001F3C1" + horse_maker(horse_2, game_length) + "\n"
            str1 += "01/30" + "  \U0001F3C1" + horse_maker(horse_3, game_length) + "\n"
            str1 += "01/30" + "  \U0001F3C1" + horse_maker(horse_4, game_length) + "\n"
            bot.send_message(message.from_user.id, str1, reply_markup=show_keyboard_horses, parse_mode="html")
            time.sleep(1)
            while True:
                horse_1 += random.randint(1, 3)
                horse_2 += random.randint(1, 3)
                horse_3 += random.randint(1, 3)
                horse_4 += random.randint(1, 3)

                if horse_1 > game_length:
                    horse_1 = game_length
                if horse_2 > game_length:
                    horse_2 = game_length
                if horse_3 > game_length:
                    horse_3 = game_length
                if horse_4 > game_length:
                    horse_4 = game_length

                if horse_1 < 10:
                    horse_5 = "0" + str(horse_1)
                else:
                    horse_5 = str(horse_1)
                if horse_2 < 10:
                    horse_6 = "0" + str(horse_2)
                else:
                    horse_6 = str(horse_2)
                if horse_3 < 10:
                    horse_7 = "0" + str(horse_3)
                else:
                    horse_7 = str(horse_3)
                if horse_4 < 10:
                    horse_8 = "0" + str(horse_4)
                else:
                    horse_8 = str(horse_4)

                str1 = horse_5 + "/30" + "  \U0001F3C1" + horse_maker(horse_1, game_length) + "\n"
                str1 += horse_6 + "/30" + "  \U0001F3C1" + horse_maker(horse_2, game_length) + "\n"
                str1 += horse_7 + "/30" + "  \U0001F3C1" + horse_maker(horse_3, game_length) + "\n"
                str1 += horse_8 + "/30" + "  \U0001F3C1" + horse_maker(horse_4, game_length) + "\n"
                bot.send_message(message.from_user.id, str1, reply_markup=show_keyboard_horses, parse_mode="html")
                if horse_1 >= game_length:
                    win = 45
                    bot.send_message(message.from_user.id, "1\U0001F3C7 победила!", reply_markup=show_keyboard_horses,
                                     parse_mode="html")
                    break
                elif horse_2 >= game_length:
                    win = 46
                    bot.send_message(message.from_user.id, "2\U0001F3C7 победила!", reply_markup=show_keyboard_horses,
                                     parse_mode="html")
                    break
                elif horse_3 >= game_length:
                    win = 47
                    bot.send_message(message.from_user.id, "3\U0001F3C7 победила!", reply_markup=show_keyboard_horses,
                                     parse_mode="html")
                    break
                elif horse_4 >= game_length:
                    win = 48
                    bot.send_message(message.from_user.id, "4\U0001F3C7 победила!", reply_markup=show_keyboard_horses,
                                     parse_mode="html")
                    break
                time.sleep(1)
            if win == mas_workstatus[1]:
                cursor.execute("UPDATE Players SET Money = '{1}' WHERE ID = '{0}'"
                               .format(message.from_user.id, mas_player[7] + bet * 3))
                bot.send_message(message.from_user.id,
                                 "Поздравляю! Твоя лошадь победила. Ты выиграл {0}$".format(bet * 3),
                                 reply_markup=show_keyboard_horses,
                                 parse_mode="html")
            else:
                cursor.execute("UPDATE Players SET Money = '{1}' WHERE ID = '{0}'"
                               .format(message.from_user.id, mas_player[7] - bet))
                bot.send_message(message.from_user.id,
                                 "К сожалению, твоя лошадь проиграла. Ты потерял {0}$".format(bet),
                                 reply_markup=show_keyboard_horses,
                                 parse_mode="html")
            connection.commit()

        else:
            bot.send_message(message.from_user.id,
                             "Ты попытался обмануть, но тебя разоблачили и выкинули c ипподрома! У тебя недостаточно денег для такой ставки!",
                             reply_markup=show_keyboard_main)

    except:
        if message.text == "\U00002B05Назад":
            hippodrome_1(message)
        else:
            bot.send_message(message.from_user.id, "Прикольная ставка, но тут принимаются только $!",
                             reply_markup=show_keyboard_horses, parse_mode="html")
            cursor.execute("UPDATE WorkStatus SET Status_2 = 1 WHERE ID = '{0}'".format(message.from_user.id))
            connection.commit()

    cursor.execute("UPDATE WorkStatus SET Status = 0 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def the_horses_are(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM WorkStatus WHERE ID = '{0}'".format(message.from_user.id))
    mas_workstatus = cursor.fetchone()

    if mas_workstatus[1] == 45:
        bot.send_message(message.from_user.id, "Внимательнее смотри за своей лошадью - 1\U0001F3C7")
    elif mas_workstatus[1] == 46:
        bot.send_message(message.from_user.id, "Внимательнее смотри за своей лошадью - 2\U0001F3C7")
    elif mas_workstatus[1] == 47:
        bot.send_message(message.from_user.id, "Внимательнее смотри за своей лошадью - 3\U0001F3C7")
    elif mas_workstatus[1] == 48:
        bot.send_message(message.from_user.id, "Внимательнее смотри за своей лошадью - 4\U0001F3C7")


def attack_1(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Players WHERE ID = '{0}'".format(message.from_user.id))
    mas_player = cursor.fetchone()

    if mas_player[1] == "\U0001F004Мафия":
        show_keyboard_attack = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        show_keyboard_attack.row("\U0001F694Спецназ")
        show_keyboard_attack.row("\U0001F5E1Наёмники", "\U0001F44AМародёры")
        show_keyboard_attack.row("\U00002B05Назад")
    elif mas_player[1] == "\U0001F694Спецназ":
        show_keyboard_attack = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        show_keyboard_attack.row("\U0001F004Мафия")
        show_keyboard_attack.row("\U0001F5E1Наёмники", "\U0001F44AМародёры")
        show_keyboard_attack.row("\U00002B05Назад")
    elif mas_player[1] == "\U0001F5E1Наёмники":
        show_keyboard_attack = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        show_keyboard_attack.row("\U0001F004Мафия")
        show_keyboard_attack.row("\U0001F694Спецназ", "\U0001F44AМародёры")
        show_keyboard_attack.row("\U00002B05Назад")
    elif mas_player[1] == "\U0001F44AМародёры":
        show_keyboard_attack = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        show_keyboard_attack.row("\U0001F004Мафия")
        show_keyboard_attack.row("\U0001F694Спецназ", "\U0001F5E1Наёмники")
        show_keyboard_attack.row("\U00002B05Назад")
    bot.send_message(message.from_user.id, "Выбирай соперника", reply_markup=show_keyboard_attack)
    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def defend(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Players WHERE ID = '{0}'".format(message.from_user.id))
    mas_player = cursor.fetchone()

    bot.send_message(message.from_user.id, "Ты встал в оборону базы" + mas_player[1][:1] + "!")
    cursor.execute("UPDATE Players SET Status = '{1} {2}' WHERE ID = '{0}'"
                   .format(message.from_user.id, mas_player[1][:1], "Ты в обороне базы!"))
    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def attack_2(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Players WHERE ID = '{0}'".format(message.from_user.id))
    mas_player = cursor.fetchone()

    if message.text[:1] == mas_player[1][:1]:
        cursor.execute(
            "UPDATE Players SET Status = '{1} {2}' WHERE ID = '{0}'".format(message.from_user.id, mas_player[1][:1],
                                                                            "Ты в обороне базы!"))
        bot.send_message(message.from_user.id, "Ты встал в оборону базы" + mas_player[1][:1] + "!")

    else:
        cursor.execute(
            "UPDATE Players SET Status = '{1} {2}' WHERE ID = '{0}'".format(message.from_user.id, message.text[:1],
                                                                            "Ты нападаешь на врагов!"))
        bot.send_message(message.from_user.id, "Ты нападаешь на врагов " + message.text[:1] + "!")
    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()
    player_information(message)


def adventures_1(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()

    bot.send_message(message.from_user.id, "Задания: \n"
                                           "<b>\U0001F3F9Стрельбище</b> \n"
                                           "Требуется - <b>1 единица выносливости</b>\U0001F50B \n"
                                           "Скорее всего вы получите малое количество опыта и денег\n"
                                           "\n"
                                           "<b>\U0001F303Вылазка в город</b> \n"
                                           "Требуется - <b>2 единицы выносливости</b>\U0001F50B \n"
                                           "Вы получите огромный опыт, но вряд ли найдёте что-нибудь ценное \n"
                                           "\n"
                                           "<b>\U0001F4B0Ограбление</b> \n"
                                           "Требуется - <b>3 единицы выносливости</b>\U0001F50B \n"
                                           "Вы не научитесь ничему новому, но сможете хорошо заработать"
                     , reply_markup=show_keyboard_quests, parse_mode="html")
    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def adventures_2(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Players WHERE ID = '{0}'".format(message.from_user.id))
    mas_player = cursor.fetchone()

    now_time = list(time.gmtime())
    now_time[3] += 3

    if now_time[3] % 4 == 3 and now_time[4] >= 50:
        bot.send_message(message.from_user.id, "Сейчас не до квестов: скоро битва")

    else:

        if message.text == "\U0001F3F9Полигон":
            if mas_player[8] >= 1:
                index_exp = random.randint(100, 200) / 100
                index_money = random.randint(20, 70) / 100
                bot.send_message(message.from_user.id, "Ты пошел на полигон\U0001F3F9", reply_markup=show_keyboard_main)
                cursor.execute("UPDATE WorkStatus SET Status = 11 WHERE ID = '{0}'".format(message.from_user.id))
                cursor.execute("UPDATE Players SET Status = '{1}' WHERE ID = '{0}'".format(message.from_user.id,
                                                                                           "\U0001F3F9Ты сейчас на полигоне"))
                cursor.execute("UPDATE Players SET Stamina = '{1}' WHERE ID = '{0}'".format(message.from_user.id,
                                                                                            mas_player[8] - 1))
                connection.commit()
                connection.close()
                time.sleep(180)
                bot.send_message(message.from_user.id,
                                 "Ты вернулся с полигона и заработал {0}\U0001F31F и {1}\U0001F4B0"
                                 .format(int(index_exp * mas_player[3]), int(index_money * mas_player[3]) + 1),
                                 parse_mode="html")
                connection = sqlite3.connect("database", check_same_thread=False)
                cursor = connection.cursor()
                cursor.execute("UPDATE Players SET Experience = '{1}' WHERE ID = '{0}'".format(message.from_user.id,
                                                                                               mas_player[6] + int(
                                                                                                   index_exp *
                                                                                                   mas_player[3])))
                cursor.execute("UPDATE Players SET Money = '{1}' WHERE ID = '{0}'".format(message.from_user.id,
                                                                                          mas_player[7] + int(
                                                                                              index_money * mas_player[
                                                                                                  3]) + 1))
            else:
                bot.send_message(message.from_user.id, "У тебя слишком мало выносливости\U0001F50B",
                                 reply_markup=show_keyboard_main)

        elif message.text == "\U0001F303Город":
            if mas_player[8] >= 2:
                index_exp = random.randint(300, 500) / 100
                index_money = random.randint(50, 100) / 100
                bot.send_message(message.from_user.id, "Ты пошел на вылазку в город\U0001F303",
                                 reply_markup=show_keyboard_main)
                cursor.execute("UPDATE WorkStatus SET Status = 12 WHERE ID = '{0}'".format(message.from_user.id))
                cursor.execute("UPDATE Players SET Status = '{1}' WHERE ID = '{0}'".format(message.from_user.id,
                                                                                           "\U0001F303Ты сейчас в городе"))
                cursor.execute("UPDATE Players SET Stamina = '{1}' WHERE ID = '{0}'".format(message.from_user.id,
                                                                                            mas_player[8] - 2))
                connection.commit()
                connection.close()
                time.sleep(300)
                bot.send_message(message.from_user.id, "Ты вернулся из города и заработал {0}\U0001F31F и {1}\U0001F4B0"
                                 .format(int(index_exp * mas_player[3]), int(index_money * mas_player[3]) + 1),
                                 parse_mode="html")
                connection = sqlite3.connect("database", check_same_thread=False)
                cursor = connection.cursor()
                cursor.execute("UPDATE Players SET Experience = '{1}' WHERE ID = '{0}'".format(message.from_user.id,
                                                                                               mas_player[6] + int(
                                                                                                   index_exp *
                                                                                                   mas_player[3])))
                cursor.execute("UPDATE Players SET Money = '{1}' WHERE ID = '{0}'".format(message.from_user.id,
                                                                                          mas_player[7] + int(
                                                                                              index_money * mas_player[
                                                                                                  3]) + 1))
            else:
                bot.send_message(message.from_user.id, "У тебя слишком мало выносливости\U0001F50B",
                                 reply_markup=show_keyboard_main)

        elif message.text == "\U0001F4B0Ограбление":
            if mas_player[8] >= 3:
                index_exp = random.randint(200, 500) / 100
                index_money = random.randint(100, 200) / 100
                bot.send_message(message.from_user.id, "Ты пошел на ограбление\U0001F4B0",
                                 reply_markup=show_keyboard_main)
                cursor.execute("UPDATE WorkStatus SET Status = 12 WHERE ID = '{0}'".format(message.from_user.id))
                cursor.execute("UPDATE Players SET Status = '{1}' WHERE ID = '{0}'".format(message.from_user.id,
                                                                                           "\U0001F4B0Ты сейчас на ограблении",
                                                                                           message.from_user.id))
                cursor.execute("UPDATE Players SET Stamina = '{1}' WHERE ID = '{0}'".format(message.from_user.id,
                                                                                            mas_player[8] - 3))
                connection.commit()
                connection.close()
                time.sleep(420)
                bot.send_message(message.from_user.id,
                                 "Ты вернулся с ограбления и заработал {0}\U0001F31F и {1}\U0001F4B0"
                                 .format(int(index_exp * mas_player[3]), int(index_money * mas_player[3]) + 1),
                                 parse_mode="html")
                connection = sqlite3.connect("database", check_same_thread=False)
                cursor = connection.cursor()
                cursor.execute("UPDATE Players SET Experience = '{1}' WHERE ID = '{0}'".format(message.from_user.id,
                                                                                               mas_player[6] + int(
                                                                                                   index_exp *
                                                                                                   mas_player[3])))
                cursor.execute("UPDATE Players SET Money = '{1}' WHERE ID = '{0}'".format(message.from_user.id,
                                                                                          mas_player[7] + int(
                                                                                              index_money * mas_player[
                                                                                                  3]) + 1))
            else:
                bot.send_message(message.from_user.id, "У тебя слишком мало выносливости\U0001F50B",
                                 reply_markup=show_keyboard_main)

        cursor.execute("UPDATE WorkStatus SET Status = 0 WHERE ID = '{0}'".format(message.from_user.id))
        cursor.execute("UPDATE Players SET Status = '{1}' WHERE ID = '{0}'".format(message.from_user.id,
                                                                                   "\U0001F6CCТы сейчас отдыхаешь"))
        cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))
        connection.commit()

        cursor.execute("SELECT * FROM Players WHERE ID = '{0}'".format(message.from_user.id))
        mas_player = cursor.fetchone()
        if mas_player[6] >= int(((1.3 * mas_player[3]) ** 3 + 5)):
            bot.send_sticker(message.from_user.id, "CAADAgADAgADwaQgEUnTa9-GYgNvAg")

        connection.commit()
        connection.close()


def warrior(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()

    player_information(message)
    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def base(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()

    bot.send_message(message.from_user.id, "\U0001F392 - рюкзак со сняряжением \n"
                                           "\U0001F5C3 - склад со снаряжением \n"
                                           "\U0001F4DC - отчет о битве \n"
                                           "\U0001F4B0 - торговец снаряжением \n"
                                           "\U0001F37B - бар с картами \n"
                                           "\U0001F40E - ставки на лошадок \n"
                                           "\U0001F396 - рейтинг игроков",
                     reply_markup=show_keyboard_base)
    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def storage(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Inventory_off WHERE ID = '{0}'".format(message.from_user.id))
    mas_inventory_off = cursor.fetchone()

    str1 = ""
    off_counter = 0
    for elem in mas_inventory_off:
        if elem in dict_inventory and elem != "Пусто" and elem != "Нет":
            if dict_inventory[elem][0][0] == "Helmet":
                str1 += "<b>\U0001F3A9" + dict_inventory[elem][1] + "</b>"
            elif dict_inventory[elem][0][0] == "Armor":
                str1 += "<b>\U0001F454" + dict_inventory[elem][1] + "</b>"
            elif dict_inventory[elem][0][0] == "Gloves":
                str1 += "<b>\U0001F94A" + dict_inventory[elem][1] + "</b>"
            elif dict_inventory[elem][0][0] == "Boots":
                str1 += "<b>\U0001F456" + dict_inventory[elem][1] + "</b>"
            elif dict_inventory[elem][0][0] == "Pants":
                str1 += "<b>\U0001F45F" + dict_inventory[elem][1] + "</b>"
            elif dict_inventory[elem][0][0] == "Primary weapon":
                str1 += "<b>\U0001F5E1" + dict_inventory[elem][1] + "</b>"
            elif dict_inventory[elem][0][0] == "Secondary weapon":
                str1 += "<b>\U00002694" + dict_inventory[elem][1] + "</b>"
            else:
                str1 += "<b>" + dict_inventory[elem][1] + "</b>"
            str1 += " ("
            str1 += "+" + str(dict_inventory[elem][2]) + "\U0001F5E1"
            str1 += "  +" + str(dict_inventory[elem][3]) + "\U0001F6E1 "
            str1 += "/on_" + elem
            str1 += ")"
            str1 += "\n"
            off_counter += 1
    bot.send_message(message.from_user.id, "\U0001F5C3<b>Склад ({0}/16)</b>: \n"
                                           "\n"
                                           "{1}"
                     .format(off_counter, str1),
                     reply_markup=show_keyboard_base, parse_mode="html")
    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def dealer(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()

    bot.send_message(message.from_user.id, "Покупка и продажа снаряжения!", reply_markup=show_keyboard_market)
    cursor.execute("UPDATE WorkStatus SET Status_2 = 1 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def buy(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()

    bot.send_message(message.from_user.id, '\U0001F392За полный комплект экипировки выдаются бонусы: \n'
                                           '\n'
                                           '<i>\U0001F1EB\U0001F1F7203 "Штурмовой"</i>     |+1\U0001F5E1  | +1\U0001F6E1 \n'
                                           '<i>\U0001F1F7\U0001F1FAКомфорт "ГП"</i>            |+2\U0001F5E1  | +2\U0001F6E1 \n'
                                           '<i>\U0001F1F7\U0001F1FAСфера-3</i>                      |+3\U0001F5E1  | +3\U0001F6E1 \n'
                                           '<i>\U0001F1FA\U0001F1F8Шкура дракона</i>        |+4\U0001F5E1  | +4\U0001F6E1 \n'
                                           '<i>\U0001F1F7\U0001F1FAСапфир "ПРОФИ"</i>     |+5\U0001F5E1  | +5\U0001F6E1 \n'
                                           '<i>\U0001F1F7\U0001F1FAШилд "Штурмовой"</i> |+0\U0001F5E1  | +10\U0001F6E1 \n'
                                           '<i>\U0001F1F7\U0001F1FAМодуль-5М</i>                 |+10\U0001F5E1| +0\U0001F6E1 \n',
                     reply_markup=show_keyboard_market_buy, parse_mode='html')
    cursor.execute("UPDATE WorkStatus SET Status_2 = 2 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def weapons(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()

    # if message.text == "\U0001F5E1Основное оружие":
    #     bot.send_message(message.from_user.id, "\U0001F5E1Винтовки и \U0001F6E1Снайперки",
    #                      reply_markup=show_keyboard_market_buy_1)
    #     cursor.execute("UPDATE WorkStatus SET Status_2 = 3 WHERE ID = '{0}'".format(message.from_user.id))
    #     connection.commit()
    #     connection.close()
    #
    # elif message.text == "\U00002694Дополнительное оружие":
    #     bot.send_message(message.from_user.id, "\U0001F5E1Пистолеты и \U0001F6E1Пистолеты-пулемёты",
    #                      reply_markup=show_keyboard_market_buy_2)
    #     cursor.execute("UPDATE WorkStatus SET Status_2 = 3 WHERE ID = '{0}'".format(message.from_user.id))
    #     connection.commit()
    #     connection.close()

    if message.text == "\U0001F5E1Винтовки":
        bot.send_message(message.from_user.id, "<b>\U0001F1FA\U0001F1F8Barret REC7 (+2\U0001F5E1+0\U0001F6E150\U0001F4B0)</b> \n"
                                               "Купить: /buy_1131 \n"
                                               "\n"
                                               "<b>\U0001F1E9\U0001F1EA\U0001F1FA\U0001F1F8HK416 (+4\U0001F5E1+0\U0001F6E1100\U0001F4B0)</b> \n"
                                               "Купить: /buy_1132 \n"
                                               "\n"
                                               "<b>\U0001F1EB\U0001F1F7Famas (+7\U0001F5E1+0\U0001F6E1200\U0001F4B0)</b> \n"
                                               "Купить: /buy_1133 \n"
                                               "\n"
                                               "<b>\U0001F1F7\U0001F1FAA-545 (+10\U0001F5E1+1\U0001F6E1450\U0001F4B0)</b> \n"
                                               "Купить: /buy_1134 \n"
                                               "\n"
                                               "<b>\U0001F1FA\U0001F1F8M4 (+12\U0001F5E1+2\U0001F6E1800\U0001F4B0)</b> \n"
                                               "Купить: /buy_1135 \n"
                                               "\n"
                                               "<b>\U0001F1E7\U0001F1EA\U0001F1FA\U0001F1F8FN SCAR (+15\U0001F5E1+3\U0001F6E11300\U0001F4B0)</b> \n"
                                               "Купить: /buy_1136 \n"
                                               "\n"
                                               "<b>\U0001F1F7\U0001F1FAAK-12 (+19\U0001F5E1+4\U0001F6E11850\U0001F4B0)</b> \n"
                                               "Купить: /buy_1137 \n"
                                               "\n"
                                               "<b>\U0001F1F7\U0001F1F8Застава М21 (+22\U0001F5E1+5\U0001F6E12500\U0001F4B0)</b> \n"
                                               "Купить: /buy_1138 \n",
                         reply_markup=show_keyboard_market_buy, parse_mode="html")
        cursor.execute("UPDATE WorkStatus SET Status_2 = 2 WHERE ID = '{0}'".format(message.from_user.id))
        connection.commit()
        connection.close()

    elif message.text == "\U0001F6E1Снайперки":
        bot.send_message(message.from_user.id, "<b>\U0001F1E9\U0001F1EAHaenel G29 (+1\U0001F5E1+2\U0001F6E140\U0001F4B0)</b> \n"
                                               "Купить: /buy_1141 \n"
                                               "\n"
                                               "<b>\U0001F1F0\U0001F1F7S&T Motiv K14 (+3\U0001F5E1+5\U0001F6E180\U0001F4B0)</b> \n"
                                               "Купить: /buy_1142 \n"
                                               "\n"
                                               "<b>\U0001F1F7\U0001F1FAВС-121 (+5\U0001F5E1+8\U0001F6E1170\U0001F4B0)</b> \n"
                                               "Купить: /buy_1143 \n"
                                               "\n"
                                               "<b>\U0001F1F7\U0001F1FAСК-16 (+7\U0001F5E1+12\U0001F6E1350\U0001F4B0)</b> \n"
                                               "Купить: /buy_1144 \n"
                                               "\n"
                                               "<b>\U0001F1FA\U0001F1F8FN SPR (+9\U0001F5E1+16\U0001F6E1600\U0001F4B0)</b> \n"
                                               "Купить: /buy_1145 \n"
                                               "\n"
                                               "<b>\U0001F1FA\U0001F1F8Barret M98B (+11\U0001F5E1+20\U0001F6E1950\U0001F4B0)</b> \n"
                                               "Купить: /buy_1146 \n"
                                               "\n"
                                               "<b>\U0001F1F7\U0001F1FAОРСИС Т-5000 (+13\U0001F5E1+26\U0001F6E11500\U0001F4B0)</b> \n"
                                               "Купить: /buy_1147 \n"
                                               "\n"
                                               "<b>\U0001F1EC\U0001F1E7Arctic Warfare (+15\U0001F5E1+30\U0001F6E12000\U0001F4B0)</b> \n"
                                               "Купить: /buy_1148 \n",
                         reply_markup=show_keyboard_market_buy, parse_mode="html")
        cursor.execute("UPDATE WorkStatus SET Status_2 = 2 WHERE ID = '{0}'".format(message.from_user.id))
        connection.commit()
        connection.close()

    elif message.text == "\U0001F5E1Пистолеты":
        bot.send_message(message.from_user.id, "<b>\U0001F1F7\U0001F1FAПЛ-14 (+2\U0001F5E1+0\U0001F6E130\U0001F4B0)</b> \n"
                                               "Купить: /buy_1111 \n"
                                               "\n"
                                               "<b>\U0001F1EC\U0001F1E7Revolver (+3\U0001F5E1+0\U0001F6E180\U0001F4B0)</b> \n"
                                               "Купить: /buy_1112 \n"
                                               "\n"
                                               "<b>\U0001F1E9\U0001F1EAHK USP (+4\U0001F5E1+0\U0001F6E1150\U0001F4B0)</b> \n"
                                               "Купить: /buy_1113 \n"
                                               "\n"
                                               "<b>\U0001F1E8\U0001F1ED\U0001F1E9\U0001F1EASIG Sauer P250 (+5\U0001F5E1+0\U0001F6E1300\U0001F4B0)</b> \n"
                                               "Купить: /buy_1114 \n"
                                               "\n"
                                               "<b>\U0001F1F7\U0001F1FA\U0001F1EE\U0001F1F9Стриж (+6\U0001F5E1+1\U0001F6E1500\U0001F4B0)</b> \n"
                                               "Купить: /buy_1115 \n"
                                               "\n"
                                               "<b>\U0001F1FA\U0001F1F8\U0001F1E7\U0001F1EAFN FNX (+8\U0001F5E1+2\U0001F6E1750\U0001F4B0)</b> \n"
                                               "Купить: /buy_1116 \n"
                                               "\n"
                                               "<b>\U0001F1F8\U0001F1EATec-9 (+10\U0001F5E1+3\U0001F6E11000\U0001F4B0)</b> \n"
                                               "Купить: /buy_1117 \n"
                                               "\n"
                                               "<b>\U0001F1FA\U0001F1F8\U0001F1EE\U0001F1F1Desert Eagle (+12\U0001F5E1+4\U0001F6E11300\U0001F4B0)</b> \n"
                                               "Купить: /buy_1118 \n",
                         reply_markup=show_keyboard_market_buy, parse_mode="html")
        cursor.execute("UPDATE WorkStatus SET Status_2 = 2 WHERE ID = '{0}'".format(message.from_user.id))
        connection.commit()
        connection.close()

    elif message.text == "\U0001F6E1Пистолеты-пулемёты":
        bot.send_message(message.from_user.id, "<b>\U0001F1F7\U0001F1FAPP-19 (+1\U0001F5E1+1\U0001F6E120\U0001F4B0)</b> \n"
                                               "Купить: /buy_1121 \n"
                                               "\n"
                                               "<b>\U0001F1E9\U0001F1EAHK UMP 45 (+2\U0001F5E1+2\U0001F6E150\U0001F4B0)</b> \n"
                                               "Купить: /buy_1122 \n"
                                               "\n"
                                               "<b>\U0001F1FA\U0001F1F8MAC-10 (+3\U0001F5E1+3\U0001F6E1100\U0001F4B0)</b> \n"
                                               "Купить: /buy_1123 \n"
                                               "\n"
                                               "<b>\U0001F1E9\U0001F1EAHK MP7 (+4\U0001F5E1+4\U0001F6E1200\U0001F4B0)</b> \n"
                                               "Купить: /buy_1124 \n"
                                               "\n"
                                               "<b>\U0001F1E8\U0001F1EDSIG SG 550 (+5\U0001F5E1+5\U0001F6E1350\U0001F4B0)</b> \n"
                                               "Купить: /buy_1125 \n"
                                               "\n"
                                               "<b>\U0001F1E7\U0001F1EAFN P90 (+6\U0001F5E1+6\U0001F6E1550\U0001F4B0)</b> \n"
                                               "Купить: /buy_1126 \n"
                                               "\n"
                                               "<b>\U0001F1FA\U0001F1F8TDI Vector (+7\U0001F5E1+7\U0001F6E1800\U0001F4B0)</b> \n"
                                               "Купить: /buy_1127 \n"
                                               "\n"
                                               "<b>\U0001F1F8\U0001F1F0\U0001F1E8\U0001F1FFScorpion EVO 3 A1 (+8\U0001F5E1+8\U0001F6E11000\U0001F4B0)</b> \n"
                                               "Купить: /buy_1128 \n",
                         reply_markup=show_keyboard_market_buy, parse_mode="html")
        cursor.execute("UPDATE WorkStatus SET Status_2 = 2 WHERE ID = '{0}'".format(message.from_user.id))
        connection.commit()
        connection.close()

    elif message.text == '\U0001F3A9Шлемы':
        bot.send_message(message.from_user.id, '<b>203 "Штурмовой" (+0\U0001F5E1+1\U0001F6E110\U0001F4B0)</b> \n'
                                        'Купить: /buy_1011 \n'
                                        '\n'
                                       '<b>Комфорт "ГП" (+0\U0001F5E1+3\U0001F6E140\U0001F4B0)</b> \n'
                                       'Купить: /buy_1021 \n'
                                       '\n'
                                       '<b>Сфера-3 (+0\U0001F5E1+4\U0001F6E180\U0001F4B0)</b> \n'
                                       'Купить: /buy_1031 \n'
                                       '\n'
                                       '<b>Шкура дракона (+0\U0001F5E1+6\U0001F6E1150\U0001F4B0)</b> \n'
                                       'Купить: /buy_1041 \n'
                                       '\n'
                                       '<b>Сапфир "ПРОФИ" (+1\U0001F5E1+8\U0001F6E1350\U0001F4B0)</b> \n'
                                       'Купить: /buy_1051 \n'
                                       '\n'
                                       '<b>Шилд "Штурмовой" (+0\U0001F5E1+10\U0001F6E1700\U0001F4B0)</b> \n'
                                       'Купить: /buy_1061 \n'
                                       '\n'
                                       '<b>Модуль-5М (+4\U0001F5E1+5\U0001F6E1900\U0001F4B0)</b> \n'
                                       'Купить: /buy_1071 \n',
                 reply_markup=show_keyboard_market_buy, parse_mode='html')
        cursor.execute("UPDATE WorkStatus SET Status_2 = 2 WHERE ID = '{0}'".format(message.from_user.id))
        connection.commit()
        connection.close()

    elif message.text == '\U0001F454Бронежилеты':
        bot.send_message(message.from_user.id, '<b>203 "Штурмовой" (+0\U0001F5E1+1\U0001F6E110\U0001F4B0)</b> \n'
                                       'Купить: /buy_1012 \n'
                                       '\n'
                                       '<b>Комфорт "ГП" (+0\U0001F5E1+3\U0001F6E140\U0001F4B0)</b> \n'
                                       'Купить: /buy_1022 \n'
                                       '\n'
                                       '<b>Сфера-3 (+0\U0001F5E1+5\U0001F6E1100\U0001F4B0)</b> \n'
                                       'Купить: /buy_1032 \n'
                                       '\n'
                                       '<b>Шкура дракона (+0\U0001F5E1+8\U0001F6E1250\U0001F4B0)</b> \n'
                                       'Купить: /buy_1042 \n'
                                       '\n'
                                       '<b>Сапфир "ПРОФИ" (+3\U0001F5E1+10\U0001F6E1500\U0001F4B0)</b> \n'
                                       'Купить: /buy_1052 \n'
                                       '\n'
                                       '<b>Шилд "Штурмовой" (+0\U0001F5E1+15\U0001F6E1800\U0001F4B0)</b> \n'
                                       'Купить: /buy_1062 \n'
                                       '\n'
                                       '<b>Модуль-5М (+6\U0001F5E1+8\U0001F6E11000\U0001F4B0)</b> \n'
                                       'Купить: /buy_1072 \n',
                 reply_markup=show_keyboard_market_buy, parse_mode='html')
        cursor.execute("UPDATE WorkStatus SET Status_2 = 2 WHERE ID = '{0}'".format(message.from_user.id))
        connection.commit()
        connection.close()

    elif message.text == '\U0001F94AПерчатки':
        bot.send_message(message.from_user.id, '<b>203 "Штурмовой" (+0\U0001F5E1+1\U0001F6E110\U0001F4B0)</b> \n'
                                       'Купить: /buy_1013 \n'
                                       '\n'
                                       '<b>Комфорт "ГП" (+0\U0001F5E1+2\U0001F6E125\U0001F4B0)</b> \n'
                                       'Купить: /buy_1023 \n'
                                       '\n'
                                       '<b>Сфера-3 (+0\U0001F5E1+3\U0001F6E170\U0001F4B0)</b> \n'
                                       'Купить: /buy_1033 \n'
                                       '\n'
                                       '<b>Шкура дракона (+0\U0001F5E1+5\U0001F6E1140\U0001F4B0)</b> \n'
                                       'Купить: /buy_1043 \n'
                                       '\n'
                                       '<b>Сапфир "ПРОФИ" (+2\U0001F5E1+6\U0001F6E1400\U0001F4B0)</b> \n'
                                       'Купить: /buy_1053 \n'
                                       '\n'
                                       '<b>Шилд "Штурмовой" (+0\U0001F5E1+8\U0001F6E1650\U0001F4B0)</b> \n'
                                       'Купить: /buy_1063 \n'
                                       '\n'
                                       '<b>Модуль-5М (+4\U0001F5E1+4\U0001F6E1850\U0001F4B0)</b> \n'
                                       'Купить: /buy_1073 \n',
                 reply_markup=show_keyboard_market_buy, parse_mode='html')
        cursor.execute("UPDATE WorkStatus SET Status_2 = 2 WHERE ID = '{0}'".format(message.from_user.id))
        connection.commit()
        connection.close()

    elif message.text == '\U0001F456Штаны':
        bot.send_message(message.from_user.id, '<b>203 "Штурмовой" (+0\U0001F5E1+1\U0001F6E110\U0001F4B0)</b> \n'
                                       'Купить: /buy_1014 \n'
                                       '\n'
                                       '<b>Комфорт "ГП" (+0\U0001F5E1+2\U0001F6E125\U0001F4B0)</b> \n'
                                       'Купить: /buy_1024 \n'
                                       '\n'
                                       '<b>Сфера-3 (+0\U0001F5E1+3\U0001F6E170\U0001F4B0)</b> \n'
                                       'Купить: /buy_1034 \n'
                                       '\n'
                                       '<b>Шкура дракона (+0\U0001F5E1+5\U0001F6E1140\U0001F4B0)</b> \n'
                                       'Купить: /buy_1044 \n'
                                       '\n'
                                       '<b>Сапфир "ПРОФИ" (+2\U0001F5E1+6\U0001F6E1400\U0001F4B0)</b> \n'
                                       'Купить: /buy_1054 \n'
                                       '\n'
                                       '<b>Шилд "Штурмовой" (+0\U0001F5E1+8\U0001F6E1650\U0001F4B0)</b> \n'
                                       'Купить: /buy_1064 \n'
                                       '\n'
                                       '<b>Модуль-5М (+4\U0001F5E1+4\U0001F6E1850\U0001F4B0)</b> \n'
                                       'Купить: /buy_1074 \n',
                 reply_markup=show_keyboard_market_buy, parse_mode='html')
        cursor.execute("UPDATE WorkStatus SET Status_2 = 2 WHERE ID = '{0}'".format(message.from_user.id))
        connection.commit()
        connection.close()

    elif message.text == '\U0001F45FБотинки':
        bot.send_message(message.from_user.id, '<b>203 "Штурмовой" (+0\U0001F5E1+1\U0001F6E110\U0001F4B0)</b> \n'
                                       'Купить: /buy_1015 \n'
                                       '\n'
                                       '<b>Комфорт "ГП" (+0\U0001F5E1+2\U0001F6E125\U0001F4B0)</b> \n'
                                       'Купить: /buy_1025 \n'
                                       '\n'
                                       '<b>Сфера-3 (+0\U0001F5E1+3\U0001F6E170\U0001F4B0)</b> \n'
                                       'Купить: /buy_1035 \n'
                                       '\n'
                                       '<b>Шкура дракона (+0\U0001F5E1+5\U0001F6E1140\U0001F4B0)</b> \n'
                                       'Купить: /buy_1045 \n'
                                       '\n'
                                       '<b>Сапфир "ПРОФИ" (+2\U0001F5E1+6\U0001F6E1400\U0001F4B0)</b> \n'
                                       'Купить: /buy_1055 \n'
                                       '\n'
                                       '<b>Шилд "Штурмовой" (+0\U0001F5E1+8\U0001F6E1650\U0001F4B0)</b> \n'
                                       'Купить: /buy_1065 \n'
                                       '\n'
                                       '<b>Модуль-5М (+4\U0001F5E1+4\U0001F6E1850\U0001F4B0)</b> \n'
                                       'Купить: /buy_1075 \n',
                 reply_markup=show_keyboard_market_buy, parse_mode='html')
        cursor.execute("UPDATE WorkStatus SET Status_2 = 2 WHERE ID = '{0}'".format(message.from_user.id))
        connection.commit()
        connection.close()


def sell(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Inventory_off WHERE ID = '{0}'".format(message.from_user.id))
    mas_inventory_off = cursor.fetchone()

    str1 = ""
    off_counter = 0
    for elem in mas_inventory_off:
        if elem in dict_inventory and elem != "Пусто" and elem != "Нет":
            if dict_inventory[elem][0][0] == "Helmet":
                str1 += "<b>\U0001F3A9" + dict_inventory[elem][1] + "</b>"
            elif dict_inventory[elem][0][0] == "Armor":
                str1 += "<b>\U0001F454" + dict_inventory[elem][1] + "</b>"
            elif dict_inventory[elem][0][0] == "Gloves":
                str1 += "<b>\U0001F94A" + dict_inventory[elem][1] + "</b>"
            elif dict_inventory[elem][0][0] == "Boots":
                str1 += "<b>\U0001F456" + dict_inventory[elem][1] + "</b>"
            elif dict_inventory[elem][0][0] == "Pants":
                str1 += "<b>\U0001F45F" + dict_inventory[elem][1] + "</b>"
            elif dict_inventory[elem][0][0] == "Primary weapon":
                str1 += "<b>\U0001F5E1" + dict_inventory[elem][1] + "</b>"
            elif dict_inventory[elem][0][0] == "Secondary weapon":
                str1 += "<b>\U00002694" + dict_inventory[elem][1] + "</b>"
            else:
                str1 += "<b>" + dict_inventory[elem][1] + "</b>"
            str1 += " ("
            str1 += "+" + str(dict_inventory[elem][2]) + "\U0001F5E1"
            str1 += "  +" + str(dict_inventory[elem][3]) + "\U0001F6E1 "
            str1 += "/sell_" + elem
            str1 += ")"
            str1 += "\n"
            off_counter += 1
    bot.send_message(message.from_user.id, "\U0001F5C3<b>Склад ({0}/16)</b>: \n"
                                           "\n"
                                           "{1}"
                     .format(off_counter, str1),
                     reply_markup=show_keyboard_market, parse_mode="html")
    cursor.execute("UPDATE WorkStatus SET Status_2 = 1 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def buy_(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Inventory_off WHERE ID = '{0}'".format(message.from_user.id))
    mas_inventory_off = cursor.fetchone()
    cursor.execute("SELECT * FROM Players WHERE ID = '{0}'".format(message.from_user.id))
    mas_player = cursor.fetchone()

    cursor.execute("UPDATE WorkStatus SET Status_2 = 2 WHERE ID = '{0}'".format(message.from_user.id))
    if mas_player[7] >= dict_inventory[message.text[5:]][4] and equipment_check(mas_inventory_off, "Пусто") > 0:
        cursor.execute("UPDATE Players SET Money = '{1}' WHERE ID = '{0}'"
                       .format(message.from_user.id, mas_player[7] - dict_inventory[message.text[5:]][4]))
        cursor.execute("UPDATE Inventory_off SET '{1}' = '{2}' WHERE ID = '{0}'"
                       .format(message.from_user.id, str(equipment_check(mas_inventory_off, "Пусто")),
                               message.text[5:]))
        connection.commit()
        connection.close()
        bot.send_message(message.from_user.id, "Вы купили {0}!".format(dict_inventory[message.text[5:]][1]))
    elif mas_player[7] < dict_inventory[message.text[5:]][4]:
        bot.send_message(message.from_user.id, "У вас недостаточно денег!")
    elif equipment_check(mas_inventory_off, "Пусто") == -1:
        bot.send_message(message.from_user.id, "У вас полный склад!")


def sell_(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Inventory_on WHERE ID = '{0}'".format(message.from_user.id))
    mas_inventory_on = cursor.fetchone()
    cursor.execute("SELECT * FROM Inventory_off WHERE ID = '{0}'".format(message.from_user.id))
    mas_inventory_off = cursor.fetchone()
    cursor.execute("SELECT * FROM Players WHERE ID = '{0}'".format(message.from_user.id))
    mas_player = cursor.fetchone()

    cursor.execute("UPDATE WorkStatus SET Status_2 = 1 WHERE ID = '{0}'".format(message.from_user.id))

    if equipment_check(mas_inventory_off, message.text[6:]) > 0:
        cursor.execute("UPDATE Players SET Money = '{1}' WHERE ID = '{0}'"
                       .format(message.from_user.id, mas_player[7] + dict_inventory[message.text[6:]][4]))
        cursor.execute("UPDATE Inventory_off SET '{1}' = '{2}' WHERE ID = '{0}'"
                       .format(message.from_user.id, str(equipment_check(mas_inventory_off, message.text[6:])),
                               "Пусто"))
        connection.commit()
        connection.close()
        bot.send_message(message.from_user.id, "Вы продали {0}!".format(dict_inventory[message.text[5:]][1]))

    elif equipment_check(mas_inventory_on, message.text[6:]) > 0:
        cursor.execute("UPDATE Players SET Money = {1} WHERE ID = {0}".format(message.from_user.id, mas_player[7] +
                                                                              dict_inventory[message.text[6:]][4]))
        cursor.execute("UPDATE Inventory_on SET '{1}' = '{2}' WHERE ID = {0}"
                       .format(message.from_user.id, str(equipment_check(mas_inventory_off, message.text[6:])),
                               "Пусто"))
        connection.commit()
        connection.close()
        bot.send_message(message.from_user.id, "Вы продали {0}!".format(dict_inventory[message.text[5:]][1]))

    elif equipment_check(mas_inventory_off, message.text[6:]) == -1 and equipment_check(mas_inventory_on,
                                                                                        message.text[6:]) == -1:
        bot.send_message(message.from_user.id, "У тебя нет этого предмета!")


def on_(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Inventory_on WHERE ID = '{0}'".format(message.from_user.id))
    mas_inventory_on = cursor.fetchone()
    cursor.execute("SELECT * FROM Inventory_off WHERE ID = '{0}'".format(message.from_user.id))
    mas_inventory_off = cursor.fetchone()
    cursor.execute("SELECT * FROM Players WHERE ID = '{0}'".format(message.from_user.id))
    mas_player = cursor.fetchone()

    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))

    if equipment_check(mas_inventory_off, message.text[4:]) > 0:

        item_name, item_constant = dict_inventory[message.text[4:]][0][0], dict_inventory[message.text[4:]][0][1]
        set_attack, set_defence = 0, 0

        if item_constant in [4, 5, 6, 7, 8]:
            set_attack, set_defence = set_check(mas_inventory_on)
            cursor.execute("UPDATE Inventory_on SET 'Set' = '{1}' WHERE ID = '{0}'"
                           .format(message.from_user.id, "Нет"))
        cursor.execute("UPDATE Players SET Attack = '{1}' WHERE ID = '{0}'"
                       .format(message.from_user.id, mas_player[4] - set_attack + dict_inventory[message.text[4:]][2] -
                               dict_inventory[mas_inventory_on[item_constant]][2]))
        cursor.execute("UPDATE Players SET Defence = '{1}' WHERE ID = '{0}'"
                       .format(message.from_user.id, mas_player[5] - set_defence + dict_inventory[message.text[4:]][3] -
                               dict_inventory[mas_inventory_on[item_constant]][3]))
        cursor.execute("UPDATE Inventory_on SET '{1}' = '{2}' WHERE ID = '{0}'"
                       .format(message.from_user.id, item_name, message.text[4:]))
        cursor.execute("UPDATE Inventory_off SET '{1}' = '{2}' WHERE ID = '{0}'"
                       .format(message.from_user.id, equipment_check(mas_inventory_off, message.text[4:]),
                               mas_inventory_on[item_constant]))
        connection.commit()

        cursor.execute("SELECT * FROM Inventory_on WHERE ID = '{0}'".format(message.from_user.id))
        mas_inventory_on = cursor.fetchone()
        cursor.execute("SELECT * FROM Players WHERE ID = '{0}'".format(message.from_user.id))
        mas_player = cursor.fetchone()

        set_attack, set_defence = set_check(mas_inventory_on)
        if set_attack + set_defence > 0 and item_constant in [4, 5, 6, 7, 8]:
            cursor.execute("UPDATE Inventory_on SET 'Set' = '{1}' WHERE ID = '{0}'"
                           .format(message.from_user.id, dict_inventory[mas_inventory_on[4]][1]))
            cursor.execute("UPDATE Players SET Attack = '{1}' WHERE ID = '{0}'"
                           .format(message.from_user.id, mas_player[4] + set_attack))
            cursor.execute("UPDATE Players SET Defence = '{1}' WHERE ID = '{0}'"
                           .format(message.from_user.id, mas_player[5] + set_defence))
            connection.commit()
            bot.send_message(message.from_user.id, "Поздравляю ты собрал сэт!")

        connection.commit()
        connection.close()

        bot.send_message(message.from_user.id, "Ты надел {0}!".format(dict_inventory[message.text[5:]][1]))

    elif equipment_check(mas_inventory_off, message.text[4:]) == -1:
        bot.send_message(message.from_user.id, "У тебя нет этого предмета в сумке!")


def off_(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Inventory_on WHERE ID = '{0}'".format(message.from_user.id))
    mas_inventory_on = cursor.fetchone()
    cursor.execute("SELECT * FROM Inventory_off WHERE ID = '{0}'".format(message.from_user.id))
    mas_inventory_off = cursor.fetchone()
    cursor.execute("SELECT * FROM Players WHERE ID = '{0}'".format(message.from_user.id))
    mas_player = cursor.fetchone()

    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))

    if equipment_check(mas_inventory_on, message.text[5:]) > 0 and equipment_check(mas_inventory_off, "Пусто"):

        item_name, item_constant = dict_inventory[message.text[5:]][0][0], dict_inventory[message.text[5:]][0][1]
        set_attack, set_defence = 0, 0

        if item_constant in [4, 5, 6, 7, 8]:
            set_attack, set_defence = set_check(mas_inventory_on)
            cursor.execute("UPDATE Inventory_on SET 'Set' = '{1}' WHERE ID = '{0}'"
                           .format(message.from_user.id, "Нет"))
        cursor.execute("UPDATE Players SET Attack = '{1}' WHERE ID = '{0}'"
                       .format(message.from_user.id,
                               mas_player[4] - set_attack - dict_inventory[mas_inventory_on[item_constant]][2]))
        cursor.execute("UPDATE Players SET Defence = '{1}' WHERE ID = '{0}'"
                       .format(message.from_user.id,
                               mas_player[5] - set_defence - dict_inventory[mas_inventory_on[item_constant]][3]))
        cursor.execute("UPDATE Inventory_on SET '{1}' = '{2}' WHERE ID = '{0}'"
                       .format(message.from_user.id, item_name, "Пусто"))
        cursor.execute("UPDATE Inventory_off SET '{1}' = '{2}' WHERE ID = '{0}'"
                       .format(message.from_user.id, str(equipment_check(mas_inventory_off, "Пусто")),
                               message.text[5:]))
        connection.commit()
        connection.close()

        bot.send_message(message.from_user.id, "Ты снял {0}!".format(dict_inventory[message.text[5:]][1]))

    elif equipment_check(mas_inventory_on, message.text[5:]) == -1:
        bot.send_message(message.from_user.id, "На тебе нет этого предмета!")

    elif equipment_check(mas_inventory_off, "Пусто") == -1:
        bot.send_message(message.from_user.id, "У тебя недостаточно места на складе!")


def bar(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()

    bot.send_message(message.from_user.id, "В баре ты увидел трёх игроков в карты\U0001F3B4 \n"
                                           "\n"
                                           "В углу сидит <b>\U00002660пьяница</b> и готов сыграть с любым. "
                                           "Кажется, обыграть его будет совсем легко! (Коэффицент - 1.3) \n"
                                           "\n"
                                           "Рядом с тобой сидит <b>\U00002665девушка</b>, которая кажется что-то понимает в картах. "
                                           "Её будет не так просто обыграть! (Коэффицент - 2) \n"
                                           "\n"
                                           "В центре зала сидит <b>\U0001F0CFмастер</b>, которого никто еще не обыгрывал. "
                                           "Можешь попробовать свою удачу, но вряд ли что-то получится! (Коэффицент - 5)",
                     reply_markup=show_keyboard_bar, parse_mode="html")
    cursor.execute("UPDATE WorkStatus SET Status_2 = 1 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def cards(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()

    now_time = list(time.gmtime())
    now_time[3] += 3

    if now_time[3] % 4 == 0 and now_time[4] >= 50:
        bot.send_message(message.from_user.id, "Сейчас не до карт: скоро битва")

    else:
        if message.text == "\U00002660Пьяница":
            cursor.execute("UPDATE Workstatus SET Status = 21 WHERE ID = {0}".format(message.from_user.id))
            connection.commit()
            connection.close()

        elif message.text == "\U00002665Девушка":
            cursor.execute("UPDATE Workstatus SET Status = 22 WHERE ID = {0}".format(message.from_user.id))
            connection.commit()
            connection.close()

        elif message.text == "\U0001F0CFМастер":
            cursor.execute("UPDATE Workstatus SET Status = 23 WHERE ID = {0}".format(message.from_user.id))
            connection.commit()
            connection.close()

        bot.send_message(message.from_user.id, "Сколько ты хочешь поставить?", reply_markup=show_keyboard_bet)


def beer(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()

    bot.send_message(message.from_user.id, "Ты выпил кружку пива.", reply_markup=show_keyboard_bar)
    cursor.execute("UPDATE WorkStatus SET Status_2 = 1 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def hippodrome_1(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()

    bot.send_message(message.from_user.id, "Добро пожаловать на ипподором\U0001F40E!\n"
                                           "Выбирай лошадь\U0001F3C7, на которую хочешь поставить. \n"
                                           "Коэффицент победы на каждую лошадь равен трём.",
                     reply_markup=show_keyboard_horses, parse_mode="html")
    cursor.execute("UPDATE WorkStatus SET Status_2 = 1 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def hippodrome_2(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()

    if message.text == "1\U0001F3C7":
        cursor.execute("UPDATE WorkStatus SET Status = 41 WHERE ID = '{0}'".format(message.from_user.id))
        connection.commit()
        connection.close()

    elif message.text == "2\U0001F3C7":
        cursor.execute("UPDATE WorkStatus SET Status = 42 WHERE ID = '{0}'".format(message.from_user.id))
        connection.commit()
        connection.close()

    elif message.text == "3\U0001F3C7":
        cursor.execute("UPDATE WorkStatus SET Status = 43 WHERE ID = '{0}'".format(message.from_user.id))
        connection.commit()
        connection.close()

    elif message.text == "4\U0001F3C7":
        cursor.execute("UPDATE WorkStatus SET Status = 44 WHERE ID = '{0}'".format(message.from_user.id))
        connection.commit()
        connection.close()

    bot.send_message(message.from_user.id, "Сколько ты хочешь поставить?", reply_markup=show_keyboard_bet)


def report(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Players WHERE ID = '{0}'".format(message.from_user.id))
    mas_player = cursor.fetchone()

    str1 = ""
    str1 += "{0}{1} | \U0001F4A5:{2} | \U0001F5E1:{3} | \U0001F6E1:{4} \n".format(mas_player[1][:1], mas_player[2],
                                                                                  mas_player[3], mas_player[4],
                                                                                  mas_player[5])
    str1 += "\n"
    str1 += "В последней битве ты заработал: \n"
    str1 += "<b>Денег</b>\U0001F4B0: {0} \n".format(mas_player[11])
    str1 += "<b>Опыта</b>\U0001F31F: {0}".format(mas_player[12])
    bot.send_message(message.from_user.id, str1, reply_markup=show_keyboard_base, parse_mode="html")
    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def bag(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Inventory_on WHERE ID = '{0}'".format(message.from_user.id))
    mas_inventory_on = cursor.fetchone()

    mas_inventory_on_2 = []
    for elem in mas_inventory_on:
        if elem in dict_inventory and elem != "Пусто" and elem != "Нет":
            str1 = ""
            str1 += "<b>" + dict_inventory[elem][1] + "</b>" + " "
            str1 += " ("
            str1 += "+" + str(dict_inventory[elem][2]) + "\U0001F5E1"
            str1 += "+" + str(dict_inventory[elem][3]) + "\U0001F6E1 "
            str1 += "/off_" + elem
            str1 += ")"
            mas_inventory_on_2.append(str1)
        else:
            mas_inventory_on_2.append(elem)

    set_attack, set_defence = set_check(mas_inventory_on)

    sum_attack = dict_inventory[mas_inventory_on[1]][2] + dict_inventory[mas_inventory_on[2]][2] + \
                 dict_inventory[mas_inventory_on[4]][2]
    sum_attack += dict_inventory[mas_inventory_on[5]][2] + dict_inventory[mas_inventory_on[6]][2] + \
                  dict_inventory[mas_inventory_on[7]][2]
    sum_attack += dict_inventory[mas_inventory_on[8]][2] + set_attack

    sum_defence = dict_inventory[mas_inventory_on[1]][3] + dict_inventory[mas_inventory_on[2]][3] + \
                  dict_inventory[mas_inventory_on[4]][3]
    sum_defence += dict_inventory[mas_inventory_on[5]][3] + dict_inventory[mas_inventory_on[6]][3] + \
                   dict_inventory[mas_inventory_on[7]][3]
    sum_defence += dict_inventory[mas_inventory_on[8]][3] + set_defence

    str2 = ""
    str2 += "\U0001F392<b>Снаряжение: +{0}\U0001F5E1 +{1}\U0001F6E1</b>\n".format(sum_attack, sum_defence)
    str2 += "\n"
    str2 += "\U0001F5E1 {0} \n".format(mas_inventory_on_2[1])
    str2 += "\U00002694 {0} \n".format(mas_inventory_on_2[2])
    str2 += "\U0001F3A9 {0} \n".format(mas_inventory_on_2[4])
    str2 += "\U0001F454 {0} \n".format(mas_inventory_on_2[5])
    str2 += "\U0001F94A	{0} \n".format(mas_inventory_on_2[6])
    str2 += "\U0001F456 {0} \n".format(mas_inventory_on_2[7])
    str2 += "\U0001F45F {0} \n".format(mas_inventory_on_2[8])
    if set_attack != 0 or set_defence != 0:
        str2 += "<b>Сэт:{0} +{1}\U0001F5E1+{2}\U0001F6E1\n</b>".format(mas_inventory_on_2[9], set_attack, set_defence)
    else:
        str2 += "<b>Сэт:{0}\n</b>".format(mas_inventory_on_2[9])

    bot.send_message(message.from_user.id, str2, reply_markup=show_keyboard_base, parse_mode="html")
    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def rating(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM PLAYERS ORDER BY Experience DESC")
    mas_players_top = cursor.fetchall()
    mas_players_top_id = []

    str1 = "<b>Топ игроков:</b> \n"
    str1 += "\n"

    for i in range(min(10, len(mas_players_top))):
        player = mas_players_top[i]
        mas_players_top_id.append(player[0])
        if i == 0:
            str1 += "\U0001F947"
        elif i == 1:
            str1 += "\U0001F948"
        elif i == 2:
            str1 += "\U0001F949"
        else:
            str1 += "\U0001F397"
        str1 += "{0} <b>{1}{2}</b>   {3}\U0001F4A5|{4}\U0001F31F".format(i + 1, player[1][:1], player[2], player[3],
                                                                         player[6])
        str1 += "\n"

    str1 += "- - - - - - - - - - - - - - - - - - - - - -\n"

    for j in range(len(mas_players_top)):
        if mas_players_top[j][0] == message.from_user.id:
            answer = j
            break

    if answer <= 9:
        str1 += "Поздравляю! Ты в топе на <b>{0} месте!</b>".format(answer + 1)
    else:
        player = mas_players_top[answer - 1]
        str1 += "\U00002728{0} <b>{1}{2}</b>   {3}\U0001F4A5|{4}\U0001F31F".format(answer, player[1][:1], player[2],
                                                                                   player[3], player[6])
        str1 += "\n"
        player = mas_players_top[answer]
        str1 += "\U00002728{0} <b>{1}{2}</b>   {3}\U0001F4A5|{4}\U0001F31F".format(answer + 1, player[1][:1], player[2],
                                                                                   player[3], player[6])
        str1 += "\n"
        try:
            player = mas_players_top[answer + 1]
            str1 += "\U00002728{0} <b>{1}{2}</b>   {3}\U0001F4A5|{4}\U0001F31F".format(answer + 2, player[1][:1],
                                                                                       player[2], player[3], player[6])
            str1 += "\n"
        except:
            pass

    cursor.execute("SELECT * FROM Clans ORDER BY Points DESC")
    mas_clans = cursor.fetchall()
    str2 = "<b>\U0001F396Рейтинг фракций\U0001F396</b> \n"
    str2 += "\n"
    for i in range(len(mas_clans)):
        clan = mas_clans[i]
        if i == 0:
            str2 += "\U0001F947|"
        elif i == 1:
            str2 += "\U0001F948|"
        elif i == 2:
            str2 += "\U0001F949|"
        else:
            str2 += "\U0001F397|"
        if clan[0] == "Mafia":
            str2 += "<i>\U0001F004Мафия</i>       "
        elif clan[0] == "SWAT":
            str2 += "<i>\U0001F694Спецназ</i>    "
        elif clan[0] == "Mercenaries":
            str2 += "<i>\U0001F5E1Наёмники</i> "
        elif clan[0] == "Marauders":
            str2 += "<i>\U0001F44AМародёры</i>"
        str2 += "|<b>{0}\U0001F3C6</b>очков \n".format(clan[1])

    bot.send_message(message.from_user.id, str1, reply_markup=show_keyboard_base, parse_mode="html")
    bot.send_message(message.from_user.id, str2, reply_markup=show_keyboard_base, parse_mode="html")
    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def players_top(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM PLAYERS ORDER BY Experience DESC")
    mas_players_top = cursor.fetchall()
    mas_players_top_id = []

    str1 = "<b>Топ игроков:</b> \n"
    str1 += "\n"

    for i in range(min(10, len(mas_players_top))):
        player = mas_players_top[i]
        mas_players_top_id.append(player[0])
        if i == 0:
            str1 += "\U0001F947"
        elif i == 1:
            str1 += "\U0001F948"
        elif i == 2:
            str1 += "\U0001F949"
        else:
            str1 += "\U0001F397"
        str1 += "{0} <b>{1}{2}</b>   {3}\U0001F4A5|{4}\U0001F31F".format(i + 1, player[1][:1], player[2], player[3],
                                                                         player[6])
        str1 += "\n"

    str1 += "- - - - - - - - - - - - - - - - - - - - - -\n"

    for j in range(len(mas_players_top)):
        if mas_players_top[j][0] == message.from_user.id:
            answer = j
            break

    if answer <= 9:
        str1 += "Поздравляю! Ты в топе на <b>{0} месте!</b>".format(answer + 1)
    else:
        player = mas_players_top[answer - 1]
        str1 += "\U00002728{0} <b>{1}{2}</b>   {3}\U0001F4A5|{4}\U0001F31F".format(answer, player[1][:1], player[2],
                                                                                   player[3], player[6])
        str1 += "\n"
        player = mas_players_top[answer]
        str1 += "\U00002728{0} <b>{1}{2}</b>   {3}\U0001F4A5|{4}\U0001F31F".format(answer + 1, player[1][:1], player[2],
                                                                                   player[3], player[6])
        str1 += "\n"
        try:
            player = mas_players_top[answer + 1]
            str1 += "\U00002728{0} <b>{1}{2}</b>   {3}\U0001F4A5|{4}\U0001F31F".format(answer + 2, player[1][:1],
                                                                                       player[2], player[3], player[6])
            str1 += "\n"
        except:
            pass

    bot.send_message(message.from_user.id, str1, reply_markup=show_keyboard_main, parse_mode="html")
    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def global_top(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Clans ORDER BY Points DESC")
    mas_clans = cursor.fetchall()
    str2 = "<b>\U0001F396Рейтинг фракций\U0001F396</b> \n"
    str2 += "\n"
    for i in range(len(mas_clans)):
        clan = mas_clans[i]
        if i == 0:
            str2 += "\U0001F947|"
        elif i == 1:
            str2 += "\U0001F948|"
        elif i == 2:
            str2 += "\U0001F949|"
        else:
            str2 += "\U0001F397|"
        if clan[0] == "Mafia":
            str2 += "<i>\U0001F004Мафия</i>       "
        elif clan[0] == "SWAT":
            str2 += "<i>\U0001F694Спецназ</i>    "
        elif clan[0] == "Mercenaries":
            str2 += "<i>\U0001F5E1Наёмники</i> "
        elif clan[0] == "Marauders":
            str2 += "<i>\U0001F44AМародёры</i>"
        str2 += "|<b>{0}\U0001F3C6</b>очков \n".format(clan[1])
    bot.send_message(message.from_user.id, str2, reply_markup=show_keyboard_main, parse_mode="html")
    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def faq(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Players WHERE ID = '{0}'".format(message.from_user.id))
    mas_player = cursor.fetchone()

    str1 = ""
    #str1 += "<b>\U0001F4ACЧаты для общения с игроками\U0001F4AC</b> \n"
    #str1 += "\U0001F91C<a href='https://t.me/joinchat/AAAAAEMiYfXT_2wKoLFJbQ'>Общий чат</a>\U0001F91B \n"
    #if mas_player[1] == "\U0001F004Мафия":
        #str1 += "{0}<a href='https://t.me/joinchat/AAAAAEBBazsjlK4uNUW2-A'>Общение внутри фракции</a>{0} \n".format(
            #mas_player[1][:1])
    #elif mas_player[1] == "\U0001F694Спецназ":
        #str1 += "{0}<a href='https://t.me/joinchat/AAAAAERVY4k8xIFZfUQfMg'>Общение внутри фракции</a>{0} \n".format(
            #mas_player[1][:1])
    #elif mas_player[1] == "\U0001F5E1Наёмники":
        #str1 += "{0}<a href='https://t.me/joinchat/AAAAAEQqhEEGlWQDY0zhAw'>Общение внутри фракции</a>{0} \n".format(
            #mas_player[1][:1])
    #elif mas_player[1] == "\U0001F44AМародёры":
        #str1 += "{0}<a href='https://t.me/joinchat/AAAAAEIFTkasqbwlMVLpWw'>Общение внутри фракции</a>{0} \n".format(
            #mas_player[1][:1])
    #str1 += "\U0001F506<a href='https://t.me/townwars'>Новостной канал игры</a>\U0001F506 \n"
    #str1 += "\U0001F4DC<a href='https://t.me/town_wars_reports'>Отчеты о битвах</a>\U0001F4DC \n"
    #str1 += "\n"

    str1 += "<b>\U0001F525Рейтинг игроков и фракций\U0001F525</b> \n"
    str1 += "\U0001F396Общий рейтинг - /top \n"
    str1 += "\U0001F3C6Рейтинг фракций - /global_top \n"
    str1 += "\U0001F947Рейтинг игроков - /players_top \n"
    str1 += "\n"

    str1 += "<b>\U0001F6D1Смена фракции и ника возможна только 1 раз!\U0001F6D1</b> \n"
    str1 += "\U0001F501Смена фракции - /clan_change \n"
    str1 += "\U0001F501Смена ника - /name_change \n"
    bot.send_message(message.from_user.id, str1, reply_markup=show_keyboard_main, parse_mode="html")
    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def level_up(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Players WHERE ID = '{0}'".format(message.from_user.id))
    mas_player = cursor.fetchone()

    if mas_player[6] >= int(((1.3 * mas_player[3]) ** 3 + 5)):
        bot.send_message(message.from_user.id, "Выбирай характеристику!", reply_markup=show_keyboard_level_up)
    else:
        bot.send_message(message.from_user.id, "Тебе недостаточно опыта для следующего уровня!")
        player_information(message)
    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def feature_increase(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Players WHERE ID = '{0}'".format(message.from_user.id))
    mas_player = cursor.fetchone()

    if mas_player[6] >= int(((1.3 * mas_player[3]) ** 3 + 5)):
        if message.text == "+1 \U0001F5E1Атака":
            cursor.execute(
                "UPDATE Players SET Attack = '{1}' WHERE ID = '{0}'".format(message.from_user.id, mas_player[4] + 1))
        elif message.text == "+1 \U0001F6E1Защита":
            cursor.execute(
                "UPDATE Players SET Defence = '{1}' WHERE ID = '{0}'".format(message.from_user.id, mas_player[5] + 1))
        cursor.execute(
            "UPDATE Players SET Level = '{1}' WHERE ID = '{0}'".format(message.from_user.id, mas_player[3] + 1))
        connection.commit()
        player_information(message)
    else:
        bot.send_message(message.from_user.id, "Тебе недостаточно опыта для следующего уровня!")
        player_information(message)
    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def clan_change(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Players WHERE ID = '{0}'".format(message.from_user.id))
    mas_player = cursor.fetchone()

    cursor.execute("UPDATE WorkStatus SET Status = 31 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    if mas_player[1] == "\U0001F004Мафия":
        show_keyboard_attack = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        show_keyboard_attack.row("\U0001F694Спецназ")
        show_keyboard_attack.row("\U0001F5E1Наёмники", "\U0001F44AМародёры")
        show_keyboard_attack.row("\U00002B05Назад")
    if mas_player[1] == "\U0001F694Спецназ":
        show_keyboard_attack = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        show_keyboard_attack.row("\U0001F004Мафия")
        show_keyboard_attack.row("\U0001F5E1Наёмники", "\U0001F44AМародёры")
        show_keyboard_attack.row("\U00002B05Назад")
    if mas_player[1] == "\U0001F5E1Наёмники":
        show_keyboard_attack = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        show_keyboard_attack.row("\U0001F004Мафия")
        show_keyboard_attack.row("\U0001F694Спецназ", "\U0001F44AМародёры")
        show_keyboard_attack.row("\U00002B05Назад")
    if mas_player[1] == "\U0001F44AМародёры":
        show_keyboard_attack = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        show_keyboard_attack.row("\U0001F004Мафия")
        show_keyboard_attack.row("\U0001F694Спецназ", "\U0001F5E1Наёмники")
        show_keyboard_attack.row("\U00002B05Назад")
    bot.send_message(message.from_user.id, "В какую фракцию ты хочешь перейти?", reply_markup=show_keyboard_attack)
    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def name_change(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()

    bot.send_message(message.from_user.id, "Пришли мне имя, на которое ты хочешь сменить своё")
    cursor.execute("UPDATE WorkStatus SET Status = 32 WHERE ID = '{0}'".format(message.from_user.id))
    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()


def back(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM WorkStatus WHERE ID = '{0}'".format(message.from_user.id))
    mas_workstatus = cursor.fetchone()

    if mas_workstatus[2] == 1:
        base(message)

    elif mas_workstatus[2] == 2:
        dealer(message)

    elif mas_workstatus[2] == 3:
        buy(message)

    else:
        player_information(message)


def other(message):
    connection = sqlite3.connect("database", check_same_thread=False)
    cursor = connection.cursor()

    player_information(message)
    cursor.execute("UPDATE WorkStatus SET Status_2 = 0 WHERE ID = '{0}'".format(message.from_user.id))
    connection.commit()
    connection.close()

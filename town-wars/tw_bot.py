# -*- coding: utf-8 -*-
from functions import *
from constants import *
import sys
import time
import random
import sqlite3
import telebot
import traceback

    
@bot.message_handler(content_types=["text"])
def handle_text(message):
    try:
        connection = sqlite3.connect("database", check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Inventory_on WHERE ID = '{0}'".format(message.from_user.id))
        mas_inventory_on = cursor.fetchone()
        cursor.execute("SELECT * FROM Inventory_off WHERE ID = '{0}'".format(message.from_user.id))
        mas_inventory_off = cursor.fetchone()
        cursor.execute("SELECT * FROM Players WHERE ID = '{0}'".format(message.from_user.id))
        mas_player = cursor.fetchone()
        cursor.execute("SELECT * FROM WorkStatus WHERE ID = '{0}'".format(message.from_user.id))
        mas_workstatus = cursor.fetchone()
    
        if stop_bot_flag:
            technical_work(message)
    
        elif battle_flag:
            the_battle_is(message)
    
        elif (mas_workstatus is None) or (mas_player is None) or (mas_inventory_on is None) or (mas_inventory_off is None) or ((mas_player[1] == "0" or mas_player[2] == "NoNickName") and mas_workstatus[1] not in [1, 2]):
            registration_1(message)
    
        elif mas_workstatus[1] in [1, 2]:
            registration_2(message)
    
        elif mas_workstatus[1] in [11, 12, 13]:
            the_adventure_is(message)
    
        elif mas_workstatus[1] in [21, 22, 23]:
            the_cards(message)
    
        elif mas_workstatus[1] == 24:
            the_cards_is(message)
    
        elif mas_workstatus[1] in [31, 32]:
            changing_smth(message)
    
        elif mas_workstatus[1] in [41, 42, 43, 44]:
            the_horses(message)
    
        elif mas_workstatus[1] in [45, 46, 47, 48]:
            the_horses_are(message)
    
        elif message.text == "\U0001F5E1Атака":
            attack_1(message)
    
        elif message.text == "\U0001F6E1Оборона":
            defend(message)
    
        elif message.text in ["\U0001F004Мафия", "\U0001F694Спецназ", "\U0001F5E1Наёмники", "\U0001F44AМародёры"]:
            attack_2(message)
    
        elif message.text == "\U0001F310Задания":
            adventures_1(message)
    
        elif message.text in ["\U0001F3F9Полигон", "\U0001F303Город", "\U0001F4B0Ограбление"]:
            adventures_2(message)
    
        elif message.text == "\U0001F3C2Боец":
            warrior(message)
    
        elif message.text == "\U0001F3EFБаза":
            base(message)
    
        elif message.text == "\U0001F5C3Склад" or message.text == "/storage":
            storage(message)
    
        elif message.text == "\U0001F4B0Торговец":
            dealer(message)
    
        elif message.text == "\U0001F4E5Купить":
            buy(message)
    
        elif message.text in ["\U0001F5E1Основное оружие", "\U00002694Дополнительное оружие", "\U0001F5E1Винтовки", "\U0001F6E1Снайперки", "\U0001F5E1Пистолеты", "\U0001F6E1Пистолеты-пулемёты", "\U0001F3A9Шлемы", "\U0001F454Бронежилеты", "\U0001F94AПерчатки", "\U0001F456Штаны", "\U0001F45FБотинки"]:
            weapons(message)
    
        elif message.text == "\U0001F4E4Продать":
            sell(message)
    
        elif message.text[:5] == "/buy_" and message.text[5:9] in dict_inventory and message.text != "/buy_Нет":
            buy_(message)
    
        elif message.text[:6] == "/sell_" and message.text[6:10] in dict_inventory and message.text != "/sell_Нет":
            sell_(message)
    
        elif message.text[:4] == "/on_" and message.text[4:8] in dict_inventory and message.text != "/on_Нет":
            on_(message)
    
        elif message.text[:5] == "/off_" and message.text[5:9] in dict_inventory and message.text != "/off_Нет":
            off_(message)
    
        elif message.text == "\U0001F37BБар":
            bar(message)
    
        elif message.text in ["\U00002660Пьяница", "\U00002665Девушка", "\U0001F0CFМастер"]:
            cards(message)
    
        elif message.text == "\U0001F37AКружка пива":
            beer(message)
    
        elif message.text == "\U0001F40EИпподром":
            hippodrome_1(message)
    
        elif message.text in ["1\U0001F3C7", "2\U0001F3C7", "3\U0001F3C7", "4\U0001F3C7"]:
            hippodrome_2(message)
    
        elif message.text == "\U0001F4DCОтчет" or message.text == "/report":
            report(message)
    
        elif message.text == "\U0001F392Сумка" or message.text == "/hero":
            bag(message)
    
        elif message.text == "\U0001F396Рейтинг" or message.text == "/top":
            rating(message)
    
        elif message.text == "/players_top":
            players_top(message)
    
        elif message.text == "/global_top":
            global_top(message)
    
        elif message.text == "\U00002139F.A.Q.":
            faq(message)
    
        elif message.text == "/level_up":
            level_up(message)
    
        elif message.text in ["+1 \U0001F5E1Атака", "+1 \U0001F6E1Защита"]:
            feature_increase(message)
    
        elif message.text == "/clan_change":
            clan_change(message)
    
        elif message.text == "/name_change":
            name_change(message)
    
        elif message.text == "\U00002B05Назад":
            back(message)
    
        else:
            other(message)
            
    except Exception as e:
        
        excepter(message)


bot.polling(none_stop=True, interval=0)
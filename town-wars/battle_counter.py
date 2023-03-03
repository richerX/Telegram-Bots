# -*- coding: utf-8 -*-
from constants import *
import time
import sqlite3
import telebot


def battle_counter():
    while True:
        now_time = list(time.gmtime())
        now_time[3] += 3

        if now_time[3] % 4 == 0 and now_time[4] == 1 and not stop_bot_flag:  # hours, minutes
            battle_flag = True
            connection = sqlite3.connect("database", check_same_thread=False)
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM PLAYERS")
            mas_all_players = cursor.fetchall()
            for player in mas_all_players:
                if player[9] > player[8]:
                    cursor.execute("UPDATE Players SET Stamina = '{1}' WHERE ID = '{0}'".format(player[0], player[8] + 1))

            cursor.execute("SELECT * FROM PLAYERS")
            mas_players = cursor.fetchall()
            for player in mas_players:
                cursor.execute("UPDATE Players SET 'Battle money' = 0 WHERE ID = '{0}'".format(player[0]))
                cursor.execute("UPDATE Players SET 'Battle exp' = 0 WHERE ID = '{0}'".format(player[0]))

            dict_attack = {"mafia": 0, "swat": 0, "mercenaries": 0, "marauders": 0}  # whole attack on
            dict_attack_mafia = {"swat": 0, "mercenaries": 0, "marauders": 0}  # who attacks mafia
            dict_attack_swat = {"mafia": 0, "mercenaries": 0, "marauders": 0}  # who attack swat
            dict_attack_mercenaries = {"mafia": 0, "swat": 0, "marauders": 0}  # who attacks mercenaries
            dict_attack_marauders = {"mafia": 0, "swat": 0, "mercenaries": 0}  # who attacks marauders

            dict_defence = {"mafia": 0, "swat": 0, "mercenaries": 0, "marauders": 0}  # whole defense of

            # Attack counter

            cursor.execute("SELECT * FROM PLAYERS WHERE Status = '{0}' ORDER BY Attack DESC".format("\U0001F004 Ты нападаешь на врагов!"))  # Mafia
            mas_players_attack_mafia = cursor.fetchall()
            for player in mas_players_attack_mafia:
                dict_attack["mafia"] += player[4]
                if player[1] == "\U0001F694Спецназ":
                    dict_attack_mafia["swat"] += player[4]
                elif player[1] == "\U0001F5E1Наёмники":
                    dict_attack_mafia["mercenaries"] += player[4]
                elif player[1] == "\U0001F44AМародёры":
                    dict_attack_mafia["marauders"] += player[4]

            cursor.execute("SELECT * FROM PLAYERS WHERE Status = '{0}' ORDER BY Attack DESC".format("\U0001F694 Ты нападаешь на врагов!"))  # SWAT
            mas_players_attack_swat = cursor.fetchall()
            for player in mas_players_attack_swat:
                dict_attack["swat"] += player[4]
                if player[1] == "\U0001F004Мафия":
                    dict_attack_swat["mafia"] += player[4]
                elif player[1] == "\U0001F5E1Наёмники":
                    dict_attack_swat["mercenaries"] += player[4]
                elif player[1] == "\U0001F44AМародёры":
                    dict_attack_swat["marauders"] += player[4]


            cursor.execute("SELECT * FROM PLAYERS WHERE Status = '{0}' ORDER BY Attack DESC".format("\U0001F5E1 Ты нападаешь на врагов!"))  # Mercenaries
            mas_players_attack_mercenaries = cursor.fetchall()
            for player in mas_players_attack_mercenaries:
                dict_attack["mercenaries"] += player[4]
                if player[1] == "\U0001F004Мафия":
                    dict_attack_mercenaries["mafia"] += player[4]
                elif player[1] == "\U0001F694Спецназ":
                    dict_attack_mercenaries["swat"] += player[4]
                elif player[1] == "\U0001F44AМародёры":
                    dict_attack_mercenaries["marauders"] += player[4]

            cursor.execute("SELECT * FROM PLAYERS WHERE Status = '{0}' ORDER BY Attack DESC".format("\U0001F44A Ты нападаешь на врагов!"))  # Marauders
            mas_players_attack_marauders = cursor.fetchall()
            for player in mas_players_attack_marauders:
                dict_attack["marauders"] += player[4]
                if player[1] == "\U0001F004Мафия":
                    dict_attack_marauders["mafia"] += player[4]
                elif player[1] == "\U0001F694Спецназ":
                    dict_attack_marauders["swat"] += player[4]
                elif player[1] == "\U0001F5E1Наёмники":
                    dict_attack_marauders["mercenaries"] += player[4]

            # Defence counter

            cursor.execute("SELECT * FROM PLAYERS WHERE Status = '{0}' ORDER BY Defence DESC".format("\U0001F004 Ты в обороне базы!"))  # Mafia
            mas_players_defence_mafia = cursor.fetchall()
            for player in mas_players_defence_mafia:
                dict_defence["mafia"] += player[5]

            cursor.execute("SELECT * FROM PLAYERS WHERE Status = '{0}' ORDER BY Defence DESC".format("\U0001F694 Ты в обороне базы!"))  # SWAT
            mas_players_defence_swat = cursor.fetchall()
            for player in mas_players_defence_swat:
                dict_defence["swat"] += player[5]

            cursor.execute("SELECT * FROM PLAYERS WHERE Status = '{0}' ORDER BY Defence DESC".format("\U0001F5E1 Ты в обороне базы!"))  # Mercenaries
            mas_players_defence_mercenaries = cursor.fetchall()
            for player in mas_players_defence_mercenaries:
                dict_defence["mercenaries"] += player[5]

            cursor.execute("SELECT * FROM PLAYERS WHERE Status = '{0}' ORDER BY Defence DESC".format("\U0001F44A Ты в обороне базы!"))  # Marauders
            mas_players_defence_marauders = cursor.fetchall()
            for player in mas_players_defence_marauders:
                dict_defence["marauders"] += player[5]

            # Battle counter

            mafia_points = 0
            swat_points = 0
            mercenaries_points = 0
            marauders_points = 0

            if dict_attack["mafia"] > dict_defence["mafia"]:
                money = 0

                cursor.execute("SELECT * FROM PLAYERS WHERE Clan = '{0}'".format("\U0001F004Мафия"))
                mas_mafia = cursor.fetchall()
                for player in mas_mafia:
                    money += 0.25 * player[7]
                    cursor.execute("SELECT * FROM PLAYERS WHERE ID = '{0}'".format(player[0]))
                    mas_player = cursor.fetchone()
                    money_1 = int(mas_player[11] - 0.25 * player[7])
                    cursor.execute("UPDATE Players SET 'Battle money' = '{1}' WHERE ID = '{0}'".format(player[0], money_1))
                    cursor.execute("UPDATE Players SET 'Battle exp' = '{1}' WHERE ID = '{0}'".format(player[0], player[3]))

                mafia_money = int(money)

                for player in mas_players_attack_mafia:
                    cursor.execute("SELECT * FROM PLAYERS WHERE ID = '{0}'".format(player[0]))
                    mas_player = cursor.fetchone()
                    money_1 = int(mas_player[11] + money * (player[4] / dict_attack["mafia"]))
                    cursor.execute("UPDATE Players SET 'Battle money' = '{1}' WHERE ID = '{0}'".format(player[0], money_1))
                    cursor.execute("UPDATE Players SET 'Battle exp' = '{1}' WHERE ID = '{0}'".format(player[0], player[3] + player[4]))

                swat_points += int(money * (dict_attack_mafia["swat"] / dict_attack["mafia"]))
                mercenaries_points += int(money * (dict_attack_mafia["mercenaries"] / dict_attack["mafia"]))
                marauders_points += int(money * (dict_attack_mafia["marauders"] / dict_attack["mafia"]))

            elif dict_attack["mafia"] <= dict_defence["mafia"]:
                money = 0

                for player in mas_players_attack_mafia:
                    money += 0.3 * player[7]
                    cursor.execute("SELECT * FROM PLAYERS WHERE ID = '{0}'".format(player[0]))
                    mas_player = cursor.fetchone()
                    money_1 = int(mas_player[11] - 0.3 * player[7])
                    cursor.execute("UPDATE Players SET 'Battle money' = '{1}' WHERE ID = '{0}'".format(player[0], money_1))
                    cursor.execute("UPDATE Players SET 'Battle exp' = '{1}' WHERE ID = '{0}'".format(player[0], player[3]))

                mafia_money = int(money)

                for player in mas_players_defence_mafia:
                    cursor.execute("SELECT * FROM PLAYERS WHERE ID = '{0}'".format(player[0]))
                    mas_player = cursor.fetchone()
                    money_1 = int(mas_player[11] + int(money * player[5] / dict_defence["mafia"]))
                    cursor.execute("UPDATE Players SET 'Battle money' = '{1}' WHERE ID = '{0}'".format(player[0], money_1))
                    cursor.execute("UPDATE Players SET 'Battle exp' = '{1}' WHERE ID = '{0}'".format(player[0], player[3] + player[5]))

                mafia_points += mafia_money


            if dict_attack["swat"] > dict_defence["swat"]:
                money = 0

                cursor.execute("SELECT * FROM PLAYERS WHERE Clan = '{0}'".format("\U0001F694Спецназ"))
                mas_swat = cursor.fetchall()
                for player in mas_swat:
                    money += 0.25 * player[7]
                    cursor.execute("SELECT * FROM PLAYERS WHERE ID = '{0}'".format(player[0]))
                    mas_player = cursor.fetchone()
                    money_1 = int(mas_player[11] - 0.25 * player[7])
                    cursor.execute("UPDATE Players SET 'Battle money' = '{1}' WHERE ID = '{0}'".format(player[0], money_1))
                    cursor.execute("UPDATE Players SET 'Battle exp' = '{1}' WHERE ID = '{0}'".format(player[0], player[3]))

                swat_money = int(money)

                for player in mas_players_attack_swat:
                    cursor.execute("SELECT * FROM PLAYERS WHERE ID = '{0}'".format(player[0]))
                    mas_player = cursor.fetchone()
                    money_1 = int(mas_player[11] + money * (player[4] / dict_attack["swat"]))
                    cursor.execute("UPDATE Players SET 'Battle money' = '{1}' WHERE ID = '{0}'".format(player[0], money_1))
                    cursor.execute("UPDATE Players SET 'Battle exp' = '{1}' WHERE ID = '{0}'".format(player[0], player[3] + player[4]))

                mafia_points += int(money * (dict_attack_swat["mafia"] / dict_attack["swat"]))
                mercenaries_points += int(money * (dict_attack_swat["mercenaries"] / dict_attack["swat"]))
                marauders_points += int(money * (dict_attack_swat["marauders"] / dict_attack["swat"]))

            elif dict_attack["swat"] <= dict_defence["swat"]:
                money = 0

                for player in mas_players_attack_swat:
                    money += 0.3 * player[7]
                    cursor.execute("SELECT * FROM PLAYERS WHERE ID = '{0}'".format(player[0]))
                    mas_player = cursor.fetchone()
                    money_1 = int(mas_player[11] - 0.3 * player[7])
                    cursor.execute("UPDATE Players SET 'Battle money' = '{1}' WHERE ID = '{0}'".format(player[0], money_1))
                    cursor.execute("UPDATE Players SET 'Battle exp' = '{1}' WHERE ID = '{0}'".format(player[0], player[3]))

                swat_money = int(money)

                for player in mas_players_defence_swat:
                    cursor.execute("SELECT * FROM PLAYERS WHERE ID = '{0}'".format(player[0]))
                    mas_player = cursor.fetchone()
                    money_1 = int(mas_player[11] + money * (player[5] / dict_defence["swat"]) // 1)
                    cursor.execute("UPDATE Players SET 'Battle money' = '{1}' WHERE ID = '{0}'".format(player[0], money_1))
                    cursor.execute("UPDATE Players SET 'Battle exp' = '{1}' WHERE ID = '{0}'".format(player[0], player[3] + player[5]))

                swat_points += swat_money


            if dict_attack["mercenaries"] > dict_defence["mercenaries"]:
                money = 0

                cursor.execute("SELECT * FROM PLAYERS WHERE Clan = '{0}'".format("\U0001F5E1Наёмники"))
                mas_mercenaries = cursor.fetchall()
                for player in mas_mercenaries:
                    money += 0.25 * player[7]
                    cursor.execute("SELECT * FROM PLAYERS WHERE ID = '{0}'".format(player[0]))
                    mas_player = cursor.fetchone()
                    money_1 = int(mas_player[11] - 0.25 * player[7])
                    cursor.execute("UPDATE Players SET 'Battle money' = '{1}' WHERE ID = '{0}'".format(player[0], money_1))
                    cursor.execute("UPDATE Players SET 'Battle exp' = '{1}' WHERE ID = '{0}'".format(player[0], player[3]))

                mercenaries_money = int(money)

                for player in mas_players_attack_mercenaries:
                    cursor.execute("SELECT * FROM PLAYERS WHERE ID = '{0}'".format(player[0]))
                    mas_player = cursor.fetchone()
                    money_1 = int(mas_player[11] + money * (player[4] / dict_attack["mercenaries"]))
                    cursor.execute("UPDATE Players SET 'Battle money' = '{1}' WHERE ID = '{0}'".format(player[0], money_1))
                    cursor.execute("UPDATE Players SET 'Battle exp' = '{1}' WHERE ID = '{0}'".format(player[0], player[3] + player[4]))

                mafia_points += int(money * (dict_attack_mercenaries["mafia"] / dict_attack["mercenaries"]))
                swat_points += int(money * (dict_attack_mercenaries["swat"] / dict_attack["mercenaries"]))
                marauders_points += int(money * (dict_attack_mercenaries["marauders"] / dict_attack["mercenaries"]))

            elif dict_attack["mercenaries"] <= dict_defence["mercenaries"]:
                money = 0

                for player in mas_players_attack_mercenaries:
                    money += 0.3 * player[7]
                    cursor.execute("SELECT * FROM PLAYERS WHERE ID = '{0}'".format(player[0]))
                    mas_player = cursor.fetchone()
                    money_1 = int(mas_player[11] - 0.3 * player[7])
                    cursor.execute("UPDATE Players SET 'Battle money' = '{1}' WHERE ID = '{0}'".format(player[0], money_1))
                    cursor.execute("UPDATE Players SET 'Battle exp' = '{1}' WHERE ID = '{0}'".format(player[0], player[3]))

                mercenaries_money = int(money)

                for player in mas_players_defence_mercenaries:
                    cursor.execute("SELECT * FROM PLAYERS WHERE ID = '{0}'".format(player[0]))
                    mas_player = cursor.fetchone()
                    money_1 = int(mas_player[11] + money * player[5] / dict_defence["mercenaries"])
                    cursor.execute("UPDATE Players SET 'Battle money' = '{1}' WHERE ID = '{0}'".format(player[0], money_1))
                    cursor.execute("UPDATE Players SET 'Battle exp' = '{1}' WHERE ID = '{0}'".format(player[0], player[3] + player[5]))

                mercenaries_points += mercenaries_money


            if dict_attack["marauders"] > dict_defence["marauders"]:
                money = 0

                cursor.execute("SELECT * FROM PLAYERS WHERE Clan = '{0}'".format("\U0001F44AМародёры"))
                mas_marauders = cursor.fetchall()
                for player in mas_marauders:
                    money += 0.25 * player[7]
                    cursor.execute("SELECT * FROM PLAYERS WHERE ID = '{0}'".format(player[0]))
                    mas_player = cursor.fetchone()
                    money_1 = int(mas_player[11] - 0.25 * player[7])
                    cursor.execute("UPDATE Players SET 'Battle money' = '{1}' WHERE ID = '{0}'".format(player[0], money_1))
                    cursor.execute("UPDATE Players SET 'Battle exp' = '{1}' WHERE ID = '{0}'".format(player[0], player[3]))

                marauders_money = int(money)

                for player in mas_players_attack_marauders:
                    cursor.execute("SELECT * FROM PLAYERS WHERE ID = '{0}'".format(player[0]))
                    mas_player = cursor.fetchone()
                    money_1 = int(mas_player[11] + money * (player[4] / dict_attack["marauders"]))
                    cursor.execute("UPDATE Players SET 'Battle money' = '{1}' WHERE ID = '{0}'".format(player[0], money_1))
                    cursor.execute("UPDATE Players SET 'Battle exp' = '{1}' WHERE ID = '{0}'".format(player[0], player[3] + player[4]))

                mafia_points += int(money * (dict_attack_marauders["mafia"] / dict_attack["marauders"]))
                swat_points += int(money * (dict_attack_marauders["swat"] / dict_attack["marauders"]))
                mercenaries_points += int(money * (dict_attack_marauders["mercenaries"] / dict_attack["marauders"]))

            elif dict_attack["marauders"] <= dict_defence["marauders"]:
                money = 0

                for player in mas_players_attack_marauders:
                    money += 0.3 * player[7]
                    cursor.execute("SELECT * FROM PLAYERS WHERE ID = '{0}'".format(player[0]))
                    mas_player = cursor.fetchone()
                    money_1 = int(mas_player[11] - 0.3 * player[7])
                    cursor.execute("UPDATE Players SET 'Battle money' = '{1}' WHERE ID = '{0}'".format(player[0], money_1))
                    cursor.execute("UPDATE Players SET 'Battle exp' = '{1}' WHERE ID = '{0}'".format(player[0], player[3]))

                marauders_money = int(money)

                for player in mas_players_defence_marauders:
                    cursor.execute("SELECT * FROM PLAYERS WHERE ID = '{0}'".format(player[0]))
                    mas_player = cursor.fetchone()
                    money_1 = int(mas_player[11] + money * player[5] / dict_defence["marauders"])
                    cursor.execute("UPDATE Players SET 'Battle money' = '{1}' WHERE ID = '{0}'".format(player[0], money_1))
                    cursor.execute("UPDATE Players SET 'Battle exp' = '{1}' WHERE ID = '{0}'".format(player[0], player[3] + player[5]))

                marauders_points += marauders_money

            cursor.execute("SELECT * FROM PLAYERS")
            mas_players = cursor.fetchall()

            for player in mas_players:
                cursor.execute("UPDATE Players SET Money = '{1}' WHERE ID = '{0}'".format(player[0], (player[7] + player[11]) // 1))
                cursor.execute("UPDATE Players SET Experience = '{1}' WHERE ID = '{0}'".format(player[0], (player[6] + player[12]) // 1))
                cursor.execute("UPDATE Players SET Status = '{1}' WHERE ID = '{0}'".format(player[0], "\U0001F6CCТы сейчас отдыхаешь!"))
                cursor.execute("UPDATE WorkStatus SET Status = 0 WHERE ID = '{0}'".format(player[0]))

            str1 = "<b>\U00002694Итоги сражений\U00002694</b> \n"
            str1 += "\n"

            if dict_attack["mafia"] > dict_defence["mafia"]:
                str1 += "\U0001F004Базу мафии уничтожили\n"
            elif dict_attack["mafia"] <= dict_defence["mafia"]:
                str1 += "\U0001F004База мафии выстояла\n"
            str1 += "\U00002694Топ атаки:"
            for i in range(min(3, len(mas_players_attack_mafia))):
                player = mas_players_attack_mafia[i]
                str1 += "{0}{1}".format(player[1][:1], player[2])
            str1 += "\n"
            str1 += "\U0001F6E1Топ защиты:"
            for i in range(min(3, len(mas_players_defence_mafia))):
                player = mas_players_defence_mafia[i]
                str1 += "{0}{1}".format(player[1][:1], player[2])
            str1 += "\n"
            if dict_attack["mafia"] > dict_defence["mafia"]:
                str1 += ("\U0001F4B0Нападавшие разграбили базу на {0} $ \n".format(mafia_money))
            elif dict_attack["mafia"] <= dict_defence["mafia"]:
                str1 += ("\U0001F4B0Защитники отобрали у нападавших {0} $ \n".format(mafia_money))
            str1 += "\n"

            if dict_attack["swat"] > dict_defence["swat"]:
                str1 += "\U0001F694Базу спецназа уничтожили\n"
            elif dict_attack["swat"] <= dict_defence["swat"]:
                str1 += "\U0001F694База спецназа выстояла\n"
            str1 += "\U00002694Топ атаки:"
            for i in range(min(3, len(mas_players_attack_swat))):
                player = mas_players_attack_swat[i]
                str1 += "{0}{1}".format(player[1][:1], player[2])
            str1 += "\n"
            str1 += "\U0001F6E1Топ защиты:"
            for i in range(min(3, len(mas_players_defence_swat))):
                player = mas_players_defence_swat[i]
                str1 += "<b>{0}{1}</b>".format(player[1][:1], player[2])
            str1 += "\n"
            if dict_attack["swat"] > dict_defence["swat"]:
                str1 += ("\U0001F4B0Нападавшие разграбили базу на {0} $ \n".format(swat_money))
            elif dict_attack["swat"] <= dict_defence["swat"]:
                str1 += ("\U0001F4B0Защитники отобрали у нападавших {0} $ \n".format(swat_money))
            str1 += "\n"

            if dict_attack["mercenaries"] > dict_defence["mercenaries"]:
                str1 += "\U0001F5E1Базу наёмников уничтожили\n"
            elif dict_attack["mercenaries"] <= dict_defence["mercenaries"]:
                str1 += "\U0001F5E1База наёмников выстояла\n"
            str1 += "\U00002694Топ атаки:"
            for i in range(min(3, len(mas_players_attack_mercenaries))):
                player = mas_players_attack_mercenaries[i]
                str1 += "<b>{0}{1}</b>".format(player[1][:1], player[2])
            str1 += "\n"
            str1 += "\U0001F6E1Топ защиты:"
            for i in range(min(3, len(mas_players_defence_mercenaries))):
                player = mas_players_defence_mercenaries[i]
                str1 += "<b>{0}{1}</b>".format(player[1][:1], player[2])
            str1 += "\n"
            if dict_attack["mercenaries"] > dict_defence["mercenaries"]:
                str1 += ("\U0001F4B0Нападавшие разграбили базу на {0} $ \n".format(mercenaries_money))
            elif dict_attack["mercenaries"] <= dict_defence["mercenaries"]:
                str1 += ("\U0001F4B0Защитники отобрали у нападавших {0} $ \n".format(mercenaries_money))
            str1 += "\n"

            if dict_attack["marauders"] > dict_defence["marauders"]:
                str1 += "\U0001F44AБазу марадёров уничтожили\n"
            elif dict_attack["marauders"] <= dict_defence["marauders"]:
                str1 += "\U0001F44AБаза марадёров выстояла\n"
            str1 += "\U00002694Топ атаки:"
            for i in range(min(3, len(mas_players_attack_marauders))):
                player = mas_players_attack_marauders[i]
                str1 += "<b>{0}{1}</b>".format(player[1][:1], player[2])
            str1 += "\n"
            str1 += "\U0001F6E1Топ защиты:"
            for i in range(min(3, len(mas_players_defence_marauders))):
                player = mas_players_defence_marauders[i]
                str1 += "{0}{1}".format(player[1][:1], player[2])
            str1 += "\n"
            if dict_attack["marauders"] > dict_defence["marauders"]:
                str1 += ("\U0001F4B0Нападавшие разграбили базу на {0} $ \n".format(marauders_money))
            elif dict_attack["marauders"] <= dict_defence["marauders"]:
                str1 += ("\U0001F4B0Защитники отобрали у нападавших {0} $ \n".format(marauders_money))
            str1 += "\n"
            str1 += "\n"
            str1 += "<b>\U0001F396Итоговый рейтинг\U0001F396</b> \n"
            str1 += "\n"
            str1 += "\U0001F004Мафия +{0}\U0001F3C6 \n".format(mafia_points)
            str1 += "\U0001F694Спецназ +{0}\U0001F3C6 \n".format(swat_points)
            str1 += "\U0001F5E1Наёмники +{0}\U0001F3C6 \n".format(mercenaries_points)
            str1 += "\U0001F44AМародёры +{0}\U0001F3C6 \n".format(marauders_points)

            cursor.execute("SELECT * FROM Clans")
            mas_clans = cursor.fetchall()
            for clan in mas_clans:
                if clan[0] == "Mafia":
                    cursor.execute("UPDATE Clans SET Points = '{0}' WHERE Name = 'Mafia'".format(clan[1] + mafia_points))
                elif clan[0] == "SWAT":
                    cursor.execute("UPDATE Clans SET Points = '{0}' WHERE Name = 'SWAT'".format(clan[1] + swat_points))
                elif clan[0] == "Mercenaries":
                    cursor.execute("UPDATE Clans SET Points = '{0}' WHERE Name = 'Mercenaries'".format(clan[1] + mercenaries_points))
                elif clan[0] == "Marauders":
                    cursor.execute("UPDATE Clans SET Points = '{0}' WHERE Name = 'Marauders'".format(clan[1] + marauders_points))

            connection.commit()
            connection.close()

            bot.send_message(report_chat_id, str1, parse_mode="html")
            battle_flag = False
            time.sleep(600)

        elif now_time[4] == 1 and not stop_bot_flag:
            connection = sqlite3.connect("database", check_same_thread=False)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM PLAYERS")
            mas_all_players = cursor.fetchall()
            for player in mas_all_players:
                if player[9] > player[8]:
                    cursor.execute("UPDATE Players SET Stamina = '{1}' WHERE ID = '{0}'".format(player[0], player[8] + 1))
            connection.commit()
            connection.close()
            time.sleep(600)

        else:
            time.sleep(10)


battle_counter()
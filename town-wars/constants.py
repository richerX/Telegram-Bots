# -*- coding: utf-8 -*-
import telebot


# ------------------------- Constants -------------------------


stop_bot_flag = False
battle_flag = False


# --------------------------- Token ---------------------------


bot = telebot.TeleBot("")

report_chat_id = ""

# --------------------------- Inventory  ---------------------------


dict_inventory = {'1011': [['Helmet', 4], '\U0001F1EB\U0001F1F7203 "Штурмовой"', 0, 1, 10, 'Шлем'],
                  '1012': [['Armor', 5], '\U0001F1EB\U0001F1F7203 "Штурмовой"', 0, 1, 10, 'Бронежилет'],
                  '1013': [['Gloves', 6], '\U0001F1EB\U0001F1F7203 "Штурмовой"', 0, 1, 10, 'Перчатки'],
                  '1014': [['Pants', 7], '\U0001F1EB\U0001F1F7203 "Штурмовой"', 0, 1, 10, 'Штаны'],
                  '1015': [['Boots', 8], '\U0001F1EB\U0001F1F7203 "Штурмовой"', 0, 1, 10, 'Ботинки'],

                  '1021': [['Helmet', 4], '\U0001F1F7\U0001F1FAКомфорт "ГП"', 0, 3, 40, 'Шлем'],
                  '1022': [['Armor', 5], '\U0001F1F7\U0001F1FAКомфорт "ГП"', 0, 3, 40, 'Бронежилет'],
                  '1023': [['Gloves', 6], '\U0001F1F7\U0001F1FAКомфорт "ГП"', 0, 2, 25, 'Перчатки'],
                  '1024': [['Pants', 7], '\U0001F1F7\U0001F1FAКомфорт "ГП"', 0, 2, 25, 'Штаны'],
                  '1025': [['Boots', 8], '\U0001F1F7\U0001F1FAКомфорт "ГП"', 0, 2, 25, 'Ботинки'],

                  '1031': [['Helmet', 4], '\U0001F1F7\U0001F1FAСфера-3', 0, 4, 80, 'Шлем'],
                  '1032': [['Armor', 5], '\U0001F1F7\U0001F1FAСфера-3', 0, 5, 100, 'Бронежилет'],
                  '1033': [['Gloves', 6], '\U0001F1F7\U0001F1FAСфера-3', 0, 3, 70, 'Перчатки'],
                  '1034': [['Pants', 7], '\U0001F1F7\U0001F1FAСфера-3', 0, 3, 70, 'Штаны'],
                  '1035': [['Boots', 8], '\U0001F1F7\U0001F1FAСфера-3', 0, 3, 70, 'Ботинки'],

                  '1041': [['Helmet', 4], '\U0001F1FA\U0001F1F8Шкура дракона', 0, 6, 150, 'Шлем'],
                  '1042': [['Armor', 5], '\U0001F1FA\U0001F1F8Шкура дракона', 0, 8, 250, 'Бронежилет'],
                  '1043': [['Gloves', 6], '\U0001F1FA\U0001F1F8Шкура дракона', 0, 5, 140, 'Перчатки'],
                  '1044': [['Pants', 7], '\U0001F1FA\U0001F1F8Шкура дракона', 0, 5, 140, 'Штаны'],
                  '1045': [['Boots', 8], '\U0001F1FA\U0001F1F8Шкура дракона', 0, 5, 140, 'Ботинки'],

                  '1051': [['Helmet', 4], '\U0001F1F7\U0001F1FAСапфир "ПРОФИ"', 1, 8, 350, 'Шлем'],
                  '1052': [['Armor', 5], '\U0001F1F7\U0001F1FAСапфир "ПРОФИ"', 3, 10, 500, 'Бронежилет'],
                  '1053': [['Gloves', 6], '\U0001F1F7\U0001F1FAСапфир "ПРОФИ"', 2, 6, 400, 'Перчатки'],
                  '1054': [['Pants', 7], '\U0001F1F7\U0001F1FAСапфир "ПРОФИ"', 2, 6, 400, 'Штаны'],
                  '1055': [['Boots', 8], '\U0001F1F7\U0001F1FAСапфир "ПРОФИ"', 2, 6, 400, 'Ботинки'],

                  '1061': [['Helmet', 4], '\U0001F1F7\U0001F1FAМодуль-5М', 0, 10, 700, 'Шлем'],
                  '1062': [['Armor', 5], '\U0001F1F7\U0001F1FAМодуль-5М', 0, 15, 800, 'Бронежилет'],
                  '1063': [['Gloves', 6], '\U0001F1F7\U0001F1FAМодуль-5М', 0, 8, 650, 'Перчатки'],
                  '1064': [['Pants', 7], '\U0001F1F7\U0001F1FAМодуль-5М', 0, 8, 650, 'Штаны'],
                  '1065': [['Boots', 8], '\U0001F1F7\U0001F1FAМодуль-5М', 0, 8, 650, 'Ботинки'],

                  '1071': [['Helmet', 4], '\U0001F1F7\U0001F1FAШилд "Штурмовой"', 4, 5, 900, 'Шлем'],
                  '1072': [['Armor', 5], '\U0001F1F7\U0001F1FAШилд "Штурмовой"', 6, 8, 1000, 'Бронежилет'],
                  '1073': [['Gloves', 6], '\U0001F1F7\U0001F1FAШилд "Штурмовой"', 4, 4, 850, 'Перчатки'],
                  '1074': [['Pants', 7], '\U0001F1F7\U0001F1FAШилд "Штурмовой"', 4, 4, 850, 'Штаны'],
                  '1075': [['Boots', 8], '\U0001F1F7\U0001F1FAШилд "Штурмовой"', 4, 4, 850, 'Ботинки'],

                  '1111': [['Secondary weapon', 2], '\U0001F1F7\U0001F1FAПЛ-14', 2, 0, 30, 'Дополнительное оружие'],
                  '1112': [['Secondary weapon', 2], '\U0001F1EC\U0001F1E7Revolver', 3, 0, 80, 'Дополнительное оружие'],
                  '1113': [['Secondary weapon', 2], '\U0001F1E9\U0001F1EAHK USP', 4, 0, 150, 'Дополнительное оружие'],
                  '1114': [['Secondary weapon', 2], '\U0001F1E8\U0001F1ED\U0001F1E9\U0001F1EASIG Sauer P250', 5, 0, 300, 'Дополнительное оружие'],
                  '1115': [['Secondary weapon', 2], '\U0001F1F7\U0001F1FA\U0001F1EE\U0001F1F9Стриж', 6, 1, 500, 'Дополнительное оружие'],
                  '1116': [['Secondary weapon', 2], '\U0001F1FA\U0001F1F8\U0001F1E7\U0001F1EAFN FNX', 8, 2, 750, 'Дополнительное оружие'],
                  '1117': [['Secondary weapon', 2], '\U0001F1F8\U0001F1EATec-9', 10, 3, 1000, 'Дополнительное оружие'],
                  '1118': [['Secondary weapon', 2], '\U0001F1FA\U0001F1F8\U0001F1EE\U0001F1F1Desert Eagle', 12, 4, 1300, 'Дополнительное оружие'],

                  '1121': [['Secondary weapon', 2], '\U0001F1F7\U0001F1FAPP-19', 1, 1, 20, 'Дополнительное оружие'],
                  '1122': [['Secondary weapon', 2], '\U0001F1E9\U0001F1EAHK UMP 45', 2, 2, 50, 'Дополнительное оружие'],
                  '1123': [['Secondary weapon', 2], '\U0001F1FA\U0001F1F8MAC-10', 3, 3, 100, 'Дополнительное оружие'],
                  '1124': [['Secondary weapon', 2], '\U0001F1E9\U0001F1EAHK MP7', 4, 4, 200, 'Дополнительное оружие'],
                  '1125': [['Secondary weapon', 2], '\U0001F1E8\U0001F1EDSIG SG 550', 5, 5, 350, 'Дополнительное оружие'],
                  '1126': [['Secondary weapon', 2], '\U0001F1E7\U0001F1EAFN P90', 6, 6, 550, 'Дополнительное оружие'],
                  '1127': [['Secondary weapon', 2], '\U0001F1FA\U0001F1F8TDI Vector', 7, 7, 800, 'Дополнительное оружие'],
                  '1128': [['Secondary weapon', 2], '\U0001F1F8\U0001F1F0\U0001F1E8\U0001F1FFScorpion EVO 3 A1', 8, 8, 1000, 'Дополнительное оружие'],

                  '1131': [['Primary weapon', 1], '\U0001F1FA\U0001F1F8Barret REC7', 2, 0, 50, 'Основное оружие'],
                  '1132': [['Primary weapon', 1], '\U0001F1E9\U0001F1EA\U0001F1FA\U0001F1F8HK416', 4, 0, 100, 'Основное оружие'],
                  '1133': [['Primary weapon', 1], '\U0001F1EB\U0001F1F7Famas', 7, 0, 200, 'Основное оружие'],
                  '1134': [['Primary weapon', 1], '\U0001F1F7\U0001F1FAA-545', 10, 1, 450, 'Основное оружие'],
                  '1135': [['Primary weapon', 1], '\U0001F1FA\U0001F1F8M4', 12, 2, 800, 'Основное оружие'],
                  '1136': [['Primary weapon', 1], '\U0001F1E7\U0001F1EA\U0001F1FA\U0001F1F8FN SCAR', 15, 3, 1300, 'Основное оружие'],
                  '1137': [['Primary weapon', 1], '\U0001F1F7\U0001F1FAAK-12', 19, 4, 1850, 'Основное оружие'],
                  '1138': [['Primary weapon', 1], '\U0001F1F7\U0001F1F8Застава М21', 22, 5, 2500, 'Основное оружие'],

                  '1141': [['Primary weapon', 1], '\U0001F1E9\U0001F1EAHaenel G29', 1, 2, 40, 'Основное оружие'],
                  '1142': [['Primary weapon', 1], '\U0001F1F0\U0001F1F7S&T Motiv K14', 3, 5, 80, 'Основное оружие'],
                  '1143': [['Primary weapon', 1], '\U0001F1F7\U0001F1FAВС-121', 5, 8, 170, 'Основное оружие'],
                  '1144': [['Primary weapon', 1], '\U0001F1F7\U0001F1FAСК-16', 7, 12, 350, 'Основное оружие'],
                  '1145': [['Primary weapon', 1], '\U0001F1FA\U0001F1F8FN SPR', 9, 16, 600, 'Основное оружие'],
                  '1146': [['Primary weapon', 1], '\U0001F1FA\U0001F1F8Barret M98B', 11, 20, 950, 'Основное оружие'],
                  '1147': [['Primary weapon', 1], '\U0001F1F7\U0001F1FAОРСИС Т-5000', 13, 26, 1500, 'Основное оружие'],
                  '1148': [['Primary weapon', 1], '\U0001F1EC\U0001F1E7Arctic Warfare', 15, 30, 2000, 'Основное оружие'],

                  'Пусто': ['Пусто', 'Пусто', 0, 0, 0],
                  'Нет': ['Нет', 'Нет', 0, 0, 0]
                  }


# --------------------------- Keyboards  ---------------------------


show_keyboard_main = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
show_keyboard_main.row("\U0001F5E1Атака", "\U0001F6E1Оборона", "\U0001F310Задания")
show_keyboard_main.row("\U0001F3C2Боец", "\U0001F3EFБаза", "\U00002139F.A.Q.")


show_keyboard_clan = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
show_keyboard_clan.row("\U0001F004Мафия", "\U0001F694Спецназ")
show_keyboard_clan.row("\U0001F5E1Наёмники", "\U0001F44AМародёры")


show_keyboard_quests = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
show_keyboard_quests.row("\U0001F3F9Полигон", "\U0001F303Город")
show_keyboard_quests.row("\U0001F4B0Ограбление")
show_keyboard_quests.row("\U00002B05Назад")


show_keyboard_base = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
show_keyboard_base.row("\U0001F392Сумка", "\U0001F5C3Склад", "\U0001F4DCОтчет")
show_keyboard_base.row("\U0001F4B0Торговец", "\U0001F37BБар", "\U0001F40EИпподром")
show_keyboard_base.row("\U0001F396Рейтинг")
show_keyboard_base.row("\U00002B05Назад")


show_keyboard_level_up = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
show_keyboard_level_up.row("+1 \U0001F5E1Атака", "+1 \U0001F6E1Защита")
show_keyboard_level_up.row("\U00002B05Назад")

show_keyboard_market = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
show_keyboard_market.row("\U0001F4E5Купить", "\U0001F4E4Продать")
show_keyboard_market.row("\U00002B05Назад")

show_keyboard_market_buy = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
show_keyboard_market_buy.row("\U0001F5E1Винтовки", "\U0001F6E1Снайперки")
show_keyboard_market_buy.row("\U0001F5E1Пистолеты", "\U0001F6E1Пистолеты-пулемёты")
show_keyboard_market_buy.row("\U0001F3A9Шлемы", "\U0001F454Бронежилеты", "\U0001F94AПерчатки")
show_keyboard_market_buy.row("\U0001F456Штаны", "\U0001F45FБотинки", "\U00002B05Назад")

# show_keyboard_market_buy_1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
# show_keyboard_market_buy_1.row("\U0001F5E1Винтовки", "\U0001F6E1Снайперки")
# show_keyboard_market_buy_1.row("\U00002B05Назад")
#
# show_keyboard_market_buy_2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
# show_keyboard_market_buy_2.row("\U0001F5E1Пистолеты", "\U0001F6E1Пистолеты-пулемёты")
# show_keyboard_market_buy_2.row("\U00002B05Назад")

show_keyboard_bar = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
show_keyboard_bar.row("\U00002660Пьяница", "\U00002665Девушка", "\U0001F0CFМастер")
show_keyboard_bar.row("\U0001F37AКружка пива")
show_keyboard_bar.row("\U00002B05Назад")

show_keyboard_bet = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
show_keyboard_bet.row("10", "50", "100")
show_keyboard_bet.row("200", "500", "1000")
show_keyboard_bet.row("\U00002B05Назад")

show_keyboard_stop_bot = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
show_keyboard_stop_bot.row("\U0001F6A7 Технические работы \U0001F6A7")

show_keyboard_horses = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
show_keyboard_horses.row("1\U0001F3C7", "2\U0001F3C7")
show_keyboard_horses.row("3\U0001F3C7", "4\U0001F3C7")
show_keyboard_horses.row("\U00002B05Назад")
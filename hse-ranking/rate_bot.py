# -*- coding: utf-8 -*-
import sys
import time
import threading
import traceback
import telebot
import gspread
from telebot import types
from oauth2client.service_account import ServiceAccountCredentials


bot = telebot.TeleBot("")


def excepter(message):
    try:
        error_class = sys.exc_info()[0]
        error = sys.exc_info()[1]
        line = sys.exc_info()[2].tb_lineno
        
        mas_time = time.asctime().split()
        string_time = mas_time[2] + " " + mas_time[1] + " " + mas_time[4] + " | " + mas_time[3]
        
        file_name = "Error"
        file = open('{0}.txt'.format(file_name), 'w')
        file.write('Filename: ' + 'Rate bot' + '\n')
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
        bot.send_document("", file_to_send)
        if message != '':
            bot.send_message(message.from_user.id, "Software error has occurred. Report has already been sent to developers. Sorry.", parse_mode = 'HTML')
    
    except:
        file_name = "ErrorLog"
        file = open('{0}.txt'.format(file_name), 'a')
        mas_time = time.asctime().split()
        string_time = mas_time[2] + " " + mas_time[1] + " " + mas_time[4] + " | " + mas_time[3]
        error_class = sys.exc_info()[0]
        file.write(str(string_time) + " | problem with excepter() | " + str(sys.exc_info()) + " | " + '\n')
        file.close()


def read_users(filename):
    all_users = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                user = dict()
                lines = [line]
                for i in range(7):
                    lines.append(file.readline())
                user["number"] = int(lines[0].split()[1][1:])
                user["id"] = int(lines[1].split()[1])
                user["is_bot"] = lines[2].split()[1]
                user["username"] = lines[3].split()[1]
                user["first_name"] = lines[4].split()[1]
                user["last_name"] = lines[5].split()[1]
                user["language_code"] = lines[6].split()[1]
                all_users.append(user)
    except:
        pass
    return all_users


def write_user(message, filename, all_users):
    all_id = []
    max_number = 0
    for user in all_users:
        all_id.append(user['id'])
        if user['number'] > max_number:
            max_number = user['number']
    if message.from_user.id not in all_id:
        with open(filename, "a", encoding="utf-8") as file:
            file.write('USER №' + str(max_number + 1) + '\n')
            file.write('id: ' + str(message.from_user.id) + '\n')
            file.write('is_bot: ' + str(message.from_user.is_bot) + '\n')
            file.write('username: ' + str(message.from_user.username) + '\n')
            file.write('first_name: ' + str(message.from_user.first_name) + '\n')
            file.write('last_name: ' + str(message.from_user.last_name) + '\n')
            file.write('language_code: ' + str(message.from_user.language_code) + '\n')
            file.write(' \n')


def send_users(admin_id):
    with open("users.txt", "r", encoding="utf-8") as file_to_send:
        bot.send_document(admin_id, file_to_send, reply_markup = keyboard_admin, parse_mode = 'HTML')

def send_updates(admin_id):
    answer = ""
    with open("UpdateLogCalc.txt", 'r', encoding="utf-8") as file:
        answer += "Calsulus last update - " + file.readline()[:22].strip() + "\n"
    with open("UpdateLogDisc.txt", 'r', encoding="utf-8") as file:
        answer += "Discrete last update - " + file.readline()[:22].strip() + "\n"
    bot.send_message(admin_id, answer, reply_markup = keyboard_admin, parse_mode = 'HTML')
    
def sorter(x):
    return -x[1][0], x[0]


def make_int(string):
    try:
        answer = int(string)
    except:
        try:
            answer = int(float(string))
        except:
            answer = int(string.split(',')[0])
    return answer


def rating_update_calculus():
    
    while True:
        
        try:
            
            '''
            Reading the informatiom from Google table
            '''
            
            global actual_points_calculus
            
            scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
            credentials = ServiceAccountCredentials.from_json_keyfile_name("", scope)
            gc = gspread.authorize(credentials)
            urls = [""]
            name_points_calculus = dict()
            for url in urls:
                wb = gc.open_by_url(url)
                sheets = wb.worksheets()
                for sheet_open in sheets:
                    sheet = wb.worksheet(sheet_open.title)
                    matrix = sheet.get_all_values()
                        
                    if '181' in wb.title:
                        group = 181
                    else:
                        group = 182
                    for i in range(1, len(matrix) - 2):
                        surname = matrix[i][1]
                        name = matrix[i][2]
                        full_name = surname + " " + name
                        if name_points_calculus.get(full_name) == None and full_name != ' ':
                            name_points_calculus[full_name] = [0, group]
                        for j in range(5, len(matrix[i])):
                            if matrix[i][j] not in [None, '']:
                                name_points_calculus[full_name][0] += int(matrix[i][j])
            actual_points_calculus = name_points_calculus
            
            file_name = "UpdateLogCalc"
            file = open('{0}.txt'.format(file_name), 'w')
            mas_time = time.asctime().split()
            string_time = mas_time[2] + " " + mas_time[1] + " " + mas_time[4] + " | " + mas_time[3]
            file.write(str(string_time) + " | calc | " + 'Updated information' + '\n')
            file.close()             
        
        except gspread.exceptions.APIError:
            file_name = "ErrorLog"
            file = open('{0}.txt'.format(file_name), 'a')
            mas_time = time.asctime().split()
            string_time = mas_time[2] + " " + mas_time[1] + " " + mas_time[4] + " | " + mas_time[3]
            error_class = sys.exc_info()[0]
            file.write(str(string_time) + " | calc | " + str(error_class) + '\n')
            file.close()
        
        except oauth2client.client.HttpAccessTokenRefreshError:
            file_name = "ErrorLog"
            file = open('{0}.txt'.format(file_name), 'a')
            mas_time = time.asctime().split()
            string_time = mas_time[2] + " " + mas_time[1] + " " + mas_time[4] + " | " + mas_time[3]
            error_class = sys.exc_info()[0]
            file.write(str(string_time) + " | calc | " + str(error_class) + '\n')
            file.close()
        
        except:
            excepter('')
        
        time.sleep(60)
        
        
def rating_update_discrete():
    
    while True:
        
        try:
        
            '''
            Reading the informatiom from Google table
            '''
            
            global actual_points_discrete
            
            scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
            credentials = ServiceAccountCredentials.from_json_keyfile_name("", scope)
            gc = gspread.authorize(credentials)
            url = ""
            wb = gc.open_by_url(url)
            sheets = wb.worksheets()
            name_points_discrete = dict()
            
            for sheet_open in sheets:
                sheet = wb.worksheet(sheet_open.title)
                matrix = sheet.get_all_values()
                if sheet.title == 'BCI 181 attendance':
                    i_range = 77  # number of last row (literally)
                    j_range_1 = 24  # X column
                    j_range_2 = 19  # Q column
                    group = 181
                    cut = True
                    special_test_cut = False
                    divide_by_five = False
                    skip = [0, 1, 37, 38, 39, 40, 41]
                elif sheet.title == 'BCI 182 attendance ':
                    i_range = 77  # number of last row (literally)
                    j_range_1 = 24  # X column
                    j_range_2 = 17  # Q column
                    group = 182
                    cut = True
                    special_test_cut = False
                    divide_by_five = False
                    skip = [0, 1, 37, 38, 39, 40, 41]
                elif sheet.title == 'BCI 181 activity at classes':
                    i_range = 77  # number of last row (literally)
                    j_range_1 = 24  # X column
                    j_range_2 = 14  # N column                    
                    group = 181
                    cut = True
                    special_test_cut = False
                    divide_by_five = False
                    skip = [0, 1, 37, 38, 39, 40, 41]
                elif sheet.title == 'BCI 182 activity at classes':
                    i_range = 77  # number of last row (literally)
                    j_range_1 = 24  # X column
                    j_range_2 = 13  # N column                     
                    group = 182
                    cut = True
                    special_test_cut = False
                    divide_by_five = False
                    skip = [0, 1, 37, 38, 39, 40, 41]                
                elif sheet.title == 'BCI 181 activity at classes (PC and Class Work)':
                    j_range = 13  # N column 
                    group = 181
                    cut = False
                    special_test_cut = False
                    divide_by_five = True
                    skip = [0, 1]
                elif sheet.title == 'BCI 182 activity at classes (PC and Class Work)':
                    j_range = 12  # N column 
                    group = 182
                    cut = False
                    special_test_cut = False
                    divide_by_five = True
                    skip = [0, 1]
                elif sheet.title == 'BCI 181 Test':
                    j_range = 8  # H column
                    group = 181
                    cut = False
                    special_test_cut = True
                    divide_by_five = False
                    skip = [0, 1, 2]   
                elif sheet.title == 'BCI 182 Test':
                    j_range = 8  # H column
                    group = 182
                    cut = False
                    special_test_cut = True
                    divide_by_five = False
                    skip = [0, 1, 2]                   
                else:
                    pass
                
                if sheet.title in ['BCI 181 Home Work', 'BCI 182 Home Work']:
                    if sheet.title == 'BCI 181 Home Work':
                        group = 181
                    else:
                        group = 182
                    for i in range(2, 37):
                        surname = matrix[i][1]
                        name = matrix[i][2]
                        full_name = surname + " " + name
                        if name_points_discrete.get(full_name) == None:
                            name_points_discrete[full_name] = [0, group]
                        if matrix[i][5] not in [None, '']:
                            name_points_discrete[full_name][0] += make_int(matrix[i][5])
                
                elif sheet.title in ['BCI 181 Accumlated Grade', 'BCI 182 Accumlated Grade']:
                    pass
                
                elif sheet.title in ['BCI 181 attendance', 'BCI 182 attendance ', 'BCI 181 activity at classes', 'BCI 182 activity at classes']:
                    for i in range(37):
                        if i not in skip:
                            surname = matrix[i][1]
                            name = matrix[i][2]
                            full_name = surname + " " + name
                            length = len(matrix[i]) - int(cut == True)
                            if special_test_cut:
                                length = 8
                            if name_points_discrete.get(full_name) == None:
                                name_points_discrete[full_name] = [0, group]
                            divide_by_five_sum = 0
                            for j in range(4, j_range_1):
                                if matrix[i][j] not in [None, '']:
                                    if divide_by_five:
                                        divide_by_five_sum += make_int(matrix[i][j])
                                    else:
                                        name_points_discrete[full_name][0] += make_int(matrix[i][j])
                            if divide_by_five:
                                name_points_discrete[full_name][0] += divide_by_five_sum // 5
                    for i in range(38, i_range):
                        if i not in skip:
                            surname = matrix[i][1]
                            name = matrix[i][2]
                            full_name = surname + " " + name
                            length = len(matrix[i]) - int(cut == True)
                            if special_test_cut:
                                length = 8
                            if name_points_discrete.get(full_name) == None:
                                name_points_discrete[full_name] = [0, group]
                            divide_by_five_sum = 0
                            for j in range(4, j_range_2):
                                if matrix[i][j] not in [None, '']:
                                    if divide_by_five:
                                        divide_by_five_sum += make_int(matrix[i][j])
                                    else:
                                        name_points_discrete[full_name][0] += make_int(matrix[i][j])
                            if divide_by_five:
                                name_points_discrete[full_name][0] += divide_by_five_sum // 5
                
                else:
                    for i in range(len(matrix)):
                        if i not in skip:
                            surname = matrix[i][1]
                            name = matrix[i][2]
                            full_name = surname + " " + name
                            if name_points_discrete.get(full_name) == None:
                                name_points_discrete[full_name] = [0, group]
                            divide_by_five_sum = 0
                            for j in range(4, j_range):
                                if matrix[i][j] not in [None, '']:
                                    if divide_by_five:
                                        divide_by_five_sum += make_int(matrix[i][j])
                                    else:
                                        name_points_discrete[full_name][0] += make_int(matrix[i][j])
                            if divide_by_five:
                                name_points_discrete[full_name][0] += divide_by_five_sum // 5

            actual_points_discrete = name_points_discrete
            
            file_name = "UpdateLogDisc"
            file = open('{0}.txt'.format(file_name), 'w')
            mas_time = time.asctime().split()
            string_time = mas_time[2] + " " + mas_time[1] + " " + mas_time[4] + " | " + mas_time[3]
            file.write(str(string_time) + " | disc | " + 'Updated information' + '\n')
            file.close()            
        
        except gspread.exceptions.APIError:
            file_name = "ErrorLog"
            file = open('{0}.txt'.format(file_name), 'a')
            mas_time = time.asctime().split()
            string_time = mas_time[2] + " " + mas_time[1] + " " + mas_time[4] + " | " + mas_time[3]
            error_class = sys.exc_info()[0]
            file.write(str(string_time) + " | disc | " + str(error_class) + '\n')
            file.close()
        
        except oauth2client.client.HttpAccessTokenRefreshError:
            file_name = "ErrorLog"
            file = open('{0}.txt'.format(file_name), 'a')
            mas_time = time.asctime().split()
            string_time = mas_time[2] + " " + mas_time[1] + " " + mas_time[4] + " | " + mas_time[3]
            error_class = sys.exc_info()[0]
            file.write(str(string_time) + " | disc | " + str(error_class) + '\n')
            file.close()        
        
        except:
            excepter('')
        
        time.sleep(60)

actual_points_discrete = {'Updating info 1': [0, 181], 'Updating info 2': [0, 182]}
actual_points_calculus = {'Updating info 1': [0, 181], 'Updating info 2': [0, 182]}

def rating(user_id, subject, personal, group_mode, person, group_number):
    
    try:

        if subject == 'calculus':
            for_pre_students = actual_points_calculus
        elif subject == 'discrete':
            for_pre_students = actual_points_discrete
        else:
            for_pre_students = {'Updating info 1': [0, 181], 'Updating info 2': [0, 182]}
        pre_students = sorted(for_pre_students.items(), key = sorter)  #  Making students from pre_students
        students = []
        for student in pre_students:
            students.append([student[0], student[1][0], student[1][1]])
        
        if group_mode:
            students = [i for i in students if i[2] == int(group_number)]  #  Choose students from right group
        
        place_by_point = dict()  #  Getting all places and points
        places_list = []
        points_list = []    
        place_begin = 1
        for i in range(len(students)):
            if i != len(students) - 1 and students[i][1] == students[i + 1][1]:
                continue
            else:
                place_end = i + 1
                place_by_point[students[i][1]] = [place_begin, place_end]
                places_list.append([place_begin, place_end])
                points_list.append(students[i][1])   
                place_begin = i + 2  
    
        '''
        Printing the first block of informatiom from Google table
        '''
    
        final_string = '-' * 30 + "\n"
        head_string = ''
        if subject == 'calculus':
            head_string += '\U0001F537 '
        elif subject == 'discrete':
            head_string += '\U0001F536 '
        if group_mode and group_number == '181':
            head_string += 'GROUP 181 '
        elif group_mode and group_number == '182':
            head_string += 'GROUP 182 '
        else:
            head_string += 'RANKING '
        head_string += subject.upper()
        final_string += ("|" + "{:^27}".format(head_string) + "|" + "\n")     
        final_string += ('-' * 30 + "\n")
        final_string += ("| \U0001F396 " + "|  \U0001F3C6  " + "|" + "{:^14}".format('\U0001F194') + "|" + "\n")
        final_string += ('-' * 30 + "\n") 
        if personal:
            for full_name, points, group in students:
                if full_name == person:
                    if place_by_point[points][0] == place_by_point[points][1]:
                        place = str(place_by_point[points][0])
                    else:
                        place = str(place_by_point[points][0]) + "-" + str(place_by_point[points][1])
                    final_string += ("|" + "{:^5}".format(str(place)) + "|" + "{:^5}".format(str(points)) + "|" + "{:^16}".format(short_names[full_name]) + "|" +"\n")
                    final_string += ('-' * 30 + "\n")
        else:
            for full_name, points, group in students:
                if place_by_point[points][0] == place_by_point[points][1]:
                    place = str(place_by_point[points][0])
                else:
                    place = str(place_by_point[points][0]) + "-" + str(place_by_point[points][1])
                final_string += ("|" + "{:^5}".format(str(place)) + "|" + "{:^5}".format(str(points)) + "|" + "{:^16}".format(short_names[full_name]) + "|" +"\n")
                final_string += ('-' * 30 + "\n")

        '''
        Sending answer to the user
        '''    
    
        mas_to_string = final_string.split('\n')
        if len(mas_to_string) < 115:
            ranges = [[4, len(mas_to_string)]]
        else:
            ranges = [[4, 101], [100, len(mas_to_string)]]
        for a, b in ranges:
            string_to_send = ''
            string_to_send += mas_to_string[0] + "\n"
            string_to_send += mas_to_string[1] + "\n"
            string_to_send += mas_to_string[2] + "\n"
            string_to_send += mas_to_string[3] + "\n"
            for i in range(a, b):
                string_to_send += mas_to_string[i] + "\n"
            if subject == 'calculus':
                bot.send_message(user_id, "<pre>{0}</pre>".format(string_to_send), reply_markup = keyboard_calculus, parse_mode = 'HTML')
            elif subject == 'discrete':
                bot.send_message(user_id, "<pre>{0}</pre>".format(string_to_send), reply_markup = keyboard_discrete, parse_mode = 'HTML')
    
    except:
        file_name = "ErrorLog"
        file = open('{0}.txt'.format(file_name), 'a')
        mas_time = time.asctime().split()
        string_time = mas_time[2] + " " + mas_time[1] + " " + mas_time[4] + " | " + mas_time[3]
        error_class = sys.exc_info()[0]
        file.write(str(string_time) + " | problem with rating() | " + str(sys.exc_info()) + " | " + '\n')
        file.close()        

def feedback_sender(message):
    
    try:
        file_name = "Feedback"
        file = open('{0}.txt'.format(file_name), 'w')
        file.write('USER:' + '\n')
        file.write('id: ' + str(message.from_user.id) + '\n')
        file.write('is_bot: ' + str(message.from_user.is_bot) + '\n')
        file.write('username: ' + str(message.from_user.username) + '\n')
        file.write('first_name: ' + str(message.from_user.first_name) + '\n')
        file.write('last_name: ' + str(message.from_user.last_name) + '\n')
        file.write('language_code: ' + str(message.from_user.language_code) + '\n')
        file.write('\n')
        file.write(message.text + '\n')
        file.close()
        file_to_send = open('{0}.txt'.format(file_name), 'r')
        bot.send_document(287352001, file_to_send)
    
    except:
        file_name = "ErrorLog"
        file = open('{0}.txt'.format(file_name), 'a')
        mas_time = time.asctime().split()
        string_time = mas_time[2] + " " + mas_time[1] + " " + mas_time[4] + " | " + mas_time[3]
        error_class = sys.exc_info()[0]
        file.write(str(string_time) + " | problem with feedback_sender() | " + str(sys.exc_info()) + " | " + '\n')
        file.close()           

keyboard_main = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main.row("\U0001F4D8 Calculus", '\U0001F4D9 Discrete math')
keyboard_main.row("\U0001F4D3 Feedback")

keyboard_discrete = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_discrete.row("\U0001F536 \U0001F4F6", "\U0001F536 \U0001F194")
keyboard_discrete.row("\U0001F536 181", "\U0001F4D6 Menu", '\U0001F536 182')

keyboard_calculus = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_calculus.row("\U0001F537 \U0001F4F6", "\U0001F537 \U0001F194")
keyboard_calculus.row("\U0001F537 181", "\U0001F4D6 Menu", '\U0001F537 182')

keyboard_admin = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_admin.row("Users", 'Updates')
keyboard_admin.row("\U0001F4D6 Menu")


admins_id = [""]
waiting_feedback_from = set()

@bot.message_handler(content_types = ["text"])
def handle_text(message):
    
    try:
        
        # add user block
        
        all_users = read_users("users.txt")
        write_user(message, "users.txt", all_users)
        
        # start and feedback block
        
        if message.from_user.id in waiting_feedback_from:
            waiting_feedback_from.remove(message.from_user.id)
            feedback_sender(message)
            bot.send_message(message.from_user.id, "Your feedback has been sent to the developers. Thank you! \U0001F44D", reply_markup = keyboard_main, parse_mode = 'HTML') 
        
        elif message.text == "\U0001F4D3 Feedback" or message.text == "/feedback":
            waiting_feedback_from.add(message.from_user.id)
            bot.send_message(message.from_user.id, "Send me your feedback with the next message \U0001F603", reply_markup = keyboard_main, parse_mode = 'HTML')        
        
        elif message.text == "/start":
            bot.send_message(message.from_user.id, '\U0001F44B Hello. I can show ranking tables for BCI students for calculus and discrete math. Info is updated every minute.', reply_markup = keyboard_main, parse_mode = 'HTML')
        
        # admin block
        
        elif message.text == "/admin_panel":
            if message.from_user.id in admins_id:
                bot.send_message(message.from_user.id, "\U0001F607 Hello, my lovely admin", reply_markup = keyboard_admin, parse_mode = 'HTML')
            else:
                bot.send_message(message.from_user.id, "You are not admin", reply_markup = keyboard_main, parse_mode = 'HTML')
        
        elif message.text == "Users":
            if message.from_user.id in admins_id:
                send_users(message.from_user.id)
            else:
                bot.send_message(message.from_user.id, "You are not admin", reply_markup = keyboard_main, parse_mode = 'HTML')
        
        elif message.text == "Updates":
            if message.from_user.id in admins_id:
                send_updates(message.from_user.id)
            else:
                bot.send_message(message.from_user.id, "You are not admin", reply_markup = keyboard_main, parse_mode = 'HTML')
        
        # main messages
        
        elif message.text == "\U0001F4D8 Calculus":
            bot.send_message(message.from_user.id, '\U0001F537 Calculus ranking', reply_markup = keyboard_calculus, parse_mode = 'HTML')
            
        elif message.text == '\U0001F4D9 Discrete math':
            bot.send_message(message.from_user.id, '\U0001F536 Discrete math ranking', reply_markup = keyboard_discrete, parse_mode = 'HTML')
            
        elif message.text == "\U0001F4D6 Menu":
            bot.send_message(message.from_user.id, '\U0001F4D6 Main menu', reply_markup = keyboard_main, parse_mode = 'HTML')
        
        # discrete math
        
        elif message.text.split()[0] == "\U0001F536":  # discrete
            
            if message.text == "\U0001F536 \U0001F4F6":  # rating
                rating(message.from_user.id, 'discrete', False, False, '', '')
                
            elif message.text == "\U0001F536 \U0001F194":  # id
                bot.send_message(message.from_user.id, '\U0001F536 Discrete math ID', reply_markup = keyboard_inline_groups, parse_mode = 'HTML')
                
            elif message.text == "\U0001F536 181":
                rating(message.from_user.id, 'discrete', False, True, '', '181')
                
            elif message.text == '\U0001F536 182':
                rating(message.from_user.id, 'discrete', False, True, '', '182')
        
        # calculus
        
        elif message.text.split()[0] == "\U0001F537":  # calculus
            
            if message.text == "\U0001F537 \U0001F4F6":  # rating
                rating(message.from_user.id, 'calculus', False, False, '', '')
                
            elif message.text == "\U0001F537 \U0001F194":  # id
                bot.send_message(message.from_user.id, '\U0001F537 Calculus ID', reply_markup = keyboard_inline_groups, parse_mode = 'HTML')
                
            elif message.text == "\U0001F537 181":
                rating(message.from_user.id, 'calculus', False, True, '', '181')
                
            elif message.text == '\U0001F537 182':
                rating(message.from_user.id, 'calculus', False, True, '', '182')
        
        # other messages
        
        else:
            bot.send_message(message.from_user.id, '<b>\U0001F537 I can only show ratings \U0001F536</b>', reply_markup = keyboard_main, parse_mode = 'HTML')
    
    except Exception as e:
                        
        excepter(message)


@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call): 
    
    try:
        
        if call.data == "181":
            bot.edit_message_reply_markup(call.from_user.id, message_id = call.message.message_id, reply_markup = keyboard_inline_names_181)
        
        elif call.data == "182":
            bot.edit_message_reply_markup(call.from_user.id, message_id = call.message.message_id, reply_markup = keyboard_inline_names_182)
        
        elif call.message.text == '\U0001F536 Discrete math ID' and call.data in names:
            rating(call.from_user.id, 'discrete', True, False, call.data, '')
            
        elif call.message.text == '\U0001F537 Calculus ID' and call.data in names:
            rating(call.from_user.id, 'calculus', True, False, call.data, '')
            
        else:
            bot.send_message(call.from_user.id, "Didn't find your in the list of students", reply_markup = keyboard_main)
    
    except Exception as e:
                        
        excepter(call)
    
    bot.answer_callback_query(call.id)


threading.Thread(target=rating_update_discrete).start()
threading.Thread(target=rating_update_calculus).start()
bot.polling(none_stop=True, interval=0)

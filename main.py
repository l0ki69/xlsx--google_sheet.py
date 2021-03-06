from pprint import pprint
import apiclient
import httplib2
import xlrd
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import gspread

def Univ_file(file_name):
    list_univ = []
    file = open(file_name)
    for line in file:
        list_univ.append(line.replace('\n', '').split('|'))
        # print(list_univ)
    file.close()
    # print(list_univ)
    return list_univ


def Sort_Dict_Name(list_inf):
    buf_lst = []  # sorted name
    Buf_Lst = []  # Buf_list
    for lst in list_inf:
        buf_lst.append(lst[0])
    buf_lst.sort()
    for i in buf_lst:
        for j in list_inf:
            if i == j[0]:
                break
        Buf_Lst.append(list_inf.pop(list_inf.index(j)))
    # print(Buf_Lst)
    return (Buf_Lst)




# Начало обработки таблицы excel

def Work_Excel(file_name):
    excel_data_file = xlrd.open_workbook(file_name)
    sheet = excel_data_file.sheet_by_index(0)

    list_info_stud = []

    num_rows = sheet.nrows
    num_col = sheet.ncols

    dict_univ = {}
    univ = ""

    list_univ = Univ_file('University.txt')

    for i in range(len(list_univ)):
        dict_univ[list_univ[i][0]] = []

    for i in range(1, num_rows):
        list_info_stud.append((str(sheet.cell(i, 2)).replace('text:', '').replace("'", "")))
        list_info_stud.append((str(sheet.cell(i, 6)).replace('text:', '').replace("'", "")))
        list_info_stud.append((str(sheet.cell(i, 7)).replace('text:', '').replace("'", "")))
        univ = str(sheet.cell(i, 5)).replace('text:', '').replace("'", "").rstrip()
        buf_list = list_info_stud[:]
        key = ""

        for i in range(len(list_univ)):
            for j in range(len(list_univ[i])):
                if univ.lower().replace(' ','') == list_univ[i][j].lower().replace(' ',''):
                    key = list_univ[i][0]
                    break
            if (key != ""):
                break

        if (key == ""):
            print(univ," ",buf_list)
            print("\033[31m {}" .format("University not found") )
            print("\033[37m {}" .format("") )
            return

        dict_univ[key].append(buf_list)
        list_info_stud.clear()

    for key in dict_univ.keys(): #sorted
        dict_univ[key] = Sort_Dict_Name(dict_univ[key])

    # print("EXCELLENT")
    return(dict_univ)


# Конец обработки excel

def Print_dict(d):
    for i in d.keys():
        print(i, " : ", d[i])

Dict_info = {}

Dict_info = Work_Excel(file_name = './vygruzka_17_10.xlsx')

#Print_dict(Dict_info)

#print(len(Dict_info['РТУ МИРЭА']),Dict_info['РТУ МИРЭА'])




# Начало работы с google sheets

def google_sheet_work(Name_Sheets):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(Name_Sheets).sheet1
    data = sheet.get_all_records()

    key = 'Бгуор'
    print(Dict_info[key])
    print(len(Dict_info[key]))
    for i in range(0, len(Dict_info[key])):
        # row = [i - 1 , "Титаренко Алексей Андреевич" , "https://vk.com/l0ki69" , "https://sun9-46.userapi.com/c855232/v855232754/1eee16/DgBkCyRvxjs.jpg"]
        row = [i + 1]
        row.extend(Dict_info[key][i])

        sheet.insert_row(row, i + 2)
        row.clear()
    #pprint(data)

# Конец работы с google sheets

google_sheet_work("SheetsTest")
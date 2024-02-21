from selenium.webdriver.common.by import By
from Database import *


def line_separate(string):
    tmp = string[0]
    separate_char = (".", ":", ",", ";")
    for char_index in range(1, len(string)-1):
        if string[char_index] == " " and string[char_index-1] in separate_char:
            continue
        if string[char_index] in separate_char and string[char_index+1] == " ":
            tmp += string[char_index] + "\n"
        else:
            tmp += string[char_index]
    return tmp


def find_links(browser):
    elems = browser.find_elements(By.CSS_SELECTOR, ".Info_info__twBU2 [href]")
    raw_links = [elem.get_attribute('href') for elem in elems]
    elems2 = browser.find_elements(By.TAG_NAME, "h2")
    names = [name.text for name in elems2]
    links = []
    for link in raw_links:
        if link[-8:] == 'reviews/':
            links.append(link[:-8])
    return links, names


def info_separate(info):
    training = 'None'
    support = 'None'
    typical = 'None'
    platform = 'None'
    for ele in info:
        tmp = ele.split(',')
        if tmp[0] == 'Typical customers':
            typical = ','.join(tmp[1:])
        elif tmp[0] == 'Platforms supported':
            platform = ','.join(tmp[1:])
        elif tmp[0] == 'Support options':
            support = ','.join(tmp[1:])
        elif tmp[0] == 'Training options':
            training = ','.join(tmp[1:])
    return [typical, platform, support, training]


def change_list_of_tuple_to_dictionary(list_tuple):
    dic = {}
    for tuple in list_tuple:
        key = tuple[0]
        dic[key] = [x for x in tuple[1:]]
    return dic


def get_service_from_db():
    info = change_list_of_tuple_to_dictionary(DatabaseConnector("info").select())
    platform = change_list_of_tuple_to_dictionary(DatabaseConnector("platform").select())
    review = change_list_of_tuple_to_dictionary(DatabaseConnector("review").select())
    service = change_list_of_tuple_to_dictionary(DatabaseConnector("service").select())
    support_options = change_list_of_tuple_to_dictionary(DatabaseConnector("support_options").select())
    training_option = change_list_of_tuple_to_dictionary(DatabaseConnector("training_option").select())
    typical_customer = change_list_of_tuple_to_dictionary(DatabaseConnector("typical_customer").select())
    rs = []
    for key in service.keys():
        cloud_service = service[key]
        info_index = info[cloud_service[2]]
        service_info = [typical_customer[info_index[0]], platform[info_index[1]], support_options[info_index[2]], training_option[info_index[3]]]
        reviews = review[cloud_service[1]]
        rs.append(CloudService(key, cloud_service[0], service_info, cloud_service[3], reviews, cloud_service[4],
                               cloud_service[5].strftime("%Y-%m-%d %H:%M:%S"), cloud_service[6]))
    return rs, platform, support_options, training_option, typical_customer


def insert_info_ele(dic, database):
    table = DatabaseConnector(database, 'qwedfgbnm123')
    for key in dic.keys():
        try:
            table.insert((dic[key], key))
        except:
            continue
    table.commit()


def insert_info_service_review(dic, database):
    table = DatabaseConnector(database, 'qwedfgbnm123')
    for key in dic.keys():
        tmp = dic[key]
        tmp.insert(0, key)
        tmp = tuple(tmp)
        try:
            table.insert(tmp)
        except:
            continue
    table.commit()



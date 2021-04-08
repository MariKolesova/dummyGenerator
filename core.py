from urllib.request import urlopen
import re
import random
import sys
import math
from urllib.parse import quote
from pytils import translit
from urllib.error import URLError, HTTPError


def generation(count_female, count_male, middle_age, html_flag, file_name):
    with open(file_name, 'w+') as file:
        if html_flag:
            file.write('<html>\n<body>\n<H1>Информация о людях\n</H1>\n')
            place = file.tell()
        else:
            place = 0
        if count_female != 0:
            position = person_generation(count_female, female_name_list()[0:-5], surname_generation(),
                                         female_patronymic_generation(),
                                         middle_age, city_generation()[0:-9], "female", html_flag, file, place)
            if position != place:
                place = position
        if count_male != 0:
            person_generation(count_male, male_name_list(), surname_generation(), male_patronymic_generation(),
                              middle_age, city_generation()[0:-9], "male", html_flag, file, place)
        if html_flag:
            file.write('</body>\n</html>')


def person_generation(count, names, surnames, patrs, years, cities, gender, html, file, place):
    for j in range(count):
        name = names[random.randint(0, len(names) - 1)]
        if gender == "female":
            surname = surnames[random.randint(0, len(surnames) - 1)] + "a"
        else:
            surname = surnames[random.randint(0, len(surnames) - 1)]
        patronymic, mail = patrs[random.randint(0, len(patrs) - 1)], mail_generation(name, surname)
        if html == 0:
            print(surname, name, patronymic, "возраст:", math.trunc(math.fabs(random.gauss(years, 10))), "телефон:",
                  89000000000 + random.randint(0, 999999999), "почта:", mail, "город:",
                  cities[random.randint(0, len(cities) - 1)])
        else:
            file.seek(place, 0)
            file.write('<p>\n{} {} {}, {} {}, {} {}, {} {}, {} {}\n</p>\n'.format(surname, name,
                       patronymic, "возраст:", math.trunc(math.fabs(random.gauss(years, 10))), "телефон:", 89000000000 +
                       random.randint(0, 999999999), "почта:", mail, "город:",
                       cities[random.randint(0, len(cities) - 1)]))
            place = file.tell()
    return place


def get_internet_page(page_name, site_flag):
    try:
        if site_flag == "wikipedia":
            with urlopen('https://ru.wikipedia.org/wiki/' + quote(page_name)) as page:
                return page.read().decode('utf-8', errors='ignore')
        elif site_flag == "wiktionary":
            with urlopen('https://ru.wiktionary.org/wiki/' + quote(page_name)) as page:
                return page.read().decode('utf-8', errors='ignore')
        else:
            with urlopen(page_name) as page:
                return page.read().decode('utf-8', errors='ignore')
    except (URLError, HTTPError):
        sys.exit("Нет подключения к интернету")


def male_name_list():
    result_male_list = list()
    male_page = get_internet_page('Категория:Русские_мужские_имена', "wikipedia")
    pattern1 = re.compile(r'a href=(.+) title="(\w*) .+">\2')
    list1 = pattern1.findall(male_page)
    for tuples in list1:
        result_male_list.append(tuples[1])
    result_male_list = result_male_list[0:11]
    pattern2 = re.compile(r'a href=(.+) title="(\w*)">\2')
    list2 = pattern2.findall(male_page)
    for tuples in list2:
        result_male_list.append(tuples[1])
    return result_male_list


def female_name_list():
    result_female_list = list()
    female_page = get_internet_page('Категория:Русские_женские_имена', "wikipedia")
    list1 = re.findall(r'a href=(.+) title="(\w*)">\2', female_page)
    for tuples in list1:
        result_female_list.append(tuples[1])
    list2 = re.findall(r'a href=(.+) title="(\w*) .+">\2', female_page)
    for tuples in list2:
        result_female_list.append(tuples[1])
    return result_female_list


def male_patronymic_generation():
    result_list = list()
    patr_page = get_internet_page('Категория:Мужские_отчества/ru', "wiktionary")
    pattern = re.compile(r'a href=(.+) title="(\w*)">\2')
    alist = re.findall(pattern, patr_page)
    for tuples in alist:
        result_list.append(tuples[1])
    return result_list


def female_patronymic_generation():
    result_list = list()
    patr_page = get_internet_page('Категория:Женские_отчества/ru', "wiktionary")
    pattern = re.compile(r'a href=(.+) title="(\w*)">\2')
    alist = re.findall(pattern, patr_page)
    for tuples in alist:
        result_list.append(tuples[1])
    return result_list


def surname_generation():
    sur_page = get_internet_page('http://imja.name/familii/pyatsot-chastykh-familij.shtml', "imja.name")
    pattern = re.compile(r'<td class="topin1">(\w*)')
    result = re.findall(pattern, sur_page)
    return result


def city_generation():
    result_list = []
    pattern1 = re.compile(r'a href=(.+) title="(\w*)">\2')
    pattern2 = re.compile(r'a href=(.+) title="(\w*) (\w*)">\2')
    pattern3 = re.compile(r'a href=(.+) title="(\w*)-(\w*)-(\w*)">\2')
    city_page = get_internet_page('Список_городов_России', "wikipedia")
    alist1 = re.findall(pattern1, city_page)
    alist2 = re.findall(pattern2, city_page)
    alist3 = re.findall(pattern3, city_page)
    for tuples in alist1:
        if tuples[1][len(tuples[1]) - 2:] != "ая":
            if tuples[1][len(tuples[1]) - 2:] != "ия":
                if tuples[1][len(tuples[1]) - 4:] != "стан":
                    if not (tuples[1].isdigit()):
                        result_list.append(tuples[1])
    for tuples in alist2:
        if tuples[2] != "край" and tuples[2] != "область" and tuples[2] != "век":
            if not(tuples[1].isdigit()):
                result_list.append(tuples[1] + ' ' + tuples[2])
    for tuples in alist3:
        result_list.append(tuples[1] + '-' + tuples[2] + '-' + tuples[3])
    return list(set(result_list))


def mail_generation(name, surname):
    transl_name = translit.translify(name)
    transl_surname = translit.translify(surname)
    mail = transl_name + transl_surname + "@mail.ru"
    return mail

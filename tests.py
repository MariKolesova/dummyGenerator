import unittest
from unittest.mock import patch
import os
from core import *


class TestGeneratorMethods(unittest.TestCase):
    def test_mail_generation(self):
        self.assertEqual(mail_generation('Василиса', 'Трофимова'), "VasilisaTrofimova@mail.ru")

    def test_person_generation(self):
        female_names = ['Карина', 'Наталья', 'Вероника']
        surnames = ['Петров', 'Иванов']
        female_patronymic = ['Петровна', 'Владимировна']
        city = ['Москва', 'Новосибирск', 'Казань', 'Томск']
        with open("file.html", "w+") as file:
            file.write('<html>\n<body>\n<H1>Информация о людях\n</H1>\n')
            place = file.tell()
            person_generation(3, female_names, surnames, female_patronymic, 45, city, "female",
                              1, file, place)
        with open("file.html", 'r') as file:
            text = file.read()
            alist = re.findall(r'<p>', text)
        self.assertEqual(len(alist), 3)
        os.remove("file.html")

    def test_male_name_list(self):
        with patch('core.get_internet_page', return_value="<li><a href=\"/wiki/%D0%92%D1%81%D0%B5%D0%B2%D0%BE%D0%"
                   "BB%D0%BE%D0%B4\" title=\"Всеволод\">Всеволод</a></li>"):
            self.assertEqual(male_name_list(), ['Всеволод'])

    def test_city_generation(self):
        with patch('core.get_internet_page', return_value="<td align=\"left\"><a href=\"/wiki/%D0%A0%D0%BE%D1%81%D1%82%"
                   "D0%BE%D0%B2-%D0%BD%D0%B0-%D0%94%D0%BE%D0%BD%D1%83\" title=\"Ростов-на-Дону\">Ростов-на-Дону</a>"
                   "</td>"):
            self.assertEqual(city_generation(), ['Ростов-на-Дону'])

    def test_female_name_list(self):
        with patch('core.get_internet_page', return_value="<a href=\"/wiki/%D0%92%D0%B5%D1%80%D0%B0_(%D0%B8%D0%BC%"
                   "D1%8F)\" title=\"Вера (имя)\">Вера (имя)</a><a href=\"/wiki"
                   "/%D0%90%D0%BA%D1%83%D0%BB%D0%B8%D0%BD%D0%B0\" title="
                   "\"Акулина\">Акулина</a>"):
            self.assertEqual(female_name_list(), ['Акулина', 'Вера'])

    def test_female_patronymic_generation(self):
        with patch('core.get_internet_page', return_value="<a href=\"/wiki/%D0%9C%D0%B0%D1%80%D0%BA%D0%BE"
                   "%D0%B2%D0%BD%D0%B0\" title=\"Марковна\">Марковна</a>"):
            self.assertEqual(female_patronymic_generation(), ['Марковна'])

    def test_male_patronymic_generation(self):
        with patch('core.get_internet_page', return_value="<li><a href=\"/wiki/%D0%90%D0%B4%D0%B0%D0%BC%D0%BE%D0%B"
                   "2%D0%B8%D1%87\" title=\"Адамович\">Адамович</a></li>"):
            self.assertEqual(male_patronymic_generation(), ['Адамович'])

    def test_surname_generation(self):
        with patch('core.get_internet_page', return_value="<tr><td class=\"topin\">35</td><td class=\"topin1\">Фр"
                   "олов</td><td class=\"topin\">0,2235</td></tr><tr><td class"
                   "=\"topin\">36</td><td class=\"topin1\">Александров</td><t"
                   "d class=\"topin\">0,2234</td></tr>"):
            self.assertEqual(surname_generation(), ['Фролов', 'Александров'])

    def test_generation(self):
        generation(0, 0, 0, 1, "file.html")
        self.assertEqual(os.path.exists("file.html"), 1)

    def test_city_generation2(self):
        with patch('core.get_internet_page', return_value="<td align=\"left\"><a href=\"/wiki/%D0%92%D0%B5%D1%80%D1%85%"
                   "D0%BD%D0%B8%D0%B9_%D0%A2%D0%B0%D0%B3%D0%B8%D0%BB\" title=\"Верхний Тагил\">Верхний Тагил</a></td>"):
            self.assertEqual(city_generation(), ['Верхний Тагил'])


if __name__ == '__main__':
    unittest.main()

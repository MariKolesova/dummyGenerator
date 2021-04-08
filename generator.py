from core import *
import argparse


def get_args():
    parser = argparse.ArgumentParser(prog='generator', description='''Программа генерирует данные о человеке: ФИО,
                                     возраст, город, номер телефона''')
    parser.add_argument('-f', type=int, default=0, help="Количество женщин")
    parser.add_argument('-m', type=int, default=0, help="Количество мужчин")
    parser.add_argument('-a', type=int, default=0, help="Средний возраст")
    parser.add_argument('-html', action='store_const', const=True, default=False, help="Флаг записи в .html файл")
    parser.add_argument('-n', default='file.html', help="Имя выходного файла")
    args = parser.parse_args()
    if len(sys.argv) == 1:
        sys.exit("Запуск без параметров невозможен")
    return args


def main():
    args = get_args()
    count_female = args.f
    count_male = args.m
    if args.html:
        html_flag = 1
    else:
        html_flag = 0
    if count_female == 0 and count_male == 0:
        sys.exit("Вы не ввели количество человек")
    generation(count_female, count_male, args.a, html_flag, args.n)


if __name__ == '__main__':
    main()

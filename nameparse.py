import re
import sqlite3
from math import floor


class UneconDataset():

    def __init__(self):
        # подключение к основной БД
        self.conn = sqlite3.connect('db.sqlite3')
        self.conn.row_factory = sqlite3.Row

    @staticmethod
    def fname(s):
        name = re.findall(r'[А-Яа-я-]+ [A-ZА-Я]\.?[A-ZА-Я]\.?', s)
        return name

    @staticmethod
    def find_ltype(s):
        if 'лекция' in s.lower():
            return 'Лекция'
        elif 'практика' in s.lower():
            return 'Практика'
        else:
            return ' '

    @staticmethod
    def jaro_distance(s1, s2):
        #  Алгоритм сравнения двух строк.
        #  https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance

        ls1, ls2 = len(s1), len(s2)
        max_distance = floor(max(ls1, ls2) / 2) - 1

        m = [[0 for i in range(ls1)] for k in range(ls2)]
        for i in range(ls2):
            for k in range(ls1):
                if s2[i] == s1[k] and abs(i - k) <= max_distance:
                    m[i][k] = 1
        #  совпадающие символы
        mc = sum(sum(_) for _ in m)
        if mc == 0:
            return 0
        #  сумма главной диагонали матрицы
        ds = 0
        for i in range(min(ls1, ls2)):
            ds += m[i][i]
        #  кол-во перестановок
        t = (mc - ds) / 2

        jaro = ((mc / ls1) + (mc / ls2) + ((mc - t) / mc)) / 3
        return jaro

    @staticmethod
    def make_short_name(name):
        '''Функция форматирует
        полное ФИО в формат
        Фамилия И.О.
        :param name: полное ФИО str
        :return: Фамилия И.О. str
        '''
        parts = name.split(' ')
        short = '{0} {1}.{2}.'.format(
            parts[0],
            parts[1][0],
            parts[2][0])
        return short

    def make_teacher_list(self):
        '''
        Функция подключается к основной БД
        и возвращает список преподавателей
        для сравнения в формате Фамилия И.О.
        :return: ('Фамилия И.О.', ... )
        '''
        with self.conn:
            cur = self.conn.cursor()
            cur.execute('SELECT id, tName FROM main_teacher ORDER BY tName')
            p = cur.fetchall()

        self.etalon = {self.make_short_name(row['tName']): row['id'] for row in p}

    def find_best_match(self, lesson):
        lesson_teachers = []
        name = self.fname(lesson[4])
        # отладочные принты
        # print(lesson[4])
        # print('NAME {}'.format(name))

        for n in name:
            best_jaro = 0
            best_match = None
            # попытка ускорить алгоритм. Unsafe!
            etal = list(filter(lambda x: x[0] == n[0], self.etalon.keys()))

            for prep in etal:
                j = self.jaro_distance(n, prep)
                # print('Jaro score for {} % {}: {}'.format(n,prep,str(j)))
                if j > best_jaro:
                    best_jaro = j
                    best_match = prep
            #  В случае, если коэффициент менее 1.0, совпадений нет.
            #  Такое значение допускает до 2-3 ошибок в слове
            #  и все равно обеспечивает уверенное распознавание.
            if best_jaro >= 1.0:
                lesson_teachers.append(best_match)
            else:
                lesson_teachers.append((None, n))

        return lesson_teachers

    def export_dataset(self, ds, fn, as_file=False):
        import json
        from datetime import date

        e = {
            'dateParsed': date.today().strftime('%Y-%m-%d'),
            'datePublished': fn['date'],
            'filename': fn['local'],
            'scheduleType': fn['type'],
            'data': [],
            'noMatch': []
        }
        for l in ds:
            prep = self.find_best_match(l)
            lesson_type = self.find_ltype(l[4])

            if len(lesson_type) > 1:
                lesson_name = re.sub(lesson_type, '', l[4])
            else:
                lesson_name = l[4]

            for p in prep:
                if isinstance(p, tuple):
                    # если преподаватель не распознан -
                    # добавить в категорию noMatch
                    e['noMatch'].append({
                        'wday': l[0],
                        'wtype': l[1],
                        'time': l[2],
                        'aud': l[3],
                        'group': l[5],
                        'name': lesson_name,
                        'ltype': lesson_type,
                        'failedName': p[1]
                    })
                    continue

                e['data'].append({
                    'wday': l[0],
                    'wtype': l[1],
                    'time': l[2],
                    'aud': l[3],
                    'group': l[5],
                    'name': re.sub(p, '', lesson_name),
                    'ltype': lesson_type,
                    'tid': self.etalon[p]
                })
        print('Датасет для {} обработан.'.format(fn['local']))
        ds_path = 'datasets/' + fn['local'].split('/')[1][:-5] + '.json'

        if as_file is True:
            with open(ds_path, mode='w', encoding='utf-8') as f:
                json.dump(e, f)
            return
        else:
            return e


if __name__ == '__main__':
    uds = UneconDataset()
    uds.make_teacher_list()

    # подключение к БД, хранящей данные
    # о скачанных файлах Excel.w
    c2 = sqlite3.connect('downloaded.db')
    c2.row_factory = sqlite3.Row
    cur2 = c2.cursor()
    cur2.execute(
        '''SELECT local, date, type
        FROM files WHERE local
        LIKE "%.xlsx" AND form="Очная форма"
        AND parsed=0'''
    )
    files_to_parse = cur2.fetchall()

    for fn in files_to_parse:
        filename = fn['local']
        xlsx = unmerger.workbook_unmerge(filename)
        ds = excel_parser.parse_xlsx(xlsx)
        if ds is None:
            print('Файл {} не был корректно обработан парсером.'.format(xlsx))
            continue

        uds.export_dataset(ds, fn)
        cur3 = c2.cursor()
        cur3.execute('UPDATE files SET parsed=1 WHERE local=?', (filename,))
        c2.commit()
    c2.close()

    '''
    # проверка
    stored = open(filename+'.json','r')
    import json
    data = json.load(stored)
    stored.close()

    for l in data['data']: print(str(l)+'\n')
    print(str(data['noMatch']))
    '''

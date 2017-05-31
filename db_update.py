import json
import sqlite3
from datetime import datetime as dt
from datetime import timedelta as td
from os import listdir, remove


class UneconDBUpdate():

    def __init__(self):
        # подключение к основной БД
        self.conn = sqlite3.connect('db.sqlite3')
        self.conn.row_factory = sqlite3.Row

    def read_json(self, filename):
        # print(filename)
        with open('datasets/' + filename, 'w+', encoding='utf-8') as f:
            self.filedata = json.load(f)

    def read_dict(self, dictionary):
        self.filedata = dictionary
        # print(self.filedata)

    def get_file_info(self):
        self.pub_date = dt.strptime(
            self.filedata['datePublished'],
            '%d.%m.%Y'
        )
        if self.pub_date.month in range(1, 7):
            start_date = dt(self.pub_date.year, 2, 1)
            if start_date < self.pub_date:
                self.start_date = self.pub_date
            else:
                self.start_date = start_date + td(days=1)
            self.stop_date = dt(self.pub_date.year, 6, 15)
        else:
            self.start_date = dt(self.pub_date.year, 9, 1)
            if start_date < self.pub_date:
                self.start_date = self.pub_date
            else:
                self.start_date = start_date + td(days=1)
            self.stop_date = dt(self.pub_date.year, 12, 31)

        self.sch_type = self.filedata['scheduleType']
        # print('pub_date: {}, start_date: {}, stop_date: {}'.format(self.pub_date, self.start_date, self.stop_date))

    @staticmethod
    def next_weekday(d, wday, wtype):
        days_ahead = wday - d.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        d += td(days=days_ahead)
        if wtype != (d.isocalendar()[1] % 2):
            d += td(days=7)
        return d

    def update_lesson(self, lesson):
        wday = lesson['wday']
        wtype = lesson['wtype']
        comment = ' '
        if lesson['aud'] is None:
            lesson['aud'] = 'неизвестно'
        basedate = self.next_weekday(self.start_date, wday, wtype)
        iterdate = basedate

        with self.conn:
            cur = self.conn.cursor()
            while iterdate <= self.stop_date:
                cur.execute('''DELETE FROM main_lesson
                    WHERE lDate>=:startDate
                    AND lDate<=:endDate
                    AND lTeacher_id=:tid
                    AND lTime=:ltime
                    AND lDate=:iterdate''',
                            {'startDate': self.start_date.strftime('%Y-%m-%d'),
                             'endDate': self.stop_date.strftime('%Y-%m-%d'),
                             'tid': lesson['tid'],
                             'ltime': lesson['time'],
                             'iterdate': iterdate.strftime('%Y-%m-%d')
                             }
                            )
                iterdate += td(days=14)

        iterdate = basedate

        with self.conn:
            cur = self.conn.cursor()
            while iterdate <= self.stop_date:
                cur.execute(
                    '''INSERT INTO main_lesson(lDate,lName,lTime,lGroup,lTeacher_id,lAud,lComment) VALUES(?,?,?,?,?,?,?)''',
                    (iterdate.strftime('%Y-%m-%d'),
                     lesson['name'],
                     lesson['time'],
                     lesson['group'],
                     lesson['tid'],
                     lesson['aud'],
                     comment)
                )
                iterdate += td(days=14)

    def process_file(self, filename):
        self.read_json(filename)
        self.get_file_info()

        for lesson in self.filedata['data']:
            self.update_lesson(lesson)

    def process_dict(self, dictionary):
        self.read_dict(dictionary)
        self.get_file_info()

        for lesson in self.filedata['data']:
            try:
                self.update_lesson(lesson)
            except sqlite3.Error as e:
                print('Ошибка при внесении записей из файла {}! {}'.format(
                    self.filedata['filename'], e))
                continue
        print('Данные датасета для файла {} внесены в БД.\n'.format(self.filedata['filename']))


if __name__ == '__main__':
    files = listdir('datasets/')
    for f in files:
        dbu = UneconDBUpdate()
        dbu.process_file(f)
        del(dbu)
        remove('datasets/' + f)

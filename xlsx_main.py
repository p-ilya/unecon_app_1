import sqlite3

import nameparse
import unmerger
import excel_parser
import db_update

uds = nameparse.UneconDataset()
uds.make_teacher_list()

# подключение к БД, хранящей данные
# о скачанных файлах Excel.
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
    if xlsx is None:
        continue
    ds = excel_parser.parse_xlsx(xlsx)
    if ds is None:
        print('Файл {} не был корректно обработан парсером.'.format(xlsx))
        continue

    sorted_ds = uds.export_dataset(ds, fn, as_file=False)

    # внесение записей в БД
    dbu = db_update.UneconDBUpdate()
    dbu.process_dict(sorted_ds)
    del(dbu)

    # файл помечается как обработанный
    cur3 = c2.cursor()
    cur3.execute('UPDATE files SET parsed=1 WHERE local=?', (filename,))
    c2.commit()
c2.close()

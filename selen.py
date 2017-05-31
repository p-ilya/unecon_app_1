from urllib.request import urlretrieve
import time
import re
import sqlite3

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException



# noinspection PyByteLiteral
class Unecon_Downloader():
    # абсолютный путь к драйверу
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Chrome()
    collected_links = []
    con = sqlite3.connect('downloaded.db')

    def load_schedule_page(self):
        url = 'http://unecon.ru/schedule'
        self.driver.get(url)

        select = Select(self.driver.find_element_by_id(
            'edit-term-node-tid-depth-hierarchical-select-selects-0'
        ))
        select.select_by_value('label_0')

        submit_bttn = self.driver.find_element_by_id('edit-submit-schedule-view')
        time.sleep(5)
        submit_bttn.click()
        time.sleep(5)

    @staticmethod
    def parse_xlsx_info(info):
        parts = info.rsplit(' - ')

        form, fac, typ, kurs = ('?','?','?','?')
        for p in parts:
            if re.search(r'\w*форма$', p): form = p
            elif re.search(r'\w*[Фф]акультет\w*', p): fac = p
            elif re.search(r'\w*расписание', p): typ = p
            elif re.search(r'\w*курс', p): kurs = p
        return form, fac, typ, kurs

    def retrieve_links(self):
        #stable '//*[@id="content"]/div[2]/div[2]/table/tbody/tr/td[1]/div/ul/li/a'
        links = []
        rows = self.driver.find_elements_by_xpath(
            '//*[@id="content"]/div[2]/div[2]/table/tbody/tr'
            )
        
        for r in rows:
            link = r.find_element_by_xpath('.//td[1]/div/ul/li/a')
            link_text = link.get_attribute('href')
            info = r.find_element_by_xpath('.//td[2]').text
            form, fac, typ, kurs = self.parse_xlsx_info(info)
            upload_date = r.find_element_by_xpath('.//td[3]').text
            destination = 'files/'+link_text.rsplit('/', 1)[1]
            links.append({
                'link': link_text,
                'local': destination,
                'form': form,
                'faculty': fac,
                'sch_type': typ,
                'kurs': kurs,
                'upload': upload_date
                })

       
        return links

    def next_page(self):
        try:
            next_page_bttn = self.driver.find_element_by_xpath(
                '//*[@id="content"]/div[2]/div[3]/ul/li[last()]/a')
            next_page_bttn.click()
            time.sleep(5)
            return True
        
        except NoSuchElementException as e:
            # print('Cant flip to next page due to this:\n' + e.msg)
            return False

    def download_files(self):
        s = 0
        for l in self.collected_links:
            try:
                urlretrieve(l['link'], l['local'])
                with self.con as db:
                    db.row_factory = sqlite3.Row
                    cur = db.cursor()
                    cur.execute(
                        'INSERT INTO files (URL, local, date, faculty, type, form, course) VALUES (:link, :local, :upload, :faculty, :sch_type, :form, :kurs);',
                         l)
            except ValueError:
                print('This strange error again.')
            s += 1
        print('Downloaded {} files.'.format(s))

    def close_page(self):
        self.driver.close()

    def scenario(self):
        # загрузить страницу в нужном виде
        self.load_schedule_page()
        # получить ссылки с первой страницы
        for l in self.retrieve_links():
            self.collected_links.append(l)
        # перелистнуть на вторую стрницу
        self.next_page()

        # получаить ссылки с остальных страниц
        while True:
            a = self.next_page()
            if not a: break
            for l in self.retrieve_links():
                self.collected_links.append(l)

        print('Links total: {}'.format(len(self.collected_links)))
        for l in self.collected_links: print(str(l) + '\n\n')
        self.close_page()
        self.driver.quit()
        self.download_files()

if __name__ == '__main__':
    downloader = Unecon_Downloader()
    downloader.scenario()
    #downloader.load_schedule_page()
    #tds = downloader.retrieve_links()
    #downloader.driver.quit()

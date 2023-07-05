import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import urllib.request


class SleepingCrawling:
    def __init__(self):
        self.conn = sqlite3.connect('../database/seoul_db.db')
        self.cur = self.conn.cursor()

        self.driver = webdriver.Chrome()
        self.driver.get("https://www.google.com/search?q=%EC%8B%A0%EB%9D%BC%ED%98%B8%ED%85%94&newwindow=1&hl=ko&tbm=isch&source=hp&biw=1429&bih=969&ei=IOSkZPa8B5alhwO6-5WIBg&iflsig=AD69kcEAAAAAZKTyMD0qEm36vNmJDros0Z9cgztvG3Cc&ved=0ahUKEwj2zKzP0Pb_AhWW0mEKHbp9BWEQ4dUDCAc&uact=5&oq=%EC%8B%A0%EB%9D%BC%ED%98%B8%ED%85%94&gs_lcp=CgNpbWcQAzIICAAQgAQQsQMyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6CwgAEIAEELEDEIMBOggIABCxAxCDAToECAAQA1BxWJEKYIMLaARwAHgCgAGnAYgByguSAQMxLjmYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABAA&sclient=img")

        folder = "../img/lodges_img"
        datas = self.cur.execute("select id, 사업장명 from seoul_lodges where id > 409;")
        # input_box = self.driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
        for id, name in datas:
            input_box = self.driver.find_element(By.XPATH, '//*[@id="REsRA"]')
            input_box.clear()
            input_box.send_keys(name)
            input_box.send_keys(Keys.ENTER)
            time.sleep(0.5)
            try:
                self.driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[1]/a[1]').click()
                time.sleep(0.5)
                image_root = self.driver.find_element(By.CLASS_NAME, 'iPVvYb')
                image = image_root.get_attribute('src')
                time.sleep(0.5)
                urllib.request.urlretrieve(image, folder + f'/{id}.png')
            except:
                print(f"{id}, {name}")


        self.driver.close()


if __name__ == '__main__':
    SleepingCrawling()
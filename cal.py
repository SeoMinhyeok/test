import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException
import platform
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CollectLinks:

    def __init__(self):
        executable = ''
        if platform.system() == 'Linux':
            print('Detected OS : Linux')
            executable = '/home/at05/PycharmProjects/smh_restart/chromedriver/chromedriver_linux'
        elif platform.system() == 'Darwin':
            print('Detected OS : Mac')
            executable = './chromedriver/chromedriver_mac'
        else:
            assert False, 'Unknown OS Type'
        self.browser = webdriver.Chrome(executable)

    def get_scroll(self):
        pos = self.browser.execute_script('return window.pageYOffset')
        return pos

    def wait_and_click(self, xpath):
        try :
            w = WebDriverWait(self.browser, 15)
            elem = w.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            elem.click()

        except Exception as e:
            print('Click time out - {}'.format(xpath))
            print('Refreshing browser ...')
            self.browser.refresh()
            time.sleep(2)
            return self.wait_and_click(xpath)
        return elem

    def google(self, keyword, add_url = ""):

        self.browser.get("https://www.google.com/search?q={}&source=lnms&tbm=isch{}".format(keyword, add_url))
        time.sleep(1)
        print('Scrolling down')
        elem = self.browser.find_element_by_tag_name('body')
        for i in range(60):
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
        try :
            self.wait_and_click('//input[@id="smb"]')
            for i in range(60):
                elem.send_keys(Keys.PAGE_DOWN)
                time.sleep(0,2)
        except ElementNotVisibleException:
            pass

        photo_grid_boxes = self.browser.find_elements(By.XPATH, '//div[@class="rg_bx rg_di rg_el ivg-i"]')
        print('Scraping links')
        links = []
        for box in photo_grid_boxes:
            try:
                imgs = box.find_elements(By.TAG_NAME, 'img')
                for img in imgs:
                    src = img.get_attribute("src")
                    if src[0] != 'd':
                        links.append(src)
            except Exception as e:
                print('[Exception occurred while collecting links from google] {}'.format(e))
        print('Collect links done. Site: {}, Keyword: {}, Total: {}'.format('google', keyword, len(links)))
        self.browser.close()
        return set(links)

    def naver(self, keyword, add_url=""):
        self.browser.get(
            "https://search.naver.com/search.naver?where=image&sm=tab_jum&query={}{}".format(keyword, add_url))
        time.sleep(1)
        print('Scrolling down')
        elem = self.browser.find_element_by_tag_name("body")
        for i in range(60):
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
        try:
            self.wait_and_click('//a[@class="btn_more _more"]')
            for i in range(60):
                elem.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.2)
        except ElementNotVisibleException:
            pass
        photo_grid_boxes = self.browser.find_elements(By.XPATH, '//div[@class="photo_grid _box"]')
        print('Scraping links')
        links = []
        for box in photo_grid_boxes:
            try:
                imgs = box.find_elements(By.CLASS_NAME, '_img')
                for img in imgs:
                    src = img.get_attribute("src")
                    if src[0] != 'd':
                        links.append(src)
            except Exception as e:
                print('[Exception occurred while collecting links from naver] {}'.format(e))

        print('Collect links done. Site: {}, Keyword: {}, Total: {}'.format('naver', keyword, len(links)))
        self.browser.close()
        return set(links)

    def google_full(self, keyword, add_url=""):
        print('[Full Resolution Mode]')
        self.browser.get("https://www.google.co.kr/search?q={}&tbm=isch{}".format(keyword, add_url))
        time.sleep(1)
        elem = self.browser.find_element_by_tag_name("body")
        print('Scraping links')
        self.wait_and_click('//div[@data-ri="0"]')
        time.sleep(1)
        links = []
        # count = 1
        last_scroll = 0
        scroll_patience = 0
        while True:
            try:
                imgs = self.browser.find_elements(By.XPATH,
                                                  '//div[@class="irc_c i8187 immersive-container irc-rcd"]//img[@class="irc_mi"]')
                for img in imgs:
                    src = img.get_attribute('src')

                    if src not in links and src is not None:
                        links.append(src)
                        # print('%d: %s'%(count, src))
                        # count += 1

            except StaleElementReferenceException:
                print('[Expected Exception - StaleElementReferenceException]')
            except Exception as e:
                print('[Exception occurred while collecting links from google_full] {}'.format(e))

            scroll = self.get_scroll()
            if scroll == last_scroll:
                scroll_patience += 1
            else:
                scroll_patience = 0
                last_scroll = scroll

            if scroll_patience >= 30:
                break

            elem.send_keys(Keys.RIGHT)
        links = set(links)
        print('Collect links done. Site: {}, Keyword: {}, Total: {}'.format('google_full', keyword, len(links)))
        self.browser.close()
        return links

    def naver_full(self, keyword, add_url=""):

        print('[Full Resolution Mode]')

        self.browser.get(
            "https://search.naver.com/search.naver?where=image&sm=tab_jum&query={}{}".format(keyword, add_url))
        time.sleep(1)
        elem = self.browser.find_element_by_tag_name("body")
        print('Scraping links')
        self.wait_and_click('//div[@class="img_area _item"]')
        time.sleep(1)
        links = []
        # count = 1
        last_scroll = 0
        scroll_patience = 0
        while True:
            try:
                imgs = self.browser.find_elements(By.XPATH,
                                                  '//div[@class="image_viewer_wrap _sauImageViewer"]//img[@class="_image_source"]')

                for img in imgs:
                    src = img.get_attribute('src')

                    if src not in links and src is not None:
                        links.append(src)

            except StaleElementReferenceException:
                print('[Expected Exception - StaleElementReferenceException]')
            except Exception as e:
                print('[Exception occurred while collecting links from naver_full] {}'.format(e))

            scroll = self.get_scroll()
            if scroll == last_scroll:
                scroll_patience += 1
            else:
                scroll_patience = 0
                last_scroll = scroll
            if scroll_patience >= 30:
                break
            elem.send_keys(Keys.RIGHT)
        links = set(links)
        print('Collect links done. Site: {}, Keyword: {}, Total: {}'.format('naver_full', keyword, len(links)))
        self.browser.close()
        return links


if __name__ == '__main__':
    collect = CollectLinks()
    links = collect.google_full('Dog')
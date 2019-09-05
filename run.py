import pickle

from constants import collab_url, cookies_filepath, end_flag
from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver', options=chrome_options)

# load page
wd.get(collab_url)

# add cookies if exists
if Path(cookies_filepath).exists():
    for cookie in pickle.load(open(cookies_filepath, "rb")):
        # 'expiry' cookie is causing problem after Chrome 74
        # https://github.com/jimmy927/requestium/commit/596db69d18926981df23988e96ca33c361badb40
        cookie.pop('expiry', None)
        wd.add_cookie(cookie)
else:
    print('start auth.py first !')

# reload page, expand cells, and start all cells
wd.get(collab_url)
sleep(10)
ActionChains(wd).key_down(Keys.CONTROL).send_keys('[').perform()
sleep(3)
ActionChains(wd).key_down(Keys.CONTROL).key_down(Keys.F9).perform()
sleep(10)

# wait for the last cell to execute
while True:
    cells = wd.find_element_by_class_name('notebook-cell-list')
    for frame in cells.find_elements_by_tag_name('iframe'):
        wd.switch_to.frame(frame)
        for output in wd.find_elements_by_tag_name('pre'):
            if end_flag in output.text:
                wd.switch_to.default_content()
                ActionChains(wd).key_down(Keys.CONTROL).send_keys(']').perform()
                sleep(5)
                ActionChains(wd).key_down(Keys.CONTROL).send_keys('s').perform()
                sleep(5)
                wd.close()
                wd.quit()
        wd.switch_to.default_content()
    sleep(5)

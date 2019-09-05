import time
import pickle

from constants import google_signin_url, cookies_filepath

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def has_text(driver, text):
    driver.implicitly_wait(2)
    try:
        driver.find_element_by_xpath("//*[contains(text(), '"+str(text)+"')]")
    except NoSuchElementException:
        driver.implicitly_wait(5)
        return False
    driver.implicitly_wait(5)
    return True

def wait_for_xpath(driver, x):
    while True:
        try:
            driver.find_element_by_xpath(x)
            return True
        except:
            time.sleep(0.1)
            pass

def main():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    wd = webdriver.Chrome('chromedriver', options=chrome_options)
    wd.get(google_signin_url)

    if has_text(wd, 'Sign in'):
        wait_for_xpath(wd, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/c-wiz/div/div[4]/div/div/header/div[2]')
        pickle.dump(wd.get_cookies(), open(cookies_filepath, "wb"))
        wd.close()
        wd.quit()
    else:
        print('Did not find sign in page...')

    print("Cookies saved. You can start run.py")

if __name__ == '__main__':
    main()

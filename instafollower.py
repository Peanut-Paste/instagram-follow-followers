from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time


class InstaFollower:
    def __init__(self, driver, email, password, target_account):
        self.driver = driver
        self.email = email
        self.password = password
        self.target_account = target_account

    def scroll_container_to_bottom(self, container_element, timeout=1, scroll_step=200, max_scrolls=100):
        prev_scroll_top = 0
        new_scroll_top = scroll_step
        num_scrolls = 0

        while prev_scroll_top < new_scroll_top and num_scrolls < max_scrolls:
            self.driver.execute_script("arguments[0].scrollTo(0, arguments[1]);", container_element, new_scroll_top)
            time.sleep(timeout)

            prev_scroll_top = new_scroll_top
            new_scroll_top += scroll_step
            max_scroll_top = self.driver.execute_script("return arguments[0].scrollHeight - arguments[0].clientHeight;",
                                                   container_element)

            if new_scroll_top > max_scroll_top:
                new_scroll_top = max_scroll_top

            num_scrolls += 1

    def login(self):
        self.driver.get("https://www.instagram.com")
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        self.driver.find_element(By.NAME, "username").send_keys(self.email)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        self.driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)

    def find_followers(self):
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.x1n2onr6 svg[aria-label="Search"]'))
        )
        self.driver.find_element(By.CSS_SELECTOR, 'div.x1n2onr6 svg[aria-label="Search"]').click()
        self.driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search input"]').send_keys(self.target_account)
        self.driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search input"]').send_keys(Keys.ENTER)
        time.sleep(2)
        # result_list = [
        #     sel_obj.get_attribute("href")
        #     for sel_obj in self.driver.find_elements(By.CSS_SELECTOR, 'div.xh8yej3 div[role="none"] a.x1i10hfl')]
        # print(result_list) # This gets the link of all the account the search return.
        self.driver.find_element(By.CSS_SELECTOR, 'div.xh8yej3 div[role="none"] a.x1i10hfl').click() #First account returned
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.xieb3on li a"))
        )

        # follower_or_ing = [
        #        sel_obj.get_attribute("href")
        #        for sel_obj in self.driver.find_elements(By.CSS_SELECTOR, "ul.xieb3on li a")]
        #        # link to their following/follower page
        # # follower_or_ing[0] or follower_or_ing[1] for follower or following
        self.driver.find_element(By.CSS_SELECTOR, "ul.xieb3on li a").click()

    def follow(self):
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"] div._aano button._aj1-'))
        )
        container = self.driver.find_element(By.CSS_SELECTOR, 'div[role="dialog"] div._aano')
        self.scroll_container_to_bottom(container)
        followers = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="dialog"] div._aano button._aj1-')
        for follow in followers:
            try:
                follow.click()
                time.sleep(5)  # Play around with this to get pass the rate limit
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]')
                cancel_button.click()


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from instafollower import InstaFollower
import os

INSTAGRAM_EMAIL = os.getenv("INSTAGRAM_EMAIL")
INSTAGRAM_PW = os.getenv("INSTAGRAM_PW")
SIMILAR_ACCOUNT = "thecodergeek" #Target account


options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
insta = InstaFollower(driver, INSTAGRAM_EMAIL, INSTAGRAM_PW, SIMILAR_ACCOUNT)
insta.login()
insta.find_followers()
insta.follow()


import selenium
from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from PIL import Image
import io
import json
from chromedriver_py import binary_path

class Chrome(webdriver.Chrome):
    def __init__(self, *args, **kwargs):
        load_dotenv("creds.env")
        current_dir = os.getcwd()
        chrome_path = binary_path
        super().__init__(chrome_path, *args, **kwargs)
    def save_elem_screenshot(self, element, filename):
        try: 
            image = element.screenshot_as_png
            imageStream = io.BytesIO(image)
            im = Image.open(imageStream)
            im.save(os.getcwd() + "/" + filename)
            print("Screenshot saved!")
        except Exception:
            print("Element does not exist.")
    def slow_type(self,element, seconds, text):
        str1 = text
        for x in range(0, len(str1)):
            time.sleep(seconds)
            element.send_keys(str1[x: x + 1])





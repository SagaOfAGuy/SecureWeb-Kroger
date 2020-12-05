#!/Users/lozar/.local/share/virtualenvs/SecureWeb-buZuEbki/bin/python3
from Browser import Chrome
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from ICSWriter import start_ics, write_ics_middle, end_ics
from Printer import find_printers_nix, print_file
import time 
import argparse
import json
from PIL import Image
from pathlib import Path


class SecureWebObject():
    def __init__(self): 
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        self.options = Options()
        self.download_path = os.getcwd()
        self.options.add_argument(f"download.default_directory={os.getcwd()}")
        self.options.add_argument("headless")
        self.logged_in = False
    def login(self, url):
        self.chromedriver = Chrome(options=self.options)
        self.chromedriver.set_window_size(1920,1080)
        self.wait = WebDriverWait(self.chromedriver, 20) 
        self.chromedriver.get(url)
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        try: 
            user = self.wait.until(EC.presence_of_element_located((By.ID, "KSWUSER")))
            pswd = self.wait.until(EC.presence_of_element_located((By.ID, "PWD")))
            self.chromedriver.slow_type(user, 0.078, username)
            self.chromedriver.slow_type(pswd, 0.083, password)
            btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@value='I AGREE']")))
            btn.click()
            print("Login successful!")
            self.logged_in = True
        except NoSuchElementException:
            print("Already logged in!")
        self.resolve_exception()
    def resolve_exception(self):
        try:
            continue_btn = self.wait.until(EC.presence_of_element_located((By.ID, "btnContinue")))
            continue_btn.click()
            alert = self.chromedriver.switch_to.alert
            alert.accept()
        except (NoSuchElementException, TimeoutException, NoAlertPresentException) as error:
            pass
    def take_screenshot(self, filename):
        self.chromedriver.get("https://feed-cdc.kroger.com/EmpowerESS/,DanaInfo=myeschedule.kroger.com+Schedule.aspx")
        try:
            calendar = self.wait.until(EC.presence_of_element_located((By.ID, "calendar")))
            self.chromedriver.save_elem_screenshot(calendar, filename)
        except TimeoutException:
            print("Screenshot failed!")
    def get_schedule_events(self):
        dates = []
        self.chromedriver.get("https://feed-cdc.kroger.com/EmpowerESS/,DanaInfo=myeschedule.kroger.com+Schedule.aspx")
        self.resolve_exception()
        for number in range(1, 8):
            rows = self.wait.until((EC.presence_of_all_elements_located((By.CLASS_NAME, f"child{number}"))))
            for row in rows:
                if ((not "OffNoPay" in row.text and not "Vacation" in row.text) and (len(row.text) > 5)):
                    dates.append(row.text.replace("/", "-"))
        return dates
    def dump_shifts(self):
        ics_start = start_ics()
        ics_end = end_ics() 
        dates = self.get_schedule_events()
        icsfile = open('Schedule.ics', 'w')
        icsfile.write(ics_start+"\n")
        for date in dates:
            new_date = date.splitlines()
            shift_hours = new_date[1]
            hours = new_date[1].split('-')
            start = hours[0][0: hours[0].index(':')]
            end = hours[1][1: hours[1].index(':')]
            fraction_start = hours[0][hours[0].index(':')+1 : hours[0].index('p')]
            fraction_end = hours[1][hours[1].index(':')+1 : hours[1].index('p')]
            month = date[0:2]
            day = date[3:5]
            if ('p' in shift_hours):
                start_hour = f'{int(start) + 12}'
                end_hour = f'{int(end) + 12}'
            else:
                start_hour = start
                end_hour = end
            total_start = f'{start_hour}{fraction_start}'
            total_end = f'{end_hour}{fraction_end}'
            shift_date = write_ics_middle("Kroger", str(month), str(day), str(total_start),  str(total_end))
            icsfile.write(shift_date)
        icsfile.write(ics_end)
        icsfile.close()
        #os.remove("Kroger.png")
        self.chromedriver.quit()
        print("Browser exited")

    def set_paystub_page(self):
        self.chromedriver.execute_script("loadWindow();")
        windows = self.chromedriver.window_handles
        self.chromedriver.switch_to.window(windows[1])
        self.chromedriver.maximize_window()
        print("Getting Paystub...")
        self.chromedriver.execute_script("document.body.style.zoom='103.25%'")
        self.chromedriver.set_window_size(728, 933)
        self.chromedriver.set_window_position(0,0)

    
    def get_pay(self, paycheck_number, bulk=False):
        self.login("https://ess.kroger.com")
        printer = find_printers_nix() 
        pay_stub = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Pay Stub")))
        pay_stub.click()
        paychecks = self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "option")))
        view = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "buttonSm")))
        if(bulk == False):
            paychecks[paycheck_number].click()
            view[0].click()
            try:
                self.set_paystub_page()
            except JavascriptException:
                print("LoadWindow not defined. Restarting Browser in 5 minutes...")
                self.chromedriver.close()
                self.chromedriver.quit()
                time.sleep(300)
                self.get_pay(paycheck_number, bulk=False)
            html = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "html")))
            self.chromedriver.save_elem_screenshot(html, "Paystub.png")
            print_file("Paystub.png", printer)
            os.remove("Paystub.png")
            self.chromedriver.quit()
        else:
            for pay_cycle in range(0, paycheck_number):
                paychecks = self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "option")))
                view = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "buttonSm")))
                paychecks[pay_cycle].click()
                view[0].click()
                self.chromedriver.execute_script("loadWindow();")
                windows = self.chromedriver.window_handles
                self.chromedriver.switch_to.window(windows[1])
                self.chromedriver.set_window_size(728, 933)
                self.chromedriver.set_window_position(0, 0)
                html = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "html")))
                self.chromedriver.save_elem_screenshot(html, f"Paystub{pay_cycle}.png")
                print_file(f"Paystub{pay_cycle}.png", printer)
                print("Paystub Saved")
                self.chromedriver.close()
                self.chromedriver.switch_to.window(windows[0])
        self.chromedriver.quit()
if __name__=="__main__":
    my_parser = argparse.ArgumentParser(description='Automate SecureWeb Schedule and Paystub functions')
    my_parser.add_argument("task", type=str, default=1.0, help="schedule, pay, paybulk")
    my_parser.add_argument("--week", type=int, dest="week")
    args = my_parser.parse_args()
    if (args.task == "schedule"):
        secureweb = SecureWebObject()
        secureweb.login("https://feed.kroger.com")
        secureweb.take_screenshot("Schedule.png")
        secureweb.get_schedule_events()
        secureweb.dump_shifts()
    elif (args.task == "pay"):
        if (args.week == None):
            print("Please enter a proper pay period")
        else:
            SecureWebObject().get_pay(args.week, False)
    elif (args.task == "paybulk"):
        if (args.week == None):
            print("Please enter a proper pay period")
        else:
            SecureWebObject().get_pay(args.week, True)
    else:
        print("Please enter a valid option")









    




    
    
    












from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.edge.service import Service
from bs4 import BeautifulSoup
import sqlite3
import logging
import time 

ChromeDriver = "C:/chromedriver.exe"
DB = "Amin.db"
Log = "Linkedin.log"
Username = "Insert your USERNAME here"
Password = "Insert your PASSWORD here"
URL = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
URL2 = "https://www.linkedin.com/mynetwork/invite-connect/connections/"
URL3 = "https://www.linkedin.com/in/amin-hs-608763233/"

def dump_data(data):
    logging.info(" *** Start dumping data to sqlite3  *** ")
    con = sqlite3.connect('Amin.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE people(
                name text,
                occupation text,
                location text,
                link text
                )""")
    for lst in range(data): # lst is a list of information for one person
        try:
            cur.execute("INSERT INTO people VALUES (?,?,?,?)",(lst[0],lst[1],lst[2],lst[3]))
            con.commit()
        except:
            logging.error(f'+++info of person:{lst[0]} had problem while dumpping it+++')
    
    con.close()        
    mess = "dummped all contacts info Successfully"
    print(mess)    
    logging.info(mess)
    
def crawler(driver, links):
    info = []
    i = -1
    for lk in links:
        i+=1
        try:
            driver.get(lk)
            time.sleep(5)
            src = driver.page_source
            tmp = extract_info(src,lk)
            info.append(tmp)
            logging.info(f'id:{i} Successfully logged user:{tmp[0]}\n\n')
        except:
            logging.error(f'id:{i} +++ Error +++ raised for first try for user:{tmp[3]}\n\n')
            try:
                driver = build_driver()
                sing_in(driver)
                driver.get(lk)
                time.sleep(5)
                src = driver.page_source
                tmp = extract_info(src,lk)
                info.append(tmp)
                logging.info(f'id:{i} Successfully logged user:{tmp[0]}\n\n')
            except:
                logging.error(f'id:{i} +++++ second time Error ++++++ \n\n')
                return -1
            
        
    logging.info("SUCCESSFULLY LOGGED ALL USERS")
    return info

def crawler(driver, links):
    info = []
    i = -1
    for lk in links:
        i+=1
        try:
            driver.get(lk)
            time.sleep(5)
            src = driver.page_source
            tmp = extract_info(src,lk)
            info.append(tmp)
            logging.info(f'id:{i} Successfully logged user:{tmp[0]}\n\n')
        except:
            logging.error(f'id:{i} +++ Error +++ raised for first try for user:{tmp[3]}\n\n')
            try:
                driver = build_driver()
                sing_in(driver)
                driver.get(lk)
                time.sleep(5)
                src = driver.page_source
                tmp = extract_info(src,lk)
                info.append(tmp)
                logging.info(f'id:{i} Successfully logged user:{tmp[0]}\n\n')
            except:
                logging.error(f'id:{i} +++++ second time Error ++++++ \n\n')
                return -1
            
        
    logging.info("SUCCESSFULLY LOGGED ALL USERS")
    return info

def extract_info(src,lk):
    tmp = ["" for _ in range(0,4)]
    tmp[3] = lk
    soup = BeautifulSoup(src, "html.parser")
    intro = soup.find('div', {'class': 'pv-text-details__left-panel'})
    name_loc = intro.find("h1")
    name = name_loc.get_text().strip()
    works_at_loc = intro.find("div", {'class': 'text-body-medium'})
    works_at = works_at_loc.get_text().strip()
    intro2 = soup.find('div', {'class': 'pb2 pv-text-details__left-panel'})
    location_loc = intro2.find_all("span", {'class': 'text-body-small'})
    location = location_loc[0].get_text().strip()
    tmp[0],tmp[1],tmp[2] = name,works_at,location
    return tmp

def grab_links(driver):
    sing_in(d)
    driver.get(URL2)
    time.sleep(30)
    lnks=driver.find_elements_by_tag_name("a")
    connections_links = []
    for lnk in lnks[8:210]: # out of this range is useless 
        connections_links.append(lnk.get_attribute('href'))
    # remove dublicates
    del connections_links[1::2]
    connections_links.append(URL3)
    return connections_links

def sing_in(driver):
    driver.get(URL)
    time.sleep(5)
    # sing in
    username = driver.find_element_by_xpath("//input[@name='session_key']")
    password = driver.find_element_by_xpath("//input[@name='session_password']")

    username.send_keys(Username)
    password.send_keys(Password)
    time.sleep(5)
    submit = driver.find_element_by_xpath("//button[@type='submit']").click()
    time.sleep(5)
    
def build_driver():
    ser = Service(ChromeDriver)
    op = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ser, options=op)
    return driver

d = build_driver()

connections_links = grab_links(d)

len(connections_links)

logging.basicConfig(filename='linkedin.log',level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

info = crawler(driver= d, links =connections_links)

dump_data(info)
'''
#Created by @lameei for exporting data from https://avangemail.net/
'''
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import csv, time, os, config
from bs4 import BeautifulSoup
from tqdm import trange

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

#Go to the login page
print('Loading login page...')

driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
driver.get("https://avangemail.net/customer/guest/index")

#Logging in 

print('Loging in...')

username_field = driver.find_element_by_name("CustomerLogin[email]")
password_field = driver.find_element_by_name("CustomerLogin[password]")
username_field.send_keys(config.username)
password_field.send_keys(config.password)

button = driver.find_element_by_css_selector('.col-lg-12 .pull-right .btn')
button.click()

#The if loop is a simple mechanism for checking if login is a success. 
# if login is a success the page title would be 
# different that the title of the login page. 

if driver.title !=  "AvangEmail | Please login":
    #Get the total number of pages
    driver.get("https://avangemail.net/customer/lists/all-subscribers")

    last_page_link = driver.find_element_by_css_selector('ul.pagination li.last a').get_attribute('href')
    number_of_pages = int(last_page_link.split('/')[-1])


    #Extract data from each page

    ###Useing time stamp so the existing file would not be overwritten. 
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = 'avang-export'+timestr   
    
    #trage have been used instead of ragne to make tqdm progress bar. 
    for page in trange(number_of_pages+1):
        page_link = 'https://avangemail.net/customer/lists/all-subscribers/page/' + str(page)

        driver.get(page_link)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.findAll('table')[1]
        tbody = table.find('tbody')


        with open(r'os.getcwd'+filename+'.csv', 'a') as f:
                wr = csv.writer(f)
                wr.writerows([[td.text for td in row.find_all("td")] for row in tbody.select("tr")])
else:
    print("Login Failed!")




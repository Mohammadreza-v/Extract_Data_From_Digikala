import getpass 
from selenium import webdriver
import chromedriver_binary
from time import sleep
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1920, 1200))
display.start()


price = ""
list_prices = []

def prices_number(digiprices):
	convert_dict = {u'۱':'1', u'۲':'2', u'۳':'3', u'۴':'4', u'۵':'5', u'۶':'6', u'۷':'7', u'۸':'8', u'۹':'9', u'۰':'0'}
	for p in convert_dict.keys():
		prices = re.sub(p, convert_dict[p], digiprices)
		digiprices = prices
	digiprices = re.sub('[^0-9]', '', digiprices)

	return int(digiprices)


email = input("Enter Email or Phone Number : ")
password = getpass.getpass(prompt = "Enter Password : ")

driver = webdriver.Chrome()
driver.get("https://www.digikala.com/")
driver.maximize_window()

sleep(2)
login =  driver.find_element_by_class_name("c-header__btn-login")
driver.execute_script("arguments[0].click();", login)

sleep(2)
email_box = driver.find_element_by_name("login[email_phone]").send_keys(email)
password_box = driver.find_element_by_name("login[password]").send_keys(password)
button_login = driver.find_element_by_class_name("btn-login")
driver.execute_script("arguments[0].click();", button_login)
sleep(2)

try:
    if(driver.find_element_by_xpath("/html/body/main/div[@class='semi-modal-layout']/div[@class='c-semi-modal']/div[@class='c-semi-modal__footer']/a[@class='c-semi-modal__secondary-btn']")):
    	buttonn = driver.find_element_by_xpath("/html/body/main/div[@class='semi-modal-layout']/div[@class='c-semi-modal']/div[@class='c-semi-modal__footer']/a[@class='c-semi-modal__secondary-btn']")
    	driver.execute_script("arguments[0].click();", buttonn)
except:
    pass

your_orders = driver.find_element_by_xpath("/html/body/header/div/div/div[2]/div[1]/div/a")
driver.execute_script("arguments[0].click();", your_orders)
your_orders2 = driver.find_element_by_xpath("/html/body/header/div/div/div[2]/div[1]/div/div/div[2]/div[1]/a")
driver.execute_script("arguments[0].click();", your_orders2)

sleep(2)

n = 1
while not (driver.find_element_by_xpath('//*[@id="content"]/div/section/div[1]/section[2]/div[2]').get_attribute("class") == "c-profile-empty"):
	for i in driver.find_elements_by_xpath('//*[@id="content"]/div/section/div[1]/section[2]/div[2]/div[2]/div'):
		for j in i.find_elements_by_tag_name("div"):
			if(j.get_attribute("class") == "c-table-orders__cell c-table-orders__cell--price"):
				if(prices_number(j.get_attribute("innerHTML")) != 0):
					price = prices_number(j.get_attribute("innerHTML"))
			if(j.get_attribute("class") == "c-table-orders__cell c-table-orders__cell--payment "):
				if(j.find_element_by_tag_name("span").get_attribute("innerHTML") == "پرداخت موفق"):
					list_prices.append(price)
					#print(list_prices)
	n += 1
	driver.get("https://www.digikala.com/profile/orders/?page=%i"% n)
	sleep(2)


print(sum(list_prices))


driver.quit()
display.stop()

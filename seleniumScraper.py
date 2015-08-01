import itertools
import string
import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from StudentModel import Student



path_to_chromedriver = './chromedriver2.37' # change path as needed


credentials = []

timeout =5
driver = None



def getCredentials(): 
	file = open("../credentials.txt", "r")
	for line in file: 
		credentials.append(line)


def setUpDriver():
	chrome_options = Options()
	chrome_options.add_argument("--ignore-certificate-errors")
	chrome_options.add_argument("start-maximized")
	chrome_options.add_argument("disable-infobars")
	chrome_options.add_argument("--disable-extensions")
	chrome_options.add_argument("--test-type")
	global driver
	driver = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=chrome_options)



def goBack(): 
	 driver.execute_script("window.history.go(-1)")

def openElementInNewWindow(): 
	Browser.execute_script('document.getElementById("someID")').setAttribute("target","_blank")


def openNewWindow(): 
	body = driver.find_element_by_tag_name('body')
	body.send_keys(Keys.CONTROL + 'n')
	switchToWindow(1)

def switchToWindow(window=0):
	driver.switch_to_window(driver.window_handles[window])
	# driver.get("http://facebook.com")
	# print "New window ", driver.title

def getCurrentWindow(): 
	return driver.current_window_handle


def writePersonToFile(person=None): 
	file = open("../directory.txt", "a")
	file.write("{} \n {} \n {} \n {} \n {} \n\n".format(person.name, person.major, person.classification, person.phone, person.email))
	# file.write(person)
	file.close()




def copyStudentInfo(): 
	person = Student()
	personItems = []
	personItems = driver.find_elements_by_class_name('dir-Person-item')
	for item in personItems: 
		if(person.major == None): 
			person.major = item.text 
		elif(person.classification == None):
			person.classification = item.text
		elif(person.phone == None): 
			person.phone = item.text
		elif(person.email ==None): 
			person.email = item.text
	person.name = driver.find_element_by_tag_name('h1').text
	writePersonToFile(person)

			

def signInToShibboleth(): 
	time.sleep(2)
	if(getId('okta-signin-username')):
		driver.find_element_by_xpath('//*[@id="okta-signin-username"]').send_keys(credentials[0])
		# for input in inputs: 
	if(getId('okta-signin-password')):	
		driver.find_element_by_id('okta-signin-password').send_keys(credentials[1])
	if(getId('okta-signin-submit')):
		driver.find_element_by_id('okta-signin-submit').click()


def getLinkText(link_text):
	try:
	    element_present = EC.presence_of_element_located((By.LINK_TEXT, link_text))
	    WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
	    print "Timed out waiting for page to load"
	else: 
		return True

def getName(element_name):
	try:
	    element_present = EC.presence_of_element_located((By.NAME, element_name))
	    WebDriverWait(driver, timeout).until(element_present)
	    return True
	except TimeoutException:
	    print "Timed out waiting for page to load"

def getId(element_id): 
	try:
	    element_present = EC.presence_of_element_located((By.ID, element_id))
	    WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
	    print "Timed out waiting for page to load"
	else: 
		return True

def getClass(element_class):
	try:
	    element_present = EC.presence_of_element_located((By.CLASS_NAME, element_class))
	except TimeoutException:
	    print "Timed out waiting for page to load"
	else:
		return True


def getCombination(length=2): 
	result = []
	for guess in itertools.product(): 
		for num_length in range(0, length): 
			for num_length in itertools.combinations_with_replacement(string.digits, num_length): 
				guess = ''.join(guess)
				result.append(guess)


def main(): 
	getCredentials()
	setUpDriver()
	driver.get(credentials[2])

	characters = [''.join(i) for i in itertools.product(string.ascii_lowercase, repeat = 2)]
	# print characters

	# driver.switch_to_frame('mainFrame')
	for combo in characters: 
		driver.find_element_by_id('individuals').clear()
		driver.find_element_by_id('individuals').send_keys(combo)
		driver.find_element_by_id('individual_type__students').click()
		driver.find_element_by_id('search_individuals').click()

		ulList = driver.find_element_by_class_name('dir-Listing')
		items = ulList.find_elements_by_tag_name('li')
		inOtherWindow = True
		for item in items: 
			item.click()
			while(inOtherWindow): 
				if(getClass('right-buttons')):
					driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/a').click()
					signInToShibboleth()
					time.sleep(2)
					# if "signin=true" in driver.current_url:
					copyStudentInfo()
					driver.find_element_by_xpath('//*[@id="content"]/div/p/a').click()
					if(getId('individuals')):
						driver.find_element_by_xpath('//*[@id="individual_type__students"]').click()
						inOtherWindow = False


if __name__ == "__main__": 
	main(); 
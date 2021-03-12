from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

def get_visible(elems):
  return list(filter(lambda x: x.is_displayed(), elems))[0]

def get_addresses(filename):
  address_file = open(filename, 'r')

  addresses = []
  for line in address_file:
    addresses.append(line[:-1])

  return addresses

class HartfordSurveyBot:

  def __init__(self):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    self.driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)
    self.driver.implicitly_wait(10)

    self.driver.get('https://gis1.hartford.gov/Html5Viewer/index.html?viewer=AllCitySurvey2019')
    
    # This is to ensure the page has fully loaded, a better solution should be found
    time.sleep(10)

  def search_parcel(self, address):
    address = address.upper()

    time.sleep(1)
    search = self.driver.find_element_by_id('gcx_search')
    search.click()
    search.clear()
    search.send_keys(address)
    search.send_keys(Keys.RETURN)

    try:
      search_result = self.driver.find_element_by_xpath('//div[text()="{}"]'.format(address))
      return True

    except:
      return False

  def save_csv(self):
    time.sleep(1)
    menu_button = get_visible(self.driver.find_elements_by_xpath('//button[contains(@title, "Panel Actions")]'))
    menu_button.click()

    time.sleep(1)
    export_csv_button = get_visible(self.driver.find_elements_by_xpath('//strong[contains(text(), "Export to CSV")]'))
    actions = ActionChains(self.driver)
    actions.move_to_element(export_csv_button).perform()
    export_csv_button.click()

    time.sleep(1)
    ok_button = get_visible(self.driver.find_elements_by_xpath('//button[text()="OK"]'))
    ok_button.click()

try:
  bot = HartfordSurveyBot()

  parcel_addresses = get_addresses('parcels.txt')

  for address in parcel_addresses:
    bot.search_parcel(address)
    bot.save_csv()

except:
  print('failure')
  bot.driver.save_screenshot('fail.png')

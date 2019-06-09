import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import csv
from selenium.webdriver.common.keys import Keys

# create a new Firefox session
driver = webdriver. Firefox()
driver.implicitly_wait(30)
driver.maximize_window()

# Navigate to the application home page
#driver.get("https://www.justdial.com/Delhi/Automotive-Lubricant-Dealers/nct-10574354")

#driver.get("https://www.justdial.com/Delhi/BPO-For-Credit-Card-Processing/nct-10055836")
# url = 'https://www.justdial.com/Delhi/BPO-For-Banking-Services/nct-10892350'
url = 'https://www.justdial.com/Delhi/BPO-For-Travel-Services-in-Gurgaon/nct-10055879/page-3'
driver.get(url)

driver.implicitly_wait(20)

SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

driver.implicitly_wait(30)
alllink = driver.find_elements_by_xpath('//*[@class="lng_cont_name"]')

link_list =[]
for d in alllink:
   print(d.text)
   link_list.append(d.text)

time.sleep(3)
driver.find_element_by_xpath('//*[@id="best_deal_div"]/section/span').click()

count = 0
for i in link_list:

   count = count + 1

   b2b = driver.find_element_by_link_text(i)
   driver.implicitly_wait(20)
   b2b.click()

   automobie = driver.find_element_by_link_text('Edit This')
   driver.implicitly_wait(20)
   automobie.click()

   edit = driver.find_element_by_link_text('Edit / Modify this business')
   driver.implicitly_wait(20)
   edit.click()

   driver.implicitly_wait(30)
   driver.find_element_by_id("rdoUser").click()
   #
   driver.implicitly_wait(20)
   driver.find_elements_by_xpath('//*[@id="cat"]/button')[0].click()

   varify = None

   try :

       varify = driver.find_element_by_xpath('//*[@id="userotp"]/section/section/p[2]/span[1]')

   except NoSuchElementException:
         driver.implicitly_wait(10)

   if varify:
      driver.back()
      driver.back()

   else:

      formValue = driver.find_element_by_xpath('//*[@id="colcontent"]/div[1]/p[10]/span/span[2]')
      print(formValue.text)
      form = formValue.text

      edit = driver.find_element_by_link_text('Contact Information')
      edit.click()

      # inputs = driver.find_elements_by_xpath('//form[@name="os_home"]//input')
      # for data in inputs:
      #     print(data.get_attribute('value'))
      try:

         name = driver.find_element_by_xpath('//*[@id="contact_person_name[]"]')
         print(name.get_attribute('value'))
         names = name.get_attribute('value')
      except NoSuchElementException:
         driver.implicitly_wait(10)

      mobile_no = driver.find_element_by_xpath('//*[@id="mob_name[]"]')
      print(mobile_no.get_attribute('value'))
      mobiles = mobile_no.get_attribute('value')

      email = driver.find_element_by_xpath('//*[@id="email_id[]"]')
      print(email.get_attribute('value'))
      emails = email.get_attribute('value')

      all_record = list()

      all_record.append(form)
      all_record.append(names)
      all_record.append(mobiles)
      all_record.append(emails)

      file_object = open('website_data_cssv.csv', 'a', newline = '')
      csv_file_writer = csv.writer(file_object, delimiter=',', quoting=csv.QUOTE_MINIMAL)

      for save in all_record:
          csv_file_writer.writerow([save])

      csv_file_writer.writerow("\n ")

      driver.back()
      driver.back()
      driver.back()

      if count == 10:
         print("next page data")
         page = driver.find_element_by_link_text('2')
         driver.implicitly_wait(20)
         page.click()
         driver.implicitly_wait(20)

      print('Its worked')


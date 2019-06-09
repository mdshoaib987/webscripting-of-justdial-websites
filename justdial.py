from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import csv
import pymysql
import pandas as pd

# create a new Firefox session
driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.maximize_window()


# Navigate to the application home page
# driver.get("https://www.justdial.com/Delhi/Automotive-Lubricant-Dealers/nct-10574354")
page_nubmer = 1
record = []

while True:

    print("while loop condition.............Page - %s ..........."% page_nubmer)


    try:
        if page_nubmer > 50:
            break

        input_url = input("Enter URL--:")
        url = input_url+'/page-%s'%(page_nubmer)
        print(url)
        driver.implicitly_wait(10)
        driver.get(url)
        driver.find_element_by_xpath('//*[@id="srchbx"]').clear()
        driver.implicitly_wait(15)

        # close_cookie = driver.find_elements_by_css_selector('#cookiePolicy > div > button')
        # close_cookie[0].click()
        # driver.find_element_by_xpath('//*[@id="best_deal_div"]/section/span').click()

        driver.delete_all_cookies()
        alllink = driver.find_elements_by_xpath('//*[@class="lng_cont_name"]')
        driver.implicitly_wait(5)

        if alllink:
            print(" Data is comming ...")
        else:
            break

        link_list = []
        for d in alllink:
            print(d.text)
            link_list.append(d.text)


    except NoSuchElementException:
        driver.implicitly_wait(10)



    count = 0
    for i in link_list:

        count = count + 1
        print(count)

        try:

            driver.find_element_by_xpath('//*[@id="srchbx"]').clear()

            driver.implicitly_wait(5)
            b2b = driver.find_element_by_link_text(i)
            b2b.click()

            driver.implicitly_wait(5)
            automobie = driver.find_element_by_link_text('Edit This')
            automobie.click()

            driver.implicitly_wait(5)
            edit = driver.find_element_by_link_text('Edit / Modify this business')
            edit.click()

            driver.implicitly_wait(5)
            driver.find_element_by_id("rdoUser").click()
            #
            driver.implicitly_wait(10)
            driver.find_elements_by_xpath('//*[@id="cat"]/button')[0].click()

        except NoSuchElementException:
            pass

        varify = None

        try:

            varify = driver.find_element_by_xpath('//*[@id="userotp"]/section/section/p[2]/span[1]')

        except NoSuchElementException:
            driver.implicitly_wait(10)

        if varify:
            driver.back()
            driver.back()
            driver.implicitly_wait(10)
        else:

         try:
            formValue = driver.find_element_by_xpath('//*[@id="colcontent"]/div[1]/p[10]/span/span[2]')
            print(formValue.text)
            address = formValue.text
            driver.implicitly_wait(10)
            edit = driver.find_element_by_link_text('Contact Information')
            edit.click()
            driver.implicitly_wait(10)
            # inputs = driver.find_elements_by_xpath('//form[@name="os_home"]//input')
            # for data in inputs:
            #     print(data.get_attribute('value'))


            name = driver.find_element_by_xpath('//*[@id="contact_person_name[]"]')
            print(name.get_attribute('value'))
            names = name.get_attribute('value')


            mobile_no = driver.find_element_by_xpath('//*[@id="mob_name[]"]')
            print(mobile_no.get_attribute('value'))
            mobiles = mobile_no.get_attribute('value')

            driver.implicitly_wait(10)

            email = driver.find_element_by_xpath('//*[@id="email_id[]"]')
            print(email.get_attribute('value'))
            emails = email.get_attribute('value')

            driver.implicitly_wait(10)

            all_record = (names, mobiles,emails,address)

            record.append(all_record)


            file_object = open('website_data_cssv.csv', 'a', newline='')
            csv_file_writer = csv.writer(file_object, delimiter='|', quoting=csv.QUOTE_MINIMAL)

            for save in all_record:
                csv_file_writer.writerow([save])

            csv_file_writer.writerow("\n ")

            driver.back()
            driver.back()
            driver.back()

            driver.delete_all_cookies()

         except NoSuchElementException:
                pass
         driver.implicitly_wait(3)
         driver.delete_all_cookies()
         driver.get(url)

    page_nubmer += 1



db = pymysql.connect("localhost","root","password123","JUSTDIAL" )

print("Database is Connected ",db)
# prepare a cursor object using cursor() method
for d in record:
    print(d)

cursor = db.cursor()
print("cursor")
sql = "Insert into justdial (Name, Mobile, Email, Address) " \
                 +" values (%s, %s, %s, %s) "
# Execute the SQL command
for data in record:
     cursor.execute(sql,(data[0],data[1],data[2],data[3]))

# Commit your changes in the database
db.commit()
print("Data is Inserted successfully")

# disconnect from server
db.close()

driver.close()



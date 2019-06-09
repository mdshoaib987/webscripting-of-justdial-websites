from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException
import csv
import pymysql
from justdial.data_link import data_link

page_nubmer = 1
total_page = None
count = 0
retry_count=0
# create a new Firefox session
driver = webdriver.Chrome()
driver.implicitly_wait(20)
driver.maximize_window()


total_link = len(data_link)
print(total_link)

db = pymysql.connect("localhost","root","password123","JUSTDIAL" )

print("Database is Connected ",db)

# prepare a cursor object using cursor() method


for link in range(total_link):

    record = []
    keywords_list = []
    count = count + 1
    print("no of url is :",count)

    try:
        print(data_link[link])
        url = data_link[link]

        driver.get(url)
        driver.implicitly_wait(30)


    except NoSuchElementException:
        pass

    try:
        driver.implicitly_wait(10)
        automobie = driver.find_element_by_link_text('Edit This')
        automobie.click()

        driver.implicitly_wait(10)
        edit = driver.find_element_by_link_text('Edit / Modify this business')
        edit.click()

        driver.implicitly_wait(10)
        driver.find_element_by_id("rdoUser").click()
        #
        driver.implicitly_wait(10)
        driver.find_elements_by_xpath('//*[@id="cat"]/button')[0].click()

    except NoSuchElementException:
        pass

    verify = None

    try:

        verify = driver.find_element_by_xpath('//*[@id="userotp"]/section/section/p[2]/span[1]')

    except NoSuchElementException:
        driver.implicitly_wait(10)


    if verify:
        continue

        print('verified data')
        driver.implicitly_wait(10)
    else:

     try:
        comp_name = driver.find_element_by_xpath('//*[@id="bus_name"]')
        company_name = comp_name.get_attribute('value')
        print(company_name)

        formValue = driver.find_element_by_xpath('//*[@id="colcontent"]/div[1]/p[10]/span/span[2]')
        print(formValue.text)
        address = formValue.text
        try:

            driver.implicitly_wait(10)
            edit = driver.find_element_by_link_text('Contact Information')
            edit.click()
        except NoSuchElementException:
            pass

        try:
            alert = driver.switch_to.alert
            alert.accept()
            print("alert accepted")
            continue
        except NoAlertPresentException:
            print("no alert")
        except UnexpectedAlertPresentException:
            alert = driver.switch_to.alert
            alert.accept()
            pass


        name = driver.find_element_by_xpath('//*[@id="contact_person_name[]"]')
        print(name.get_attribute('value'))
        names = name.get_attribute('value')


        mobile_no = driver.find_element_by_xpath('//*[@id="container_mobile"]/input')
        #print(mobile_no.get_attribute('value'))

        mobiles = mobile_no.get_attribute('value')
        print(mobiles)
        driver.implicitly_wait(10)

        email = driver.find_element_by_xpath('//*[@id="email_id[]"]')
        print(email.get_attribute('value'))
        emails = email.get_attribute('value')

        driver.implicitly_wait(10)


        busines_keywords = driver.find_element_by_xpath('//*[@id="wrapper"]/div[2]/ul/li[4]/a')
        busines_keywords.click()

        driver.implicitly_wait(10)

        keywords_list = driver.find_element_by_xpath('//*[@id="colcontent"]/div[1]/div/ul').text
        keywords = keywords_list[:600]
        print(keywords)

        driver.implicitly_wait(10)

        all_record = (names, company_name, mobiles, emails, address, url, keywords)

        record.append(all_record)

        # store data in databse....
        cursor = db.cursor()
        print("cursor")
        sql = "Insert into justdial (Name, Companyname, Mobile, Email, Address,Data_url,keywords) " \
              + " values (%s, %s, %s, %s, %s, %s,%s) "
        # Execute the SQL command
        for data in record:
            cursor.execute(sql, (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))

        # Commit your changes in the database
        db.commit()
        print("Data is Inserted successfully")


        file_object = open('website_data_cssv.csv', 'a', newline='')
        csv_file_writer = csv.writer(file_object, delimiter='|', quoting=csv.QUOTE_MINIMAL)

        for save in record:
            csv_file_writer.writerow(save)

        csv_file_writer.writerow("\n ")

        driver.implicitly_wait(5)

     except NoSuchElementException:
        pass
     except ConnectionResetError:
        pass


if count == total_link:
    print("No more URL available to fetch the Data")

# disconnect from server
db.close()

driver.close()

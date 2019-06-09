from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import csv
import pymysql



page_nubmer = 1
total_page = 1
input_url = []


input_url = input("Enter URL--:").split()

# create a new Firefox session
driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.maximize_window()


while True:

    for i in input_url:
        record = []
        try:
            if page_nubmer >= total_page:

                print(input_url)
                print(len(input_url))
                url = i + '/page-%s' % (page_nubmer)
                print(url)
                driver.get(url)
                driver.implicitly_wait(5)
                page_count = driver.find_elements_by_xpath('//*[@id="setbackfix"]/div[4]/div[2]')
                driver.implicitly_wait(5)

                for link in page_count:
                    page = link.find_elements_by_tag_name('a')

                total_page = len(page)+1
                print(total_page)

            if page_nubmer > total_page:

                break

            url = i + '/page-%s' % (page_nubmer)
            print(url,'......')
            try:

                driver.get(url)
                driver.find_element_by_xpath('//*[@id="srchbx"]').clear()
                driver.implicitly_wait(10)

                driver.delete_all_cookies()
                alllink = driver.find_elements_by_xpath('//*[@class="lng_cont_name"]')
                driver.implicitly_wait(5)

                link_list = []
                for d in alllink:
                    print(d.text)
                    link_list.append(d.text)

            except NoSuchElementException:
                pass

                count = 0
                for i in link_list:

                    count = count + 1
                    print(count)

                    try:

                        driver.find_element_by_xpath('//*[@id="srchbx"]').clear()

                        b2b = driver.find_element_by_link_text(i)
                        data_url = b2b.get_attribute('href')
                        company_name = b2b.text
                        print(company_name)
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

                    verify = None

                    try:

                        verify = driver.find_element_by_xpath('//*[@id="userotp"]/section/section/p[2]/span[1]')

                    except NoSuchElementException:
                        driver.implicitly_wait(10)


                    if verify:
                        driver.get(url)
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

                        keywords = driver.find_element_by_xpath('//*[@id="colcontent"]/div[1]/div/ul').text

                        driver.implicitly_wait(10)

                        all_record = (names, company_name, mobiles, emails, address, data_url, keywords)

                        record.append(all_record)


                        file_object = open('website_data_cssv.csv', 'a', newline='')
                        csv_file_writer = csv.writer(file_object, delimiter='|', quoting=csv.QUOTE_MINIMAL)

                        for save in record:
                            csv_file_writer.writerow(save)

                        csv_file_writer.writerow("\n ")

                        driver.implicitly_wait(10)

                        driver.get(url)

                        driver.delete_all_cookies()

                     except NoSuchElementException:
                            pass
                     driver.implicitly_wait(3)
                     driver.delete_all_cookies()
                     driver.get(url)

            page_nubmer += 1
            print(page_nubmer)
            print("records")

        except TimeoutException:
            pass
            print("Timed out, No Internet connectivity")

    if record:
        db = pymysql.connect("localhost","root","password123","JUSTDIAL" )

        print("Database is Connected ",db)
        # prepare a cursor object using cursor() method

        cursor = db.cursor()
        print("cursor")
        sql = "Insert into justdial (Name, Companyname, Mobile, Email, Address,Data_url,keywords) " \
                         +" values (%s, %s, %s, %s, %s, %s,%s) "
        # Execute the SQL command
        for data in record:
             cursor.execute(sql,(data[0],data[1],data[2],data[3],data[4],data[5],data[6]))

        # Commit your changes in the database
        db.commit()
        print("Data is Inserted successfully")

        # disconnect from server
        db.close()


    else:
        print("No more data available.")

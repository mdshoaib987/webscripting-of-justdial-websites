from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import csv
import pymysql


# Navigate to the application home page
# driver.get("https://www.justdial.com/Delhi/Automotive-Lubricant-Dealers/nct-10574354")
page_nubmer = 1
record = []
total_page = None
count = 0
while True:

    try:

        if total_page :
            print("Browser is opening.......")

        else:

            input_url = input("Enter URL--:")
            url = input_url + '/page-%s' % (page_nubmer)

            # create a new Firefox session
            driver = webdriver.Firefox()
            driver.implicitly_wait(30)
            driver.maximize_window()
            driver.delete_all_cookies()

            driver.get(url)
            driver.delete_all_cookies()
            page_count = driver.find_elements_by_xpath('//*[@id="setbackfix"]/div[4]/div[2]')
            for link in page_count:
                page = link.find_elements_by_tag_name('a')
            total_page = len(page)+2
            print(total_page)

    except TimeoutException:

        print("Timed out, No Internet connectivity")


    try:
        if page_nubmer >total_page:
            break

        count = count + 1
        print(count)

        if page_nubmer == 13:
            page_no = driver.find_element_by_link_text('Next ››')
            _url = page_no.get_attribute('href')




            driver.implicitly_wait(10)

            page_count = driver.find_elements_by_xpath('//*[@id="setbackfix"]/div[4]/div[2]')
            for link in page_count:
                page = link.find_elements_by_tag_name('a')
            total_page = len(page)
            print(total_page)

        url = input_url + '/page-%s' % (page_nubmer)
        print(url)
        driver.implicitly_wait(20)
        driver.get(url)
        driver.find_element_by_xpath('//*[@id="srchbx"]').clear()
        driver.implicitly_wait(5)

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


            b2b = driver.find_element_by_link_text(i)
            data_url = b2b.get_attribute('href')
            company_name = b2b.text
            print(company_name)
            b2b.click()

            driver.delete_all_cookies()

            try:

               driver.find_element_by_xpath('//*[@id="best_deal_div"]/section/span').click()
            except NoSuchElementException:
                pass

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
            driver.delete_all_cookies()
            driver.find_element_by_xpath('//*[@id="srchbx"]').clear()

            print('verified data')
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

            driver.implicitly_wait(5)

            driver.get(url)
            # driver.back()
            # driver.back()
            # driver.back()
            # driver.back()

            driver.delete_all_cookies()

         except NoSuchElementException:
                pass
         driver.implicitly_wait(3)
         driver.delete_all_cookies()
         driver.get(url)

    page_nubmer += 1
    print(record)

if record:
    db = pymysql.connect("localhost","root","password123","JUSTDIAL" )

    print("Database is Connected ",db)
    # prepare a cursor object using cursor() method
    for d in record:
        print(d)

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

    driver.close()

else:
    print("No more data available.")

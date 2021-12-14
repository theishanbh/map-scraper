from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from time import sleep
import pandas as pd
import re, os
import requests


def run():
    global cities, places  
    cities = pd.read_csv("cities.csv",encoding= 'utf-8')['Cities']    
    places = pd.read_csv("keywords.csv",encoding= 'utf-8')['keywords']
    name_country = input("Enter country name:: ")
    print(f'Select start and end values of cities index in range (0, {len(cities)})')
    while True:
        try :
            start = int(input("Start Value :: "))
            end = int(input("End Value :: "))
            break
        except ValueError : print('Enter a valid NUMBER')
    
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('log-level=3')
    # #chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument("--no-sandbox") 
    # chrome_options.add_argument('--lang=en-US')
    # #chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=1920x1080")
    # chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome('chromedriver.exe',options=chrome_options)
    driver.get('https://www.google.com/maps')
    sleep(10)
    firstpage= driver.page_source
    filetoW=open('firstpage.html','w',encoding="utf-8")
    filetoW.write(firstpage)
    filetoW.close()
    print('written firat page')
    
    #alert=WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "I agree")]'))).click()
    # cookie_button = driver.find_element_by_xpath("//span[text()='I agree']")
    # cookie_button.click()
    #driver.find_element_by_class_name("VfPpkd-vQzf8d").click()
    

    #driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
    sleep(10)
    for place in places:
       for city in cities[start:end]:
            search_word = str(place) + " " + str(city)+ " " + name_country
            print(f'Searching for {search_word}')
            flag = True
            while(flag):
                try:
                    driver.find_element_by_id("searchboxinput").clear()
                    flag = False
                except Exception:
                    flag = True
            # 'agenzia funebre bari italy'
            driver.find_element_by_id("searchboxinput").send_keys(search_word); sleep(1)
            driver.find_element_by_id("searchbox-searchbutton").click()
            print('clicked the search')
            element_aval(driver,"a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd")
            results_scrape(driver,place,city)
    driver.quit()

row = 0
def results_scrape(driver,place,city):
    global row
    data = []
    while True:
        element_aval(driver, "a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd")
        elements = driver.find_elements_by_xpath('//a[contains(@href,"https://www.google.com/maps/place/")]')
        element_click(elements[0]); sleep(1)
        element_find_css(driver, '#sGi9mc-m5SR9c-bottom-pane .Ymd7jc.jpDWw-HiaYvf')
        print(element_find_css(driver, '#sGi9mc-m5SR9c-bottom-pane .Ymd7jc.jpDWw-HiaYvf'))

        elements = driver.find_elements_by_css_selector('#sGi9mc-m5SR9c-bottom-pane.Ymd7jc.jpDWw-HiaYvf')
        print('v1\n' + str(len(elements)))
        elements = driver.find_elements_by_css_selector('.Ymd7jc.jpDWw-HiaYvf')

        print('v2\n' + str(len(elements)))
        elements = driver.find_elements_by_css_selector('.jpDWw-HiaYvf')
        print('v3\n' + str(len(elements)))
        #elements = driver.find_elements_by_css('#sGi9mc-m5SR9c-bottom-pane .Ymd7jc.jpDWw-HiaYvf')

        pageSource = driver.page_source

        fileToW = open("page_source.html", "w", encoding="utf-8")
        fileToW.write(pageSource)


        print(elements)
        for shop in range(len(elements)):
            print(str(row) + " " + str(place) + " " + str(city))
            row += 1
            att_dict = {}
            try:
                element = driver.find_elements_by_css_selector('#sGi9mc-m5SR9c-bottom-pane .Ymd7jc.jpDWw-HiaYvf')[shop]
                try : is_ad_text = element.find_element_by_class_name('ARktye-badge').text; is_ad = True
                except : is_ad = False
                if is_ad: print('Skipping Add')
                else:
                    try:
                        element_click(element)
                        element_aval(driver,"x3AX1-LfntMc-header-title")
                        att_dict['name'] = driver.find_element_by_class_name("x3AX1-LfntMc-header-title").find_element_by_tag_name("h1").text if element_find(driver,"x3AX1-LfntMc-header-title") else ""
                        att_dict['claimed_status'] = driver.find_element_by_xpath('//*[@data-section-id="mcta"]').text if element_xpath(driver,'//*[@data-section-id="mcta"]') else ""
                        att_dict['rating'] = driver.find_element_by_class_name("aMPvhf-fI6EEc-KVuj8d").text if element_find(driver,"aMPvhf-fI6EEc-KVuj8d") else ""
                        att_dict['category'] = driver.find_element_by_xpath('//*[@jsaction="pane.rating.category"]').text if element_xpath(driver,'//*[@jsaction="pane.rating.category"]') else ""
                        att_dict['reivews'] = str(driver.find_element_by_class_name('widget-pane-link').text)[1:-1] if element_find(driver, "widget-pane-link") else ""
                        att_dict['address'] = driver.find_element_by_xpath('//*[@data-item-id="address"]').text if element_xpath(driver,'//*[@data-item-id="address"]') else ""
                        att_dict['street_address'] = driver.find_element_by_xpath('//*[@data-item-id="oloc"]').text if element_xpath(driver,'//*[@data-item-id="oloc"]') else ""
                        att_dict['phone_no'] = driver.find_element_by_xpath('//*[@data-tooltip="Copy phone number"]').text if element_xpath(driver,'//*[@data-tooltip="Copy phone number"]') else ""
                        att_dict['website'] = driver.find_element_by_xpath('//*[@data-tooltip="Open website"]').text if element_xpath(driver,'//*[@data-tooltip="Open website"]') else ""
                        if(att_dict['website'] != ""):
                            att_dict['email'],att_dict['website_inquiry_url'] = find_mail("http://"+att_dict['website'])
                        att_dict['timing'] = driver.find_element_by_class_name("cX2WmPgCkHi__section-info-hour-text").find_elements_by_tag_name("span")[1].text if element_find(driver,"cX2WmPgCkHi__section-info-hour-text") else ""
                        att_dict['image_link'] = driver.find_element_by_xpath('//*[@jsaction="pane.heroHeaderImage.click"]').find_element_by_tag_name('img').get_attribute("src") if element_xpath(driver,'//*[@jsaction="pane.heroHeaderImage.click"]') else ""
                        if re.search('!3d(.*)',driver.current_url):
                            lat_lan = str(re.search('!3d(.*)',driver.current_url).group(1)).split('!4d')
                            att_dict['longitude'] = lat_lan[0]
                            att_dict['latitude'] = lat_lan[1].split('!')[0]
                        else: att_dict['longitude'], att_dict['latitude'] = '',''
                        att_dict['URL'] = driver.current_url
                        att_dict['search_key'] = str(city)+" "+str(place) + " USA"
                        att_dict['price'] = driver.find_element_by_class_name('bRqcEmw6ZsI__price-row').find_element_by_tag_name('span').text if element_find(driver,'bRqcEmw6ZsI__price-row') else ""
                        data.append(att_dict)
                    except Exception :
                        pass
            except Exception as e:
                no_net()
            sleep(1)
        try:
            save_to_excel(data,place)
            data = []
            element_aval(driver,"searchbox-button")
            driver.find_element_by_class_name("searchbox-button").click(); sleep(2)
            driver.find_element_by_id("ppdPk-Ej1Yeb-LgbsSe-tJiF1e").click()
            next_page(driver)
            sleep(1)
        except Exception:
            no_net()
            break

def next_page(driver):
    sleep(1)
    while True:
        try:
            if driver.find_element_by_xpath('//*[@jsan="t-lAj0-0Yc4q0,7.section-refresh-overlay,7.noprint,5.top"]'):
                break
        except Exception:
            pass

def element_find_css(driver, css):
    print('find css '+css)
    try:
        if driver.find_element_by_css_selector(css) :
            print('found css') 
            return True
        else : return False
    except Exception : return False

def element_find(driver,class_name):
    print('find class ' + class_name)
    try:
        if driver.find_element_by_class_name(class_name): 
           print('found class')
           return True
        else : return False
    except Exception : return False

def element_xpath(driver,xpath):
    print('find xpath ' + xpath)
    try:
        if driver.find_element_by_xpath(xpath):
            print('found xpath')
            return True
        else:
            return False
    except Exception:
        return False

def element_aval(driver,class_name):
    print('isavail class' + class_name)
    iter = 0
    while True:
        try:
            iter += 1
            if iter % 100 == 0 :
                print('iter '+ str(iter))
                sleep(10)
            if iter >= 1000 :
                print('class not found '+ class_name)
                break
            if driver.find_element_by_class_name(class_name):
                print(' found class_name')
                break
        except Exception as e:
            #print('class exception',e)
            sleep(10)
            #print('iter '+str(iter))
            
            pass

def element_click(element):
    iter = 0
    while True:
        try:
            iter += 1
            if iter % 100 ==0 :
                print('click iter '+ str(iter))
            if iter > 1000 :
                break
            element.click()
            break

        except Exception:
            pass


def save_to_excel(data,place):
    df = pd.DataFrame(data)
    file_name = "Scrapped_data_"+" " +place+".csv"
    file_name = file_name.replace("*","")
    if os.path.exists(file_name):
    	df.to_csv(file_name,index=False,mode = 'a',header=False, encoding="utf8")
    else:
    	df.to_csv(file_name,index=False, encoding="utf8")

def no_net():
    print("might be no Internet")
    while  True:
        try:
            if requests.get("https://www.google.com/"):
                print("interent available")
                break
        except Exception:
            pass

def find_mail(url):
    try:
        website_inquiry_url = ""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

        source_code = requests.get(url, headers=headers, timeout=(10))
        curr = source_code.url

        original_curr = curr
        plain_text = source_code.text
        if '@' in plain_text:
            match = re.findall(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+', plain_text)
        else:
            match = ""
        # Get from Contact Page
        if not match:
            urls = [original_curr + '/contact/', original_curr + '/contacts/',original_curr + '/contact-us/',original_curr + '/inquiry.pl/',original_curr + '/inquiry/', original_curr +'/contatti/', original_curr + '/contatti.php', original_curr + 'contatti.asp', original_curr +'contatti.pl', original_curr +'contatti.html']
           
            for cu in urls:
                curr = cu
                source_code = requests.get(cu, headers=headers, timeout=(10))
                if(source_code.status_code != 404):
                    website_inquiry_url = website_inquiry_url + "," + cu
                plain_text = source_code.text
                if '@' in plain_text:
                    match = re.findall(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+', plain_text)
                    if match:
                        break
                else:
                    match = ""
            # Get from the url
            if not match:

                match = re.findall(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+', original_curr)
                # Load JavaScript of Page
                if not match:
                    options = Options()
                    options.add_argument('--headless')
                    driver = webdriver.Chrome(options=options)
                    driver.get(original_curr)
                    plain_text = driver.page_source
                    if '@' in plain_text:
                        match = re.findall(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+', plain_text)
                    else:
                        match = ""
                    if not match:
                        urls = [original_curr + '/contact/', original_curr + '/Contact/']
                        for cu in urls:
                            driver.get(cu)
                            plain_text = driver.page_source
                            if '@' in plain_text:
                                match = re.findall(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+', plain_text)
                                if match:
                                    break
                            else:
                                match = ""

                        driver.close()
                    else:
                        driver.close()

        match = list(set(match))
        email = ', '.join(match)
        if not email:
            print ("no mail")
        else:
            return email,website_inquiry_url

    except:
        print("")
    return "",website_inquiry_url

run()
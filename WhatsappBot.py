import time
import os
import glob

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

def hover_click(browser, elem):
    xoff = int(elem.get_attribute('offsetWidth'))
    yoff = int(elem.get_attribute('offsetHeight'))
    padding = 15
    hover = ActionChains(browser).move_to_element_with_offset(elem,padding,padding)
    hover.click()
    hover.perform()

def get_elem(driver, xpath):
    elem = None
    try:
        elem = driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return elem

def scroll_to_bottom(driver):
    old_height = 0
    new_height = None
    xpath= '//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div[2]/span/div/div/div'
    imageBox = driver.find_element_by_xpath(xpath)
    while(old_height != new_height):
        old_height = imageBox.get_attribute('scrollHeight')
        driver.execute_script("arguments[0].scrollTo(0,{0});".format(old_height),imageBox);
        time.sleep(3)
        new_height = imageBox.get_attribute('scrollHeight')

def pack(contact):
    #Get all Files
    home = os.path.expanduser('~')
    download = os.path.join(home,'Downloads')
    wildCard = os.path.join(download,'WhatsApp*.*')
    files = glob.glob(wildCard)

    cwd = os.getcwd()
    outPath = os.path.join(cwd,contact)
    try:
        os.mkdir(outPath)
    except OSError:
        pass
    
    for f in files:
        os.rename(f,os.path.join(outPath,os.path.basename(f)))
  

def main():
    chrome_options = Options()
    chrome_options.add_experimental_option( "prefs", {'profile.default_content_setting_values.automatic_downloads': 1})
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://web.whatsapp.com")
    print("Scan QR Code, And then Enter")
    input()
    print("Logged In")
    
    while(True):
        contact = input("Enter Contact name: ")
        downloadImages(contact,driver)
        ans = input("Download from another contact?(yes): ")
        if(ans != "yes"):
            break;
    input("Press enter to exit")
    driver.quit()
        
def downloadImages(contact,driver):
    #Open Options
    input_box = get_elem(driver,'//*[@id="main"]/header/div[2]/div/div/span')
    if input_box == False:
        print("Couldnt open Options")
        exit()
    
    input_box.click()
    time.sleep(1)
        
    #Open Media
    input_box = driver.find_elements_by_class_name( '_2y8MV')
    if(len(input_box) == 3):
        input_box[1].click()
    else:
        input_box[0].click()

    time.sleep(1)

    images = None
    imgCount = None
    while(True):
        print("Loading Pictures")
        scroll_to_bottom(driver)
        print("Pictures Loaded!")
        
        #Load Images
        images = driver.find_elements_by_class_name( '_275OX')
        imgCount = len(images)
        if(input("Loaded {0} Pictures. Load more?(yes)".format(imgCount)) != "yes"):
            break;
    
    i = 0
    batchSize = 50
    
    while(i < imgCount):
        for j in range(0,min(batchSize,imgCount-i)):
           hover_click(driver,images[i])
           i += 1
           print("\rProgress: {0}/{1}".format(i,imgCount), end = ' ')
       
        #Click Download
        download = get_elem(driver,'//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div[1]/button[5]')
        download.click()
        time.sleep(1)
            
    input("Press enter when download complete")
    #Rename Zip
    pack(contact)

main()


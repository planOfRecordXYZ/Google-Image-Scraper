#import selenium drivers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from ImageProcessor import ImageProcessor

#import helper libraries
import time
import urllib.request
from urllib.parse import urlparse
import os
import sys
import requests
import io
from PIL import Image
import cv2
import numpy as np

#custom patch libraries
import patch

from SeleniumScraper import SeleniumScraper

class GoogleImageScraper(SeleniumScraper):
    def __init__(self, webdriver_path, search_key, headless):
        super().__init__(webdriver_path, headless)
        
        self.search_key = search_key
        self.url = "https://www.google.com/search?q=%s&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947"%(search_key)
        self.indx = -1

    def startup(self):
        self.driver.get(self.url)
        time.sleep(3)

    def shutdown(self):
        self.driver.quit()
        print("[INFO] Google search ended")

    def is_element_visible_in_viewpoint(self, element) -> bool:
        return self.driver.execute_script("var elem = arguments[0],                 "
                                     "  box = elem.getBoundingClientRect(),    "
                                     "  cx = box.left + box.width / 2,         "
                                     "  cy = box.top + box.height / 2,         "
                                     "  e = document.elementFromPoint(cx, cy); "
                                     "for (; e; e = e.parentElement) {         "
                                     "  if (e === elem)                        "
                                     "    return true;                         "
                                     "}                                        "
                                     "return false;                            "
                                     , element)

    def next_url(self):
        print("[INFO] Gathering image links")

        #find and click image
        self.indx += 1
        imgurl = self.driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img'%(str(self.indx)))
        
        if not self.is_element_visible_in_viewpoint(imgurl):
            ActionChains(self.driver).move_to_element(imgurl).perform()
            time.sleep(1)

        imgurl.click()

        try:
            #select image from the popup
            time.sleep(1)
            
            class_names = ["n3VNCb"]
            
            images = [self.driver.find_elements(By.CLASS_NAME, class_name) for class_name in class_names if len(self.driver.find_elements(By.CLASS_NAME, class_name)) != 0 ][0]

            for image in images:
                #only download images that starts with http
                src_link = image.get_attribute("src")
                if(("http" in  src_link) and (not "encrypted" in src_link)):
                    print(
                        f"[INFO] {self.search_key}: \t {src_link}")
                    return src_link
        except Exception as e:
            print("[INFO] Unable to get link: ", e)

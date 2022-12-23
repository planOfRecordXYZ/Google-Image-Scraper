# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 13:01:02 2020

@author: OHyic
"""
#import selenium drivers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

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

class GoogleImageScraper():
    def __init__(self, webdriver_path, image_path, search_key, number_of_images, headless, output_size, keep_filenames, max_missed, token_name):
        #check parameter types
        image_path = os.path.join(image_path, search_key)
        if (type(number_of_images)!=int):
            print("[Error] Number of images must be integer value.")
            return
        if not os.path.exists(image_path):
            print("[INFO] Image path not found. Creating a new folder.")
            os.makedirs(image_path)
        #check if chromedriver is updated
        while(True):
            try:
                #try going to www.google.com
                options = Options()
                if(headless):
                    options.add_argument('--headless')
                driver = webdriver.Chrome(webdriver_path, chrome_options=options)
                driver.set_window_size(1400,1050)
                driver.get("https://www.google.com")
                if driver.find_elements(By.ID, "L2AGLb"):
                    driver.find_element(By.ID, "L2AGLb").click()
                break
            except:
                #patch chromedriver if not available or outdated
                try:
                    driver
                except NameError:
                    is_patched = patch.download_lastest_chromedriver()
                else:
                    is_patched = patch.download_lastest_chromedriver(driver.capabilities['version'])
                if (not is_patched):
                    exit("[ERR] Please update the chromedriver.exe in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")

        self.driver = driver
        self.search_key = search_key
        self.number_of_images = number_of_images
        self.webdriver_path = webdriver_path
        self.image_path = image_path
        self.url = "https://www.google.com/search?q=%s&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947"%(search_key)
        self.headless=headless
        self.output_size = output_size
        self.keep_filenames = keep_filenames
        self.max_missed = max_missed
        self.token_name = token_name

    def detect_faces(self, image):
      # Convert the image from PIL.Image format to a NumPy array
      image = np.array(image)

      # Convert the image to grayscale
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

      # Load the face detector
      face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

      # Detect faces in the image
      faces = face_cascade.detectMultiScale(gray, 1.3, 5)

      # Return the list of face bounding boxes
      return faces

    def process_image(self, image, path):
        width, height = image.size

        if width < self.output_size or height < self.output_size:
            raise Exception("Has smaller resolution than output_size, skipping")

        if width < height:
            new_width = self.output_size
            new_height = int(height * self.output_size / width)
        else:
            new_width = int(width * self.output_size / height)
            new_height = self.output_size

        image = image.resize((new_width, new_height), Image.ANTIALIAS)
        face_boxes = self.detect_faces(image)

        if len(face_boxes) == 0:
            raise Exception("Has no faces")

        if len(face_boxes) > 1:
            raise Exception("Has more than one face")

        face_box = face_boxes[0]
        center_x = face_box[0] + face_box[2] / 2
        center_y = face_box[1] + face_box[3] / 2
        top = center_y - self.output_size / 2
        left = center_x - self.output_size / 2
        bottom = center_y + self.output_size / 2
        right = center_x + self.output_size / 2

        # Adjust top and left values to ensure they do not go outside the bounds of the original image
        if top < 0:
            bottom = bottom + abs(top)
            top = 0
        if left < 0:
            right = right + abs(left)
            left = 0

        # Adjust bottom and right values to ensure they do not go outside the bounds of the original image
        if bottom > new_height:
            rest = bottom - new_height
            top = top - rest
            bottom = new_height
        if right > new_width:
            rest = right - new_width
            left = left - rest
            right = new_width

        image = image.crop((left, top, right, bottom))
        image.save(path)

    def process_url(self, image_url, count):
        print("[INFO] Saving image with URL: %s"%(image_url))
        search_string = ''.join(e for e in self.search_key if e.isalnum())
        image = requests.get(image_url,timeout=5)
        if image.status_code != 200:
            raise Exception("Discarded due to error code %s"%(image.status_code))
        else:
            with Image.open(io.BytesIO(image.content)) as image_from_web:
                try:
                    if (self.keep_filenames):
                        #extact filename without extension from URL
                        o = urlparse(image_url)
                        image_url = o.scheme + "://" + o.netloc + o.path
                        name = os.path.splitext(os.path.basename(image_url))[0]
                        #join filename and extension
                        filename = "%s.%s"%(name,image_from_web.format.lower())
                    else:
                        filename = "%s (%s).%s"%(self.token_name,str(count + 1),image_from_web.format.lower())

                    image_path = os.path.join(self.image_path, filename)
                    self.process_image(image_from_web, image_path)
                    print("[INFO] Saved", image_path)
                except Exception as e:
                    image_from_web.close()
                    raise e
#                    except OSError:
#                        print("[WARNING] OS Error: %s, trying anyway", %(e))
#                        rgb_im = image_from_web.convert('RGB')
#                        process_image(rgb_im, output_size, image_path)

    def scrape(self):
        print("[INFO] Gathering image links")
        count = 0
        missed_count = 0
        self.driver.get(self.url)
        time.sleep(3)
        indx = 1
        while self.number_of_images > count:
            try:
                #find and click image
                imgurl = self.driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img'%(str(indx)))
                imgurl.click()
                missed_count = 0
            except Exception:
                missed_count = missed_count + 1
                if (missed_count>self.max_missed):
                    print("[INFO] Maximum missed photos reached, exiting...")
                    break

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
                            f"[INFO] {self.search_key} \t #{count} \t {src_link}")
                        try:
                            self.process_url(src_link, count)
                            count +=1
                        except Exception as e:
                            print("[WARNING] Skipping %s, %s"%(src_link, e))
                        break
            except Exception as e:
                print("[INFO] Unable to get link: ", e)

            try:
                #scroll page to load next image
                if(count%3==0):
                    self.driver.execute_script("window.scrollTo(0, "+str(indx*60)+");")
                element = self.driver.find_element(By.CLASS_NAME, "mye4qd")
                element.click()
                print("[INFO] Loading next page")
                time.sleep(3)
            except Exception:
                time.sleep(1)
            indx += 1

        self.driver.quit()
        print("[INFO] Google search ended")

# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020

@author: OHyic

"""
#Import libraries
import os
import concurrent.futures
from GoogleImageScraper import GoogleImageScraper
from patch import webdriver_executable
import argparse

def worker_thread():
    image_scraper = GoogleImageScraper(
        webdriver_path, image_path, search_key, number_of_images, headless, output_size, keep_filenames, max_missed, token_name)
    image_scraper.scrape()

    #Release resources
    del image_scraper

if __name__ == "__main__":
    # Define the command line arguments that the program should accept
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search-key', help='the search key to use for scraping images', required=True)
    parser.add_argument('-n', '--number-of-images', type=int, help='the number of images to scrape', default=20)
    parser.add_argument('-H', '--headless', action='store_true', help='run the program in headless mode', default=True)
    parser.add_argument('-o', '--output-size', type=int, help='the desired image resolution', default=512)
    parser.add_argument('-m', '--max-missed', type=int, help='the maximum number of failed images before exiting', default=10)
    parser.add_argument('-k', '--keep-filenames', action='store_true', help='keep the original filenames of the images', default=False)
    parser.add_argument('-t', '--token_name', help='the filename to use when storing the files. I.e. tokenname "jwa" will store files "jwa (1).jpg", "jwa (2).jpg" and so on. this has no effect if --keep-filenames is True', default=None)
    
    # Parse the command line arguments
    args = parser.parse_args()

    #Define file path
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', webdriver_executable()))
    image_path = os.path.normpath(os.path.join(os.getcwd(), 'photos'))
    
    # Use the values from the command line arguments for the parameters
    search_key = args.search_key
    number_of_images = args.number_of_images
    headless = args.headless
    output_size = args.output_size
    max_missed = args.max_missed
    keep_filenames = args.keep_filenames

    # If the token_name argument is not provided, set it to the same value as the search_key argument
    if args.token_name is None:
        token_name = args.search_key
    else:
        token_name = args.token_name

    worker_thread()

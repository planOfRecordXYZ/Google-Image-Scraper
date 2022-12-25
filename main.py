#Import libraries
import os
import concurrent.futures
from GoogleImageScraper import GoogleImageScraper
from ImageProcessor import ImageProcessor
import time
from patch import webdriver_executable
import argparse

def worker_thread():
    #check parameter types
    if (type(number_of_images)!=int):
        print("[Error] Number of images must be integer value.")
        return
    if not os.path.exists(image_path):
        print("[INFO] Image path not found. Creating a new folder.")
        os.makedirs(image_path)

    image_scraper = GoogleImageScraper(webdriver_path, search_key, headless)
    image_processor = ImageProcessor(output_size)

    image_scraper.startup()
    missed_count = 0
    count = 0
    
    while not count >= number_of_images:
        try:
            image_url = image_scraper.next_url()
        except Exception as e:
            print(e)
            if missed_count >= max_missed:
                print("[ERROR]: Missed too many times, aborting")
                break
        
            missed_count +=1
            continue
        
        missed_count = 0
        
        if image_url is None:
            continue
        
        try:
            image_from_web = image_processor.process_url(image_url)
        
            try:
                images = image_processor.process_image(image_from_web)
                image_from_web.close()
            except Exception as e:
                image_from_web.close()
                raise e
        
        except Exception as e:
            print("[WARNING]: Skip processing " + image_url + ", reason: " + str(e))
        
        if len(images) > 0:
            print("[INFO] Processing image with URL: %s"%(image_url))

        for image_count, image in enumerate(images):
            if count >= number_of_images:
                break
        
            if (keep_filenames):
                #extact filename without extension from URL
                o = urlparse(image_url)
                image_url = o.scheme + "://" + o.netloc + o.path
                name = os.path.splitext(os.path.basename(image_url))[0]
                #join filename and extension
                if len(images) == 1:
                    filename = "%s.%s"%(name, image_from_web.format.lower())
                else:
                    filename = "%s (%s).%s"%(name, image_count, image_from_web.format.lower())
            else:
                filename = "%s (%s).%s"%(token_name,str(count + 1), image_from_web.format.lower())
            
            abs_image_path = os.path.join(image_path, filename)
            image.save(abs_image_path)
            count +=1
    
    image_scraper.shutdown()

    #Release resources
    del image_scraper

if __name__ == "__main__":
    # Define the command line arguments that the program should accept
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search-key', help='the search key to use for scraping images', required=True)
    parser.add_argument('-n', '--number-of-images', type=int, help='the number of images to scrape', default=20)
    parser.add_argument('-H', '--non-headless', action='store_true', help='when on, the app will not run in headless mode', default=False)
    parser.add_argument('-o', '--output-size', type=int, help='the desired image resolution', default=512)
    parser.add_argument('-m', '--max-missed', type=int, help='the maximum number of failed images before exiting', default=10)
    parser.add_argument('-k', '--keep-filenames', action='store_true', help='keep the original filenames of the images', default=False)
    parser.add_argument('-t', '--token_name', help='the filename to use when storing the files. I.e. tokenname "jwa" will store files "jwa (1).jpg", "jwa (2).jpg" and so on. this has no effect if --keep-filenames is True', default=None)
    
    # Parse the command line arguments
    args = parser.parse_args()
    
    # Use the values from the command line arguments for the parameters
    search_key = args.search_key
    number_of_images = args.number_of_images
    headless = not args.non_headless
    output_size = args.output_size
    max_missed = args.max_missed
    keep_filenames = args.keep_filenames

    #Define file path
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', webdriver_executable()))
    a_image_path = os.path.normpath(os.path.join(os.getcwd(), 'photos'))
    image_path = os.path.normpath(os.path.join(a_image_path, search_key))

    # If the token_name argument is not provided, set it to the same value as the search_key argument
    if args.token_name is None:
        token_name = args.search_key
    else:
        token_name = args.token_name

    worker_thread()

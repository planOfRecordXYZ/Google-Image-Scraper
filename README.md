# Google Image Scraper
A library for scraping Google Images for a specified person. The library resizes the images to a specified resolution (standard: 512x512), crops them and makes sure the face is still in the image. This library can be used to train AI models such as Stable Diffusion on a specific person.

## Pre-requisites:
1. Google Chrome
1. Selenium (pip install Selenium)
2. Pillow (pip install Pillow)

## Setup:
1. Open command prompt
2. Clone this repository (or [download](https://github.com/rundfunk47/Google-Image-Scraper/archive/refs/heads/master.zip))
    ```
    git clone https://github.com/rundfunk47/Google-Image-Scraper
    ```
3. Install Dependencies
    ```
    pip install -r requirements.txt
    ```
4. Run the program
    ```
    python main.py --search-key "Elon Musk"
    ```

## Usage:
This project was created to bypass Google Chrome's new restrictions on web scraping from Google Images. 
To use it, define your desired parameters in main.py and run through the command line:
```
python main.py
```

## IMPORTANT:
This program will install an updated webdriver automatically. There is no need to install your own.

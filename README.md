# Google Image Scraper for faces, for training AI models
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

## Usage:
This project was created to bypass Google Chrome's new restrictions on web scraping from Google Images. 

Type 
```
python main.py --search-key "Elon Musk" --token_name "emsk"
```

This will search Google Images for "Elon Musk", detect the face, resize the image and keep the face within the frame. Photos will be stored with the names "photos/Elon Musk/emsk (1).jpg", "photos/Elon Musk/emsk (2).jpg" and so on in this example.

Type
```
python main.py --help
```
for all the arguments

The app also comes with a script, rename.py, to help you rename files in the generated folder. This is good if you want to manually remove some photos but want to name the files like ("emsk (1).jpg", "emsk (b).jpg") and so on. It is run with the same arguments:

```
python rename.py --search-key "Elon Musk" --token_name "emsk"
```

## IMPORTANT:
This program will install an updated webdriver automatically. There is no need to install your own.

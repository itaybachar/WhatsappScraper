# Whatsapp Image Scraper
A small utility script to download WhatsApp images from selected conversations.

## Prerequisites
* For this application, the Selenium module is needed and can be downloaded [here](https://selenium-python.readthedocs.io/installation.html).
* Download the chrome web driver and create add its location to the PATH enviromental variable.

## Usage
1) Run the python script.
```
python3 WhatsappBot.py
```
2) Scan in the Whatsapp barcode into your phone application.
3) Selected desired conversation to download images from.
4) In the python terminal, press enter once and enter in the name under which the files will be saved as.
5) The program will then download the images in batches of 50. This can be repeated many times.

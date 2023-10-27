# addchoice_detector
## Building ad observatory by collecting ad data from leading websites.
This code aims to collect advertisements (screenshots, ad urls) to understand the biases that influence advertisers real time bidding strategies on ad exchanges. 
**Methods 1** - get all the image urls from har files and then classify the ads using url filter list.
**Method 2** - get all the screenshots of images iframes and background images and then run perceptual hashing algorithm to search for adchoice icon. (In US all advertisements are required to display an adchoice icon.) clasify the image as an ad image if adchoice icon is found.
We try to combine both the methods to collect close to 100% advertisement displayed on a website.
### Installation
1. Install necessary Python libraries and drivers:
  - pip install selenium
  - pip install selenium browsermob-proxy pillow
  - form selenium import webdriver
  - pip install numpy
### Usage
Used to scrape images/ iframes and background and their urls from a website. <br />
**All_iamge_SC.py** - main function which executes both the methods concurrently.<br />
**get_image_from_the_url.py** - get images,ifrmaes and background images from website while storing their urls seperately. <br />
**Image_matchinhg using Opencv** - match the image obtained from scrapping the given url with adchoice logo using opencv, can be done using template matching.Note that the code uses pixel-wise comparisons for template matching, which may be sensitive to slight variations and noise in the images.<br />
**Imghash.js**- here using Levenshtein distance on the hash value of the two images to determine if the adchoice logo is present in the extracted image.<br />


# addchoice_detector
### Installation
1. Install necessary Python libraries and drivers:
  - pip install selenium
  - pip install selenium browsermob-proxy pillow
  - form selenium import webdriver
  - pip install numpy

**get_image_from_the_url.py** - get images,ifrmaes and background images from website and store their urls seperately <br />
**Image_matchinhg using Opencv** - match the image obtained from scrapping the given url with adchoice logo using opencv, can be done using template matching.Note that the code uses pixel-wise comparisons for template matching, which may be sensitive to slight variations and noise in the images.<br />
**Imghash.js**- here using Levenshtein distance on the hash value of the two images to determine if the adchoice logo is present in the extracted image<br />


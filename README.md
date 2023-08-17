# addchoice_detector
**Getting_image.py** - get images from url where Id = ad unit<br />
**Image_matchinhg using Opencv** - match the image obtained from scrapping the given url with adchoice logo using opencv, can be done using template matching.Note that the code uses pixel-wise comparisons for template matching, which may be sensitive to slight variations and noise in the images.<br />
**Imghash.js**- here using Levenshtein distance on the hash value of the two images to determine if the adchoice logo is present in the extracted image
**get_image_from_the_url.py** - scrape all the images from the provided url with the tag img
**get_background_images.py** - scrape all background images within tag <div> and <a> form the provided url 

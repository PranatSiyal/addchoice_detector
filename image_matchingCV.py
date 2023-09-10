import cv2
import numpy as np

# Read the images
image = cv2.imread("/Users/pranatsiyal/addchoice_detector/test_screenshots/output_image.png")
template = cv2.imread("taboola.png")

# Match the template within the image
#result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

# # Find the best matching location
#min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# # Get the top-left and bottom-right coordinates of the matching region
# top_left = max_loc
# h, w = template.shape[:2]
# bottom_right = (top_left[0] + w, top_left[1] + h)

# # Draw a rectangle around the matching region
# cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

# # Display the result
# cv2.imshow("Image with Matching Region", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

def find_image(im, tpl, threshold=0.7):
    im = np.atleast_3d(im)
    tpl = np.atleast_3d(tpl)
    H, W, D = im.shape[:3]
    h, w = tpl.shape[:2]

    # Integral image and template sum per channel
    sat = im.cumsum(1).cumsum(0)
    tplsum = np.array([tpl[:, :, i].sum() for i in range(D)])

    # Calculate lookup table for all the possible windows
    iA, iB, iC, iD = sat[:-h, :-w], sat[:-h, w:], sat[h:, :-w], sat[h:, w:] 
    lookup = iD - iB - iC + iA
    # Possible matches
    possible_match = np.where(np.logical_and.reduce([lookup[..., i] == tplsum[i] for i in range(D)]))

    # Find exact match
    for y, x in zip(*possible_match):
        if np.all(im[y+1:y+h+1, x+1:x+w+1] == tpl):
            return (y+1, x+1)

    raise Exception("Image not found")
try:
    matched_location = find_image(image, template)
    if matched_location:
        print("Image Matched at location:", matched_location)
except Exception as e:
    print("Image Not Matched")
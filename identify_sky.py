'''
CS5330 Spring 2024
Lab 1 - Sky Pixel Identification
Kay (Mengxian) Cai
'''
import requests
from PIL import Image
from io import BytesIO
import cv2
import numpy as np

STARRY_NIGHT_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/800px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg"

def open_image_from_url(image_url):
  '''
  Function -- open_image_from_url
    this function opens an image from the provided url and returns the image as
    a NumPy array
  Parameter: a string, which must be a url to an image
  Return: an image in the form of a NumPy array
  Raise: errors if any exception occurs such as HTTP errors or invalid image formats
  '''
  try:
    # Make a request to the URL to get the image content
    response = requests.get(image_url)
    response.raise_for_status()
    
    # Open the image using PIL
    img_pil = Image.open(BytesIO(response.content))
    
    # Convert PIL image to NumPy array
    img_np = np.array(img_pil)
    return img_np
  
  except Exception as e:
    print(f"Error: {e}")
    return None


def identify_sky_pixels(input_img):
  '''
  Function -- identify_sky_pixels
    this function identifies the sky pixels in an image assuming the weather is 
    either sunny or cloudy, without glows (such as in dawn or dusk), it then 
    replaces all sky pixels with the corresponding pixels in the replacement image 
    (default being Vincent van Gogh's The Starry Night)
  Parameter: an image in the form of NumPy array in RGB color space, if the image
    is read in by cv2.imread, please comment out the RGB to BGR conversion code
  Return: processed image where the sky pixels are identified and replaced 
  '''
  # Open the starry night image from the Internet to be the replacement pixels
  # User can replace the parameter with url to any of their preferred replacement images
  replacement = open_image_from_url(STARRY_NIGHT_URL)
  if replacement is None:
    return

  # Convert input_img from RGB to BGR for cv2 handling  
  replacement = cv2.cvtColor(replacement, cv2.COLOR_RGB2BGR)

  # Resize the replacement image to be the same as input_img
  replacement = cv2.resize(replacement, (input_img.shape[1], input_img.shape[0]))

  # Convert input_img from RGB to BGR for cv2 handling
  # !!!IMPORTANT
  # Comment out this line if the image is read by cv2.imread thus already in RGB
  input_img = cv2.cvtColor(input_img, cv2.COLOR_RGB2BGR)

  # Apply Gaussian blur
  blurred_image = cv2.GaussianBlur(input_img, (5, 5), 0)

  # Convert the blurred image to the HSV color space
  hsv_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)

  # Sample colors from the first 30 rows of pixels assuming the top is sky
  sample_colors = hsv_image[:30, :]

  # Calculate average HSV values, round to three digits after the decimal
  average_hsv = np.round(np.mean(sample_colors, axis=(0, 1)), 3)

  # Define HSV ranges for blue and gray colors
  blue_lower = np.array([100, 50, 100])
  blue_upper = np.array([120, 255, 255])

  gray_lower = np.array([40, 0, 100])
  gray_upper = np.array([130, 50, 220])

  # Check if the HSV value falls within the blue range
  if blue_lower[0] <= average_hsv[0] <= blue_upper[0] and \
    blue_lower[1] <= average_hsv[1] <= blue_upper[1] and \
    blue_lower[2] <= average_hsv[2] <= blue_upper[2]:
    color = "blue"
    lower_range = np.array([average_hsv[0] - 10, 50, 100])
    upper_range = np.array([average_hsv[0] + 10, 255, 255])

  # Check if the HSV value falls within the gray range
  elif gray_lower[0] <= average_hsv[0] <= gray_upper[0] and \
    gray_lower[1] <= average_hsv[1] <= gray_upper[1] and \
    gray_lower[2] <= average_hsv[2] <= gray_upper[2]:
    color = "gray"
    lower_range = np.array([average_hsv[0] - 20, 0, 50])
    upper_range = np.array([average_hsv[0] + 20, 30, 220])

  # If neither blue or gray, the pixels are not sky, no range will be provided
  # Return the original image
  else:
    color = "else"
    lower_range = []
    upper_range = []
    return cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)

  # Threshold the HSV image to get only colors in the range
  mask = cv2.inRange(hsv_image, lower_range, upper_range)

  # Create the inverse of the mask
  mask_inv = cv2.bitwise_not(mask)

  # Extract sky pixels from the replacement image using the mask
  sky = cv2.bitwise_and(replacement, replacement, mask = mask)

  # Extract non-sky pixels from the input image using the inverse mask
  non_sky = cv2.bitwise_and(input_img, input_img, mask = mask_inv)

  # Combine the sky and non-sky regions to get the final image
  result = cv2.add(sky, non_sky)
  result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

  # Convert the final image back to RGB and return it
  return result

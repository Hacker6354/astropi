from astro_pi_orbit import ISS
from picamzero import Camera
from datetime import datetime, timedelta
from time import sleep
from pathlib import Path
#from math import sin, cos, sqrt, atan2
import math
import cv2
import os

base_folder = Path(__file__).parent.resolve()

iss = ISS()


def dms_to_dd(sign, degrees, minutes, seconds):
    return sign* (degrees + (minutes / 60) + (seconds / 3600))

def get_gps_coordinates(iss):
    """
    Returns a tuple of latitude longitude coordinates expressed in signed degrees minutes seconds.
    """
    point = iss.coordinates()
    return (point.longitude.signed_dms(),point.latitude.signed_dms())


def find_distance(lat1, lon1, lat2, lon2):
    R = 6378 + 408  # Earth's radius + ISS distance from earth in kilometers

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

lat,lon = get_gps_coordinates(iss)
lat1 = dms_to_dd(lat[0],lat[1],lat[2],lat[3])
lon1 = dms_to_dd(lon[0],lon[1],lon[2],lon[3])
sleep(1)
lat,lon = get_gps_coordinates(iss)
lat2 = dms_to_dd(lat[0],lat[1],lat[2],lat[3])
lon2 = dms_to_dd(lon[0],lon[1],lon[2],lon[3])

# Calculate the distance 
distance = find_distance(lat1, lon1, lat2, lon2)

print("Hello from the ISS")

estimate_kmps = distance/1 # distance took in 1 sec difference 
estimate_kmps_formatted = "{:.4f}".format(estimate_kmps)

output_string = estimate_kmps_formatted

file_path = "result.txt"
with open(file_path, 'a', encoding="utf-8") as file:
    file.write(output_string)

cam = Camera()
cloudimg = os.path.join("cloud.jpg")
cam.take_photo(cloudimg)
cam.capture_sequence("sequence", num_images=10, interval=3)

img = cv2.imread(cloudimg, 0)
height = img.shape[0]
width = img.shape[1]
ret, thresh = cv2.threshold(img, 100, 1, cv2.THRESH_BINARY) 
total = sum(map(sum, thresh)) # to find total sum of 2D array thresh
percent = total/height/width*100
percent_formatted = "{:.1f}".format(percent)
print('percentage of cloud cover is =', percent_formatted, '%')
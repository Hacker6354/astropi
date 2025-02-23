from astro_pi_orbit import ISS
from picamzero import Camera
from datetime import datetime, timedelta
from time import sleep
from pathlib import Path
#from math import sin, cos, sqrt, atan2
import math

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
print("Resault", distance)

print("Hello from the ISS")

estimate_kmps = distance/1 # distance took in 1 sec difference 
estimate_kmps_formatted = "{:.4f}".format(estimate_kmps)

output_string = estimate_kmps_formatted

file_path = "result.txt"
with open(file_path, 'a', encoding="utf-8") as file:
    file.write(output_string)

cam = Camera()
cam.take_photo("image1.jpg")
cam.take_photo("gps_image1.jpg", gps_coordinates=get_gps_coordinates(iss))
cam.capture_sequence("sequence", num_images=40, interval=1)


print("Data written to", file_path)
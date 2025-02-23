from astro_pi_orbit import ISS
from picamzero import Camera
from datetime import datetime, timedelta
from time import sleep
from pathlib import Path

import os

base_folder = Path(__file__).parent.resolve()

iss = ISS()

def get_gps_coordinates(iss):
    """
    Returns a tuple of latitude longitude coordinates expressed in signed degrees minutes seconds.
    """
    point = iss.coordinates()
    return (point.latitude.signed_dms(), point.longitude.signed_dms())

cam = Camera()

cam.take_photo("gps_image1.jpg", gps_coordinates=get_gps_coordinates(iss))
cam.capture_sequence("sequence", num_images=3, interval=3)

estimate_kmps = 7.9
estimate_kmps_formatted = "{:.4f}".format(estimate_kmps)

output_string = estimate_kmps_formatted

file_path = "result.txt"
with open(file_path, 'a', encoding="utf-8") as file:
    file.write(output_string)

print("Data written to", file_path)

start_time = datetime.now()
now_time = datetime.now()

while (now_time < start_time + timedelta(minutes=1)):
    print("Hello from the ISS")
    sleep(60)
    print("Good by from the ISS")
    now_time = datetime.now()
    
print(base_folder)

data_file = os.path.join(base_folder, "data.csv")
for i in range(10):
    with open(data_file, "a", buffering=1, encoding="utf-8") as f: # changed mode from write to append so that new lines are added at the end
        f.write(f"Some data: {i}".format(i))
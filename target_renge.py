# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import csv
import math


coordinate_file = open(sys.argv[1],'r')
target_range_file = open(sys.argv[2],'w')
target_range_x = int(sys.argv[3])
target_range_y = int(sys.argv[4])

target_range_x_min = 0
target_range_x_max = 0
target_range_y_min = 0
target_range_y_max = 0

csv_reader = csv.reader(coordinate_file, delimiter=',')

while True:

    row = next(csv_reader)
    x_range = float(row[0])
    y_range = float(row[1])
    print(x_range)



    target_range_x_min = round(x_range) - (target_range_x / 2)
    target_range_x_max = round(x_range) + (target_range_x / 2)
    target_range_y_min = round(y_range) - (target_range_y / 2)
    target_range_y_max = round(y_range) + (target_range_y / 2)

    target_range_file.write(str(target_range_x_min)+",")
    target_range_file.write(str(target_range_x_max)+",")
    target_range_file.write(str(target_range_y_min)+",")
    target_range_file.write(str(target_range_y_max)+"\n")



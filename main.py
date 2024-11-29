# fetches live stream from ip camera

import cv2
import cvzone
import pickle

import numpy as np
import pandas as pd
# from ultralytics import YOLO

def main():
    # import from .secrets
    username = ""
    password = ""
    ipaddress = ""

    capture = cv2.VideoCapture(f'rtsp://{username}:{password}@{ipaddress}')

    while(True):
        pass
    pass


if __name__ == "__main__":
    main()
from PIL import Image
from preprocessing import *
from staff_removal import *
from helper_methods import *
from transcribe import *

import cv2 as cv
import numpy as np
import configparser as cp
from PIL import Image
from ultralytics import YOLO

import os
import glob
import streamlit as st
from zipfile import ZipFile

out = glob.glob("output/*")
for f in out:
    os.remove(f)

images = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
keysig = st.slider("Insert Keysig from how many sharps and flats there are (e.g. 4 sharps = 4, 4 flats = -4)", -7, 7, 0)
bpm = st.number_input("Insert BPM")

i = -1
for img_in in images:
    print("uploaded file : ", img_in._file_urls.upload_url)

    img_open = Image.open(img_in)
    img_arr = np.array(img_open)

    config = cp.ConfigParser()
    config.read('config.ini')

    img = cv.cvtColor(img_arr, cv.COLOR_BGR2GRAY)
    # img = resize(img, int(config.get("size", "size"))) # from helper_methods
    height, width = img.shape

    img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
    _threshold, in_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    staff_lines_thicknesses, staff_lines = get_staff_lines(width, height, in_img, 0.8)
    cleaned, staff_coords = remove_staff_lines(in_img, width, staff_lines, staff_lines_thicknesses)

    size = int(config.get("size", "size"))
    staff_height = int(config.get("size", "staff_height"))
    # resize late because resize early causes the staff lines to disappear
    scaled, res_percent, border_top = resizebar(cleaned, staff_height, size, staff_coords) # from preprocessing
    staff_coords = resized_staff_coords(staff_coords, res_percent, border_top)
    print(staff_coords)

    final = Image.fromarray(scaled)

    note_list = detect("notehead.pt", final)
    rest_list, acc_list, beam_list, flag_list = detect("others.pt", final)
    aug_list = detect_aug("others.pt", final)

    notes_dict = get_notes(staff_coords)

    all_list = note_list + rest_list
    all_list = sorted(all_list, key=lambda x: x[-1][0])

    dur_notes, dur_rest = get_duration(all_list, beam_list, flag_list, aug_list)

    pitch_list = get_pitch(notes_dict, dur_notes, acc_list, keysig)
    all_list = sorted(pitch_list + rest_list, key=lambda x: x[-1][0])
    print(all_list)

    i += 1
    create_midi(i, all_list, bpm)
    
ZipFile(f'output.zip', mode='w').write(f'output/output{i}.mid')

with open(f'output.zip', "rb") as fp:
    btn = st.download_button(
        label="Download Output",
        data=fp,
        file_name="output.zip",
        mime="application/zip"
    )
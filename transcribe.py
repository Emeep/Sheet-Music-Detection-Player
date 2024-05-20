import numpy as np
from statistics import mode
import configparser as cp
from mido import *

from ultralytics import YOLO
from statistics import mean

class Notehead:
    def __init__(self, type, class_no, x, y, aug):
        self.type = type
        self.class_no = class_no
        self.x = x
        self.y = y
    def __repr__(self):
        return repr((self.type, self.class_no, self.x,
                     self.y))
    
    

def get_notes(staff_line_pos):
    notes = {'A0': 0, 'B0': 0,
             'C1': 0, 'D1': 0, 'E1': 0, 'F1': 0, 'G1': 0, 'A1': 0, 'B1': 0,
             'C2': 0, 'D2': 0, 'E2': 0, 'F2': 0, 'G2': 0, 'A2': 0, 'B2': 0,
             'C3': 0, 'D3': 0, 'E3': 0, 'F3': 0, 'G3': 0, 'A3': 0, 'B3': 0,
             'C4': 0, 'D4': 0, 'E4': 0, 'F4': 0, 'G4': 0, 'A4': 0, 'B4': 0,
             'C5': 0, 'D5': 0, 'E5': 0, 'F5': 0, 'G5': 0, 'A5': 0, 'B5': 0,
             'C6': 0, 'D6': 0, 'E6': 0, 'F6': 0, 'G6': 0, 'A6': 0, 'B6': 0,
             'C7': 0, 'D7': 0, 'E7': 0, 'F7': 0, 'G7': 0, 'A7': 0, 'B7': 0,
             'C8': 0}

    
    notes_name = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    notes_name_reversed = list(reversed(['C', 'D', 'E', 'F', 'G', 'A', 'B']))
    
    # treble clef highest default staff on f5   
    start_note = 3 # f
    start_num = 5

    pos = staff_line_pos[0]
    i = 0
    alt = True

    staff_np = np.array(staff_line_pos)
    diff = mode(np.diff(staff_np))


    # negative iteration
    while True:
        try: notes[f'{notes_name_reversed[(start_note + 1) % 7]}{start_num}']
        except: break

        if alt:
            pos_center = pos + (diff // 2)

            notes[f'{notes_name_reversed[start_note]}{start_num}'] = pos

            temp_start_num = start_num
            if start_note + 1 > 6:
                temp_start_num = start_num - 1
            notes[f'{notes_name_reversed[(start_note + 1) % 7]}{(temp_start_num)}'] = pos_center

            if i <= 3:
                i += 1
                pos = staff_line_pos[i]
            else:
                pos += diff

        if notes_name_reversed[start_note] == 'C':
            start_num -= 1
        start_note = (start_note + 1) % 7
        
        if not alt:
            alt = True
        else:
            alt = False

    if notes['A0'] == 0:
        notes['A0'] = pos

    # treble clef highest default staff on f5   
    start_note = 3 # f
    start_num = 5

    pos = staff_line_pos[0]
    i = 0
    alt = True
    # positive iteration
    while True:
        try: notes[f'{notes_name[(start_note + 1) % 7]}{start_num}']
        except: break
        
        if alt:
            pos_center = pos - (diff // 2)

            notes[f'{notes_name[start_note]}{start_num}'] = pos

            temp_start_num = start_num
            if start_note + 1 > 6:
                temp_start_num = start_num + 1
            notes[f'{notes_name[(start_note + 1) % 7]}{(temp_start_num)}'] = pos_center

            pos -= diff

        start_note = (start_note + 1) % 7
        if notes_name[start_note] == 'C':
            start_num += 1
        if not alt:
            alt = True
        else:
            alt = False

    if notes['C8'] == 0:
        notes['C8'] = pos

    return notes

def check_augdot(note_list, augdot_x):
    res_key, res_val = min(note_list, key=lambda x:abs(x-augdot_x))
    print(res_key, res_val)

def get_pitch(notes: dict, note_list):
    pitch_list = []

    for i in note_list:
        pos = i.y
        res_key, res_val = min(notes.items(), key=lambda y: abs(pos - y[1]))
        
        # TODO MAKE A CHORD RECOGNITION AND PLAY
            
        
        pitch_list.append((res_key, i.x))

    return pitch_list


def create_midi(notes, filename):
    config = cp.ConfigParser()
    config.read('config.ini')

    # Create a new MIDI file
    mid = MidiFile()

    # Create a track
    track = MidiTrack()
    mid.tracks.append(track)

    # Default tempo (adjustable if needed)
    tempo = (60000 / (int(config.get('midi', 'BPM')))) * 4 # from quarter note BPM to ms per quarter note
    track.append(MetaMessage('set_tempo', tempo=round(tempo)))
    
    for note in notes:
        note_name = note[0]
        # Extract duration if provided, otherwise default to a quarter note
        duration = note[1] if len(note) > 1 else 0.25

        # Convert note name to MIDI pitch number (C4 = 60)
        pitch = 60 + (note_name.find('C') - 3) + (len(note_name) - 1) * 12

        # Create note on and off messages
        velo = int(config.get('midi', 'velocity'))
        track.append(Message('note_on', note=pitch, velocity=velo, time=0))
        track.append(Message('note_off', note=pitch, velocity=velo, time=int(duration * 480000)))

    # Save the MIDI file
    mid.save(f'output/{filename}')
    

def detect(model_name, img):
    config = cp.ConfigParser()
    config.read('config.ini')
    
    model = YOLO(model_name)
    results = model.predict(img, imgsz=config.get('size', 'size'),
                            conf=0.05, iou=0.01, save=True, show_labels=False)

    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    names = results[0].names
    confidences = results[0].boxes.conf.tolist()

    note_list = []
    notehead = ['noteheadBlack', 'noteheadHalf', 'noteheadWhole']
    rest = ["rest128th","rest16th","rest32nd","rest64th","rest8th",
            "restDoubleWhole","restHalf",]
    # Iterate through the results
    for box, cls, conf in zip(boxes, classes, confidences):
        x1, y1, x2, y2 = box
        x1, y1, x2, y2 = round(x1), round(y1), round(x2), round(y2)

        confidence = conf
        detected_class = cls
        name = names[int(cls)]

        midx = round(mean((x1, x2)))
        midy = round(mean((y1, y2)))
        print(name, detected_class, confidence, mean((y1, y2)))
        if name in notehead:
            note_list.append(Notehead(name, detected_class, midx, midy, False))
        elif name in rest:
            note_list.append((name, midx))
            
            
    return note_list


def detect_aug(model_name, img):
    config = cp.ConfigParser()
    config.read('config.ini')
    
    model = YOLO(model_name)
    results = model.predict(img, imgsz=config.get('size', 'size'),
                            conf=0.05, iou=0.01, save=True, show_labels=False)

    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    names = results[0].names
    confidences = results[0].boxes.conf.tolist()

    note_list = []
    # Iterate through the results
    for box, cls, conf in zip(boxes, classes, confidences):
        x1, y1, x2, y2 = box
        x1, y1, x2, y2 = round(x1), round(y1), round(x2), round(y2)

        confidence = conf
        detected_class = cls
        name = names[int(cls)]

        midx = round(mean((x1, x2)))
        # midy = round(mean((y1, y2)))
        print(name, detected_class, confidence, mean((y1, y2)))
        if name == "augmentationDot":
            try:
                if note_list[-1][-1] - midx < 5:
                    continue
            except:
                pass
            
            note_list.append((name, midx))
            
    return note_list
import numpy as np
from statistics import mode
import configparser as cp

from ultralytics import YOLO
from statistics import mean

from music21 import *

class Notehead:
    def __init__(self, type, class_no, x, y, aug):
        self.type = type
        self.x = x
        self.y = y
    def __repr__(self):
        return repr((self.type, self.x,
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

def get_duration(all_list, beam_list, flag_list, aug_list):
    dur_note = []
    dur_rest = []
    
    for i in all_list:
        rest = False
        
        if i[0] == 'restDoubleWhole':
            rest = True
            dur = 2
        elif i[0] == 'restWhole':
            rest = True
            dur = 1
        elif i[0] == 'restHalf':
            rest = True
            dur = 0.5
        elif i[0] == 'restQuarter':
            rest = True
            dur = 0.25
        elif i[0] == 'rest8th':
            rest = True
            dur = 0.125
        elif i[0] == 'rest16th':
            rest = True
            dur = 0.0625
        elif i[0] == 'rest32nd':
            rest = True
            dur = 0.03125
        elif i[0] == 'rest64th':
            rest = True
            dur = 0.015625
        elif i[0] == 'rest128th':
            rest = True
            dur = 0.0078125
            
        if rest:
            i.insert(1, dur)
            dur_rest.append(i)
            continue

        if i[0] == 'noteheadDoubleWhole':
            dur = 2
        elif i[0] == 'noteheadWhole':
            dur = 1
        elif i[0] == 'noteheadHalf':
            dur = 0.5
        elif i[0] == 'noteheadBlack':
            flag_dict = {
                'flag8thDown': 0.125,
                'flag8thUp': 0.125,
                'flag16thDown': 0.0625,
                'flag16thUp': 0.0625,
                'flag32ndDown': 0.03125,
                'flag32ndUp': 0.03125,
                'flag64thDown': 0.015625,
                'flag64thUp': 0.015625,
                'flag128thDown': 0.0078125,
                'flag128thUp': 0.0078125
            }
            
            try:
                res = min(flag_list, key=lambda x: abs(i[-1][0] - x[1]))
                if abs(i[-1][0] - res[1]) < 5:
                    dur = flag_dict[res[0]]
                    i.insert(1, dur)
                    dur_note.append(i)
                    continue
            except: pass
            
            dur = 0.25
            for b in beam_list:
                if i[-1][0] in range(b[0]-5, b[1]+5):
                    dur = dur / 2
        
        try:         
            resaug = min(aug_list, key=lambda x: abs(i[-1][0] - x[0]))
            diffaug = resaug[0] - i[-1][0]
            if diffaug < 10 and diffaug > 0:
                dur = dur + (dur/2)
        except: pass
        
        i.insert(1, dur)
        dur_note.append(i)
        
    return dur_note, dur_rest
                    
def get_pitch(staff_notes: dict, all_list, accidental_list, keysig):
    config = cp.ConfigParser()
    config.read('config.ini')
    
    pitch_list = []
    noteheads = ['noteheadDoubleWhole', 'noteheadWhole', 'noteheadHalf', 'noteheadBlack']
    
    acc_dict = {"accidentalDoubleFlat": ["--", set({})],
            "accidentalDoubleSharp": ["##", set({})],
            "accidentalFlat": ["-", set({})],
            "accidentalNatural": ["", set({})],
            "accidentalSharp": ["#", set({})]
        }
    
    keysig_sharp = ['F', 'C', 'G', 'D', 'A', 'E', 'B']
    keysig_flat = ['B', 'E', 'A', 'D', 'G', 'C', 'F']
    
    if keysig > 0:
        for i in range(0, keysig):
            acc_dict["accidentalSharp"][1].add(keysig_sharp[i])
    elif keysig < 0:
        for i in range(0, abs(keysig)):
            acc_dict["accidentalFlat"][1].add(keysig_flat[i])
    
    for symbol in all_list:    
        res = []
        for pos in range(2, len(symbol)):
            posx = symbol[pos][0]
            posy = symbol[pos][1]
        
            res_key, res_val = min(staff_notes.items(), key=lambda y: abs(posy - y[1]))
            
            base_pitch = res_key[0]
            acc = ""
            
            for key, val in acc_dict.items():
                if base_pitch in val[1]:
                    acc = f'{val[0]}'
            
            for acc_index in accidental_list:
                print(int(posx), acc_index[1])
                dif = int(posx) - int(acc_index[1])
                if dif < 10 and dif >= 0:
                    if acc_index[0] == "accidentalNatural":
                        for key, val in acc_dict.items():
                            try:
                                acc_dict[acc_index[0]][1].remove(base_pitch)
                            except: pass
                    
                    print(acc_dict[acc_index[0]][1])
                    acc_dict[acc_index[0]][1].add(base_pitch)
                    acc = acc_dict[acc_index[0]][0]
                    break
            
            res_key = res_key[:1] + f'{acc}' + res_key[1:]
            res.append(res_key)
        
        symbol.insert(1, res)
        pitch_list.append(symbol)

    return pitch_list
    

def detect(model_name, img):
    config = cp.ConfigParser()
    config.read('config.ini')
    
    model = YOLO(model_name)
    results = model.predict(img, imgsz=config.get('size', 'size'),
                            conf=0.05, iou=0.5, save=True, show_labels=False)

    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    names = results[0].names
    confidences = results[0].boxes.conf.tolist()

    note_list = []
    retothers = False
    
    rest_list = []
    acc_list = []
    beam_list = []
    flag_list = []
    # Iterate through the results
    for box, cls, conf in zip(boxes, classes, confidences):
        x1, y1, x2, y2 = box
        x1, y1, x2, y2 = round(x1), round(y1), round(x2), round(y2)

        confidence = conf
        # detected_class = cls
        name = names[int(cls)]

        midx = round(mean((x1, x2)))
        midy = round(mean((y1, y2)))
        
        print(name, midx, confidence)
        
        if model_name == 'weights/notehead.pt':
            chord = False 
            for note_index in range(len(note_list)):
                if abs(note_list[note_index][-1][0] - midx) < 5:
                    note_list[note_index].append([midx, midy])
                    chord = True
                    break
            
            if not chord:
                note_list.append([name, [midx, midy]])
        else:
            retothers = True
            rest = ["rest128th","rest16th","rest32nd","rest64th","rest8th",
                    "restDoubleWhole","restHalf", "restQuarter", 'restWhole']
            accidental = ["accidentalDoubleFlat","accidentalDoubleSharp",
                          "accidentalFlat","accidentalNatural","accidentalSharp"]
            # flags = ["flag128thDown","flag128thUp","flag16thDown","flag16thUp","flag32ndDown","flag32ndUp","flag64thDown","flag64thUp","flag8thDown","flag8thUp",]
            
            if name in rest:
                rest_list.append([name, [midx]])
            elif name in accidental:
                acc_list.append([name, midx])
            elif name == "beam":
                beam_list.append([x1, x2])
            else:
                flag_list.append([name, midx])
                

    if model_name == "weights/others.pt":
        retothers = True
        
    if retothers:
        rest_list = sorted(rest_list, key=lambda x: x[-1][0])
        acc_list = sorted(acc_list, key=lambda x: x[-1])
        beam_list = sorted(beam_list, key=lambda x: x[0])
        flag_list = sorted(flag_list, key=lambda x: x[-1])
        
        return rest_list, acc_list, beam_list, flag_list
    
    note_list = sorted(note_list, key=lambda x: x[-1][0])
    return note_list


def detect_aug(model_name, img):
    config = cp.ConfigParser()
    config.read('config.ini')
    
    model = YOLO(model_name)
    results = model.predict(img, imgsz=config.get('size', 'size'), classes=[21],
                            conf=0.001, iou=0.01, save=True, show_labels=False)

    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    names = results[0].names
    confidences = results[0].boxes.conf.tolist()
    
    aug_list = []
    # Iterate through the results
    for box, cls, conf in zip(boxes, classes, confidences):
        x1, y1, x2, y2 = box
        x1, y1, x2, y2 = round(x1), round(y1), round(x2), round(y2)

        confidence = conf
        # detected_class = cls
        name = names[int(cls)]
        
        print(name, confidence)

        midx = round(mean((x1, x2)))
        midy = round(mean((y1, y2)))
        
        if name == "augmentationDot":     
            chord = False 
            for note_index in range(len(aug_list)):
                dif = aug_list[note_index][0] - midx
                if dif < 5 and dif >= 0:
                    chord = True
                    break
            
            if not chord:
                aug_list.append([midx])

    aug_list = sorted(aug_list, key=lambda x: x[0])
    return aug_list
    
def create_midi(all_list, BPM):
    config = cp.ConfigParser()
    config.read('config.ini')
    
    s = stream.Stream()
    s.append(tempo.MetronomeMark(number=BPM))
    
    rest = ["rest128th","rest16th","rest32nd","rest64th","rest8th",
        "restDoubleWhole","restHalf","restQuarter",'restWhole']
    
    for symbol in all_list:
        name = symbol[0]
        
        if name in rest:
            dur = symbol[1]
            
            r = note.Rest()
            r.duration.quarterLength = dur * 4
            s.append(r)
            continue
        
        dur = symbol[2]
        pitch = symbol[1]
        
        if len(pitch) > 1:
            c = chord.Chord(pitch)
            c.duration.quarterLength = dur * 4
            s.append(c)
        else:
            n = note.Note(pitch[0])
            n.duration.quarterLength = dur * 4
            s.append(n)    

    s.write('midi', fp=f'output/output.mid')
        
    
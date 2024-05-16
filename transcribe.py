import numpy as np
from statistics import mode

notes = {'a0':0, 'b0':0,
         'c1':0, 'd1':0, 'e1':0, 'f1':0, 'g1':0, 'a1':0, 'b1':0,
         'c2':0, 'd2':0, 'e2':0, 'f2':0, 'g2':0, 'a2':0, 'b2':0,
         'c3':0, 'd3':0, 'e3':0, 'f3':0, 'g3':0, 'a3':0, 'b3':0, 
         'c4':0, 'd4':0, 'e4':0, 'f4':0, 'g4':0, 'a4':0, 'b4':0, 
         'c5':0, 'd5':0, 'e5':0, 'f5':0, 'g5':0, 'a5':0, 'b5':0, 
         'c6':0, 'd6':0, 'e6':0, 'f6':0, 'g6':0, 'a6':0, 'b6':0,
         'c7':0, 'd7':0, 'e7':0, 'f7':0, 'g7':0, 'a7':0, 'b7':0,
         'c8':0}

def get_notes(staff_line_pos):
    notes_name_reversed = list(reversed(['c', 'd', 'e', 'f', 'g', 'a', 'b']))

    print(notes_name_reversed)
    
    # treble clef highest default staff on f5   
    start_note = 3 # f
    start_num = 5

    staff_np = np.array(staff_line_pos)
    diff = mode(np.diff(staff_np))

    pos = staff_line_pos[0]
    i = 0
    alt = True

    # negative iteration
    while True:
        try: notes[f'{notes_name_reversed[(start_note + 1) % 7]}{start_num}']
        except: break

        print(f'{notes_name_reversed[start_note]}{start_num}')

        if alt:
            pos_center = pos + (diff // 2)

            notes[f'{notes_name_reversed[start_note]}{start_num}'] = pos
            notes[f'{notes_name_reversed[(start_note + 1) % 7]}{start_num}'] = pos_center

            if i <= 3:
                i += 1
                pos = staff_line_pos[i]
            else:
                pos += diff

        if notes_name_reversed[start_note] == 'c':
            start_num -= 1

        start_note = (start_note + 1) % 7
        if not alt:
            alt = True
        else:
            alt = False

    if notes['a0'] == 0:
        notes['a0'] = pos

    # negative iteration
    # while True:
    #     try: notes[f'{notes_name[start_note]}{start_num - 1}']
    #     except: break

    #     pos_center = pos - diff // 2

    #     notes[f'{notes_name[start_note]}{start_num}'] = pos
    #     notes[f'{notes_name[start_note]}{start_num - 1}'] = pos_center

    #     if i <= 4:
    #         pos = min(staff_line_pos[i], pos - diff)
    #     else:
    #         pos -= diff


    return notes  
notes = {'g3':0, 'a3':0, 'b3':0, 
         'c4':0, 'd4':0, 'e4':0, 'f4':0, 'g4':0, 'a4':0, 'b4':0, 
         'c5':0, 'd5':0, 'e5':0, 'f5':0, 'g5':0, 'a5':0, 'b5':0, 
         'c6':0, 'd6':0, 'e6':0, 'f6':0, 'g6':0, 'a6':0}

def get_notes(staff_line_pos):
    notes = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
    
    # treble clef starts on E4    
    start_note = 2 # e
    start_num = 4

    notes[f'{notes[start_note]}{start_num}'] = staff_line_pos[0]

    while notes[f'{notes[start_note]}{start_num}']:
        pass
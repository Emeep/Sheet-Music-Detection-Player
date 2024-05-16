notes_name = ['c', 'd', 'e', 'f', 'g', 'a', 'b']

start_note = 4 # g

while True:
    print(notes_name[start_note])

    start_note  = (start_note + 1) % 7
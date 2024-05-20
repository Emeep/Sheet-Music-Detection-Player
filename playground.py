from mido import *
import configparser as cp

def create_midi(notes, filename):
    config = cp.ConfigParser()
    config.read('config.ini')

    # Create a new MIDI file
    mid = MidiFile()

    # Create a track
    track = MidiTrack()
    mid.tracks.append(track)

    # Default tempo (adjustable if needed)
    tempo = (60000 / (int(config.get('midi', 'BPM')))) * 4  # from quarter note BPM to ms per quarter note
    track.append(MetaMessage('set_tempo', tempo=round(tempo)))

    for chord in notes:
        # Check if it's a chord or single note
        if isinstance(chord[0], list):  # If it's a chord
            for note_name in chord[0]:
                # Convert note name to MIDI pitch number (C4 = 60)
                pitch = 60 + (note_name.find('C') - 3) + (len(note_name) - 1) * 12

                # Create note on and off messages for each note in the chord
                velo = config.get('midi', 'velocity')
                track.append(Message('note_on', note=pitch, velocity=int(velo), time=0))
                track.append(Message('note_off', note=pitch, velocity=int(velo), time=int(chord[1] * 480000)))
        else:  # If it's a single note
            note_name = chord[0]
            # Extract duration if provided, otherwise default to a quarter note
            duration = chord[1] if len(chord) > 1 else 0.25

            # Convert note name to MIDI pitch number (C4 = 60)
            pitch = 60 + (note_name.find('C') - 3) + (len(note_name) - 1) * 12

            # Create note on and off messages
            velo = config.get('midi', 'velocity')
            track.append(Message('note_on', note=pitch, velocity=int(velo), time=0))
            track.append(Message('note_off', note=pitch, velocity=int(velo), time=int(duration * 480000)))

    # Save the MIDI file
    mid.save(f'output/{filename}')

# Example usage
notes = [["C4"], [["C5", "D5"], 0.5], ["D5", 1]]
create_midi(notes, "my_song1.mid")
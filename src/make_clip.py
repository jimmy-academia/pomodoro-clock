import keyboard
import subprocess
from pathlib import Path
from pydub import AudioSegment


# work_song = '/Users/jimmyyeh/Documents/Music/we_are_standing.mp3'
# work_clip = 'work.mp3'
rest_song = '/Users/jimmyyeh/Documents/Music/Christopher_Tin_Waloyo_Yamoni.mp3'
rest_clip = 'rest.mp3'

if not Path(rest_clip).exists():
    print('making rest_clip!')
    audio = AudioSegment.from_file(rest_song)
    play_time = 120 # 30 seconds
    fade_time = 12
    play_audio = audio[:play_time*1000]
    play_audio = play_audio.fade_out(fade_time*1000)
    play_audio.export(rest_clip, format="mp3")

print('done')
# print('test play')
# # subprocess.run(["ffmpeg", "-i", path, "-ss", "00:00:00", "-t", f"00:{mm}:{ss}", "-c", "copy", path_short])

# process = subprocess.Popen(["afplay", work_clip])
# while process.poll() is None:
#     event = keyboard.read_event()
#     if event.event_type == "down":
#         print(f"Key {event.name} was pressed")
#         print('this stopped the alarm')
#         process.kill()
# process.kill()



# for path, path_short, playtime in zip([args.path_work, args.path_rest], [path_work_alarm_short, path_rest_alarm_short], [args.work_playtime, args.rest_playtime]):
#     print(f'copy short version alarm if not exists at {path_short}')
#     if not path_short.exists():
#         mm = f'{playtime//60:02d}'
#         ss = f'{playtime%60:02d}'
#         subprocess.run(["ffmpeg", "-i", path, "-ss", "00:00:00", "-t", f"00:{mm}:{ss}", "-c", "copy", path_short])

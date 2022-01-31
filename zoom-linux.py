# zoom.sh converted to work with linux by Musiz#1215
# Example "Zoom" movie generation
# e.g. py zoom.py "A painting of zooming in to a surreal, alien world" Zoom.png 180 25

from sys import argv
from random import randint
from os import system
from shutil import copyfile
import requests
import subprocess

TEXT = argv[1]
FILENAME = argv[2]
MAX_EPOCHS = argv[3]
MAX_ITERATIONS = argv[4]
padded_count = 0
spacer = "###############"

url = "PUT DISCORD WEBHOOK URL HERE!!! PUT DISCORD WEBHOOK URL HERE!!! PUT DISCORD WEBHOOK URL HERE!!!"

LR = 0.1
OPTIMISER = "Adam"
SEED = randint(1, 9999999999) # Keep the same seed each epoch for more deterministic runs

FILENAME_NO_EXT = FILENAME.split('.')[0]
FILE_EXTENSION = FILENAME.split('.')[1]

# Initial run
system(f'mkdir Zoom/{FILENAME_NO_EXT}')
system(f'python generate.py -p="{TEXT}" -opt="{OPTIMISER}" -lr={LR} -i={MAX_ITERATIONS} -se={MAX_ITERATIONS} --seed={SEED} -o="Zoom/{FILENAME_NO_EXT}/{FILENAME}"')
copyfile(f'Zoom/{FILENAME_NO_EXT}/{FILENAME}', f'Zoom/{FILENAME_NO_EXT}/{FILENAME_NO_EXT}-0000.{FILE_EXTENSION}')

# Initial distort

# img = Image.open(f'Zoom/{FILENAME_NO_EXT}/{FILENAME}')
# width, height = img.size
# left = top = 4
# right = width - 4
# bottom = height - 4
# img = img.crop((left, top, right, bottom)) # crop image
# img = img.rotate(2) # rotate image
# img = img.save(f'Zoom/{FILENAME_NO_EXT}/{FILENAME}')

system(f'convert Zoom/{FILENAME_NO_EXT}/{FILENAME} -distort SRT 1.01,0 -gravity center Zoom/{FILENAME_NO_EXT}/{FILENAME}') # zoom
system(f'convert Zoom/{FILENAME_NO_EXT}/{FILENAME} -distort SRT 1 -gravity center Zoom/{FILENAME_NO_EXT}/{FILENAME}') # rotate

# Feedback image loop

for i in range(int(MAX_EPOCHS)):
    padded_count += 1
    print(f'{spacer} {padded_count} {spacer}')
    system(f'python generate.py -p="{TEXT}" -opt="{OPTIMISER}" -lr={LR} -i={MAX_ITERATIONS} -se={MAX_ITERATIONS} --seed={SEED} -ii="Zoom/{FILENAME_NO_EXT}/{FILENAME}" -o="Zoom/{FILENAME_NO_EXT}/{FILENAME}"')
    copyfile(f'Zoom/{FILENAME_NO_EXT}/{FILENAME}', f'Zoom/{FILENAME_NO_EXT}/{FILENAME_NO_EXT}-{padded_count}.{FILE_EXTENSION}')

    system(f'convert Zoom/{FILENAME_NO_EXT}/{FILENAME} -distort SRT 1.01,0 -gravity center Zoom/{FILENAME_NO_EXT}/{FILENAME}') # zoom
    system(f'convert Zoom/{FILENAME_NO_EXT}/{FILENAME} -distort SRT 1 -gravity center Zoom/{FILENAME_NO_EXT}/{FILENAME}') # rotate

# zip and upload to https://transfer.sh

system(f'zip {FILENAME_NO_EXT}.zip Zoom/{FILENAME_NO_EXT}/*')

link = subprocess.check_output([f'curl --upload-file Zoom/{FILENAME_NO_EXT}/{FILENAME_NO_EXT}.zip https://transfer.sh/{FILENAME_NO_EXT}'])

# send data over webhook

data = {
    "content" : link,
    "username" : "VQGAN+CLIP VPS RETURN"
}
result = requests.post(url, json = data)
# convert to mp4 with ffmpeg

# system(f'ffmpeg -r 24 -f image2 -i Zoom/{FILENAME_NO_EXT}/{FILENAME_NO_EXT}-%d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p output/{FILENAME_NO_EXT}.mp4')

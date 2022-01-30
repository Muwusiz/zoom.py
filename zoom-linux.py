from sys import argv
from random import randint
from os import system
from shutil import copyfile
from PIL import Image
from scipy import ndimage, misc

TEXT = argv[1]
FILENAME = argv[2]
MAX_EPOCHS = argv[3]
MAX_ITERATIONS = argv[4]
padded_count = 0
spacer = "###############"

LR = 0.1
OPTIMISER = "Adam"
SEED = randint(1, 9999999999) # Keep the same seed each epoch for more deterministic runs

FILENAME_NO_EXT = FILENAME.split('.')[0]
FILE_EXTENSION = FILENAME.split('.')[1]

# Initial run
system(f'mkdir Zoom\{FILENAME_NO_EXT}')
system(f'python generate.py -p="{TEXT}" -opt="{OPTIMISER}" -lr={LR} -i={MAX_ITERATIONS} -se={MAX_ITERATIONS} --seed={SEED} -o="Zoom/{FILENAME_NO_EXT}/{FILENAME}"')
copyfile(f'Zoom/{FILENAME_NO_EXT}/{FILENAME}', f'Zoom/{FILENAME_NO_EXT}/{FILENAME_NO_EXT}-0000.{FILE_EXTENSION}')

# Initial distort

img = Image.open(f'Zoom/{FILENAME_NO_EXT}/{FILENAME}')
width, height = img.size
left = top = 4
right = width - 4
bottom = height - 4
img = img.crop((left, top, right, bottom)) # crop image
img = img.rotate(2) # rotate image
img = img.save(f'Zoom/{FILENAME_NO_EXT}/{FILENAME}')

# Feedback image loop

for i in range(int(MAX_EPOCHS)):
    padded_count += 1
    print(f'{spacer} {padded_count} {spacer}')
    system(f'python generate.py -p="{TEXT}" -opt="{OPTIMISER}" -lr={LR} -i={MAX_ITERATIONS} -se={MAX_ITERATIONS} --seed={SEED} -ii="Zoom/{FILENAME_NO_EXT}/{FILENAME}" -o="Zoom/{FILENAME_NO_EXT}/{FILENAME}"')
    copyfile(f'Zoom/{FILENAME_NO_EXT}/{FILENAME}', f'Zoom/{FILENAME_NO_EXT}/{FILENAME_NO_EXT}-{padded_count}.{FILE_EXTENSION}')
    img = Image.open(f'Zoom/{FILENAME_NO_EXT}/{FILENAME}')
    width, height = img.size
    left = top = 4
    right = width - 4
    bottom = height - 4
    img = img.crop((left, top, right, bottom)) # crop image
    img = img.rotate(2) # rotate image
    img = img.save(f'Zoom/{FILENAME_NO_EXT}/{FILENAME}')

# convert to mp4 with ffmpeg

system(f'ffmpeg -r 24 -f image2 -i Zoom/{FILENAME_NO_EXT}/{FILENAME_NO_EXT}-%d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p output/{FILENAME_NO_EXT}.mp4')

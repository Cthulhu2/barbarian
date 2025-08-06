#!/usr/bin/env python3
import subprocess
from pathlib import Path
from PIL import Image


def find_crop_top(img: Image, px):
    for y in range(img.height):
        for x in range(img.width):
            px_ = px[x, y]
            if px_ != 0:
                return y
    return 0


def find_crop_left(img: Image, px):
    for x in range(img.width):
        for y in range(img.height):
            px_ = px[x, y]
            if px_ != 0:
                return x
    return 0


def find_crop_right(img: Image, px):
    for x in range(img.width - 1):
        for y in range(img.height):
            px_ = px[img.width - x - 1, y]
            if px_ != 0:
                return img.width - x
    return img.width


def find_crop_bottom(img: Image, px):
    for y in range(img.height - 1):
        for x in range(img.width):
            px_ = px[x, img.height - y - 1]
            if px_ != 0:
                return img.height - y
    return img.height


def crop(filename: Path, same_output):
    with Image.open(filename) as img:
        width = img.width
        height = img.height
        px = img.load()
        box = (find_crop_left(img, px), find_crop_top(img, px),
               find_crop_right(img, px), find_crop_bottom(img, px))

        info = img.info
        img = img.crop(box)
        box = (box[0], box[1], width - box[2], height - box[3])
        if not same_output:
            output = filename.with_stem(filename.stem + '-' + '-'.join([str(_) for _ in box]))
        else:
            output = filename
        img.save(output, save_all=False, optimize=True, palette=img.palette, **info)
    subprocess.run(['gifsicle', '-o', output, output])


if __name__ == '__main__':
    for f in Path('barbariantuw/img/spritesA/').glob('genou*.gif'):
        crop(f, False)
    for i in range(8):
        for f in Path(f'barbariantuw/img/spritesB/spritesB{i}').glob('genou*.gif'):
            crop(f, True)

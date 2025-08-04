#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
from typing import List

from PIL import Image


def ss(output: str, filenames: List[Path]):
    with Image.new('RGBA', (1, 1)) as dest:
        max_width = 0
        max_height = 0
        box = (0, 0, 0, 0)
        for filename in filenames:
            with Image.open(filename) as img:
                max_width += img.width
                max_height = max(max_height, img.height)

        dest = dest.resize((max_width, max_height))
        for filename in filenames:
            with Image.open(filename) as img:
                box = (box[0], box[1],
                       box[0] + img.width, img.height)
                dest.paste(img, box)
                print(box)
                box = (box[0] + img.width, box[1],
                       0, box[1])
        dest.save(output, save_all=False, optimize=True, **img.info)
    subprocess.run(['gifsicle', '-o', output, output])


if __name__ == '__main__':
    ss_path = Path('barbariantuw/img/spritesA/attente.gif')
    os.remove(ss_path)
    ss(ss_path, sorted(list(Path('barbariantuw/img/spritesA/')
                            .glob('attente*.gif'))))
    for i in range(8):
        ss_path = Path(f'barbariantuw/img/spritesB/spritesB{i}/attente.gif')
        os.remove(ss_path)
        ss(ss_path, sorted(list(Path(f'barbariantuw/img/spritesB/spritesB{i}')
                                .glob('attente*.gif'))))

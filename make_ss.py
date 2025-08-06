#!/usr/bin/env python3
import json
import os
from pathlib import Path
from typing import List, Tuple, Optional

from PIL import Image


class SkylinePacker:
    def __init__(self, width: int):
        self.width = width
        self.skyline: List[Tuple[int, int, int]] = [(0, width, 0)]

    def find_position(self, w: int, h: int) -> Optional[Tuple[int, int]]:
        best_x, best_y = None, None
        min_y = float('inf')

        for x, seg_width, seg_height in self.skyline:
            if seg_width >= w:
                if seg_height < min_y:
                    min_y = seg_height
                    best_x = x
                    best_y = seg_height

        if best_x is not None:
            return best_x, best_y
        return None

    def update_skyline(self, x: int, y: int, w: int, h: int):
        new_skyline = []
        sprite_right = x + w
        sprite_top = y + h

        for seg_x, seg_w, seg_h in self.skyline:
            seg_right = seg_x + seg_w

            if seg_right <= x or seg_x >= sprite_right:
                new_skyline.append((seg_x, seg_w, seg_h))
            else:
                if seg_x < x:
                    new_skyline.append((seg_x, x - seg_x, seg_h))
                if seg_right > sprite_right:
                    new_skyline.append((sprite_right, seg_right - sprite_right, seg_h))
                new_skyline.append((x, w, sprite_top))

        merged = []
        for seg in new_skyline:
            if not merged:
                merged.append(seg)
                continue
            last = merged[-1]
            if last[1] == 0:
                continue
            if last[2] == seg[2] and last[0] + last[1] == seg[0]:
                merged[-1] = (last[0], last[1] + seg[1], last[2])
            else:
                merged.append(seg)
        merged.sort(key=lambda s: s[0])
        self.skyline = merged

    def get_height(self) -> int:
        return max((h for _, _, h in self.skyline), default=0)

    def get_width(self) -> int:
        return self.width


def pack_sprites_skyline(
    frames: List[Path],
    output_image: str,
    output_json: str,
    max_width: int = 860,
    max_height: int = 1024
):
    sprites = []
    for f in frames:
        img = Image.open(f)
        img.name = f.name
        sprites.append(img)

    sprites.sort(key=lambda sprite: (-sprite.height, -sprite.width))

    packer = SkylinePacker(max_width)

    sprite_data = {}
    used_sprites = []

    for s in sprites:
        pos = packer.find_position(s.width, s.height)
        if pos is None:
            print(f"No {s.name} ({s.width}x{s.height})")
            continue

        x, y = pos
        if y + s.height > max_height:
            print(f"No height {s.name}")
            continue

        packer.update_skyline(x, y, s.width, s.height)

        sprite_data[s.name] = {'x': x, 'y': y, 'w': s.width, 'h': s.height}
        used_sprites.append(s)

    total_width = max_width
    total_height = packer.get_height()

    with Image.new('RGBA', (total_width, total_height), (0, 0, 0, 0)) as atlas:
        for s in used_sprites:
            rect = sprite_data[s.name]
            atlas.paste(s, (rect['x'], rect['y']))
        atlas.save(output_image)

    metadata = {
        "width": total_width,
        "height": total_height,
        "sprites": sprite_data
    }
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)


if __name__ == "__main__":
    ssA_path = Path('barbariantuw/img/spritesA.gif')
    if ssA_path.exists():
        os.remove(ssA_path)
    ssA_frames = sorted(list(Path('barbariantuw/img/spritesA/').glob('*.gif')))

    pack_sprites_skyline(ssA_frames, ssA_path, ssA_path.with_name('spritesA.json'))

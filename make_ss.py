#!/usr/bin/env python3
import ast
import os
from pathlib import Path
from typing import List, Tuple, Optional

from PIL import Image
from pygame import Rect


class SkylinePacker:
    def __init__(self, width: int):
        self.width = width
        self.skyline: List[Tuple[int, int, int]] = [(0, width, 0)]

    def find_position(self, w: int, h: int) -> Optional[Tuple[int, int]]:
        best_x, best_y = None, None
        min_y = float('inf')

        for seg_x, seg_w, seg_y in self.skyline:
            if seg_w >= w and seg_y < min_y:
                min_y = seg_y
                best_x = seg_x
                best_y = seg_y

        if best_x is not None:
            return best_x, best_y
        return None

    def update_skyline(self, x: int, y: int, w: int, h: int):
        new_skyline = []
        sprite_right = x + w
        sprite_top = y + h

        for seg_x, seg_w, seg_y in self.skyline:
            seg_right = seg_x + seg_w

            if seg_right <= x or seg_x >= sprite_right:
                new_skyline.append((seg_x, seg_w, seg_y))
            else:
                if seg_x < x:
                    new_skyline.append((seg_x, x - seg_x, seg_y))
                if seg_right > sprite_right:
                    new_skyline.append((sprite_right, seg_right - sprite_right, seg_y))
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
        return max((y for _, _, y in self.skyline), default=0)

    def get_width(self) -> int:
        return self.width


def pack_sprites_skyline(
        frames: List[Path],
        output: Path,
        max_width: int = 994,
        max_height: int = 2048
):
    sprites = []
    for frame in frames:
        img = Image.open(frame)
        img.name = frame.stem
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

        sprite_data[s.name] = Rect(x, y, s.width, s.height)
        used_sprites.append(s)

    total_width = max_width
    total_height = packer.get_height()

    with Image.new('RGBA', (total_width, total_height), (0, 0, 0, 0)) as atlas:
        for s in used_sprites:
            rect = sprite_data[s.name]
            atlas.paste(s, (rect[0], rect[1]))
        atlas.save(output)

    class_def = ast.ClassDef(output.stem, [], keywords=[], body=[
        ast.Assign([ast.Name(name.upper(), ast.Store())],
                   value=ast.Constant(value, name))
        for name, value in sorted(sprite_data.items())
        if not name.startswith('__') and not callable(value)
    ], decorator_list=[])
    ast.fix_missing_locations(class_def)
    return ast.unparse(class_def)


if __name__ == "__main__":
    ssA_path = Path('barbariantuw/img/spritesA.gif')
    if ssA_path.exists():
        os.remove(ssA_path)
    ssA_frames = sorted(list(Path('barbariantuw/img/spritesA/')
                             .glob('*.gif')))
    class_defs = [pack_sprites_skyline(ssA_frames, ssA_path)]

    for i in range(8):
        ssB_path = Path(f'barbariantuw/img/spritesB{i}.gif')
        if ssB_path.exists():
            os.remove(ssB_path)
        ssB_frames = sorted(list(Path(f'barbariantuw/img/spritesB/spritesB{i}')
                                 .glob('*.gif')))
        class_defs.append(pack_sprites_skyline(ssB_frames, ssB_path))

    sorted(class_defs)
    ss_py = Path('barbariantuw/spritesheets.py')
    with open(ss_py, 'w', encoding='utf-8') as f:
        f.write('\n'.join(('# GENERATED SPRITES SOURCE RECTS',
                           '# DO NOT EDIT MANUALLY',
                           'from pygame import Rect',
                           '\n\n')))
        f.write('\n\n\n'.join(class_defs))
        f.write('\n')

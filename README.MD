# Barbarian - The Ultimate Warrior

Amiga 500 game remake written in Python and [PyGame CE][0].

## Installation

### Linux
_TODO: Linux executable_

### Windows
_TODO: Windows executable_

### Pip
_TODO: PIP package_

## Controls

* `ESC` - close window and exit

|           | Player 1             | Player 2 |
|-----------|----------------------|----------|
| **LEFT**  | `Left`, `Numpad 4`   | `J`      |
| **RIGHT** | `Right`, `Numpad 6`  | `L`      |
| **UP**    | `Up`, `Numpad 8`     | `I`      |
| **DOWN**  | `Down`, `Numpad 2`   | `K`      |
| **FIRE**  | `RShift`, `Numpad 0` | `Space`  |

## Credits

* Font "PressStart2P". Thanks very much to [CodeMan38][1] for a fonts.
  Also see [SIL OPEN FONT LICENSE Version 1.1][2]
* Thanks very much to [F.L.][3] for BASIC source code of Barbarian.

## Links

* [PyGame CE][0]
* [F.L. remakes][3]

[0]: https://pyga.me/
[1]: https://github.com/codeman38
[2]: barbariantuw/fnt/OFL.txt?raw=true
[3]: http://barbarian.1987.free.fr/indexEN.htm

## Build

Clone repo:
```shell
$ git clone https://codeberg.org/cthulhu/barbarian.git
```
Create virtual environment:
```shell
$ cd barbarian
$ python3 -m venv .venv
$ source .venv/bin/activate
```
Install dev-dependencies:
```shell
(.venv) $ pip install .[dev]
(.venv) $ pip install git+https://github.com/AppImageCrafters/appimage-builder.git
```
### PIP
Package for pypi.org:
```shell
(.venv) $ python3 -m build
```

### PygBag
WebAssembly zip-archive for itch.io:
```shell
(.venv) $ rm -rf pygbag/barbariantuw/* \
  && cp -r barbariantuw pygbag \
  && pygbag --archive pygbag
```

### Nuitka and AppImage
Executable AppImage:
```shell
(.venv) $ python3 -m nuitka --standalone \
  --include-data-dir=barbariantuw/fnt=barbariantuw/fnt \
  --include-data-dir=barbariantuw/img=barbariantuw/img \
  --include-data-dir=barbariantuw/snd=barbariantuw/snd \
  --include-data-dir=AppImage=. \
  barbariantuw
  
(.venv) $ appimage-builder --recipe AppImageBuilder.yml
```

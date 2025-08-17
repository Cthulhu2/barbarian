# Barbarian - The Ultimate Warrior

Amiga 500 game remake written in Python and [PyGame CE][0].

![preview](https://codeberg.org/cthulhu/barbarian/raw/branch/master/readme/preview.png)
<video src="https://codeberg.org/cthulhu/barbarian/raw/branch/master/readme/demo.mp4"
       width="640" height="480" controls>
</video>

## Installation

### Linux
Download executable from [releases](https://codeberg.org/cthulhu/barbarian/releases).

### Windows
Download executable from [releases](https://codeberg.org/cthulhu/barbarian/releases).

### PIP
```shell
pip install barbariantuw
```
Launch:
```shell
barbariantuw
```

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

### Nuitka
To reduce output filesize use virtual environment with nuitka package only.
```shell
$ python3 -m venv .venv-nuitka
$ source .venv-nuitka/bin/activate
(.venv-nuitka) $ pip install .[nuitka]
```
Executable:
```shell
(.venv-nuitka) $ python3 -m build_nuitka
```

## Profiling
Memory:
```shell
(.venv) $ rm barbariantuw.bin
(.venv) $ python3 -m memray run -o barbariantuw.bin -m barbariantuw
(.venv) $ python3 -m memray flamegraph barbariantuw.bin
(.venv) $ <browser> memray-flamegraph-barbariantuw.html
```
> NOTE: memray not available on Windows

CPU:
```shell
(.venv) $ python -m cProfile -o barbariantuw.prof -m barbariantuw
(.venv) $ snakeviz barbariantuw.prof
```

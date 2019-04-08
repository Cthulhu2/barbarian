Barbarian
=========

This is **'Barbarian -- The Ultimate Warrior'** game clone written in Python and [PyGame](https://www.pygame.org).
It's in progress. In fact, it has two scenes only:
* Some kind of battle with stupid AI. [barbarian.battle.demo.webm (~180Kb)](https://github.com/Cthulhu2/barbarian/blob/master/readme/barbarian.battle.demo.webm?raw=true)
* An animation viewer. [barbarian.anim-viewer.demo.webm (~600Kb)](https://github.com/Cthulhu2/barbarian/blob/master/readme/barbarian.anim-viewer.demo.webm?raw=true)


Installation
------------

After clone the project you needs to install some pre-requisites:

* At first you need [Python3](https://www.python.org/downloads/) interpreter (3.5 or better?).

* There is [psutil](https://pypi.org/project/psutil/) used in this project and it may require [python3-devel](https://github.com/giampaolo/psutil/issues/1143) package installed on Linux systems;

* The _PyGame_ framework and _psutil_ can be installed with [pip](https://pip.pypa.io/en/stable/installing/) and _requirements.txt_ file:
  
  ```pip install -r requirements.txt```

Launch
------

In project directory you can start battle scene:

```python3 src/main.py```

Or animation viewer scene:

```python3 srs/main.py -v```

`-d` -- debug options shows FPS, CPU and memory usage info.


There are keys to control the left barbarian used in battle scene:
* `6` -- left
* `7` -- right
* `8` -- up
* `9` -- down
* `0` -- fire
* `ESC` -- close window and exit

Credits
-------
* Art. Thanks very much to [Jicehel](https://www.deviantart.com/jicehel/) for 2D sprites. If you want use this art in other projects please ask [Jicehel](https://www.deviantart.com/jicehel/) first.
* Font. "PressStart2P". Thanks very much to [CodeMan38](https://github.com/codeman38) for a fonts. Also see [SIL OPEN FONT LICENSE Version 1.1](https://github.com/Cthulhu2/barbarian/blob/master/resources/font/OFL.txt?raw=true)
* Source code are provided under [MIT](https://github.com/Cthulhu2/barbarian/blob/master/LICENSE?raw=tru) licence.

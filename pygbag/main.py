import platform
import barbariantuw.__main__

platform.window.canvas.style.imageRendering = "pixelated"
# pygbag `main.py` needs to be in parent package for barbariantuw.
# separate directory for excluding root files in WASM zip
# (README.MD, pyproject.toml etc)
barbariantuw.__main__.run()

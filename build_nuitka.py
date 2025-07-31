#!/usr/bin/env python3
import subprocess
import sys

from nuitka.utils.Utils import getArchitecture

from barbariantuw import __version__, PROG

arch = getArchitecture()


def main():
    nuitka_args = [
        f'--product-name={PROG}',
        f'--product-version={__version__}',
        '--file-description=\'Barbarian - The Ultimate Warrior\' game clone',
        '--onefile',
        '--onefile-tempdir-spec={CACHE_DIR}/{PRODUCT}/{VERSION}',
        '--noinclude-setuptools-mode=nofollow',
        '--noinclude-unittest-mode=nofollow',
        '--noinclude-pytest-mode=nofollow',
        '--include-data-dir=barbariantuw/fnt=barbariantuw/fnt',
        '--include-data-dir=barbariantuw/img=barbariantuw/img',
        '--include-data-dir=barbariantuw/snd=barbariantuw/snd',
    ]
    # TODO: Linux/Windows-icon
    if sys.platform == "linux":
        nuitka_args.extend([
            '--linux-icon=barbariantuw/img/menu/icone.gif',
            f'--output-filename={PROG}-{__version__}_linux_{arch}.bin',
        ])
    elif sys.platform == "windows":
        nuitka_args.extend([
            '--windows-icon-from-ico=barbariantuw/img/menu/icone.gif',
            '--windows-console-mode=disable',
            f'--output-filename=barbariantuw-{__version__}_win_{arch}.exe',
        ])
    subprocess.run([
        'nuitka', *nuitka_args, 'barbariantuw'
    ], check=True)


if __name__ == "__main__":
    main()

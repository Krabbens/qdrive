import os
import sys
import colorama

def launch():
    print(colorama.Fore.GREEN + 'Starting pipeline...')
    pipeline = [
        #'build_shaders.py',
        'main.py'
    ]
    for script in pipeline:
        print(colorama.Fore.LIGHTCYAN_EX + 'Running ' + script)
        os.system(sys.executable + ' ' + script)


if __name__ == '__main__':
    launch()
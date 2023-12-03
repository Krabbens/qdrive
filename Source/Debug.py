import colorama
import sys
import inspect
from PyQt5.QtCore import QThread

class Debug:
    main_thread_id = None

    def __init__(self, level="d"):
        self.debug = len(sys.argv) > 1 and "d" in sys.argv[1]
        self.is_worker = int(QThread.currentThreadId()) != self.main_thread_id
        self.colors = [
            colorama.Fore.LIGHTRED_EX,
            colorama.Fore.RED,
            colorama.Fore.BLUE,
            colorama.Fore.GREEN,
            colorama.Fore.RESET,
        ]
        self.level = "t" if self.is_worker and "t" in sys.argv[1] else level
        self.levels = {
            "d" : colorama.Fore.LIGHTRED_EX + "[debug] ",
            "t" : colorama.Fore.LIGHTBLUE_EX + "[thread " + str(int(QThread.currentThreadId()))[:3] + "] ",
            "vv" : colorama.Fore.LIGHTYELLOW_EX + "[vv] ",
            "vvv" : colorama.Fore.RED + "[vvv] ",
        }

    def __call__(self, *args, **kwargs):
        if self.debug and self.level in sys.argv[1]:
            stack = inspect.stack()
            caller_cls = stack[1][0].f_locals["self"].__class__.__name__
            caller_method = stack[1][0].f_code.co_name
            print(
                self.levels[self.level]
                + self.colors[0]
                + caller_cls
                + self.colors[-1]
                + "."
                + self.colors[1]
                + caller_method
                + " ",
                end="",
            )
            for i in range(len(args) - 1):
                print(self.colors[i + 2] + str(args[i]), end=" ")
            print(self.colors[-1] + str(args[-1]), end="")
            print(colorama.Fore.RESET)

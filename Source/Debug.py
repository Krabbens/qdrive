import colorama
import sys
import inspect


class Debug:
    def __init__(self, level=0):
        self.debug = len(sys.argv) > 1 and sys.argv[1] == "--debug"
        self.colors = [
            colorama.Fore.LIGHTRED_EX,
            colorama.Fore.RED,
            colorama.Fore.BLUE,
            colorama.Fore.GREEN,
            colorama.Fore.RESET,
        ]
        self.level = level
        self.levels = [
            colorama.Fore.LIGHTRED_EX + "[debug] ",
            colorama.Fore.LIGHTBLUE_EX + "[info] ",
            colorama.Fore.LIGHTYELLOW_EX + "[warning] ",
            colorama.Fore.RED + "[error] ",
        ]

    def __call__(self, *args, **kwargs):
        if self.debug:
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
                print(self.colors[i + 2] + str(args[i]), end="")
            print(self.colors[-1] + str(args[-1]), end="")
            print(colorama.Fore.RESET)

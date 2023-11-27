from PyQt5.QtCore import QThread
from Source.Thread import Thread
from Source.ThreadCallback import ThreadCallback as TC
import colorama
import sys

debug = len(sys.argv) > 1 and sys.argv[1] == '--debug'

class ThreadWrapper(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.threads = {}        

    def manageThread(self, funcName):
        if funcName in self.threads:
            self.threads[funcName].throw()
            self.threads.pop(funcName)

    def getInstance(self, variables, target):
        className = target.__qualname__.split(".")[0]
        for var in variables.values():
            if type(var).__name__ == className:
                return var
        return self

    def future(*args, **kwargs):
        def decorator(func):
            def wrap(self, *_args):
                self.manageThread(func.__name__)
                if debug:
                    print(colorama.Fore.LIGHTRED_EX + "[debug] " + colorama.Fore.GREEN + "ThreadWrapper.future: " + colorama.Fore.RESET + func.__name__)
                    print(colorama.Fore.LIGHTRED_EX + "[debug] " + colorama.Fore.GREEN + "Args: " + colorama.Fore.RESET + str(_args))
                targetSelf = self.getInstance(vars(self), kwargs["target"])
                if "callback" in kwargs:
                    callbackSelf = self.getInstance(vars(self), kwargs["callback"])
                funcArgs = [kwargs["target"]]
                funcArgs.append(targetSelf)
                funcArgs.extend(_args)
                if debug:
                    print(colorama.Fore.LIGHTRED_EX + "[debug] " + colorama.Fore.GREEN + "FuncArgs: " + colorama.Fore.RESET + str(funcArgs))
                t = Thread(funcArgs, func.__name__)
                if "callback" in kwargs:
                    t.threadSignal.connect(getattr(callbackSelf, kwargs["callback"].__name__))
                t.quitSignal.connect(self.manageThread)
                self.threads[func.__name__] = t
                t.start()
            wrap.__name__ = func.__name__
            return wrap
        return decorator

    def future_callback(*args, **kwargs):
        def decorator(func):
            def wrap(self, *_args):
                self.manageThread(func.__name__)
                print("ThreadWrapper.future:", func.__name__)
                targetSelf = self.getInstance(vars(self), kwargs["target"])
                callbackSelf = self.getInstance(vars(self), kwargs["callback"])
                funcArgs = [kwargs["target"]]
                funcArgs.append(targetSelf)
                funcArgs.extend(_args)
                t = TC(funcArgs, func.__name__)
                t.threadSignal.connect(getattr(callbackSelf, kwargs["callback"].__name__))
                t.quitSignal.connect(self.manageThread)
                self.threads[func.__name__] = t
                t.start()
            wrap.__name__ = func.__name__
            return wrap
        return decorator
    
    future = staticmethod(future)
    future_callback = staticmethod(future_callback)
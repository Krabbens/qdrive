from PyQt5.QtCore import QThread
from Source.Thread.Thread import Thread
from Source.Thread.ThreadCallback import ThreadCallback as TC
from Source.Debug import Debug
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
                Debug()("Run:", func.__name__)
                targetSelf = self.getInstance(vars(self), kwargs["target"])
                if "callback" in kwargs:
                    callbackSelf = self.getInstance(vars(self), kwargs["callback"])
                funcArgs = [kwargs["target"]]
                funcArgs.append(targetSelf)
                funcArgs.extend(_args)
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
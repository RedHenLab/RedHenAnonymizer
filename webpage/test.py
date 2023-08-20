import os
from background_runner import BackgroundRunner
from flask_executor import Executor



if __name__=="__main__":
    hider=BackgroundRunner(Executor)
    hider.do_task()
    print("Done")
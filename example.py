from mrrobot.catcher import Catcher
from mrrobot.logger import FileLogger


l = FileLogger(filename="output.txt",
               buffer_size=8)

c = Catcher(logger=l)
c.run()

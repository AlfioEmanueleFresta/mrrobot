import os
import platform

system = platform.system()

if 'Windows' in system:
    from .catchers.windows import Catcher

elif 'Linux' in system:
    from .catchers.linux import Catcher

elif 'Mac' in system:
    from .catchers.mac import Catcher

else:
    raise NotImplementedError("Sorry, there is no key catcher available for your platform ('%s')." % system)

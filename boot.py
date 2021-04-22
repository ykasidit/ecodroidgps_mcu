# cant run in linux python
# pylint: disable=E0401

import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
#import webrepl
#webrepl.start()
import gc
gc.collect()

from killerbee import *

# Inspired by code in zbwireshark
with KillerBee() as kb:
    try: 
        kb.set_channel(20,)
    except:
        print("Error setting channel")
        sys.exit(1)
    kb.sniffer_on()
    while (True):
        data = kb.pnext()
        if data != None:
            print(data)

from subprocess import Popen
import time
#Popen(["python","HFTv1/sarp_simulator.py","CRVUSDT","30"]) 
Popen(["python","sarp_simulator.py", "XRPUSDT","28"])
#Popen(["python","HFTv1/sarp_simulator.py", "ETHUSDT","0.02"])
#Popen(["python","HFTv1/sarp_simulator.py", "AAVEUSDT","0.01"])
#Popen(["python","HFTv1/sarp_simulator.py", "ATOMUSDT","2"])
#Popen(["python","HFTv1/sarp_simulator.py", "BTCUSDT","0.01"])

bar = [
    "[=     ]","[ =    ]","[  =   ]","[   =  ]",
    "[    = ]","[     =]","[    = ]","[   =  ]",
    "[  =   ]","[ =    ]"
]
i = 0

while True:
    print(bar[i % len(bar)], end="\r")
    time.sleep(.2)
    i += 1
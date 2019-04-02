import os, sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import numpy as np
import math
# Hw1
from src.gui.Hw1Layout import Hw1Layout
from src.algorithm.FuzzyAlgorithmHw1 import FuzzyAlgorithmHw1

if __name__== "__main__":
    app = Hw1Layout()
    app.mainloop()

    # a = FuzzyAlgorithmHw1()
    # a.fuzzyAlgorithmPPT(0,0,0)
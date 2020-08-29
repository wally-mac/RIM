import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


path = r"C:\Users\A02295870\Box\Thesis_sites"

all_files = glob.glob(path + "/**/**/**/**/**/valley_bottom_metrics.csv")

#all_files = [r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Mill_Creek\codetest_0817\03_Analysis\DCE_01\01_Metrics\valley_bottom_metrics.csv", r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Mill_Creek\codetest_0817\03_Analysis\DCE_02\01_Metrics\valley_bottom_metrics.csv", r"C:\Users\A02295870\Box\Thesis_sites\metrics.csv"]

metrics2 = pd.concat([pd.read_csv(f) for f in all_files])

metrics2.to_csv(os.path.join(path, "metrics2.csv"))

import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


path = r"C:\Users\A02295870\Box\Thesis_sites"

all_files = glob.glob(path + "/**/**/**/**/**/valley_bottom_metrics.csv")


metrics2 = pd.concat([pd.read_csv(f) for f in all_files])


metrics2.to_csv(os.path.join(path, "metrics2.csv"))

print("created csv...")

data = pd.read_csv(os.path.join(path, "metrics2.csv"))

grad_vall = data.grad_vall.tolist()
tot_pct = data.tot_pct.tolist()
dam_dens = data.dam_dens.tolist()
ratio_act = data.ratio_act.tolist()
date = data.date.tolist()


plt.scatter(ratio_act, tot_pct)
plt.show()

plt.scatter(dam_dens, tot_pct)
plt.show()

plt.scatter(grad_vall, tot_pct)
plt.show()

plt.boxplot(tot_pct)
plt.show()

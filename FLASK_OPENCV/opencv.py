#%%
import cv2
import numpy as np
import matplotlib.pyplot as plt

f = cv2.imread('./acnh_fall.jpg')
plt.imshow(f)

f_rgb = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
plt.imshow(f_rgb)

f_rgb.shape
type(f_rgb)
plt.imshow(f[:,:,::-1])
# %%

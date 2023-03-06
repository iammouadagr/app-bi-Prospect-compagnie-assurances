import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.impute import SimpleImputer
# Turn interactive plotting off
plt.ioff()

# read input text and put data inside a data frame
prospect = pd.read_csv('../data/base_prospect.csv')
# prospect =  pd.DataFrame(prospect)

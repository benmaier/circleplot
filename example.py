import numpy as np
import matplotlib.pyplot as pl
import cPickle as pickle

from circleplot import half_circle_plot

data = pickle.load(open('example_data.p','r'))

times = sorted(data.keys())

for t in times:
    fig, ax = pl.subplots(1,1)

    half_circle_plot(data[t], maxN=100,ax=ax,sort=True,lw=1)
    ax.plot([-2,2],[-2,2],'-k')

pl.show()

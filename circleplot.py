from matplotlib import pyplot as pl

import matplotlib.patches as mpatches
import numpy as np

import cPickle as pickle

def split_species(sp):
    "return all single species present in this infected"
    if 'B' in sp:
        s1,s2 = sp.split('B')
        if s1 == '':
            return ['B'+s2]
        else:
            return [ s1, 'B'+s2 ]
    else:
        return [sp]

def arc_patch(center, radius, species='A', ax=None, resolution=50, **kwargs):
    "draw a half circle according to center and radius and species"
    if species.startswith('A'):
        theta1 = 45.
        theta2 = -135.
        color = 'r'
    elif species.startswith('B'):
        theta1 = 225.
        theta2 = 45.
        color = 'g'
    # make sure ax is not empty
    if ax is None:
        ax = pl.gca()
    # generate the points
    theta = np.linspace(np.radians(theta1), np.radians(theta2), resolution)
    points = np.vstack((radius*np.cos(theta) + center[0], 
                        radius*np.sin(theta) + center[1]))
    if 'lw' not in kwargs:
        kwargs['lw'] = 2
    if 'alpha' not in kwargs:
        kwargs['alpha'] = 0.2
    # build the polygon and add it to the axes
    poly = mpatches.Polygon(points.T, 
                            closed=True, 
                            fill=True, 
                            color=color,
                            **kwargs)
    ax.add_patch(poly)
    return poly

def half_circle_plot(t_data,
                     maxN,
                     ax,
                     xlim=[-3,3],
                     ylim=[-3,3],
                     maxR=0.25,
                     sort=True,
                     **kwargs
                     ):
    interaction_params = t_data[0]
    frequencies = t_data[1]
    "draw a half circle plot for all interaction parameters and species frequencies"

    # get single species
    keys = set(frequencies.keys())
    single_species = []
    for k in keys:
        single_species.extend(split_species(k))
    single_species = set(single_species)

    # initiate 0 frequency for every species
    fs = { sp: 0 for sp in single_species}

    # sum up frequencies for all species
    for k in keys:
        for sp in split_species(k):
            fs[sp] += frequencies[k][1]

    for p in interaction_params:
        spA = p[0][0]
        spB = p[0][1]
        if fs[spA] == 0:
            #print spA, spB, fs[spA], fs[spB], [ (k,f) for k,f in frequencies.items() if spA in k ]
            continue
        elif fs[spB] == 0:
            #print spA, spB, fs[spA], fs[spB], [ (k,f) for k,f in frequencies.items() if spB in k ]
            continue
        
        center = [ np.log(p[1][0])/np.log(2.), np.log(p[1][1])/np.log(2.) ]

        #sort for higher ineraction rate
        if sort:
            ndx = np.argsort(center)[::-1]
        else:
            ndx = [0,1]
        center = [center[ndx[0]], center[ndx[1]]]
        sp1, sp2 = p[0][ndx[0]], p[0][ndx[1]]
        frequency = np.array([fs[sp1],fs[sp2]])

        radius = np.sqrt(frequency/float(maxN)) * maxR
        arc_patch(center,radius[0],species=sp1,**kwargs)
        arc_patch(center,radius[1],species=sp2,**kwargs)
    
    ax.set_xlim([xlim[0]-maxR,xlim[1]+maxR])
    ax.set_ylim([ylim[0]-maxR,ylim[1]+maxR])
    ax.set_aspect('equal')

if __name__=="__main__":

    exmpl_interaction = [
                            ( ('A1', 'B1'), (0.0, 0.0) ),
                            ( ('A2', 'B1'), (1.0, 0.0) ),
            ]
    exmpl_frequencies = {
                             'A1': [0,10],
                             'A2': [0,20],
                             'B1': [0,30],
                             'A1B1': [0,30],
                             'A2B1': [0,1],
                        }
            

    data = pickle.load(open('example_data.p','r'))

    times = sorted(data.keys())


    for t in times:
        fig, ax = pl.subplots(1,1)

        half_circle_plot(data[t], maxN=100,ax=ax,sort=True)
        ax.plot([-2,2],[-2,2],'-k')

    pl.show()

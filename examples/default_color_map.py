from sys import path as sys_path
sys_path.append('./../')
import SlopeOrientation.CyclicColormap as cc
from pylab import *

cmap = cc.cyclic_colormap()

figure('',(6,6))
cc.cyclic_colorbar( cmap, ax = gca() )

xticks([]); yticks([]);
savefig('../Figures/default_color_map.svg', bbox_inches = 'tight')

show()

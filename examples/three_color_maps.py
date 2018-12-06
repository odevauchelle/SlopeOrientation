from sys import path as sys_path
sys_path.append('./../')
import SlopeOrientation.CyclicColormap as cc
from pylab import *

color_path = [ 'tab:blue', 'tab:orange', 'tab:green', 'tab:purple' ]

figure('',(12,4))

for i in range( 2, 5 ) :
    subplot(1, 3, i-1)
    cmap = cc.cyclic_colormap( color_path = color_path[:i] )
    cc.cyclic_colorbar( cmap, ax = gca() )
    gca().set_title( str(i) + ' colors' )

savefig('../Figures/default_color_maps.svg', bbox_inches = 'tight')

show()

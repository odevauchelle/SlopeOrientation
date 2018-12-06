from sys import path as sys_path
sys_path.append('./../')
import SlopeOrientation.CyclicColormap as cc


from pylab import *

h = loadtxt('../Data/h.csv')

dxh, dyh = gradient(h)
orientation = angle( dxh + 1j*dyh )

figure('',(6,6))
margin = .05
axes([ margin, margin, 1-2*margin, 1-2*margin ])

cmap = cc.cyclic_colormap()

contour( h, colors = 'white', linestyles = '--', alpha = .3 )
imshow( orientation, cmap = cmap )
axis('equal')
axis('off')

cc.cyclic_colorbar( cmap, ticks = cc.geo_ticks )

savefig('../Figures/angle_orientation_map.svg')
show()

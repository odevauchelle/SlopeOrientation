from sys import path as sys_path
sys_path.append('./../')
import SlopeOrientation.CyclicColormap as cc
from pylab import *

x = linspace(-1,1,100)
y = x
X,Y = meshgrid(x,y)
z = X + 1j*Y
f = ( z - .5 )*( z + .2 +.5j )**3

figure('', ( 6, 6) )
cmap = cc.cyclic_colormap()
imshow( angle(f), cmap = cmap, extent = ( min(x), max(x), min(y), max(y)) )

axis('equal')

cc.cyclic_colorbar( cmap )


savefig('../Figures/analytic_function.svg')
show()

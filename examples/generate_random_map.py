from pylab import *

x = linspace( 0,1, 50 )
y = x

x, y = meshgrid( x, y )

h = 0*x
k = 10.

for _ in range(20) :

    amplitude = rand()
    phase = rand()*2*pi
    orientation = rand()*2*pi

    h += amplitude*real( exp( 1j*k*( cos(orientation)*x + sin(orientation)*y + phase )  ) )

# h = (x -.5 )**2 + (y -.5 )**2

contourf( x, y, h )
axis('equal')
show()

savetxt( '../Data/h.csv', h )

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Olivier Devauchelle, Pauline Delorme, François Métivier
# Guilin, China, december 2018

from matplotlib import colors as mpl_colors
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon, Circle
from mpl_toolkits.axes_grid.inset_locator import inset_axes

from pylab import *

default_color_path = [ 'tab:blue', 'tab:orange', 'green' ] # at least three colors

def anything_to_rgb( color ) :

    try :
        color = colors.ColorConverter.colors[ color ]
        color = mpl_colors.hex2color( color ) # rgb
        return color

    except :
        return color

def cyclic_colormap( color_path = default_color_path, segments = 100, color_map_name = 'default_cyclic' ) :

    '''
    Create a cyclic colormap
    colormap = cyclic_color_map( color_path = default_color_path, segments = 100, color_map_name = 'default_cyclic' )

    Parameters
    ------------
        color_path : list of colors with at least three distinct colors
        segments : int

    Returns
    ------------
        Cyclic color map
    '''

    color_path = map( anything_to_rgb, color_path )

    color_path = color_path + [ color_path[0] ] # close the color path

    return mpl_colors.LinearSegmentedColormap.from_list( color_map_name, color_path, N = segments )

def z_tuple( z ) :
    return real(z), imag(z)

math_ticks = [ [ 0, '$0$' ], [ pi/2, r'$\pi/2$' ], [ -pi/2, r'$-\pi/2$' ], [ pi, r'$\pi$' ],  ]
geo_ticks = [ [ 0, 'E' ], [ pi/2, r'N' ], [ -pi/2, r'S' ], [ pi, r'W' ],  ]

border_style = { 'lw' : 1, 'color' : 'black' }
ticks_length = .1

def cyclic_colorbar( cmap, ax = None, internal_radius = .4, show_border = True, Nb_segments = 100, bckgrnd_color = 'white', bckgrnd_alpha = .5, bckgrnd_radius = 1.6, ticks = math_ticks ):

    if ax == None :
        print 'toto'
        ax = inset_axes( gca(), width="25%", height="25%", loc=1 )
        ax.axis('off')

    theta = linspace( 0, 2*pi, Nb_segments )

    external_radius = 1

    for i in range( len(theta) - 1 ) :

        segment = [ z_tuple( external_radius*exp( 1j*theta[i] ) ) ]
        segment += [ z_tuple( external_radius*exp( 1j*theta[i+1] ) ) ]
        segment += [ z_tuple( internal_radius*exp( 1j*theta[i+1] ) ) ]
        segment += [ z_tuple( internal_radius*exp( 1j*theta[i] ) ) ]

        segment += [ segment[0] ]

        ax.add_collection( PatchCollection( [ Polygon( segment ) ], facecolor = cmap( theta[i]/(2*pi) ), edgecolor = 'none'  ) )

    if show_border :
        ax.plot( external_radius*cos(theta),  external_radius*sin(theta), **border_style )
        ax.plot( internal_radius*cos(theta),  internal_radius*sin(theta), **border_style )

        ticks_r = external_radius*array( [ 1, 1 + ticks_length  ] )
        ticks_label_r = external_radius*( 1 + 3*ticks_length  )
        for tick in ticks :
            theta = tick[0]
            ax.plot( ticks_r*cos(theta),  ticks_r*sin(theta),  **border_style )
            ax.text( ticks_label_r*cos(theta),  ticks_label_r*sin(theta), tick[1], color = border_style['color'], ha = 'center', va = 'center' )

    if bckgrnd_color != None :
        ax.add_collection( PatchCollection(  [ Circle( ( 0, 0 ), radius = bckgrnd_radius ) ], facecolor = bckgrnd_color, alpha = bckgrnd_alpha, zorder = 0 ) )

    ax.axis('equal')
    ax.axis('off')


##########################
#
# SANDBOX
#
##########################

if __name__ == '__main__':

    cmap = cyclic_colormap()

    figure()
    cyclic_colorbar( cmap )

    show()

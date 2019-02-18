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

# New versions of matlplotlib use that way to include the inset_axes
try:
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
except ImportWarning:
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
    ----------
        color_path : list of colors with at least three distinct colors
        segments : int

    Returns
    -------
        Cyclic color map
    '''

    color_path = map( anything_to_rgb, color_path )

    # For python 3
    color_path = list(color_path)

    color_path = color_path + [ color_path[0] ] # close the color path

    return mpl_colors.LinearSegmentedColormap.from_list( color_map_name, color_path, N = segments )

def z_tuple( z ) :
    return real(z), imag(z)

math_ticks = [ [ 0, '$0$' ], [ pi/2, r'$\pi/2$' ], [ -pi/2, r'$-\pi/2$' ], [ pi, r'$\pi$' ],  ]
geo_ticks = [ [ 0, 'E' ], [ pi/2, r'N' ], [ -pi/2, r'S' ], [ pi, r'W' ],  ]

def cyclic_colorbar( cmap, ax = None, internal_radius = .4,
                     show_border = True, Nb_segments = 100,
                     bckgrnd_color = 'white', bckgrnd_alpha = .5,
                     bckgrnd_radius = 1.6, ticks = math_ticks,
                     ticks_length = .1, border_style = {'lw' : 1, 'color' : 'black'},
                     inset_loc=1, inset_width='25%', inset_height='25%'):
    '''
    Add a cyclic colorbar

    Parameters
    ----------

    cmap: matplotlib colormap
        The colormap used to draw the colorbar 

    ax: matplotlib axes or None, optional
        The axes on which the colorbar is added, the default value is
        None, this create an "inset_axes" with the location defined by
        inset_loc and the width/height defined by inset_width,
        inset_height arguments. 

    internal_radius: float, optional
        The inner radius of the colorbar. The value should be between
        0 and 1 (the outer radius of the colorbar).

    show_border: boolean, optional
        Display border for the colorbar.

    Nb_segments: int, optional
        Number of segments to display colormap inside the colorbar

    bckgrnd_color: string, optional
       The color of the background.

    bckgrnd_alpha, float, optional
       The background opacity, should be between 0 and 1.

    bckgrnd_radius, float, optional
       The radius of the background.

    ticks: list, optional
       The list of ticks described as (coordinate, string). Examples:
       math_ticks = [[ 0, '$0$' ], [ pi/2, r'$\pi/2$' ], [ -pi/2, r'$-\pi/2$' ], [ pi, r'$\pi$' ]]
       geo_ticks = [[ 0, 'E' ], [ pi/2, r'N' ], [ -pi/2, r'S' ], [ pi, r'W' ],]

    ticks_length: float, optional
       The radial spacing of ticks.

    border_style: dict, optional
       The style for the border of the colormap. It's defined as a
       dict which contains arguments accepted by the matplotlib plot
       function.
    
    inset_loc: int or string, optional
       The position of the colorbar if ax = None.

    inset_width: int or string, optional
       The width of the colorbar inset axes if ax = None.

    inset_height: int or string, optional
       The height of the colorbar inset axes if ax = None.
    '''
    
    if ax is None :
        ax = inset_axes(gca(), width=inset_width, height=inset_height, loc=inset_loc)
        ax.set_xlim(-1,1)
        ax.set_ylim(-1,1)
        ax.axis('off')

    theta = linspace( 0, 2*pi, Nb_segments )
    external_radius=1
    
    for i in range( len(theta) - 1 ) :

        segment = [z_tuple(external_radius*exp(1j*theta[i]))]
        segment += [z_tuple(external_radius*exp(1j*theta[i+1]))]
        segment += [z_tuple(internal_radius*exp(1j*theta[i+1]))]
        segment += [z_tuple(internal_radius*exp(1j*theta[i]))]

        segment += [ segment[0] ]

        ax.add_collection( PatchCollection( [ Polygon( segment ) ],
                                            facecolor = cmap( theta[i]/(2*pi) ),
                                            edgecolor = cmap( theta[i]/(2*pi) ))
        )

    if show_border :
        ax.plot( external_radius*cos(theta), external_radius*sin(theta), **border_style )
        ax.plot( internal_radius*cos(theta), internal_radius*sin(theta), **border_style )

        ticks_r = external_radius*array( [ 1, 1 + ticks_length  ] )
        ticks_label_r = external_radius*( 1 + 3*ticks_length  )
        for tick in ticks :
            theta = tick[0]
            ax.plot( ticks_r*cos(theta),
                     ticks_r*sin(theta), **border_style )
            ax.text( ticks_label_r*cos(theta),
                     ticks_label_r*sin(theta), tick[1],
                     color=border_style['color'], ha='center', va='center' )

    if bckgrnd_color != None :
        ax.add_collection( PatchCollection(  [ Circle( (0, 0), radius = bckgrnd_radius ) ],
                                             facecolor = bckgrnd_color, alpha = bckgrnd_alpha,
                                             zorder = 0 ) )

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

# SlopeOrientation

SlopeOrientation is a Python library to create and use cyclic colormaps with Matplotlib.

Cyclic colormaps can represent the spatial distribution of an angle.

## Quick example

```python
import SlopeOrientation.CyclicColormap as cc
from pylab import *

cmap = cc.cyclic_colormap()

figure( '', ( 6, 6 ) )
cc.cyclic_colorbar( cmap, ax = gca() )

xticks([]); yticks([]);

show()
```
![Default colormap](./Figures/default_color_map.svg)

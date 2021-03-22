from turf.square_grid import square_grid
import json

bbox = [-95, 30 ,-85, 40]
cellSide = 50
options = "{units: 'miles'}"

squareGrid = square_grid(bbox, cellSide, options)
print(squareGrid["features"][0])
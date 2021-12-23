from datetime import datetime
from datetime import timedelta
import matplotlib
import matplotlib.pyplot as plt
import json

data = json.loads(r"""{ 
    "bbox_area":[11.10499, 55.14280 ,11.26270, 55.23284],
    "cell_side":2,
    "unit":"kilometers",
    "table":"ships_opt",
    "table_spaceTimeCube":"space_time_cube_219005068",
    "year":2021,
    "month":09,
    "day":1,
    "time":15,
    "i":5
    }""")
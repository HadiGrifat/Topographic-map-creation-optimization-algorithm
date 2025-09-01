import gpxpy
from pyproj import Transformer
import numpy as np

def load_gpx_data(filename):
    with open(filename, 'r') as f:
        gpx = gpxpy.parse(f)

    lats, lons, alts = [], [], []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lats.append(point.latitude)
                lons.append(point.longitude)
                alts.append(point.elevation)
    return lats, lons, alts

def normalize_elevation(alts):
    alts = np.array(alts) # convert to numpy array
    alts -= np.min(alts) # normalizing elevation so min(alts) = 0
    return alts

def coord_transform(lats, lons):
    transformer = Transformer.from_crs("epsg:4326", "epsg:32636", always_xy=True) # tranforming latitude and longitude from degree into meters for projection
    x, y = transformer.transform(lons, lats)
    return x, y
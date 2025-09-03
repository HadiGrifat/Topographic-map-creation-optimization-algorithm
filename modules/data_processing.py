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

def load_multiple_gpx(gpx_files):
    '''
    load and combine data from multiple gpx files
    arguments: list of gpx file paths
    return: combined lats, lons, alts lists
    '''
    all_lats, all_lons, all_alts = [], [], []
    for filename in gpx_files:
        print(f"loading {filename}...")
        lats, lons, alts = load_gpx_data(filename)
        all_lats.extend(lats)
        all_lons.extend(lons)
        all_alts.extend(alts)
    return all_lats, all_lons, all_alts

def normalize_elevation(alts):
    alts = np.array(alts) # convert to numpy array
    alts -= np.min(alts) # normalizing elevation so min(alts) = 0
    return alts

def coord_transform(lats, lons):
    transformer = Transformer.from_crs("epsg:4326", "epsg:32636", always_xy=True) # tranforming latitude and longitude from degree into meters for projection
    x, y = transformer.transform(lons, lats)
    # normalize coordinates so min(x) = 0 and min(y) = 0, similar to elevation normalization
    x = np.array(x) - np.min(x)
    y = np.array(y) - np.min(y)
    return x, y
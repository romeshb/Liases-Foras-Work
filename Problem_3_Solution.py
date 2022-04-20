"""
Solution to Problem 3
"""


import pandas as pd
import numpy as np

source = pd.read_excel(r"Problem_3_Dataset.xlsx", sheet_name="SOURCE")  # loading from sheet 1
destination = pd.read_excel(r"Problem_3_Dataset.xlsx", sheet_name="DESTINATION")  # loading from sheet 2

# source columns
source['Source_ID'] = source.index  # Create column with original index id
source.rename(columns={"Latitude": 'Source_Latitude', 'Longitude': "Source_Longitude"}, inplace=True)  # Rename columns
source = source[['Source_ID', "Source_Latitude", "Source_Longitude"]]  # rearranging the columns
# destination columns
destination['Destination_ID'] = destination.index  # Create column with original index id
destination.rename(columns={"Latitude": 'Destination_Latitude', 'Longitude': "Destination_Longitude"}, inplace=True)
destination = destination[['Destination_ID', "Destination_Latitude", "Destination_Longitude"]]  # Rearrange columns

# Creating DataFrame with all the possible combinations of Source and Destinations coordinates
result = pd.merge(source, destination, how="cross")
print(f"The possible Source and Destination combinations are {result.shape[0]}.")


# Custom function for calculations of Distance between source and destination in KMs.
def haversine_distance(lat1, long1, lat2, long2):
    """ To get the distance between two points using coordinates,
    Greater Circle Distance.
    (reference: https://en.wikipedia.org/wiki/Great-circle_distance)
    """
    # Simple and unoptimized code here,
    # lat1, long1, lat2, long2 = map(lambda x: x/57.295827, [lat1, long1, lat2, long2]) #lat/(180/3.14159) or lat/57.258
    # delta_long = long2 - long1
    # delta_angle = (np.arccos(np.sin(lat1) * np.sin(lat2) + np.cos(lat1) * np.cos(lat2) * np.cos(delta_long))*6378.137
    # radius = 6378.137 # considering radius of earth at equator
    # return delta_angle* radius  # considering radius of earth at equator

    # optimized code from here,
    lat1, long1, lat2, long2 = map(lambda x: x / 57.295827, [lat1, long1, lat2, long2])
    return np.arccos(np.sin(lat1) * np.sin(lat2) + np.cos(lat1) * np.cos(lat2) * np.cos(long2 - long1)) * 6378.137


# We'll avoid using for loops, apply, map functions as it would increase the runtime and space complexity.
# Instead, passing string values directly to the function we get Order of N, O(N) complexity.
result['Distance_KM'] = haversine_distance(result['Source_Latitude'], result['Source_Longitude'],
                                           result['Destination_Latitude'], result['Destination_Longitude'])
pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 10)
print(result)  # check the output dataframe

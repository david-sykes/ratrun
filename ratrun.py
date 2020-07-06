import numpy as np
import os
import requests


KM_TO_LAT_LON = 1/111 # 1 degree is ~ 111km


def create_route_pairs(centre, radius_km, number_of_points):
  radius_latlon = radius_km * KM_TO_LAT_LON
  start_angles = np.linspace(0.01, 2*np.pi, number_of_points)[:-1] # Create semi circle of points and remove the last
  end_angles = []
  for a in start_angles:
    if a < np.pi:
      end_angles.append(a + np.pi)
    else:
      end_angles.append(a - np.pi)
  start_points = [(centre[0] + radius_latlon*np.cos(a), centre[1] + radius_latlon*np.sin(a)) for a in start_angles]
  end_points = [(centre[0] + radius_latlon*np.cos(a), centre[1] + radius_latlon*np.sin(a)) for a in end_angles]
  return list(zip(start_points, end_points))


def get_directions(origin, destination):
  url = 'https://maps.googleapis.com/maps/api/directions/json'
  origin_str = f'{origin[0]},{origin[1]}'
  destination_str = f'{destination[0]},{destination[1]}'
  params = dict(origin=origin_str,
              destination=destination_str,
              key=os.environ['API_KEY'],
              alteratives='true',
              mode='driving',
              departure_time='now')
  directions = requests.get(url, params=params)
  return directions

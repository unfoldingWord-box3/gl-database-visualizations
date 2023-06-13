import geopandas as gpd
from shapely.geometry import Polygon, Point
import random
import csv

# Load your polygon layer into a GeoDataFrame
polygon_gdf = gpd.read_file('polygons.gpkg')

# Reproject the GeoDataFrame to EPSG:7755
polygon_gdf = polygon_gdf.to_crs(epsg=7755)

# Create a new column to store the maximum possible minimum distance
polygon_gdf['max_min_distance'] = None

# Iterate over each polygon and calculate the maximum possible minimum distance
for index, row in polygon_gdf.iterrows():
    polygon = row['geometry']
    
    # Fix invalid geometries
    if not polygon.is_valid:
        polygon = polygon.buffer(0)
    
    # Calculate the size-based density factor for random points
    density_factor = polygon.length / polygon.area
    
    # Set a minimum number of points for smaller polygons
    min_num_points = 100  # Adjust as needed
    
    # Adjust the number of random points based on polygon size and desired density
    num_points = max(int(polygon.area * density_factor / 1000), min_num_points)
    
    # Generate random points within the polygon
    points = []
    bbox = polygon.bounds  # Get the bounding box of the polygon
    min_x, min_y, max_x, max_y = bbox
    max_attempts = 1000  # Maximum number of attempts to generate points
    attempts = 0
    while len(points) < num_points and attempts < max_attempts:
        rand_x = random.uniform(min_x, max_x)
        rand_y = random.uniform(min_y, max_y)
        point = Point(rand_x, rand_y)
        if polygon.contains(point):
            points.append(point)
        attempts += 1
    
    # Calculate the minimum distance from each point to the border
    min_distances = [polygon.boundary.distance(point) for point in points]
    
    # Check if the min_distances list is empty
    if min_distances:
        # Find the maximum of the minimum distances and convert it to kilometers
        max_min_distance = max(min_distances) / 1000
    else:
        max_min_distance = 0  # Set a default value if no points are within the polygon
    
    # Store the maximum possible minimum distance in the 'max_min_distance' column
    polygon_gdf.at[index, 'max_min_distance'] = max_min_distance

# Create a CSV file to store the results
output_file = 'polygon_distances.csv'

# Open the CSV file in write mode and write the header
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['ISO', 'Polygon Index', 'Max Min Distance']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    # Write the ISO, polygon index, and corresponding maximum possible minimum distance to each row
    for index, row in polygon_gdf.iterrows():
        iso = row['iso']
        polygon_index = index
        max_min_distance = row['max_min_distance']
        writer.writerow({'ISO': iso, 'Polygon Index': polygon_index, 'Max Min Distance': max_min_distance})

print(f"CSV file '{output_file}' created successfully.")

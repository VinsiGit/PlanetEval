import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('cleaning/eval.csv')

# Calculate the habitable zone boundaries
data['hz_inner'] = np.sqrt(data['st_lum'] / 1.1)
data['hz_outer'] = np.sqrt(data['st_lum'] / 0.53)

# Determine if the planet is in the habitable zone
data['in_habitable_zone'] = (data['pl_orbsmax'] >= data['hz_inner']) & (data['pl_orbsmax'] <= data['hz_outer'])

# Filter planets in the habitable zone
habitable_planets = data[data['in_habitable_zone']]

# Calculate the distance from the center of the habitable zone
habitable_planets['hz_center'] = (habitable_planets['hz_inner'] + habitable_planets['hz_outer']) / 2
habitable_planets['distance_from_hz_center'] = np.abs(habitable_planets['pl_orbsmax'] - habitable_planets['hz_center'])

# Normalize the distance for color mapping
norm = plt.Normalize(habitable_planets['distance_from_hz_center'].min(), habitable_planets['distance_from_hz_center'].max())
colors = plt.cm.viridis(norm(habitable_planets['distance_from_hz_center']))

# Convert RA and Dec from degrees to radians
ra_rad = np.radians(habitable_planets['ra'])
dec_rad = np.radians(habitable_planets['dec'])

# Calculate Cartesian coordinates
x = habitable_planets['sy_dist'] * np.cos(dec_rad) * np.cos(ra_rad)
y = habitable_planets['sy_dist'] * np.cos(dec_rad) * np.sin(ra_rad)
z = habitable_planets['sy_dist'] * np.sin(dec_rad)

# Display the first few Cartesian coordinates to verify conversion
cartesian_coords = pd.DataFrame({'x': x, 'y': y, 'z': z})
print(cartesian_coords.head())

# Plot in 3D Space
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create a 3D scatter plot with color coding
scatter = ax.scatter(x, y, z, c=colors, marker='o')

# Set labels
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Z Coordinate')

# Set title
ax.set_title('3D Scatter Plot of RA, Dec, and Distance with Habitability')

# Add a color bar
cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
cbar.set_label('Distance from Habitable Zone Center')

# Show plot
plt.show()
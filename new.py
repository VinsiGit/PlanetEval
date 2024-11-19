import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('cleaning/training.csv')


# Normalize the distance for color mapping
norm = plt.Normalize(0, 50)
colors = plt.cm.viridis(norm(data['pl_esi']))

# Convert RA and Dec from degrees to radians
ra_rad = np.radians(data['ra'])
dec_rad = np.radians(data['dec'])

# Calculate Cartesian coordinates
x = data['sy_dist'] * np.cos(dec_rad) * np.cos(ra_rad)
y = data['sy_dist'] * np.cos(dec_rad) * np.sin(ra_rad)
z = data['sy_dist'] * np.sin(dec_rad)

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
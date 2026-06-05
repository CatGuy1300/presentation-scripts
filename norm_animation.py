import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from itertools import product, combinations

# 1. DEFINE THE RAW MESH (Vertices and Faces)
# A simple 3D shape (a pyramid), large and placed far away from the origin
vertices = np.array([
    [100, 100, 20],  # V0: Base corner 1
    [160, 100, 20],  # V1: Base corner 2
    [160, 140, 20],  # V2: Base corner 3
    [100, 140, 20],  # V3: Base corner 4
    [130, 120, 120]  # V4: Apex (Top point)
], dtype=float)

# Faces define how vertices connect to form the solid skin (Triangles & Quads)
faces = [
    [0, 1, 4],  # Side 1
    [1, 2, 4],  # Side 2
    [2, 3, 4],  # Side 3
    [3, 0, 4],  # Side 4
    [0, 1, 2, 3]  # Bottom Base
]

# 2. CALCULATE NORMALIZATION MATH (Just like Hunyuan3D)
# Find the Axis-Aligned Bounding Box (AABB) center
bbox_min = np.min(vertices, axis=0)
bbox_max = np.max(vertices, axis=0)
center = (bbox_max + bbox_min) / 2.0

# Center the vertices
centered_vertices = vertices - center

# Find max Euclidean distance for uniform scaling
max_distance = np.max(np.linalg.norm(centered_vertices, axis=1))

# 3. SET UP THE ANIMATION
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')


def update(frame):
    ax.clear()

    # Set starting camera view and axis limits
    ax.view_init(elev=20, azim=45)
    ax.set_xlabel('X');
    ax.set_ylabel('Y');
    ax.set_zlabel('Z')

    if frame < 30:
        # Phase 1: Show the raw, off-center mesh
        ax.set_xlim(-2, 180);
        ax.set_ylim(-2, 180);
        ax.set_zlim(-2, 180)
        current_v = vertices
        ax.set_title("Step 1: Raw Mesh\nVertices are far from origin, Faces follow them")

    elif frame < 70:
        # Phase 2: Animate translation (Subtracting Bounding Box Center)
        ax.set_xlim(-2, 180);
        ax.set_ylim(-2, 180);
        ax.set_zlim(-2, 180)
        progress = (frame - 30) / 40.0
        # Smoothly interpolate vertices moving to origin
        current_v = vertices - (center * progress)
        ax.set_title("Step 2: Centering\nSubtracting AABB center from Vertices")

    else:
        # Phase 3: Animate uniform scaling into the Unit Cube
        # Zoom camera in to the origin
        ax.set_xlim(-1.5, 1.5);
        ax.set_ylim(-1.5, 1.5);
        ax.set_zlim(-1.5, 1.5)
        progress = min(1.0, (frame - 70) / 40.0)

        # Smoothly interpolate shrinking
        scale_factor = 1.0 - (progress * (1.0 - (1.0 / max_distance)))
        current_v = centered_vertices * scale_factor
        ax.set_title("Step 3: Uniform Scaling\nVertices scaled down. Max distance touches the Unit Cube.")

        # Draw the Unit Cube [-1, 1] bounds
        r = [-1, 1]
        for s, e in combinations(np.array(list(product(r, r, r))), 2):
            if np.sum(np.abs(s - e)) == r[1] - r[0]:
                ax.plot3D(*zip(s, e), color="red", linestyle="--", alpha=0.3)

    # DRAW THE MESH FACES
    # We rebuild the 3D polygons every frame based on the new vertex positions
    poly3d = [[current_v[vert_id] for vert_id in face] for face in faces]

    # Render the solid mesh (Cyan skin with Blue wireframe edges)
    mesh_collection = Poly3DCollection(poly3d, facecolors='cyan', linewidths=1.5, edgecolors='blue', alpha=0.7)
    ax.add_collection3d(mesh_collection)

    # Plot the Origin
    ax.scatter([0], [0], [0], color='red', s=60, label="Origin (0,0,0)", zorder=5)
    ax.legend(loc="upper left")


# Run animation (130 frames total)
ani = animation.FuncAnimation(fig, update, frames=130, interval=50)

# Save the GIF
print("Generating GIF... This will take about 10-15 seconds.")
ani.save('mesh_normalization.gif', writer='pillow', fps=20)
print("Done! Check your folder for 'mesh_normalization.gif'.")
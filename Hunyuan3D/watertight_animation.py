import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 1. CREATE DEFECTIVE GEOMETRY (A broken "C" shape with a gap)
# This represents a slice of a 3D mesh that has a hole in it
theta = np.linspace(np.pi / 4, 7 * np.pi / 4, 100)  # Leaves a 90-degree gap
x_mesh = 0.6 * np.cos(theta)
y_mesh = 0.6 * np.sin(theta)

# 2. INITIALIZE QUERY GRID
grid_res = 25
x_g = np.linspace(-1, 1, grid_res)
y_g = np.linspace(-1, 1, grid_res)
xx, yy = np.meshgrid(x_g, y_g)
grid_points = np.c_[xx.ravel(), yy.ravel()]

# 3. CALCULATE SDF & WINDING NUMBER (Simulated)
# Winding number mathematically "knows" what the inside is, even with the gap
# Distance is negative if inside, positive if outside
distances = np.sqrt(grid_points[:, 0] ** 2 + grid_points[:, 1] ** 2) - 0.6
colors = np.where(distances < 0, 'dodgerblue', 'crimson')

fig, ax = plt.subplots(figsize=(7, 7))


def update(frame):
    ax.clear()
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.axis('off')  # Hide axes for a cleaner look

    # Phase 1: Show the broken mesh
    if frame < 30:
        ax.plot(x_mesh, y_mesh, color='black', lw=6, label='Broken Mesh')
        ax.set_title("Step 1: Defective Geometry\n(Notice the massive gap on the right!)", fontsize=14)
        ax.legend(loc="upper left")

    # Phase 2: Fade in the query grid
    elif frame < 60:
        ax.plot(x_mesh, y_mesh, color='black', lw=6)
        alpha = min(1.0, (frame - 30) / 20.0)
        ax.scatter(grid_points[:, 0], grid_points[:, 1], c='gray', s=30, alpha=alpha, label='Query Grid')
        ax.set_title("Step 2: Initialize Spatial Query Grid\n(Encompassing the entire object)", fontsize=14)
        ax.legend(loc="upper left")

    # Phase 3: Color the grid based on SDF and Winding Number
    elif frame < 100:
        ax.plot(x_mesh, y_mesh, color='black', lw=6)
        progress = min(1.0, (frame - 60) / 20.0)

        # Transition dots from gray to their calculated SDF colors
        ax.scatter(grid_points[:, 0], grid_points[:, 1], c=colors, s=30, alpha=progress, label='+ Outside / - Inside')
        ax.set_title("Step 3: SDF & Winding Number Math\n(Blue = Inside Space, Red = Outside Space)", fontsize=14)
        ax.legend(loc="upper left")

    # Phase 4: Extract the watertight mesh via Marching Cubes
    else:
        # Fade out the old mesh and grid slightly to highlight the new surface
        ax.plot(x_mesh, y_mesh, color='black', lw=6, alpha=0.2)
        ax.scatter(grid_points[:, 0], grid_points[:, 1], c=colors, s=30, alpha=0.15)

        # Plot the 0-level Isosurface (The Marching Cubes boundary)
        ax.contour(xx, yy, distances.reshape(grid_res, grid_res), levels=[0], colors='limegreen', linewidths=6)

        # Add a dummy line just for the legend
        ax.plot([], [], color='limegreen', lw=6, label='New Watertight Surface')
        ax.set_title("Step 4: Marching Cubes Extraction\n(A perfect, closed boundary at the Zero-Level!)", fontsize=14,
                     color='green')
        ax.legend(loc="upper left")


# Run animation (150 frames total)
ani = animation.FuncAnimation(fig, update, frames=150, interval=60)

print("Generating GIF... (Takes about 10 seconds)")
ani.save('watertight_step.gif', writer='pillow', fps=20)
print("Done! Check your folder for 'watertight_step.gif'.")
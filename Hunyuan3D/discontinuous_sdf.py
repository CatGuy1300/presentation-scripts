import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.spatial.distance import cdist

# 1. CREATE COMPLEX DEFECTIVE GEOMETRY
theta = np.linspace(0.6, 2 * np.pi - 0.6, 200)
r_mesh = 0.6 + 0.2 * np.sin(5 * theta)
x_mesh = r_mesh * np.cos(theta)
y_mesh = r_mesh * np.sin(theta)
mesh_pts = np.c_[x_mesh, y_mesh]

# 2. INITIALIZE QUERY GRID
grid_res = 30
x_g = np.linspace(-1.2, 1.2, grid_res)
y_g = np.linspace(-1.2, 1.2, grid_res)
xx, yy = np.meshgrid(x_g, y_g)
grid_points = np.c_[xx.ravel(), yy.ravel()]

# 3. CALCULATE SDF MATH
distances = np.min(cdist(grid_points, mesh_pts), axis=1)

angles = np.arctan2(grid_points[:, 1], grid_points[:, 0])
angles = np.where(angles < 0, angles + 2 * np.pi, angles)
r_true = 0.6 + 0.2 * np.sin(5 * angles)
grid_r = np.linalg.norm(grid_points, axis=1)

inside = grid_r < r_true
sdf = np.where(inside, -distances, distances)
colors = np.where(sdf < 0, 'dodgerblue', 'crimson')

# --- NEW FOOLPROOF METHOD: Dynamically find the exact sign-flip ---
# Grab the middle horizontal row of the grid (y ~ 0)
mid_row = grid_res // 2
row_start = mid_row * grid_res
row_end = row_start + grid_res
row_sdfs = sdf[row_start:row_end]

# Mathematically find the exact index where the SDF flips from Negative to Positive
sign_flips = np.where(np.diff(np.sign(row_sdfs)) > 0)[0]

# Pick the right-most flip (which sits exactly at our gap)
flip_idx = sign_flips[-1]
idx_inside = row_start + flip_idx  # The last Blue dot
idx_outside = row_start + flip_idx + 1  # The first Red dot
gap_points_idx = [idx_inside, idx_outside]

# ------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 8))


def update(frame):
    ax.clear()
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis('off')

    ax.plot(x_mesh, y_mesh, color='black', lw=5, zorder=3, label="Broken Input Mesh")

    if frame < 30:
        ax.set_title("Step 1: Complex Broken Geometry\n(Notice the missing star arm on the right)", fontsize=14)
        ax.legend(loc="upper left")

    elif frame < 70:
        progress = min(1.0, (frame - 30) / 20.0)
        ax.scatter(grid_points[:, 0], grid_points[:, 1], c=colors, s=35, alpha=progress * 0.8)
        ax.set_title("Step 2: Calculate SDF\nRed = Outside (+), Blue = Inside (-)", fontsize=14)
        ax.legend(loc="upper left")

    elif frame < 120:
        ax.scatter(grid_points[:, 0], grid_points[:, 1], c=colors, s=35, alpha=0.3)

        for idx in gap_points_idx:
            px, py = grid_points[idx]
            val = sdf[idx]

            c = 'dodgerblue' if val < 0 else 'crimson'
            ax.scatter(px, py, c=c, s=150, edgecolors='black', linewidths=2, zorder=4)

            # Smart Text Alignment
            if val < 0:
                ax.text(px - 0.05, py, f"{val:+.2f}", fontsize=12, fontweight='bold',
                        color='black', va='center', ha='right', zorder=5,
                        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))
            else:
                ax.text(px + 0.05, py, f"{val:+.2f}", fontsize=12, fontweight='bold',
                        color='black', va='center', ha='left', zorder=5,
                        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))

        ax.set_title("Step 3: The Discontinuity Flaw!\nNotice the numbers jump from + to - without hitting 0.",
                     fontsize=14, color='darkred')

    else:
        ax.scatter(grid_points[:, 0], grid_points[:, 1], c=colors, s=35, alpha=0.15)
        ax.contour(xx, yy, sdf.reshape(grid_res, grid_res), levels=[0], colors='limegreen', linewidths=4, zorder=2)
        ax.plot([], [], color='limegreen', lw=4, label='Marching Cubes Surface')
        ax.set_title(
            "Step 4: Marching Cubes to the Rescue\nIt detects the sign flip and interpolates a flat 'drum skin' across the gap!",
            fontsize=13, color='green')
        ax.legend(loc="upper left")


ani = animation.FuncAnimation(fig, update, frames=170, interval=60)
print("Generating perfectly aligned GIF... (Takes about 15 seconds)")
ani.save('marching_cubes_perfect.gif', writer='pillow', fps=15)
print("Done!")
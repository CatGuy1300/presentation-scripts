import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def get_hammersley_sphere(N, delta1=0, delta2=0):
    """Generates points on a sphere using the Hammersley sequence with a delta offset."""
    pts = []
    for i in range(N):
        u = (i / N + delta1) % 1.0
        # Van der Corput sequence for base 2
        n, vdc, denom = i, 0, 1
        while n:
            denom *= 2
            n, remainder = divmod(n, 2)
            vdc += remainder / denom
        v = (vdc + delta2) % 1.0

        # Map to sphere
        theta = 2 * np.pi * u
        phi = np.arccos(1 - 2 * v)
        x = np.sin(phi) * np.cos(theta)
        y = np.sin(phi) * np.sin(theta)
        z = np.cos(phi)
        pts.append([x, y, z])
    return np.array(pts)


N = 150  # Number of cameras used in the paper
np.random.seed(42)
random_pts = np.random.normal(size=(N, 3))
random_pts /= np.linalg.norm(random_pts, axis=1)[:, np.newaxis]

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')


def update(frame):
    ax.clear()
    ax.set_xlim([-1.2, 1.2]);
    ax.set_ylim([-1.2, 1.2]);
    ax.set_zlim([-1.2, 1.2])
    ax.set_axis_off()  # Hide axes for a clean look

    # Draw a faint wireframe sphere in the center representing the 3D mesh
    u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
    ax.plot_wireframe(0.5 * np.cos(u) * np.sin(v), 0.5 * np.sin(u) * np.sin(v), 0.5 * np.cos(v), color="gray",
                      alpha=0.1)

    if frame < 40:
        # Phase 1: Pure Random (Shows clustering and gaps)
        ax.scatter(random_pts[:, 0], random_pts[:, 1], random_pts[:, 2], color='crimson', s=40)
        ax.set_title("Phase 1: Pure Random Camera Placement\n(Notice the clusters and massive blind spots!)",
                     fontsize=14)
    elif frame < 80:
        # Phase 2: Hammersley Sequence
        ham_pts = get_hammersley_sphere(N)
        ax.scatter(ham_pts[:, 0], ham_pts[:, 1], ham_pts[:, 2], color='dodgerblue', s=40)
        ax.set_title("Phase 2: Hammersley Sequence\n(Cameras are perfectly and evenly distributed!)", fontsize=14)
    else:
        # Phase 3: Applying Delta Offset
        progress = (frame - 80) / 60.0
        # Smoothly change delta from 0 to 1
        ham_pts = get_hammersley_sphere(N, delta1=progress, delta2=progress)
        ax.scatter(ham_pts[:, 0], ham_pts[:, 1], ham_pts[:, 2], color='limegreen', s=40)
        ax.set_title("Phase 3: The Delta Offset (δ)\nThe 'Cage' shifts so every 3D model gets uniquely angled photos!",
                     fontsize=14)


ani = animation.FuncAnimation(fig, update, frames=140, interval=60)
print("Generating Hammersley GIF...")
ani.save('hammersley_cameras.gif', writer='pillow', fps=15)
print("Done! Saved 'hammersley_cameras.gif'.")
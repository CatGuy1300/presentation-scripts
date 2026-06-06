import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 1. Generate base Hammersley Sequence (u, v) in 2D space
N = 150
u_base = np.zeros(N)
v_base = np.zeros(N)

for i in range(N):
    u_base[i] = i / N
    # Van der Corput sequence for v
    n, vdc, denom = i, 0, 1
    while n:
        denom *= 2
        n, remainder = divmod(n, 2)
        vdc += remainder / denom
    v_base[i] = vdc

# Create a rainbow color map so we can track the cameras as they move!
colors = plt.cm.hsv(u_base)

# 2. Setup Side-by-Side Plot
fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(121)  # Left: 2D Wrapping Paper
ax2 = fig.add_subplot(122, projection='3d')  # Right: 3D Sphere


def update(frame):
    ax1.clear();
    ax2.clear()

    # Calculate the Delta Offset (Moves continuously)
    # delta_u slides horizontally, delta_v slides vertically
    delta_u = (frame / 150.0) * 2.0
    delta_v = (frame / 150.0) * 1.0

    # APPLY THE MATH: Shift and Modulo (The Pac-Man wrap-around!)
    u_new = (u_base + delta_u) % 1.0
    v_new = (v_base + delta_v) % 1.0

    # --- LEFT PLOT: 2D "Wrapping Paper" ---
    ax1.set_xlim(0, 1);
    ax1.set_ylim(0, 1)
    ax1.set_title(f"Step 1 & 2: The 2D 'Wrapping Paper'\nDelta Shift: δu={delta_u % 1:.2f}, δv={delta_v % 1:.2f}",
                  fontsize=13)
    ax1.set_xlabel("u (Longitude)");
    ax1.set_ylabel("v (Latitude)")
    ax1.scatter(u_new, v_new, c=colors, s=50, edgecolors='black')

    # --- RIGHT PLOT: 3D Sphere Projection ---
    ax2.set_xlim([-1, 1]);
    ax2.set_ylim([-1, 1]);
    ax2.set_zlim([-1, 1])
    ax2.set_axis_off()
    ax2.set_title("Step 3: Projected onto 3D Sphere\nCameras rotate but stay perfectly spaced!", fontsize=13)

    # Draw faint wireframe globe
    u_globe, v_globe = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
    ax2.plot_wireframe(0.9 * np.cos(u_globe) * np.sin(v_globe), 0.9 * np.sin(u_globe) * np.sin(v_globe),
                       0.9 * np.cos(v_globe), color="gray", alpha=0.1)

    # Math: Convert 2D (u, v) to 3D Sphere coordinates
    theta = 2 * np.pi * u_new
    phi = np.arccos(1 - 2 * v_new)
    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)

    ax2.scatter(x, y, z, c=colors, s=50, edgecolors='black')


# Create smooth 150-frame animation
ani = animation.FuncAnimation(fig, update, frames=150, interval=50)

print("Generating the Delta Wrapping GIF...")
ani.save('delta_wrapping_proof.gif', writer='pillow', fps=20)
print("Done! Saved 'delta_wrapping_proof.gif'.")
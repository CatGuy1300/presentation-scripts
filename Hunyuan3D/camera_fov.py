import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Object dimensions
R_obj = 1.0

fig, ax = plt.subplots(figsize=(8, 8))


def update(frame):
    ax.clear()
    ax.set_xlim(-5, 5)
    ax.set_ylim(-1, 10)
    ax.axis('off')

    # Animate FoV from 70 degrees down to 10 degrees, then back up
    # Using a sine wave for smooth back-and-forth oscillation
    progress = np.sin((frame / 120) * np.pi)
    fov_deg = 70.0 - (progress * 60.0)  # Moves between 70 and 10

    # MATH: To keep the object framed, r = R / sin(FoV / 2)
    fov_rad = np.radians(fov_deg)
    r_cam = R_obj / np.sin(fov_rad / 2.0)

    # Draw the 3D Object (Top-down view as a circle)
    circle = plt.Circle((0, 0), R_obj, color='dodgerblue', alpha=0.5, label="3D Mesh")
    ax.add_patch(circle)

    # Draw the Camera
    ax.scatter([0], [r_cam], color='black', s=100, zorder=5, label="Virtual Camera")

    # Draw the Camera's Vision Cone (Frustum)
    # The lines go from the camera down exactly tangent to the object
    L = 12  # Length of the vision lines
    left_x = -L * np.sin(fov_rad / 2.0)
    left_y = r_cam - L * np.cos(fov_rad / 2.0)
    right_x = L * np.sin(fov_rad / 2.0)
    right_y = r_cam - L * np.cos(fov_rad / 2.0)

    # Fill the vision cone
    ax.fill([0, left_x, right_x], [r_cam, left_y, right_y], color='yellow', alpha=0.2)
    ax.plot([0, left_x], [r_cam, left_y], color='orange', lw=2, linestyle='--')
    ax.plot([0, right_x], [r_cam, right_y], color='orange', lw=2, linestyle='--')

    # Add dynamic text showing the exact numbers
    ax.text(0, 9.5, f"Camera Lens (FoV): {fov_deg:.1f}°", fontsize=14, ha='center', fontweight='bold')
    ax.text(0, 8.8, f"Camera Distance (r): {r_cam:.2f}", fontsize=14, ha='center', color='darkred')

    ax.set_title("Ensuring Consistent Object Framing\nAs the lens gets narrower, the camera moves further back!",
                 fontsize=15)
    ax.legend(loc="upper left")


# 120 frames for a full smooth loop
ani = animation.FuncAnimation(fig, update, frames=120, interval=50)

print("Generating FoV GIF...")
ani.save('camera_fov.gif', writer='pillow', fps=20)
print("Done! Saved 'camera_fov.gif'.")
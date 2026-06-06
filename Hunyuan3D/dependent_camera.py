import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# The hidden math constant from the paper!
R_obj = 0.866

fig, ax = plt.subplots(figsize=(8, 8))


def update(frame):
    ax.clear()
    ax.set_xlim(-4, 4)
    ax.set_ylim(-1, 11)
    ax.axis('off')

    # Draw the 3D Object
    ax.add_patch(plt.Circle((0, 0), R_obj, color='dodgerblue', alpha=0.5))

    # Phase 1: Independent FoV change (Radius stays fixed)
    if frame < 50:
        progress = frame / 50.0
        fov_deg = 70.0 - (progress * 60.0)  # Shrinks 70 down to 10
        r_cam = 1.51  # Camera doesn't move!
        title = "What if they were independent?\nFoV shrinks, Camera stays still. Object is CROPPED!"
        color = 'crimson'

    # Phase 2: Independent Radius change (FoV stays fixed)
    elif frame < 100:
        progress = (frame - 50) / 50.0
        fov_deg = 70.0  # Lens stays wide
        r_cam = 1.51 + (progress * 8.43)  # Camera moves back to 9.94
        title = "What if they were independent?\nCamera moves back, FoV stays wide. Object is a TINY DOT!"
        color = 'crimson'

    # Phase 3: The Hunyuan3D Way (Radius is a function of FoV)
    else:
        progress = (frame - 100) / 60.0
        if progress > 1.0: progress = 1.0  # Pause at the end

        # FoV is chosen...
        fov_deg = 70.0 - (progress * 60.0)
        fov_rad = np.radians(fov_deg)

        # ...And radius is calculated mathematically!
        r_cam = R_obj / np.sin(fov_rad / 2.0)
        title = "The Hunyuan3D Math\nRadius is a function of FoV. Object is ALWAYS perfectly framed!"
        color = 'limegreen'

    # Draw Camera
    ax.scatter([0], [r_cam], color='black', s=100, zorder=5)

    # Draw Camera's Vision Cone (Frustum)
    fov_rad = np.radians(fov_deg)
    L = 15  # Length of vision lines
    lx, ly = -L * np.sin(fov_rad / 2), r_cam - L * np.cos(fov_rad / 2)
    rx, ry = L * np.sin(fov_rad / 2), r_cam - L * np.cos(fov_rad / 2)

    ax.fill([0, lx, rx], [r_cam, ly, ry], color=color, alpha=0.2)
    ax.plot([0, lx], [r_cam, ly], color=color, lw=2, linestyle='--')
    ax.plot([0, rx], [r_cam, ry], color=color, lw=2, linestyle='--')

    # Add Text
    ax.text(0, 10.3, title, fontsize=13, ha='center', fontweight='bold')
    ax.text(0, 9.5, f"FoV: {fov_deg:.1f}°  |  Radius: {r_cam:.2f}", fontsize=14, ha='center')


# 180 frames total
ani = animation.FuncAnimation(fig, update, frames=180, interval=50)

print("Generating Mathematical Proof GIF...")
ani.save('framing_proof.gif', writer='pillow', fps=20)
print("Done! Saved 'framing_proof.gif'.")
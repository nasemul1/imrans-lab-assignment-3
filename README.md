# imrans-lab-assignment-3

## How to run the rocket launch animation

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Render the animation (OpenGL recommended for 3D):
   ```
   manim -pqh --renderer=opengl starship_mission.py RocketLaunchScene
   ```

- The output video will open automatically if successful.
- You can adjust quality by changing `-pqh` to `-pql` (low) or `-pqh` (high).


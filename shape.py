import svgwrite
import math

CENTER = (150, 150)  # Center coordinates of the circle
RADIUS = 100  # Radius of the circle


def deg2rad(angle):
    return angle * 2 * math.pi / 360


def rad2deg(angle):
    return angle / 2 / math.pi * 360


def create_circle(dwg, circle_center, circle_radius):
    return dwg.circle(
        center=circle_center, r=circle_radius, fill="none", stroke="#ffd42a"
    )


def move(origin, length, angle):
    return (origin[0] + length * math.cos(angle), origin[1] + length * math.sin(angle))


def move_convex(origin, length, angle):
    return (
        origin[0] + length * math.cos(angle) + math.sin(2 * angle) * length,
        origin[1] + length * math.sin(angle) + math.sin(2 * angle) * length,
    )


def create_arc(dwg, origin, radius, angle, angleStart, strokeColor="#555"):
    """Create an arc as a Path. The arc is a portion of a circle of origin 'origin' and radius 'radius', starting at angleStart and lasting until angle."""
    coords = []
    for a in range(1, round(rad2deg(angle))):
        c = move(origin, radius, deg2rad(a) + angleStart)
        coords.append(c)

    path_data = f"M {' '.join([f'{x},{y}' for x, y in coords])}"
    return dwg.path(d=path_data, fill="none", stroke=strokeColor)


def create_convex_shape(filename, n, f):
    """
    Create a shape with n convex arc, f being a convex factor. Saved in filename.
    """

    dwg = svgwrite.Drawing(filename, size=("300", "300"), profile="tiny")

    circle = create_circle(dwg, CENTER, RADIUS)
    dwg.add(circle)

    for i in range(n):
        """radius_f is the new radius used to draw a convex arc"""
        radius_f = RADIUS * math.sqrt(
            (1 - f * math.cos(math.pi / n)) ** 2 + (f * math.sin(math.pi / n)) ** 2
        )

        """ drawing_angle is the angle along which the convex arc is drawn """
        drawing_angle = 2 * (
            math.asin(f * math.sin(math.pi / n) / (radius_f / RADIUS)) + math.pi / n
        )

        angle_quadrant = i * (2 * math.pi / n)

        origin_t = (
            CENTER[0] + math.cos(angle_quadrant) * f * RADIUS,
            CENTER[1] + math.sin(angle_quadrant) * f * RADIUS,
        )

        angle_start = angle_quadrant - drawing_angle / 2

        convex_arc = create_arc(
            dwg, origin_t, radius_f, drawing_angle, angle_start, "#111"
        )

        dwg.add(convex_arc)

    dwg.save(pretty=True)


CONVEX_F = [0, 0.25, 0.4]

for n in [3, 4, 5, 6]:
    for f in CONVEX_F:
        create_convex_shape(f"convex{n}_factor{f}.svg", n, f)

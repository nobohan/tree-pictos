import svgwrite
import math

CENTER = (150, 150)  # Center coordinates of the circle
RADIUS = 100  # Radius of the circle
N = 4


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


def create_arc(dwg, origin, radius, angle, angleStart):
    """Create an arc as a Path. The arc is a portion of a circle of origin 'origin' and radius 'radius', starting at angleStart and lasting until angle."""
    coords = []
    for a in range(1, round(rad2deg(angle))):
        c = move(origin, radius, deg2rad(a) + angleStart)
        coords.append(c)

    path_data = f"M {' '.join([f'{x},{y}' for x, y in coords])}"
    return dwg.path(d=path_data, fill="none", stroke="#555")


def create_convex_arc(dwg, origin, radius, angle, angleStart, convex_f, i, n):
    """
    Create an arc as a Path. The arc is a portion of a circle of origin 'origin'
    and radius 'radius', starting at angleStart and lasting until angle.
    The origin point is translated by a convex_f factor. The radius is adapted by
    this convex_f factor.
    """
    coords = []

    radius_t = radius * math.sqrt(
        (1 - convex_f) ** 2 + (convex_f * math.tan((2 * math.pi) / (2 * n))) ** 2
    )

    x_sign = 1 if i in [0, 3] else -1
    y_sign = 1 if i in [0, 1] else -1
    if n == 3:
        origin_t = (
            origin[0] + x_sign * convex_f * radius, # * math.cos((2 * math.pi) / (2 * n)),
            origin[1] + y_sign * convex_f * radius * math.tan((2 * math.pi) / (2 * n)),
        )
    else:  # n=4
        origin_t = (
            origin[0] + x_sign * convex_f * radius,
            origin[1] + y_sign * convex_f * radius,
        )

    for a in range(1, round(rad2deg(angle))):
        c = move(origin_t, radius_t, deg2rad(a) + angleStart)
        coords.append(c)

    path_data = f"M {' '.join([f'{x},{y}' for x, y in coords])}"
    return dwg.path(d=path_data, fill="none", stroke="#111")


def create_convex_shape(filename, n, convex_f):
    dwg = svgwrite.Drawing(filename, size=("300", "300"), profile="tiny")

    circle = create_circle(dwg, CENTER, RADIUS)
    dwg.add(circle)

    for i in range(n):
        arc = create_arc(dwg, CENTER, RADIUS, 2 * math.pi / n, i * (2 * math.pi / n))
        dwg.add(arc)

        print("angle")
        angle = 2 * (
            math.atan(convex_f * RADIUS / (RADIUS - convex_f * RADIUS)) + math.pi / n
        )
        print(angle)
        angle_start = -(angle - 2 * math.pi / n) / 2 + i * (2 * math.pi / n)
        print("angle start")
        print(rad2deg(angle_start))
        convex_arc = create_convex_arc(
            dwg, CENTER, RADIUS, angle, angle_start, convex_f, i, n
        )
        dwg.add(convex_arc)

    dwg.save(pretty=True)


CONVEX_F = [0, 0.2, 0.25, 0.33, 0.4, 0.5]
# CONVEX_F = [0.25]

for n in [3, 4]:
    for f in CONVEX_F:
        create_convex_shape(f"convex{n}_factor{f}.svg", n, f)

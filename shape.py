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
        center=circle_center, r=circle_radius, fill="none", stroke="yellow"
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
    return dwg.path(d=path_data, fill="none", stroke="blue")


def create_convex_arc(dwg, origin, radius, angle, angleStart, convex_f, i):
    """Create an arc as a Path. The arc is a portion of a circle of origin 'origin' and radius 'radius', starting at angleStart and lasting until angle."""
    coords = []
    x_sign = 1 if i in [0, 3] else -1
    y_sign = 1 if i in [0, 1] else -1
    origin_t = (
        origin[0] + x_sign * convex_f * radius,
        origin[1] + y_sign * convex_f * radius,
    )
    radius_t = radius * math.sqrt(2 * (convex_f * convex_f) - 2 * convex_f + 1)
    for a in range(1, round(rad2deg(angle))):
        c = move(origin_t, radius_t, deg2rad(a) + angleStart)
        coords.append(c)

    path_data = f"M {' '.join([f'{x},{y}' for x, y in coords])}"
    return dwg.path(d=path_data, fill="none", stroke="black")


def create_convex_shape(filename, n, convex_f):
    dwg = svgwrite.Drawing(filename, size=("300", "300"), profile="tiny")

    circle = create_circle(dwg, CENTER, RADIUS)
    dwg.add(circle)

    for i in range(n):
        arc = create_arc(dwg, CENTER, RADIUS, 2 * math.pi / n, i * (2 * math.pi / n))
        dwg.add(arc)

        angle = 2 * (
            math.atan(convex_f * RADIUS / (RADIUS - convex_f * RADIUS)) + math.pi / n
        )
        angle_start = -(angle - 2 * math.pi / n) / 2 + i * (2 * math.pi / n)
        print("angle start")
        print(rad2deg(angle_start))
        convex_arc = create_convex_arc(
            dwg, CENTER, RADIUS, angle, angle_start, convex_f, i
        )
        dwg.add(convex_arc)

    dwg.save(pretty=True)


CONVEX_F = [0, 0.25, 0.33, 0.5, 0.75, 0.99]
#CONVEX_F = [0.33, 0.5]

for n in [4]:
    for f in CONVEX_F:
        create_convex_shape(f"shape{n}_factor{f}.svg", n, f)

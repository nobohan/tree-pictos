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


def create_arc(dwg, origin, radius, angle, angleStart, strokeColor="#555"):
    """Create an arc as a Path. The arc is a portion of a circle of origin 'origin' and radius 'radius', starting at angleStart and lasting until angle."""
    coords = []
    for a in range(1, round(rad2deg(angle))):
        c = move(origin, radius, deg2rad(a) + angleStart)
        coords.append(c)

    path_data = f"M {' '.join([f'{x},{y}' for x, y in coords])}"
    return dwg.path(d=path_data, fill="none", stroke=strokeColor)


def create_convex_arc(dwg, origin, radius, angle, g, angle_quartant, n):
    """
    Create an arc as a Path. The arc is a portion of a circle of origin 'origin'
    and radius 'radius', starting at angleStart and lasting until angle.
    The origin point is translated by a convex_f factor. The radius is adapted by
    this convex_f factor.
    """

    angle_quartant_start = angle_quartant + ((2 * math.pi)/(2 * n))

    origin_t = (
        origin[0] + math.cos(angle_quartant_start) * g * RADIUS,
        origin[1] + math.sin(angle_quartant_start) * g * RADIUS,
    )

    angle_start = angle_quartant - (angle - 2 * math.pi / n) / 2

    return create_arc(dwg, origin_t, radius, angle, angle_start, "#111")


def create_convex_shape(filename, n, g):
    dwg = svgwrite.Drawing(filename, size=("300", "300"), profile="tiny")

    circle = create_circle(dwg, CENTER, RADIUS)
    dwg.add(circle)

    for i in range(n):
        arc = create_arc(dwg, CENTER, RADIUS, 2 * math.pi / n, i * (2 * math.pi / n))
        dwg.add(arc)

        #print("angle")
        angle = 2 * (
            math.atan(g * RADIUS / (RADIUS - g * RADIUS)) + math.pi / n
        ) #TODO normaliser la formule en fct de radius_t
        #print(angle)


        radius_t = RADIUS * math.sqrt(
            (1 - g * math.cos(math.pi / n)) ** 2 + (g * math.sin(math.pi / n)) ** 2
        )
        print(radius_t)
        angle_quartant = i * (2 * math.pi / n)

        print("angle quartant")
        print(rad2deg(angle_quartant))
        convex_arc = create_convex_arc(
            dwg, CENTER, radius_t, angle, g, angle_quartant, n
        )
        dwg.add(convex_arc)

    dwg.save(pretty=True)


G = [0, 0.2, 0.25, 0.33, 0.4, 0.5]
G = [0, 0.25, 0.4]
# CONVEX_F = [0.25]

for n in [3, 4, 5, 6 ]:
    for g in G:
        create_convex_shape(f"convex{n}_factor{g}.svg", n, g)

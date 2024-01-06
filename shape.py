import svgwrite
import math

CENTER = (250, 250)  # Center coordinates of the circle
RADIUS = 100  # Radius of the circle
DOT_RADIUS = 4
STROKE_WIDTH = 4


def deg2rad(angle):
    return angle * 2 * math.pi / 360


CHOUYA = deg2rad(2)  # Small angle needed to really finish the arc


def rad2deg(angle):
    return angle / 2 / math.pi * 360


def create_circle(
    dwg, circle_center, circle_radius, stroke_color="#ffd42a", stroke_width=1
):
    return dwg.circle(
        center=circle_center,
        r=circle_radius,
        fill="none",
        stroke=stroke_color,
        stroke_width=stroke_width,
    )


def create_dot(dwg, circle_center, circle_radius=DOT_RADIUS, color="#111"):
    return dwg.circle(center=circle_center, r=circle_radius, fill=color, stroke=color)


def move(origin, length, angle):
    return (origin[0] + length * math.cos(angle), origin[1] + length * math.sin(angle))


def create_arc(dwg, origin, radius, angle, angleStart, strokeColor="#555"):
    """
    Create an arc as a Path. The arc is a portion of a circle of origin 'origin'
    and radius 'radius', starting at angleStart and lasting until angle.
    """
    coords = []
    for a in range(1, round(rad2deg(angle))):
        c = move(origin, radius, deg2rad(a) + angleStart)
        coords.append(c)

    path_data = f"M {' '.join([f'{x},{y}' for x, y in coords])}"
    return dwg.path(
        d=path_data, fill="none", stroke=strokeColor, stroke_width=STROKE_WIDTH
    )


def convex_arc_radius(convexity, angle_quadrant):
    """
    Compute a new radius used to draw a convex arc
    """
    return RADIUS * math.sqrt(
        (1 - convexity * math.cos(angle_quadrant / 2)) ** 2
        + (convexity * math.sin(angle_quadrant / 2)) ** 2
    )


def convex_drawing_angle(convexity, angle_quadrant, convex_radius):
    """
    Compute an angle along which the convex arc is drawn
    """
    return (
        2
        * (
            math.asin(
                convexity * math.sin(angle_quadrant / 2) / (convex_radius / RADIUS)
            )
            + angle_quadrant / 2
        )
        + CHOUYA
    )


def concave_arc_radius(concavity, angle_quadrant):
    """
    Compute a new radius used to draw a concave arc
    """
    return -RADIUS * math.sqrt(
        (1 - 2 * concavity * math.cos(angle_quadrant / 2) + concavity**2)
    )


def concave_drawing_angle(concavity, angle_quadrant, concave_radius):
    """
    Compute an angle along which the concave arc is drawn
    """
    return (
        2
        * math.acos(
            RADIUS * (concavity - math.cos(angle_quadrant / 2)) / concave_radius
        )
        + CHOUYA
    )


def create_broadleaved_symbol(
    filename, n, convex_or_concave, curvity, points=None, centroid=False
):
    """
    Create a broadleaved tree symbol with n convex or concave arc, curvity being a convex
    or concave factor. Points can be added, as well as a centroid. Pictogram saved as
    filename in svg.
    """

    dwg = svgwrite.Drawing(filename, size=("500", "500"), profile="tiny")

    angle_quadrant = 2 * math.pi / n

    for i in range(n):
        if convex_or_concave == "convex":
            radius = convex_arc_radius(curvity, angle_quadrant)
            drawing_angle = convex_drawing_angle(curvity, angle_quadrant, radius)
        else:
            radius = concave_arc_radius(curvity, angle_quadrant)
            drawing_angle = concave_drawing_angle(curvity, angle_quadrant, -radius)

        angle_quadrant_i = i * angle_quadrant

        origin_t = (
            CENTER[0] + math.cos(angle_quadrant_i) * curvity * RADIUS,
            CENTER[1] + math.sin(angle_quadrant_i) * curvity * RADIUS,
        )

        angle_start = angle_quadrant_i - drawing_angle / 2

        arc = create_arc(dwg, origin_t, radius, drawing_angle, angle_start, "#111")

        dwg.add(arc)

        for p in points:
            new_origin = move(CENTER, RADIUS * p, angle_quadrant_i - angle_quadrant / 2)
            circle = create_dot(dwg, new_origin)
            dwg.add(circle)

        if centroid:
            circle = create_circle(dwg, CENTER, 10, stroke_color="#111", stroke_width=4)
            dwg.add(circle)

    dwg.save(pretty=True)


N = [3, 4, 5]
CONVEXITY = [0.25, 0.4]

for n in N:
    for c in CONVEXITY:
        create_broadleaved_symbol(
            f"convex{n}_factor{c}.svg", n, "convex", c, [1.2, 1.6, 2], True
        )

CONCAVITY = [3, 4]

for n in N:
    for c in CONCAVITY:
        create_broadleaved_symbol(
            f"concave{n}_factor{c}.svg", n, "concave", c, [1.2, 1.6, 2], True
        )

import svgwrite
import math

CENTER = (250, 250)  # Center coordinates of the circle
RADIUS = 100  # Radius of the circle
DOT_RADIUS = 4
STROKE_WIDTH = 4

def deg2rad(angle):
    return angle * 2 * math.pi / 360

CHOUYA = deg2rad(2) # Small angle needed to really finish the arc


def rad2deg(angle):
    return angle / 2 / math.pi * 360


def create_circle(dwg, circle_center, circle_radius, stroke_color="#ffd42a", stroke_width=1):
    return dwg.circle(
        center=circle_center, r=circle_radius, fill="none", stroke=stroke_color, stroke_width=stroke_width
    )


def create_dot(dwg, circle_center, circle_radius=DOT_RADIUS, color="#111"):
    return dwg.circle(center=circle_center, r=circle_radius, fill=color, stroke=color)


def move(origin, length, angle):
    return (origin[0] + length * math.cos(angle), origin[1] + length * math.sin(angle))


def create_arc(dwg, origin, radius, angle, angleStart, strokeColor="#555"):
    """Create an arc as a Path. The arc is a portion of a circle of origin 'origin' and radius 'radius', starting at angleStart and lasting until angle."""
    coords = []
    for a in range(1, round(rad2deg(angle))):
        c = move(origin, radius, deg2rad(a) + angleStart)
        coords.append(c)

    path_data = f"M {' '.join([f'{x},{y}' for x, y in coords])}"
    return dwg.path(
        d=path_data, fill="none", stroke=strokeColor, stroke_width=STROKE_WIDTH
    )


def create_convex_shape(filename, n, convexity, points=[], centroid=False):
    """
    Create a shape with n convex arc, convexity being a convex factor. Saved in filename.
    """

    dwg = svgwrite.Drawing(filename, size=("500", "500"), profile="tiny")

    circle = create_circle(dwg, CENTER, RADIUS)
    dwg.add(circle)

    alpha = 2 * math.pi / n

    for i in range(n):
        """radius_f is the new radius used to draw a convex arc"""
        radius_f = RADIUS * math.sqrt(
            (1 - convexity * math.cos(alpha / 2)) ** 2
            + (convexity * math.sin(alpha / 2)) ** 2
        )

        """ drawing_angle is the angle along which the convex arc is drawn """
        drawing_angle = 2 * (
            math.asin(convexity * math.sin(alpha / 2) / (radius_f / RADIUS)) + alpha / 2
        ) + CHOUYA

        angle_quadrant = i * alpha

        origin_t = (
            CENTER[0] + math.cos(angle_quadrant) * convexity * RADIUS,
            CENTER[1] + math.sin(angle_quadrant) * convexity * RADIUS,
        )

        angle_start = angle_quadrant - drawing_angle / 2

        convex_arc = create_arc(
            dwg, origin_t, radius_f, drawing_angle, angle_start, "#111"
        )

        dwg.add(convex_arc)

        for p in points:
            new_origin = move(CENTER, RADIUS * p, angle_quadrant - alpha / 2)
            circle = create_dot(dwg, new_origin)
            dwg.add(circle)

        if centroid:
            circle = create_circle(dwg, CENTER, 10, stroke_color="#111", stroke_width=4)
            dwg.add(circle)

    dwg.save(pretty=True)


#TODO factorise convex and concave functions. Externalise radius_f and drawing_angle computation

def create_concave_shape(filename, n, f, points=[], centroid=False):
    """
    Create a shape with n concave arc, f being a concave factor. Saved in filename.
    """

    dwg = svgwrite.Drawing(filename, size=("500", "500"), profile="tiny")

    circle = create_circle(dwg, CENTER, RADIUS)
    dwg.add(circle)

    alpha = 2 * math.pi / n

    for i in range(n):
        """radius_f is the new radius used to draw a concave arc"""
        radius_f = RADIUS * math.sqrt((1 - 2 * f * math.cos(alpha / 2) + f**2))

        """drawing_angle is the angle along which the concave arc is drawn"""
        drawing_angle = 2 * math.acos(RADIUS * (f - math.cos(alpha / 2)) / radius_f) + CHOUYA

        angle_quadrant = i * alpha

        origin_t = (
            CENTER[0] + math.cos(angle_quadrant) * f * RADIUS,
            CENTER[1] + math.sin(angle_quadrant) * f * RADIUS,
        )

        angle_start = angle_quadrant - drawing_angle / 2

        concave_arc = create_arc(
            dwg, origin_t, -radius_f, drawing_angle, angle_start, "#111"
        )

        dwg.add(concave_arc)

        for p in points:
            new_origin = move(CENTER, RADIUS * p, angle_quadrant - alpha / 2)
            circle = create_dot(dwg, new_origin)
            dwg.add(circle)
        
        if centroid:
            circle = create_circle(dwg, CENTER, 10, stroke_color="#111", stroke_width=4)
            dwg.add(circle)

    dwg.save(pretty=True)


N = [3, 4, 5]
CONVEX_F = [0.25, 0.4]

for n in N:
    for f in CONVEX_F:
        create_convex_shape(f"convex{n}_factor{f}.svg", n, f, [1.2, 1.6, 2], True)

CONCAVE_F = [3, 4]

for n in N:
    for f in CONCAVE_F:
        create_concave_shape(f"concave{n}_factor{f}.svg", n, f, [1.2, 1.6, 2], True)

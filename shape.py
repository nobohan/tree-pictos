import svgwrite
import math

CENTER = (250, 250)  # Center coordinates of the circle
RADIUS = 100  # Radius of the circle
DOT_RADIUS = 14
O_RADIUS = 22
STROKE_WIDTH = 36
MAIN_BRANCH_START_LENGTH = 0.75 * RADIUS
BRANCH_LENGTH = 20
STROKE_COLOR = "#09711c"


def deg2rad(angle):
    return angle * 2 * math.pi / 360


CHOUYA = deg2rad(2)  # Small angle needed to really finish the arc


def rad2deg(angle):
    return angle / 2 / math.pi * 360


def draw_circle(
    dwg, circle_center, circle_radius, stroke_color="#ffd42a", stroke_width=STROKE_WIDTH
):
    return dwg.circle(
        center=circle_center,
        r=circle_radius,
        fill="none",
        stroke=stroke_color,
        stroke_width=stroke_width,
    )


def draw_dot(dwg, circle_center, circle_radius=DOT_RADIUS, color=STROKE_COLOR):
    return dwg.circle(center=circle_center, r=circle_radius, fill=color, stroke=color)


def move(origin, length, angle):
    return (origin[0] + length * math.cos(angle), origin[1] + length * math.sin(angle))


def draw_line(dwg, start_point, end_point, strokeColor=STROKE_COLOR):
    """
    Draw a line from a start_point to an end_point
    """
    coords = [start_point, end_point]

    path_data = f"M {' '.join([f'{x},{y}' for x, y in coords])}"
    return dwg.path(
        d=path_data, fill="none", stroke=strokeColor, stroke_width=STROKE_WIDTH
    )


def draw_arc(dwg, origin, radius, angle, angleStart, strokeColor="#555"):
    """
    Draw an arc as a Path. The arc is a portion of a circle of origin 'origin'
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


def draw_branch(dwg, origin, angle_main_branch, branch_length):
    """
    Draw some branches starting from a origin point, orthogonally from the angle_main_branch
    """

    start_point = move(origin, branch_length, angle_main_branch + math.pi / 2)
    end_point = move(origin, branch_length, angle_main_branch - math.pi / 2)

    line = draw_line(dwg, start_point, end_point)
    return line


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


def get_filename(leaved, curvity, n, dots, centre):
    if leaved == "broadleaved":
        l = "B"
    else:
        l = "C"
    if curvity == "convex":
        cu = "+"
    elif curvity == "concave":
        cu = "-"
    else:
        cu = ""
    if dots is None:
        d = ""
    else:
        d = f"d{len(dots)}"
    if centre is None:
        c = ""
    else:
        c = f"{centre}"

    if curvity == "circular" and n == 1:
        return f"{l}{d}{c}.svg"
    else:
        return f"{l}{n}{cu}{d}{c}.svg"


def get_exp(n):
    if n == 1:
        return chr(0x00B9)
    elif n == 2:
        return chr(0x00B2)
    elif n == 3:
        return chr(0x00B3)
    else:
        return ""


def get_symbol_label(leaved, curvity, n, dots, centre):
    if leaved == "broadleaved":
        l = "B"
    else:
        l = "C"
    if curvity == "convex":
        cu = "+"
    elif curvity == "concave":
        cu = "-"
    else:
        cu = ""
    if dots is None:
        d = ""
    else:
        d = f"d{get_exp(len(dots))}"
    if centre is None:
        c = ""
    else:
        c = f"{centre}"

    if curvity == "circular" and n == 1:
        return f"{l}{d}{c}"
    else:
        return f"{l}{n}{cu}{d}{c}"


def draw_broadleaved_symbol(
    dwg, center, n, convex_or_concave, curvity, dots=None, centroid=None, label=False
):
    """
    Draw a broadleaved tree symbol with n convex or concave arc, curvity being a convex
    or concave factor. Points can be added, as well as a centroid. Returns the drawing
    svgwrite object.
    """
    if label:
        symbol_label = get_symbol_label("broadleaved", convex_or_concave, n, dots, centroid)
        paragraph = dwg.add(
            dwg.g(
                class_="label",
            )
        )
        paragraph.add(dwg.text(symbol_label, (center[0] - 10, center[1] - 180)))

    angle_quadrant = 2 * math.pi / n

    has_drawn_circle = False

    for i in range(n):
        angle_quadrant_i = i * angle_quadrant

        if convex_or_concave == "circular":
            if not has_drawn_circle:
                circle = draw_circle(dwg, center, RADIUS, stroke_color=STROKE_COLOR)
                dwg.add(circle)
                has_drawn_circle = True

        else:
            if convex_or_concave == "convex":
                radius = convex_arc_radius(curvity, angle_quadrant)
                drawing_angle = convex_drawing_angle(curvity, angle_quadrant, radius)
            elif convex_or_concave == "concave":
                radius = concave_arc_radius(curvity, angle_quadrant)
                drawing_angle = concave_drawing_angle(curvity, angle_quadrant, -radius)

            origin_t = (
                center[0] + math.cos(angle_quadrant_i) * curvity * RADIUS,
                center[1] + math.sin(angle_quadrant_i) * curvity * RADIUS,
            )

            angle_start = angle_quadrant_i - drawing_angle / 2

            arc = draw_arc(
                dwg, origin_t, radius, drawing_angle, angle_start, STROKE_COLOR
            )
            dwg.add(arc)

        if dots:
            for p in dots:
                new_origin = move(
                    center, RADIUS * p, angle_quadrant_i - angle_quadrant / 2
                )
                dot = draw_dot(dwg, new_origin)
                dwg.add(dot)

    if centroid:
        if centroid == "p":
            point = draw_dot(dwg, center)
            dwg.add(point)
        elif centroid == "o":
            circle = draw_circle(dwg, center, O_RADIUS, stroke_color=STROKE_COLOR)
            dwg.add(circle)

    return dwg


def draw_needleleaved_symbol(dwg, center, n, branches=None, centroid=None, label=False):
    """
    Draw a needle-leaved tree symbol with n spikes.
    Branches can be added, as well as a centroid. Returns the drawing
    svgwrite object.
    """
    if label:
        symbol_label = get_symbol_label("needleleaved", None, n, branches, centroid)
        paragraph = dwg.add(
            dwg.g(
                class_="label",
            )
        )
        paragraph.add(dwg.text(symbol_label, (center[0] - 10, center[1] - 180)))


    circle = draw_circle(dwg, center, RADIUS, stroke_color=STROKE_COLOR)
    dwg.add(circle)

    angle_quadrant = 2 * math.pi / n

    for i in range(n):
        angle_quadrant_i = i * angle_quadrant + math.pi / n

        # draw main branch
        if branches:
            main_branch_length = RADIUS * (branches[-1] - 1) + 2 * BRANCH_LENGTH
        else:
            main_branch_length = MAIN_BRANCH_START_LENGTH

        start_point = move(center, RADIUS, angle_quadrant_i)
        end_point = move(center, RADIUS + main_branch_length, angle_quadrant_i)
        line = draw_line(dwg, start_point, end_point)
        dwg.add(line)

        # draw sub-branches
        if branches:
            position = len(branches)
            ib = 1
            for b in branches:
                new_origin = move(center, RADIUS * b, angle_quadrant_i)

                branch = draw_branch(
                    dwg, new_origin, angle_quadrant_i, position * BRANCH_LENGTH
                )
                dwg.add(branch)

                position = position - 1
                ib = ib + 1

    if centroid:
        if centroid == "p":
            point = draw_dot(dwg, center)
            dwg.add(point)
        elif centroid == "o":
            circle = draw_circle(dwg, center, O_RADIUS, stroke_color=STROKE_COLOR)
            dwg.add(circle)

    return dwg


def create_broadleaved_symbol(n, convex_or_concave, curvity, dots=None, centroid=None, label=False):
    """
    Create a broadleaved tree symbol with n convex or concave arc, curvity being a convex
    or concave factor. Points can be added, as well as a centroid. The pictogram is saved
    in svg.
    """
    filename = get_filename(
        "broadleaved",
        convex_or_concave,
        n,
        dots,
        centroid,
    )

    dwg = svgwrite.Drawing(filename, size=("500", "500"), profile="full")
    dwg.embed_font(name="Alfphabet", filename="fonts/Alfphabet-III.otf")
    dwg.embed_stylesheet(
        """
    .label {
        font-family: "Alfphabet";
        font-size: 14;
        font-weight: bold;
    }"""
    )

    dwg = draw_broadleaved_symbol(
        dwg, CENTER, n, convex_or_concave, curvity, dots, centroid, label
    )

    dwg.save(pretty=True)


def create_needleleaved_symbol(n, branches=None, centroid=None, label=False):
    filename = get_filename(
        "needleleaved",
        "",
        n,
        branches,
        centroid,
    )

    dwg = svgwrite.Drawing(filename, size=("500", "500"), profile="full")
    dwg.embed_font(name="Alfphabet", filename="fonts/Alfphabet-III.otf")
    dwg.embed_stylesheet(
        """
    .label {
        font-family: "Alfphabet";
        font-size: 14;
        font-weight: bold;
    }"""
    )

    dwg = draw_needleleaved_symbol(dwg, CENTER, n, branches, centroid, label)

    dwg.save(pretty=True)

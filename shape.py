import svgwrite
import math

# Set constants
CENTER = (150, 150)   # Center coordinates of the circle
RADIUS = 100          # Radius of the circle


def create_circle(dwg, circle_center, circle_radius):
    return dwg.circle(center=circle_center, r=circle_radius, fill='none', stroke='yellow')


def move(origin, length, angle):
    return (origin[0] + length * math.cos(angle), origin[1] + length * math.sin(angle))

def move_convex(origin, length, angle):
    return (origin[0] + length * math.cos(angle) + math.sin(2*angle)*length, origin[1] + length * math.sin(angle)+ math.sin(2*angle)*length)


def create_arc(dwg, origin, radius, angle, angleStart):
    """ Create an arc as a Path. The arc is a portion of a circle of origin 'origin' and radius 'radius', starting at angleStart and lasting until angle."""
    coords = []
    for a in range(1, round(rad2deg(angle))):
        c = move(origin, radius, deg2rad(a) + angleStart)
        coords.append(c)

    path_data = f"M {' '.join([f'{x},{y}' for x, y in coords])}"
    return dwg.path(d=path_data, fill='none', stroke='black')


def create_convex_arc(dwg, origin, radius, angle, angleStart):
    """ Create an arc as a Path. The arc is a portion of a circle of origin 'origin' and radius 'radius', starting at angleStart and lasting until angle."""
    coords = []
    for a in range(1, round(rad2deg(angle))):
        c = move_convex(origin, radius, deg2rad(a) + angleStart)
        coords.append(c)

    path_data = f"M {' '.join([f'{x},{y}' for x, y in coords])}"
    return dwg.path(d=path_data, fill='none', stroke='blue')


def deg2rad(angle):
    return angle*2*math.pi/360

def rad2deg(angle):
    return angle/2/math.pi*360

def create_shape(filename):

    dwg = svgwrite.Drawing(filename, size=('300', '300'), profile='tiny')

    circle = create_circle(dwg, CENTER, RADIUS)
    dwg.add(circle)

    arc = create_arc(dwg, CENTER, RADIUS, deg2rad(360/4*3), deg2rad(45/2))
    dwg.add(arc)

    convex_arc = create_convex_arc(dwg, CENTER, RADIUS, deg2rad(360/4*3), deg2rad(45/2))
    dwg.add(convex_arc)

    dwg.save(pretty=True)


svg_filename = 'shape.svg'
create_shape(svg_filename)

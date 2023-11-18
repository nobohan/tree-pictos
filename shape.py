import svgwrite
import math

CENTER = (150, 150)   # Center coordinates of the circle
RADIUS = 100          # Radius of the circle
N = 4

def deg2rad(angle):
    return angle*2*math.pi/360

def rad2deg(angle):
    return angle/2/math.pi*360

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


def create_convex_arc(dwg, origin, radius, angle, angleStart, convex_f):
    """ Create an arc as a Path. The arc is a portion of a circle of origin 'origin' and radius 'radius', starting at angleStart and lasting until angle."""
    coords = []
    origin_t = (origin[0] + convex_f*radius, origin[1] + convex_f*radius)
    radius_t = radius * math.sqrt(2 * (convex_f*convex_f) - 2 * convex_f + 1)
    for a in range(1, round(rad2deg(angle))):
        c = move(origin_t, radius_t, deg2rad(a) + angleStart)
        coords.append(c)

    path_data = f"M {' '.join([f'{x},{y}' for x, y in coords])}"
    return dwg.path(d=path_data, fill='none', stroke='blue')

def create_shape(filename, convex_f):

    dwg = svgwrite.Drawing(filename, size=('300', '300'), profile='tiny')

    circle = create_circle(dwg, CENTER, RADIUS)
    dwg.add(circle)

    arc = create_arc(dwg, CENTER, RADIUS, deg2rad(360/N), deg2rad(0))
    dwg.add(arc)


    angle = 4 * math.atan(convex_f) + deg2rad(360/N) #TODO trouver la fonction qui change les 2 angles en fonction de convex_f
    angle_start = (angle - deg2rad(360/N)) / 2
    print(angle)
    #print(angle_start)
    convex_arc = create_convex_arc(dwg, CENTER, RADIUS, angle, -angle_start, convex_f)
    dwg.add(convex_arc)

    dwg.save(pretty=True)


svg_filename = 'shape.svg'

CONVEX_F = [0, 0.25, 0.33, 0.5, 0.75, 1]

for f in CONVEX_F:
    create_shape(f'shape.svg_{f}', f)

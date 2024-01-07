from shape import create_broadleaved_symbol

N = [3, 4, 5]

convexity = 0.3
concavity = 3

dot1 = 1.2
dot2 = 1.6
dot3 = 2
DOTS = [None, [dot1], [dot1, dot2], [dot1, dot2, dot3]]
CENTRE = [False, True]  # TODO differentiate centroid and round


def get_filename(leaved, curvity, n, dots, centre):  # TODO better syntax of filename
    if leaved == "broadleaved":
        l = "B"
    else:
        l = "C"
    if curvity == "convex":
        cu = "+"
    else:
        cu = "-"
    if dots is None:
        d = ''
    else:
        d = len(dots)
    if centre:
        c = "o"
    else: 
        c = "c"

    return f"{l}{cu}{n}{d}{c}.svg"


for n in N:
    for d in DOTS:
        for c in CENTRE:
            filename = get_filename(
                "broadleaved",
                "convex",
                n,
                d,
                c,
            )
            create_broadleaved_symbol(filename, n, "convex", convexity, d, c)
            filename = get_filename(
                "broadleaved",
                "concave",
                n,
                d,
                c,
            )
            create_broadleaved_symbol(
                filename,
                n,
                "concave",
                concavity,
                d,
                c,
            )

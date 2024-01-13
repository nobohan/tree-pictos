from shape import create_broadleaved_symbol

N = (3, 4, 5)

convexity = 0.3
concavity = 3

dot1 = 1.2
dot2 = 1.6
dot3 = 2
DOTS = (None, [dot1], [dot1, dot2], [dot1, dot2, dot3])

CENTRE = (None, "p", "o")

for c in CENTRE:
    create_broadleaved_symbol(1, "circular", 0, None, c)

for n in (3, 5):
    for d in DOTS[1:4]:
        for c in CENTRE:
            create_broadleaved_symbol(n, "circular", 0, d, c)

for n in N:
    for d in DOTS:
        for c in CENTRE:
            create_broadleaved_symbol(n, "convex", convexity, d, c)
            create_broadleaved_symbol(n, "concave", concavity, d, c)

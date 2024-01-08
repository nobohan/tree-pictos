from shape import create_broadleaved_symbol

N = (3, 4, 5)  ##TODO N=0 but with 3 or 5 dots...

convexity = 0.3
concavity = 3

dot1 = 1.2
dot2 = 1.6
dot3 = 2
DOTS = (None, [dot1], [dot1, dot2], [dot1, dot2, dot3])
CENTRE = (None, "p", "o")


for n in N:
    for d in DOTS:
        for c in CENTRE:
            create_broadleaved_symbol(n, "convex", convexity, d, c)
            create_broadleaved_symbol(n, "concave", concavity, d, c)

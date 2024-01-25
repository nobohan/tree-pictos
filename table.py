from shape import draw_broadleaved_symbol, draw_needleleaved_symbol, get_symbol_label
import svgwrite

convexity = 0.5
concavity = 3

dot1 = 1.2
dot2 = 1.6
dot3 = 2
DOTS = (None, [dot1], [dot1, dot2], [dot1, dot2, dot3])

b1 = 1.4
b2 = 1.8
b3 = 2.2
BRANCHES = (None, [b1], [b1, b2], [b1, b2, b3])

CENTRE = (None, "p", "o")

filename = "symbols-table.svg"

dwg = svgwrite.Drawing(filename, size=("6000", "5500"), profile="full")
dwg.embed_font(name="Alfphabet", filename="fonts/Alfphabet-III.otf")
dwg.embed_stylesheet(
    """
.label {
    font-family: "Alfphabet";
    font-size: 14;
    font-weight: bold;
}"""
)

X = list(range(250, 6250, 500))
Y = list(range(250, 6250, 500))

ii = 0
ORIGINS = ((X[0], Y[0]), (X[4], Y[0]), (X[8], Y[0]))
for c in CENTRE:
    dwg = draw_broadleaved_symbol(dwg, ORIGINS[ii], 1, "circular", 0, None, c)
    ii = ii + 1


ii = 0
ORIGINS = (
    (X[1], Y[0]), (X[2], Y[0]), (X[3], Y[0]), (X[5], Y[0]), (X[6], Y[0]), (X[7], Y[0]), (X[9], Y[0]), (X[10], Y[0]), (X[11], Y[0]),
    (X[1], Y[1]), (X[2], Y[1]), (X[3], Y[1]), (X[5], Y[1]), (X[6], Y[1]), (X[7], Y[1]), (X[9], Y[1]), (X[10], Y[1]), (X[11], Y[1]),
)
for n in (3, 5):
    for c in CENTRE:
        for d in DOTS[1:4]:
            dwg = draw_broadleaved_symbol(dwg, ORIGINS[ii], n, "circular", 0, d, c)
            ii = ii + 1


for n in (3, 4, 5):
    dwg = draw_broadleaved_symbol(dwg, (X[0], Y[n-1]), n, "convex", convexity, None, None)
    dwg = draw_broadleaved_symbol(dwg, (X[4], Y[n-1]), n, "convex", convexity, None, "p")
    dwg = draw_broadleaved_symbol(dwg, (X[8], Y[n-1]), n, "convex", convexity, None, "o")
    ii = 0
    ORIGINS = (
        (X[1], Y[n-1]), (X[2], Y[n-1]), (X[3], Y[n-1]), (X[5], Y[n-1]), (X[6], Y[n-1]), (X[7], Y[n-1]), (X[9], Y[n-1]), (X[10], Y[n-1]), (X[11], Y[n-1])
    )
    for c in CENTRE:
        for d in DOTS[1:4]:
            dwg = draw_broadleaved_symbol(dwg, ORIGINS[ii], n, "convex", convexity, d, c)
            ii = ii + 1


for n in (3, 4, 5):
    dwg = draw_broadleaved_symbol(dwg, (X[0], Y[n+2]), n, "concave", concavity, None, None)
    dwg = draw_broadleaved_symbol(dwg, (X[4], Y[n+2]), n, "concave", concavity, None, "p")
    dwg = draw_broadleaved_symbol(dwg, (X[8], Y[n+2]), n, "concave", concavity, None, "o")
    ii = 0
    ORIGINS = (
        (X[1], Y[n+2]), (X[2], Y[n+2]), (X[3], Y[n+2]), (X[5], Y[n+2]), (X[6], Y[n+2]), (X[7], Y[n+2]), (X[9], Y[n+2]), (X[10], Y[n+2]), (X[11], Y[n+2])
    )
    for c in CENTRE:
        for d in DOTS[1:4]:
            dwg = draw_broadleaved_symbol(dwg, ORIGINS[ii], n, "concave", concavity, d, c)
            ii = ii + 1


for n in (3, 4, 5):
    ii = 0
    ORIGINS = (
        (X[0], Y[n+5]), (X[1], Y[n+5]), (X[2], Y[n+5]), (X[3], Y[n+5]), (X[4], Y[n+5]), (X[5], Y[n+5]), (X[6], Y[n+5]), (X[7], Y[n+5]), (X[8], Y[n+5]), (X[9], Y[n+5]), (X[10], Y[n+5]), (X[11], Y[n+5])
    )
    for c in CENTRE:
        for branch in BRANCHES:
            draw_needleleaved_symbol(dwg, ORIGINS[ii], n, branch, c)
            ii = ii + 1


dwg.save(pretty=True)

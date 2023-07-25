from manim import *
import queue

# 马走日
dir = [[1, 2], [1, -2], [-1, 2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]]
n = 5
m = 4
d = np.full([n, m], -1)

dots = dict()
for r in range(n):
    for c in range(m):
        dots[(n-1-r,c)] = Dot(np.array([c, r, 0]))


def arrow(a, b):
    return Arrow(a, b, stroke_width=3, buff=0.05, max_tip_length_to_length_ratio=0.05, color=YELLOW)

g = Group()

def label(scn, r, c):
    scn.play(dots[(r,c)].animate.set_fill(GREEN), run_time=0.5)
    dist = Text(f"{d[r,c]}",color=BLUE).next_to(dots[(r,c)], UP, buff=0).scale(0.5)
    info = Text(f"({r}, {c}, {d[r,c]})").scale(0.4)
    if len(g) == 0:
        info.move_to(np.array([-5, 3, 0]))
    else:
        info.next_to(g[-1])
    scn.play(Create(dist))
    scn.play(ReplacementTransform(dots[(r,c)].copy(), info))
    g.add(info)


def bfs(r, c, scn):
    q = queue.Queue()
    d[r,c] = 0
    label(scn, r, c)
    q.put((r, c))
    while not q.empty():
        r, c = q.get()
        scn.play(Indicate(dots[(r, c)]))
        info = g[0]
        shift = g.get_left() - g.remove(g[0]).get_left()
        scn.play(info.animate.move_to(np.array([-5, 0, 0])).set_fill(PURPLE),
                 dots[(r,c)].animate.set_fill(PURPLE),
                 g.animate.shift(shift))
        for x, y in dir:
            nr = r + x
            nc = c + y
            if 0 <= nr and nr < n and 0 <= nc and nc < m and d[nr,nc] == -1:
                d[nr,nc] = d[r,c] + 1
                q.put((nr, nc))
                a = arrow(dots[(r, c)], dots[(nr, nc)])
                scn.play(Create(a), run_time=0.5)
                label(scn, nr, nc)
                scn.play(FadeOut(a), run_time=0.5)
        scn.play(dots[(r,c)].animate.set_fill(RED),
                 FadeOut(info))

class BFS(Scene):
    def construct(self):
        self.add(Group(*dots.values()).move_to(ORIGIN))
        self.add(Line(np.array([-6, 3.5, 0]), np.array([6, 3.5, 0])))
        self.add(Line(np.array([-6, 2.6, 0]), np.array([6, 2.6, 0])))
        bfs(0, 0, self)
        self.wait(2)
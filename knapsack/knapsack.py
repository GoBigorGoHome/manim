from manim import *


class MyTable(Table):
    def get(self, i: int, j: int):
        return self[0][i * self.col_dim + j]
    def set(self, i: int, j: int, target: Mobject):
        self[0][i * self.col_dim + j] = target.move_to(self[0][i * self.col_dim + j])
        return self
        

#  the assignment operator = in Python does not mutate the left-hand side,
# it only assigns a new name to the right-hand side.
class Knapsack(Scene):
    def construct(self):
        N = 3
        M = 10
        a = [(4, 7), (3, 6), (5, 11)]
        t = np.full((N+1, M+1), '.')
        F = np.zeros((N+1, M+1), dtype=np.int32)
        f = MyTable(t, include_outer_lines=True).scale(0.6).shift(RIGHT*2)
        f.get_rows().set_opacity(0)
        text = MathTex(r"N=3, M= 10\\ 4\ 7\\ 3\ 6 \\ 5\ 11").next_to(f, LEFT, buff=1)
        title = Title("01背包问题", tex_template=TexTemplateLibrary.ctex)
        self.add(text, f, title)
        self.wait(0.5)        
        for i in range(M + 1):
            self.play(f.animate.set(0, i, Text('0').scale(0.5)), run_time=0.1)
        for i in range(N):
            w, v = a[i]
            for j in range(min(M+1, w)):
                F[i+1][j] = F[i][j]
                t = Text(f"{F[i+1][j]}").move_to(f.get(i + 1, j)).scale(0.5)
                self.play(ReplacementTransform(f.get(i, j).copy(), t), run_time=0.5)
                f.set(i + 1, j, t)
            for j in range(w, M + 1):
                F[i+1][j] = max(F[i][j], F[i][j-w] + v)
                t = Text(f"{F[i+1][j]}").move_to(f.get(i + 1, j)).scale(0.5)
                self.play(Indicate(f.get(i, j)), Indicate(f.get(i, j - w)))
                # self.play(ReplacementTransform(Group(f.get(i, j), f.get(i, j - w)).copy(), t))
                f.set(i + 1, j, t)
        self.wait(2)
    
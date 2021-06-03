from GUI.Shapes.Shape import Shape


class Line(Shape):

    def __init__(self, parent, p0, p1, color, plot_style="o-"):
        super().__init__(parent, [p0[0], p1[0]], [p0[1], p1[1]], color, plot_style)

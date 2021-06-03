from GUI.Shapes.Shape import Shape


class Point(Shape):

    def __init__(self, parent, x0, y0, color, plot_style="o-"):
        super().__init__(parent, [x0], [y0], color, plot_style)

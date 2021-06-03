class Shape:

    def __init__(self, parent, x_coords, y_coords, color, plot_style="o-"):
        self.parent = parent
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.color = [color]
        self.plot_style = [plot_style]
        self.graph = [[self.x_coords, self.y_coords]]

    def modify_point(self, point_index, point):
        self.x_coords[point_index], self.y_coords[point_index] = point

    def append_point(self, point):
        self.x_coords.append(point[0])
        self.y_coords.append(point[1])

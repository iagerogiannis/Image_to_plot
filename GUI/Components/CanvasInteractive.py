import math
import matplotlib.figure as mpl_fig
import matplotlib.animation as anim
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.image as mpimg

from GUI.Shapes.Shapes import *
from plot_calculator.transformers import *
from plot_calculator.exporter import Exporter as expo


class CanvasInteractive(FigureCanvas):

    def __init__(self, parent):
        FigureCanvas.__init__(self, mpl_fig.Figure())
        self.parent = parent

        self.transformers = []
        self.axis_system_tree_ids = []

        self.shapes = []
        self.plots = []
        self.plot2shape_indices = []
        self.plots_clickable = []
        self.plots_visible = []
        self.shape_tree_ids = []
        self.axis_system_data = {"ortho": False,
                                 "points": 0,
                                 "levels": 0}

        self.pressed = False
        self.plot_selected = None
        self.point_selected = None
        self.new_shape = None
        self.points_appended = 0
        self.dbl_click = False
        self.tangent = False

        self.button_press_connection = self.mpl_connect("button_press_event", self.button_press_callback)
        self.motion_connection = self.mpl_connect('motion_notify_event', self.mouse_move_callback)
        self.button_release_connection = self.mpl_connect('button_release_event', self.button_release_callback)

        self.ax = self.figure.subplots()
        self.figure.subplots_adjust(bottom=0, top=1, left=0, right=1)
        self.ax.set_autoscale_on(False)

        self.animation = anim.FuncAnimation(self.figure, self.update_canvas, interval=1, blit=True)

    def update_canvas(self, i):
        return *self.plots,

    def tilt_shape(self, shape_index):
        shape_index = self.standardize_index(shape_index, self.shapes)
        plots_affected = [i for i in range(len(self.plot2shape_indices)) if self.plot2shape_indices[i] == shape_index]

        for plot_index in plots_affected:
            i = plot_index - plots_affected[0]
            x_data = self.shapes[shape_index].graph[i][0]
            y_data = self.shapes[shape_index].graph[i][1]
            self.plots[plot_index].set_xdata(x_data)
            self.plots[plot_index].set_ydata(y_data)

    def resume_interaction(self):
        self.button_press_connection = self.mpl_connect("button_press_event", self.button_press_callback)
        self.motion_connection = self.mpl_connect('motion_notify_event', self.mouse_move_callback)
        self.button_release_connection = self.mpl_connect('button_release_event', self.button_release_callback)
        self.animation.resume()
        self.draw()

    def pause_interaction(self):
        self.mpl_disconnect(self.button_press_connection)
        self.mpl_disconnect(self.motion_connection)
        self.mpl_disconnect(self.button_release_connection)
        self.animation.pause()

    def resize_axes(self, xl, xr, yd, yu):
        self.ax.set_xlim(xl, xr)
        self.ax.set_ylim(yd, yu)

    def update_shape_point(self, point):
        shape_index = self.plot2shape_indices[self.plot_selected]
        if type(self.shapes[shape_index]) == CompCubBezierShape:
            self.shapes[shape_index].modify_point(self.point_selected, point, tangent=self.tangent)
        else:
            self.shapes[shape_index].modify_point(self.point_selected, point)
        self.tilt_shape(shape_index)

    def detect_point(self, point, radius=0.015):
        x0, y0, x_range, y_range = self.detect_limits()
        std_point = self.standardize_point(point, [x0, y0], [x_range, y_range])
        plot_ind = None
        point_ind = None
        for i in range(len(self.plots)):
            if self.plots_clickable[i]:
                x_coords = self.plots[i].get_xdata()
                y_coords = self.plots[i].get_ydata()
                for j in range(len(x_coords)):
                    shape_point = [x_coords[j], y_coords[j]]
                    std_shape_point = self.standardize_point(shape_point, [x0, y0], [x_range, y_range])
                    r = math.sqrt((std_shape_point[0] - std_point[0]) ** 2 + (std_shape_point[1] - std_point[1]) ** 2)
                    if r < radius:
                        radius = r
                        point_ind = j
                        plot_ind = i
        self.point_selected = point_ind
        self.plot_selected = plot_ind

    def detect_limits(self):
        left, right = self.ax.get_xlim()
        down, up = self.ax.get_ylim()
        return left, down, right - left, up - down

    @staticmethod
    def standardize_point(point, point0, ranges):
        point[0] = (point[0] - point0[0]) / ranges[0]
        point[1] = (point[1] - point0[1]) / ranges[1]
        return point

    def set_axis_system(self):
        self.axis_system_data = self.parent.parent.call_axis_system_definition_pop_up()
        self.new_shape = "axis_system"
        self.points_appended = 0

    # -- Add Shapes ----------------------------------------------------------------------------------------------------
    def add_shape(self, shape: Shape, clickable, visible):
        self.shapes.append(shape)
        for i in range(len(shape.graph)):
            self.plots.append(self.ax.plot(*self.shapes[-1].graph[i], shape.plot_style[i])[0])
            self.plots_clickable.append(clickable[i])
            self.plots_visible.append(visible[i])
            self.plots[-1].set_color(shape.color[i])
            self.plot2shape_indices.append(len(self.shapes) - 1)

    def draw_shape(self, shape):
        self.new_shape = shape
        self.points_appended = 0

    def draw_point(self, x, y):
        self.add_shape(Point(self, x, y, "blue"), clickable=[True], visible=[True])
        self.points_appended += 1

    def append_point_to_shape(self, shape_index, point):
        self.shapes[shape_index].append_point(point)
        self.tilt_shape(shape_index)
        self.points_appended += 1

    def line_from_points(self, point_id_1, point_id_2, for_polyline=False):

        point_id_1 = self.standardize_index(point_id_1, self.shapes)
        point_id_2 = self.standardize_index(point_id_2, self.shapes)

        p0 = [self.shapes[point_id_1].x_coords[0], self.shapes[point_id_1].y_coords[0]]
        p1 = [self.shapes[point_id_2].x_coords[0], self.shapes[point_id_2].y_coords[0]]

        for i in sorted([point_id_1, point_id_2], reverse=True):
            self.remove_shape(i)

        if not for_polyline:
            self.add_shape(Line(self, p0, p1, "blue"), clickable=[True], visible=[True])
        else:
            self.add_shape(PolyLine(self, [p0[0], p1[0]], [p0[1], p1[1]], "blue"), clickable=[True], visible=[True])

    def spline_from_polyline(self, polyline_id):

        polyline_id = self.standardize_index(polyline_id, self.shapes)

        cp_x = self.shapes[polyline_id].x_coords
        cp_y = self.shapes[polyline_id].y_coords

        self.remove_shape(polyline_id)

        if self.new_shape == "bezier":
            self.add_shape(BezierShape(self, cp_x, cp_y, "blue", "grey"), clickable=[True, False],
                           visible=[True, True])
        elif self.new_shape == "comp_quad_bezier":
            self.add_shape(CompQuadBezierShape(self, cp_x, cp_y, "blue", "grey"), clickable=[True, False],
                           visible=[True, True])
        elif self.new_shape == "comp_cub_bezier":
            self.add_shape(CompCubBezierShape(self, cp_x, cp_y, "blue", "grey"), clickable=[True, False],
                           visible=[True, True])

    def complete_shape_addition(self):

        unique_ids = self.parent.shape_added_callback(self.new_shape, self.axis_system_data)
        if self.new_shape == "axis_system":
            self.axis_system_tree_ids.append(unique_ids[0])
            self.shape_tree_ids += unique_ids[1:]
        else:
            self.shape_tree_ids += unique_ids
        self.points_appended = 0
        self.point_selected = None
        self.plot_selected = None
        self.new_shape = None

    def remove_shape(self, i):
        if i < 0:
            i += len(self.shapes)
        indices = [j for j in range(len(self.plot2shape_indices)) if i == self.plot2shape_indices[j]]
        del self.shapes[i]
        for j in indices:
            del self.plots[j]
            del self.plots_clickable[j]
            del self.plots_visible[j]
            del self.plot2shape_indices[j]
            if self.new_shape is None:
                del self.shape_tree_ids[j]
        for j in range(len(self.plot2shape_indices)):
            if self.plot2shape_indices[j] > i:
                self.plot2shape_indices[j] -= len(indices)
        self.draw()

    def toggle_visibility(self, tree_id):

        graph_id = self.shape_tree_ids.index(tree_id)

        self.plots_clickable[graph_id] = not self.plots_clickable[graph_id]
        self.plots_visible[graph_id] = not self.plots_visible[graph_id]
        self.plots[graph_id].set_visible(not self.plots[graph_id].get_visible())

    def load_image(self, filename):
        img = mpimg.imread(filename)
        (height, width, _) = img.shape
        self.ax.imshow(img)
        self.resize_axes(0, width, height, 0.)

    def set_tangent(self):
        self.tangent = True

    def unset_tangent(self):
        self.tangent = False

    @staticmethod
    def standardize_index(index, mother_list):
        if index < 0:
            return index + len(mother_list)
        else:
            return index

    # -- Callbacks -----------------------------------------------------------------------------------------------------
    def button_press_callback(self, event):
        ix, iy = event.xdata, event.ydata
        if event.dblclick and self.new_shape:
            self.dbl_click = True
            if self.new_shape == "axis_system":
                self.draw_point(ix, iy)
            elif self.new_shape == "comp_cub_bezier":
                if self.points_appended == 0:
                    for i in range(2):
                        self.draw_point(ix, iy)
                    self.line_from_points(-2, -1, True)
                    self.plot_selected = self.standardize_index(-1, self.plots)
                    self.point_selected = 1
                else:
                    if self.points_appended == 2:
                        for i in range(2):
                            self.append_point_to_shape(-1, [ix, iy])
                        self.spline_from_polyline(-1)
                    else:
                        self.append_point_to_shape(-1, [ix, iy])
                    self.plot_selected = self.standardize_index(-2, self.plots)
                    self.point_selected = self.standardize_index(-2, self.plots[-2].get_xdata())
                self.pressed = True
            else:
                if self.points_appended == 0:
                    self.draw_point(ix, iy)
                    if self.new_shape == "point":
                        # print(self.transformers[-1].coordinates(ix, iy))
                        self.complete_shape_addition()
                elif self.points_appended == 1:
                    self.draw_point(ix, iy)
                    shape_is_line = self.new_shape == "line"
                    self.line_from_points(-2, -1, not shape_is_line)
                    if shape_is_line:
                        self.complete_shape_addition()
                else:
                    self.append_point_to_shape(-1, [ix, iy])
                    if self.points_appended == 3 and \
                            (self.new_shape == "bezier" or self.new_shape == "comp_quad_bezier"):
                        self.spline_from_polyline(-1)
        if event.button == 1 and not self.dbl_click:
            self.pressed = True
            self.detect_point([ix, iy])
            if self.point_selected is not None:
                self.update_shape_point([ix, iy])
        elif event.button == 3:
            if self.new_shape:
                self.complete_shape_addition()

    def mouse_move_callback(self, event):
        ix, iy = event.xdata, event.ydata
        if self.pressed and self.point_selected is not None:
            if ix is not None and iy is not None:
                self.update_shape_point([ix, iy])

    def button_release_callback(self, event):
        if self.dbl_click:
            self.pressed = False
            self.dbl_click = False
            if self.new_shape == "axis_system" and self.points_appended == self.axis_system_data["points"] + \
                    self.axis_system_data["levels"]:
                if self.axis_system_data["ortho"]:
                    self.transformers.append(OrthoTransformer())
                else:
                    self.transformers.append(GeneralizedTransformer())
                self.parent.trigger_home()
                calibration_data = self.parent.parent.call_calibration_pop_up(self.axis_system_data["points"],
                                                                              self.axis_system_data["levels"])
                self.calibrate(calibration_data)
                self.complete_shape_addition()
        else:
            self.pressed = False

    def calibrate(self, data):

        num_of_points = self.axis_system_data["points"]
        num_of_levels = self.axis_system_data["levels"]

        i0 = len(self.shapes) - (num_of_points + num_of_levels)

        px = []
        py = []

        for i in range(len(data["points"][0])):
            px.append([self.shapes[i0 + i].x0, self.shapes[i0 + i].y0, data["points"][0][i]])
            py.append([self.shapes[i0 + i].x0, self.shapes[i0 + i].y0, data["points"][1][i]])

        i0 += num_of_points

        for i, level in enumerate(data["levels"][0]):
            px.append([self.shapes[i0 + i].x0, self.shapes[i0 + i].y0, level])

        i0 += num_of_levels // 2

        for i, level in enumerate(data["levels"][1]):
            py.append([self.shapes[i0 + i].x0, self.shapes[i0 + i].y0, level])

        self.transformers[-1].calibrate(px, py)

    def export(self, export_data):

        filepath = export_data["filepath"]
        axis_system_id = export_data["axis_system_id"]
        transformer = self.transformers[self.axis_system_tree_ids.index(axis_system_id)]
        graph_ids = export_data["graph_ids"]
        graph_names = export_data["graph_names"]
        dx_division = export_data["dx_division"]
        divisions = export_data["num_of_divisions"]
        outputs = []
        for i, graph_id in enumerate(graph_ids):
            name = graph_names[i]
            shape = self.shapes[self.plot2shape_indices[self.shape_tree_ids.index(graph_id)]]
            shape_exports = shape.export(divisions, dx_division)
            output = transformer.transform(shape_exports["graph"])
            headers = ["{} ({})".format(name, header) for header in output.columns.values]
            output.columns = headers
            outputs.append(output)
        expo.export(filepath, outputs)

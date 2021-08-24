from PyQt5.QtWidgets import QTreeView, QHeaderView, QStyledItemDelegate, QStyleOptionViewItem
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QImage
from PyQt5.QtCore import Qt


class StandardImageItem(QStandardItem):
    path_visible = './icons/visibility/visible.png'
    path_invisible = './icons/visibility/invisible.png'

    def __init__(self, visible=True):
        super().__init__()
        self.visible = visible
        self.set_image()
        self.setEditable(False)

    def set_image(self):
        if self.visible:
            image = QImage(self.path_visible)
        else:
            image = QImage(self.path_invisible)
        self.setData(image, Qt.DecorationRole)

    def toggle_visibility(self):
        self.visible = not self.visible
        self.set_image()


class IconCenterDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(IconCenterDelegate, self).initStyleOption(option, index)
        option.decorationAlignment = (Qt.AlignHCenter | Qt.AlignBottom)
        option.decorationPosition = QStyleOptionViewItem.Top


class ShapesTree(QTreeView):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.model = QStandardItemModel()
        self.setModel(self.model)

        self.headers = ['Shape', 'Visible', 'Unique ID', 'Parent ID', 'Primal Shape ID', 'Axis System']
        self.model.setHorizontalHeaderLabels(self.headers)
        self.header().setDefaultAlignment(Qt.AlignCenter)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.setColumnWidth(1, 60)
        self.hideColumn(2)
        self.hideColumn(3)
        self.hideColumn(4)
        self.hideColumn(5)
        self.expandAll()

        delegate = IconCenterDelegate(self)
        self.setItemDelegateForColumn(1, delegate)

        self.doubleClicked.connect(self.handle_double_click)

    def get_selected_row(self):
        data = {}
        self.setColumnHidden(2, False)
        self.setColumnHidden(3, False)
        indices = self.selectedIndexes()
        for i, index in enumerate(indices):
            item = self.model.itemFromIndex(index)
            data[self.headers[i]] = item.data(0)
        self.hideColumn(2)
        self.hideColumn(3)
        return data

    def get_item_by_value(self, column, value):

        def check_children(parent):
            for i in range(parent.rowCount()):
                child = parent.child(i, 0)
                if parent.child(i, column).data(0) == str(value):
                    return child
                else:
                    item = check_children(child)
                    if item:
                        return item

        root = self.model.invisibleRootItem()
        return check_children(root)

    def create_new_uid(self):

        def check_children(parent):
            nonlocal uid
            for i in range(parent.rowCount()):
                child = parent.child(i, 0)
                child_uid = int(parent.child(i, 2).data(0))
                if child_uid > uid:
                    uid = child_uid
                check_children(child)

        root = self.model.invisibleRootItem()
        uid = 0
        check_children(root)
        return uid + 1

    def get_item_by_id(self, uid):
        return self.get_item_by_value(2, uid)

    def append_child_to_selected_row(self, data):

        unique_id = self.create_new_uid()
        data["Unique ID"] = str(unique_id)

        indices = self.selectedIndexes()
        parent = self.model.itemFromIndex(indices[0])

        pid_index = indices[0].siblingAtColumn(2)
        parent_id = self.model.itemFromIndex(pid_index).data(0)

        data["Parent ID"] = str(parent_id)

        self.append_data(parent, data)

    def append_new_data(self, parent_id, data, axis_system=False, primal_child=0):
        data["Parent ID"] = str(parent_id)
        unique_id = self.create_new_uid()
        data["Unique ID"] = str(unique_id)
        if parent_id != 0:
            parent = self.get_item_by_id(parent_id)
        else:
            parent = self.model.invisibleRootItem()
        data["Primal ID"] = unique_id + primal_child
        data["Axis System"] = axis_system
        self.append_data(parent, data)
        return unique_id

    @staticmethod
    def append_data(parent, data):
        parent.appendRow([
            QStandardItem(data['Shape']),
            StandardImageItem(data['Visible']),
            QStandardItem(str(data['Unique ID'])),
            QStandardItem(str(data['Parent ID'])),
            QStandardItem(str(data['Primal ID'])),
            QStandardItem(str(data['Axis System']))
        ])

    def append_shape(self, shape, axis_data=None):

        unique_ids = []

        if shape == "point":
            unique_ids.append(self.append_new_data(0, {'Shape': 'Point', 'Visible': True}))

        elif shape == "line":
            unique_ids.append(self.append_new_data(0, {'Shape': 'Line', 'Visible': True}))

        elif shape == "polyline":
            unique_ids.append(self.append_new_data(0, {'Shape': 'Polyline', 'Visible': True}))

        elif shape == "bezier":
            self.append_new_data(0, {'Shape': 'Bezier', 'Visible': True}, primal_child=2)
            last_id = self.create_new_uid() - 1
            unique_ids.append(self.append_new_data(last_id, {'Shape': 'Control Polyline', 'Visible': True}))
            unique_ids.append(self.append_new_data(last_id, {'Shape': 'Spline', 'Visible': True}))

        elif shape == "comp_quad_bezier":
            self.append_new_data(0, {'Shape': 'Quadratic Bezier', 'Visible': True}, primal_child=2)
            last_id = self.create_new_uid() - 1
            unique_ids.append(self.append_new_data(last_id, {'Shape': 'Control Polyline', 'Visible': True}))
            unique_ids.append(self.append_new_data(last_id, {'Shape': 'Spline', 'Visible': True}))

        elif shape == "comp_cub_bezier":
            self.append_new_data(0, {'Shape': 'Cubic Bezier', 'Visible': True}, primal_child=2)
            last_id = self.create_new_uid() - 1
            unique_ids.append(self.append_new_data(last_id, {'Shape': 'Control Polyline', 'Visible': True}))
            unique_ids.append(self.append_new_data(last_id, {'Shape': 'Spline', 'Visible': True}))

        elif shape == "axis_system":
            num_of_points = axis_data["points"]
            num_of_levels = axis_data["levels"]
            unique_ids.append(self.append_new_data(0, {'Shape': 'Axis System', 'Visible': True}, axis_system=True))
            last_id = self.create_new_uid() - 1
            for i in range(num_of_points):
                unique_ids.append(self.append_new_data(last_id, {'Shape': 'Point {}'.format(str(i)), 'Visible': True}))
            for i in range(num_of_levels // 2):
                unique_ids.append(self.append_new_data(last_id, {'Shape': 'Level X{}'.format(str(i)), 'Visible': True}))
            for i in range(num_of_levels // 2):
                unique_ids.append(self.append_new_data(last_id, {'Shape': 'Level Y{}'.format(str(i)), 'Visible': True}))

        return unique_ids

    def handle_double_click(self, item_index):

        item_class = type(item_index.model().itemFromIndex(item_index)).__name__
        if item_class == "StandardImageItem":
            item_index.model().itemFromIndex(item_index).toggle_visibility()
            children_count = self.model.itemFromIndex(self.currentIndex().siblingAtColumn(0)).rowCount()
            if children_count == 0:
                tree_id = int(self.model.itemFromIndex(self.currentIndex().siblingAtColumn(2)).data(0))
                self.parent.canvas.toggle_visibility(tree_id)
            for i in range(children_count):
                tree_id = int(self.model.itemFromIndex(self.currentIndex().siblingAtColumn(0)).child(i, 2).data(0))
                self.parent.canvas.toggle_visibility(tree_id)

    def get_shapes(self):
        root = self.model.invisibleRootItem()
        return [{'Name': root.child(i, 0).data(0),
                 'id': int(root.child(i, 4).data(0))} for i in range(root.rowCount()) if
                root.child(i, 5).data(0) == 'False']

    def get_axis_systems(self):
        root = self.model.invisibleRootItem()
        return [{'Name': root.child(i, 0).data(0),
                 'id': int(root.child(i, 2).data(0))} for i in range(root.rowCount()) if
                root.child(i, 5).data(0) == 'True']

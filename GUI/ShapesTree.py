from PyQt5.QtWidgets import QTreeView, QHeaderView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from collections import deque


my_data = [{'Unique ID': 1, 'Parent ID': 0, 'Shape': 'Shape', 'Visible': ''}]
# my_data = []


class StandardItemModelAlignable(QStandardItemModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnAlignments = {}

    def set_column_alignment(self, column, alignment):
        if alignment:
            self.columnAlignments[column] = alignment
        elif column in self.columnAlignments:
            self.columnAlignments.pop(column)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            return super().data(index, role) or self.columnAlignments.get(index.column())
        return super().data(index, role)


class ShapesTree(QTreeView):

    def __init__(self, parent):
        super().__init__(parent)

        self.model = StandardItemModelAlignable()
        self.model.set_column_alignment(1, Qt.AlignCenter)

        self.headers = ['Shape', 'Visible', 'Unique ID', 'Parent ID']
        self.model.setHorizontalHeaderLabels(self.headers)
        self.header().setSectionResizeMode(QHeaderView.Stretch)
        self.header().setDefaultAlignment(Qt.AlignCenter)
        self.setModel(self.model)
        self.import_data(my_data)
        self.hideColumn(2)
        self.hideColumn(3)
        self.resizeColumnToContents(1)
        self.expandAll()

    def import_data(self, data, root=None):
        self.model.setRowCount(0)
        if root is None:
            root = self.model.invisibleRootItem()
        seen = {}
        values = deque(data)
        while values:
            value = values.popleft()
            if value['Unique ID'] == 1:
                parent = root
            else:
                pid = value['Parent ID']
                if pid not in seen:
                    values.append(value)
                    continue
                parent = seen[pid]
            unique_id = value['Unique ID']
            self.append_data(parent, value)
            seen[unique_id] = parent.child(parent.rowCount() - 1)

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

        root = self.model.item(0, 0)
        if self.model.item(0, column).data(0) == str(value):
            return root
        else:
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

        root = self.model.item(0, 0)
        uid = int(self.model.item(0, 2).data(0))
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

    def append_new_data(self, parent_id, data):
        data["Parent ID"] = str(parent_id)
        unique_id = self.create_new_uid()
        data["Unique ID"] = str(unique_id)
        if parent_id != 0:
            parent = self.get_item_by_id(parent_id)
        else:
            parent = self.model.invisibleRootItem()
        self.append_data(parent, data)

    @staticmethod
    def append_data(parent, data):
        parent.appendRow([
            QStandardItem(data['Shape']),
            QStandardItem(data['Visible']),
            QStandardItem(str(data['Unique ID'])),
            QStandardItem(str(data['Parent ID']))
        ])

from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)

from cilissa.operations import ImageOperation, Metric, Transformation
from cilissa_gui.managers import OperationsManager


class OperationsBox(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Operations")

        self.setMaximumHeight(168)

        self.main_layout = QHBoxLayout()
        self.buttons_panel = QVBoxLayout()
        self.buttons_panel.addWidget(QPushButton("&Clear"))

        self.main_layout.addWidget(Operations())
        self.main_layout.addLayout(self.buttons_panel)
        self.setLayout(self.main_layout)


class Operations(QListWidget):
    def __init__(self) -> None:
        super().__init__()

        self.operations_manager = OperationsManager()
        self.operations_manager.changed.connect(self.refresh)

        self.setMaximumHeight(168)

    @Slot()
    def refresh(self) -> None:
        self.clear()
        for item in self.operations_manager.get_order():
            item = self.create_item_from_operation(item[1])
            self.addItem(item)

    def create_item_from_operation(self, operation: ImageOperation) -> QListWidgetItem:
        if isinstance(operation, Transformation):
            icon = QIcon(":letter-t")
        elif isinstance(operation, Metric):
            icon = QIcon(":letter-m")
        else:
            icon = None
        item = QListWidgetItem(icon, operation.get_class_name(), self)
        return item

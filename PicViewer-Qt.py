import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QScrollArea, QShortcut
from PyQt5.QtGui import QImage, QPixmap, QKeySequence
from PyQt5.QtCore import Qt, QEvent, QRect

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setWidgetResizable(True)

        self.setCentralWidget(self.scroll_area)

        self.image = None
        self.image_list = []
        self.current_image_index = -1
        self.zoom_factor = 1.0
        self.fullscreen = False
        self.setWindowTitle("图片查看器")

        self.grabGesture(Qt.PinchGesture)
        
        self.open_image()

        self.center_window()
        self.bind_shortcuts()

    def bind_shortcuts(self):
        self.shortcut_next = QShortcut(QKeySequence("Space"), self)
        self.shortcut_next.activated.connect(self.next_image)
        self.shortcut_j = QShortcut(QKeySequence("J"), self)
        self.shortcut_j.activated.connect(self.next_image)
        self.shortcut_k = QShortcut(QKeySequence("K"), self)
        self.shortcut_k.activated.connect(self.previous_image)
        self.shortcut_fullscreen = QShortcut(QKeySequence("F"), self)
        self.shortcut_fullscreen.activated.connect(self.toggle_fullscreen)

    def center_window(self):
        """将窗口居中显示"""
        window_width = 800
        window_height = 600
        screen_width = self.screen().availableGeometry().width()
        screen_height = self.screen().availableGeometry().height()
        
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        
        self.setGeometry(position_right, position_top, window_width, window_height)

    def open_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图片文件", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff);;All Files (*)",
                                                   options=options)
        if file_path:
            self.load_images(file_path)
            self.show_image()

    def load_images(self, file_path):
        directory = os.path.dirname(file_path)
        self.image_list = [os.path.join(directory, f) for f in os.listdir(directory)
                           if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif', 'tiff'))]
        self.image_list.sort()
        self.current_image_index = self.image_list.index(file_path)

    def show_image(self):
        if not self.image_list:
            return

        image_path = self.image_list[self.current_image_index]
        self.image = QImage(image_path)
        self.zoom_factor = 1.0  # 重置缩放级别
        self.update_image()
        self.adjust_window_size()

    def update_image(self):
        if self.image is None:
            return

        screen_rect = self.screen().availableGeometry()
        max_width = screen_rect.width()
        max_height = screen_rect.height()

        # Zoomed image size
        image_size = self.image.size() * self.zoom_factor
        if image_size.width() > max_width or image_size.height() > max_height:
            zoomed_image = self.image.scaled(max_width, max_height, Qt.KeepAspectRatio)
        else:
            zoomed_image = self.image.scaled(image_size, Qt.KeepAspectRatio)

        self.image_label.setPixmap(QPixmap.fromImage(zoomed_image))

        self.setWindowTitle(f"{self.current_image_index + 1}/{len(self.image_list)}: {os.path.basename(self.image_list[self.current_image_index])}")

    def adjust_window_size(self):
        """Adjust window size to fit the image initially and ensure it fits within the screen."""
        if self.image is None or self.fullscreen:
            return

        screen_rect = self.screen().availableGeometry()
        image_size = self.image.size()
        window_size = self.size()

        new_width = min(image_size.width(), screen_rect.width())
        new_height = min(image_size.height(), screen_rect.height())

        self.resize(new_width, new_height)
        self.center_window()

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:  # Only zoom if Control key is pressed
            if event.angleDelta().y() > 0:
                self.zoom_factor *= 1.1
            else:
                self.zoom_factor /= 1.1
            self.update_image()

    def gestureEvent(self, event):
        if event.gesture(Qt.PinchGesture):
            pinch = event.gesture(Qt.PinchGesture)
            self.zoom_factor *= pinch.scaleFactor()
            self.update_image()
            return True
        return super().event(event)

    def event(self, event):
        if event.type() == QEvent.Gesture:
            return self.gestureEvent(event)
        return super().event(event)

    def next_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.image_list)
        self.show_image()

    def previous_image(self):
        self.current_image_index = (self.current_image_index - 1) % len(self.image_list)
        self.show_image()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.showFullScreen()
        else:
            self.showNormal()
            self.adjust_window_size()  # Ensure window size adjusts after exiting fullscreen

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.resize(800, 600)
    viewer.show()
    sys.exit(app.exec_())

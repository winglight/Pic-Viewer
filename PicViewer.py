import os
import sys
from tkinter import Tk, Label, filedialog, NW
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self):
        self.root = Tk()
        self.root.title("图片查看器")
        self.label = Label(self.root)
        self.label.pack(anchor=NW, expand=True)

        self.image_list = []
        self.current_image_index = -1
        self.current_image = None
        self.zoom_level = 1.0
        self.max_zoom = 3.0
        self.min_zoom = 0.1

        self.root.bind('<space>', self.next_image)
        self.root.bind('j', self.next_image)
        self.root.bind('k', self.previous_image)
        self.root.bind('f', self.toggle_fullscreen)
        self.root.bind('<Double-Button-1>', self.open_file_dialog)
        self.root.bind('<MouseWheel>', self.zoom_image)
        self.root.bind('<Button-4>', self.zoom_image)  # For Linux
        self.root.bind('<Button-5>', self.zoom_image)  # For Linux

        self.fullscreen = False

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.center_window()
        
        # Add support for opening files from Finder
        if sys.platform == 'darwin':
            import Cocoa
            from Foundation import NSBundle
            app = Cocoa.NSApplication.sharedApplication()
            app.setActivationPolicy_(Cocoa.NSApplicationActivationPolicyRegular)
            self.root.createcommand('::tk::mac::OpenDocument', self.open_file)

        # Check if any files were passed as arguments
        if len(sys.argv) > 1:
            self.load_images(sys.argv[1])
            self.show_image()
        else:
            self.open_file_dialog()

    def center_window(self):
        """将窗口居中显示"""
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    def open_file_dialog(self, event=None):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.load_images(file_path)
            self.show_image()

    def open_file(self, *args):
        if args:
            file_path = args[0]
            if os.path.isfile(file_path):
                self.load_images(file_path)
                self.show_image()

    def load_images(self, file_path):
        directory = os.path.dirname(file_path)
        self.image_list = [os.path.join(directory, f) for f in os.listdir(directory)
                           if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif', 'tiff'))]
        self.image_list.sort()  # 按名称排序
        self.current_image_index = self.image_list.index(file_path)

    def show_image(self):
        if not self.image_list:
            return

        image_path = self.image_list[self.current_image_index]
        self.current_image = Image.open(image_path)
        self.zoom_level = 1.0  # 重置缩放级别
        self.update_image()

    def update_image(self):
        if self.current_image is None:
            return

        img_width, img_height = self.current_image.size

        # Calculate the new size to maintain the aspect ratio
        new_width = int(img_width * self.zoom_level)
        new_height = int(img_height * self.zoom_level)

        image = self.current_image.resize((new_width, new_height), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(image)
        self.label.config(image=img_tk)
        self.label.image = img_tk

        # Update the window size to fit the image
        self.root.geometry(f'{new_width}x{new_height}')

        # Update the window title with the current image index and file name
        self.update_title()

    def zoom_image(self, event):
        if event.delta > 0 or event.num == 4:
            self.zoom_level = min(self.zoom_level * 1.1, self.max_zoom)
        elif event.delta < 0 or event.num == 5:
            self.zoom_level = max(self.zoom_level / 1.1, self.min_zoom)
        self.update_image()

    def next_image(self, event=None):
        self.current_image_index = (self.current_image_index + 1) % len(self.image_list)
        self.show_image()

    def previous_image(self, event=None):
        self.current_image_index = (self.current_image_index - 1) % len(self.image_list)
        self.show_image()

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def update_title(self):
        current_file_name = os.path.basename(self.image_list[self.current_image_index])
        title = f"{self.current_image_index + 1}/{len(self.image_list)}: {current_file_name}"
        self.root.title(title)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    viewer = ImageViewer()
    viewer.run()

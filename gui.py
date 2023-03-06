import tkinter as tk
import customtkinter
from PIL import Image, ImageTk
import cv2

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("EHC")
        self.geometry(f"{640}x{480}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure(0, weight=1)

        # create sidebar frame with widgets

        self.topbar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.topbar_frame.grid(row=0, column=0, sticky="nsew")
        self.topbar_frame.grid_rowconfigure(0, weight=1)
        self.topbar_frame.grid_columnconfigure(0, weight=1)

        self.bottombar_frame = customtkinter.CTkFrame(self, height=80, fg_color="transparent", corner_radius=16)
        self.bottombar_frame.grid(row=1, column=0, sticky="nsew")
        # self.bottombar_frame.grid_columnconfigure(0, weight=1)
        self.bottombar_frame.grid_rowconfigure(0, weight=1)
        

        # self.bottombar_frame.grid_rowconfigure(4, weight=1)
        
        self.video_frame = VideoFrame(self.topbar_frame)
        self.video_frame.grid(row=0, column=0)
        # self.columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)
        self.topbar_frame.bind("<Configure>", self.on_resize)


        # Input Widgets
        self.ip_entry =customtkinter.CTkEntry(self.bottombar_frame, placeholder_text="IP Address")
        self.ip_entry.grid(row=0, column=0)
        self.port_entry =customtkinter.CTkEntry(self.bottombar_frame, placeholder_text="Port")
        self.port_entry.grid(row=0, column=1)
        



    def on_resize(self, event):
        # Get the current size of the canvas
        canvas_width = event.width
        canvas_height = event.height
        width = 0
        height = 0

        # Calculate the aspect ratio of the video frame
        video_ratio = 1.01/1  # Change this to match your video aspect ratio
        canvas_ratio = canvas_width / canvas_height

        if canvas_ratio > video_ratio:
            # The canvas is wider than the video frame
            width = int(canvas_height * video_ratio)
            height = canvas_height
        else:
            # The canvas is taller than the video frame
            width = canvas_width
            height = int(canvas_width / video_ratio)

        # Update the size of the video frame and canvas when the window is resized
        # self.video_frame.width = event.width
        # self.video_frame.height = event.height
        # self.video_frame.video_canvas.config(width=event.width, height=event.height)
        self.video_frame.width = width
        self.video_frame.height = height
        self.video_frame.video_canvas.config(width=width, height=height)
        self.video_frame.update_frame(cv2.imread("cover_art.png"))


class VideoFrame(tk.Frame):
    def __init__(self, master, width=640, height=480, **kwargs):
        super().__init__(master, **kwargs)
        self.width = width
        self.height = height
        self.video_canvas = tk.Canvas(self, width=width, height=height)
        self.video_canvas.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
    def update_frame(self, frame):
        # Resize the frame to fit the video canvas
        frame = cv2.resize(frame, (self.width, self.height))
        # Convert the frame to an RGB image
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convert the image to a Tkinter PhotoImage
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image)
        # Set the PhotoImage as the video canvas image
        self.video_canvas.create_image(self.width/2, self.height/2, image=photo, anchor="center")
        self.video_canvas.image = photo

if __name__ == "__main__":
    app = App()
    app.mainloop()

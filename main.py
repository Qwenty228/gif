import asyncio
import os
import sys
from tkinter import filedialog
import tkinter
import customtkinter
import PIL
from PIL import ImageTk
from tkinter import *
from ging import create_gif, progress

from iini import create_image, progress

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()
        self.button_count = 1
        self._images = []


        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.button = customtkinter.CTkButton(master=self.frame,
                                                text="image",
                                                fg_color=('gray0'), 
                                                text_color='yellow',
                                                command=lambda: self.button_event(self.button))
        self.button.grid(pady=10, padx=20)
        
        self.execute_button = customtkinter.CTkButton(master=self.frame,
                                                text="execute",
                                                fg_color=('gray40'), 
                                                text_color='white',    
                                                text_font=(None, 20),
                                                command=lambda: asyncio.run(self.execute()),
                                                ).place(anchor=tkinter.CENTER, relx=0.5, rely= 0.9, height=60)
        
    async def execute(self):
        if self._images:
            g = [i for i in self._images if str(i).endswith('.gif')]
            i = [i for i in self._images if i not in g]
        
            async def counting():
                while True:
                    print(progress)
                    await asyncio.sleep(0.05)

            if g:
                task = create_gif(*(i + g +g), sp=20, bp=20)
            else:
                task = create_image(*i, sp=50, bp=100,infi=False)

            done, pending = await asyncio.wait([task, counting()], return_when=asyncio.FIRST_COMPLETED)
            print(done)


    def button_event(self, button: tkinter.Button):
        image_name = filedialog.askopenfilename(initialdir='gui/images', title="Select image", filetypes=[('image file', ('.png', '.jpg', '.gif'))])
        
        image = ImageTk.PhotoImage(PIL.Image.open(image_name).resize((100,100)))

        _, tail = os.path.split(image_name)
        self._images.append(image_name)
       
        button.configure(state=tkinter.DISABLED, text=tail, image=image)
    
        if self.button_count < 2:
            button_2 = customtkinter.CTkButton(master=self.frame,
                                                    text="another image",
                                                    fg_color=('gray0'), 
                                                    text_color='yellow',
                                                    command=lambda: self.button_event(button_2))
            button_2.grid(pady=10, padx=20)
            self.button_count +=1

    def on_closing(self, event=0):
        self.destroy()
if __name__ == "__main__":
    app = App()
    app.mainloop()
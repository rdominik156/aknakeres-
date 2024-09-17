from tkinter import *
from cell import *
from setting import *

root = Tk()
root.configure(bg="black")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.title("Aknakereső")
root.resizable(False, False)

image= ImageTk.PhotoImage(Image.open("D:\Programozás\VS gyakorlás\\aknakereső/zaszloa.png"))


# Frames
top_frame = Frame(root, bg="black", width=1440, height=180)
top_frame.place(x=0, y=0)

left_frame = Frame(root, bg="black", width=360, height=540)
left_frame.place(x=0, y=180)

center_frame = Frame(root, bg="black", width=1080, height=540)
center_frame.place(x=360, y=180)

for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        c = Cell(x, y, image)
        c.create_btm_object(center_frame)
        c.cell_btm_object.grid(row=y, column=x)

Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_object.place(x=0, y=0)
Cell.randomize_mine()

root.mainloop()
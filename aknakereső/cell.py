from tkinter import Button, Label
import random
from setting import *
from PIL import Image, ImageTk
import ctypes
import sys
import time


class Cell:
    all = []
    cell_count = CELL_COUNT-MINES
    cell_count_label_object = None
    zeros = set()
    
    def __init__(self, x, y, image, is_mine = False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_candidate = False
        self.cell_btm_object = None
        self.x = x
        self.y = y
        self.image = image

        # az összes akna
        Cell.all.append(self)

    def create_btm_object(self, location):
        btn = Button(location, width=3, height=1, image="", bg="#d3d3d3")

        btn.bind("<Button-1>", self.left_click)
        btn.bind("<Button-3>", self.right_click)
        self.cell_btm_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(location, text=f"Cells left: {Cell.cell_count}", width=12, height=4,bg="black", fg="white",font=20)
        Cell.cell_count_label_object = lbl

    def left_click(self, event):
        if not self.is_candidate:
            if self.is_mine:
                self.show_mine()
            else:                
                self.repeat_show()                

        # Win
        if Cell.cell_count == 0:
            ctypes.windll.user32.MessageBoxW(0,"You won!", "Game over", 0)
            time.sleep(3)
            sys.exit()
    
    def repeat_show(self):
        # első felfedés
        if self.cells_mines_lenght == 0:
            for object in self.surraunded_cells:
                object.show_cell()

        # második folyamatos felfedés
        while True:
            lista = list(Cell.zeros)
            if len(lista) == 0:
                break
            cell = lista.pop(0)
            self = cell
            for obj in self.surraunded_cells:
                obj.show_cell()
            self.show_cell()
            Cell.zeros.remove(self)
                
        self.show_cell()

    def show_mine(self):
        self.cell_btm_object.configure(bg="red")
        ctypes.windll.user32.MessageBoxW(0,"You click on mine", "Game over", 1)
        time.sleep(1)
        sys.exit()

    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surraunded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x-1, self.y-1),
            self.get_cell_by_axis(self.x-1, self.y),
            self.get_cell_by_axis(self.x-1, self.y+1),
            self.get_cell_by_axis(self.x, self.y-1),
            self.get_cell_by_axis(self.x+1, self.y-1),
            self.get_cell_by_axis(self.x+1, self.y),
            self.get_cell_by_axis(self.x+1, self.y+1),
            self.get_cell_by_axis(self.x, self.y+1)
        ]
        cells = [cell for cell in cells if cell is not None]
        # tartalmazza az összes kordinátát pl.: (1, 2)
        return cells

    @property
    def cells_mines_lenght(self):
        counter = 0
        for cell in self.surraunded_cells:
            if cell.is_mine:
                counter += 1
        return counter

    def show_cell(self):
        if not self.is_opened:
            # cella számának kiíratása
            if self.cells_mines_lenght != 0:
                self.cell_btm_object.configure(text=self.cells_mines_lenght, bg="grey")
            else:
                self.cell_btm_object.configure(text="", bg="grey")

            # nullás cellák listához adása
            if self.cells_mines_lenght == 0:
                Cell.zeros.add(self)

            # cella számláló
            Cell.cell_count -= 1
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(text=f"{Cell.cell_count}")

        self.is_opened = True

    def right_click(self, event):
        # funkcion
        if not self.is_opened:
            if not self.is_candidate:
                self.cell_btm_object.configure(image=self.image, width=25, height=20)
                self.is_candidate = True
            else:
                self.cell_btm_object.configure(image="", width=3, height=1)
                self.is_candidate = False


    @staticmethod
    def randomize_mine():
        # random választás
        picked_cells = random.sample(Cell.all, MINES)
        # a választott cellák aknává tétele
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

        print(picked_cells)

    def __repr__(self):
        return f"({self.x}, {self.y})"
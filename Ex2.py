from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
import math
import random



class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

class GameWindow(FloatLayout):
    def __init__(self, **kwargs):
        super(GameWindow, self).__init__(**kwargs)
        self.current_index = []
        self.static_colored = []
        self.colored = []
        self.current_figure = None
        self.all_shapes = ["Line", "Square", "Z1", "Z2", "T", "L1", "L2"]
        self.keyboard = Window.request_keyboard(None, self)

    def draw_grid(self):
        for i in range(0, 25):
            row = MyRow(id = f"{19 - i}")
            row.size_hint = (1, .05)
            row.pos_hint = {'x': 0, 'y': 1.2 - i/20}
            for j in range(0, row.cols):
                col = MyCol(color = "F", id = f"{j}")
                row.add_widget(col)
            self.add_widget(row)

    
    def move_side(self, keycode):
        
        if keycode == "left":
            self.backup_index = self.current_index.copy()
            self.event.cancel()
            for index in self.current_index:
                a = index[0]
                b = index[1]
                new_index = (a, b+1)
                if (new_index not in self.static_colored and new_index[1] in range(0,10)):
                    self.children[a].children[b].uncolor()
                    self.current_index[self.current_index.index(index)] = new_index
                else:
                    self.current_index = self.backup_index.copy()
                    self.backup_index = []
                    break
            self.move()

        if keycode == "right":
            self.backup_index = self.current_index.copy()
            self.event.cancel()
            for index in self.current_index:
                a = index[0]
                b = index[1]
                new_index = (a, b-1)
                if (new_index not in self.static_colored and new_index[1] in range(0,10)):
                    self.children[a].children[b].uncolor()
                    self.current_index[self.current_index.index(index)] = new_index
                else:
                    self.current_index = self.backup_index.copy()
                    self.backup_index = []
                    break
            self.move()

    '''def get_index_row(self, row):
        print(self.children.index(row))
        for btn in row.children:
            print("btn", row.children.index(btn))'''

    def get_index(self, btn):
        #print("x:", btn.parent.children.index(btn), "y:", btn.parent.parent.children.index(btn.parent))
        return(btn.parent.children.index(btn), btn.parent.parent.children.index(btn.parent))   

    def return_btn(self, index):
        #print(self.children[index[1]].children[index[0]])
        return(self.children[index[1]].children[index[0]])       

    def remove_row(self):
        for row in self.children:
            #self.get_index_row(row)
            if all(child.is_colored for child in row.children):
                print("remove_row", row.id)
                #self.remove_widget(row)
                break

    def rotate(self):
        print("rot1", self.current_index)
        
        self.event.cancel()
        self.saved_index = self.current_index.copy()
        center_y = self.current_index[1][0]
        center_x = self.current_index[1][1]
        print(center_x, center_y)
        for index in self.current_index:
            
            a = index[0]
            b = index[1]
            oty = a - center_y
            otx = b - center_x
            new_y = otx+center_y
            new_x = -oty+center_x
            if (new_x in range(0, 10) and new_y in range(0,20) and
            (new_x, new_y) not in self.static_colored):
                self.children[a].children[b].uncolor()
                new_index = (new_y, new_x)
                print(index, new_index, "index")
                print(a,"a",b,"b")
                self.current_index[self.current_index.index(index)] = new_index
            else:
                self.current_index = self.saved_index.copy()
                self.saved_index = []
                break

        self.move()
        


    def remove(self):
        #self.next_index = []
        for index in self.current_index:
            a = index[0]
            b = index[1]
            self.children[a].children[b].uncolor()
            new_index = (a-1, b)
            self.current_index[self.current_index.index(index)] = new_index
        #self.event = Clock.schedule_once(lambda dt: self.move(), 0.0)
        self.remove_row()
        self.move()
        


    def move(self):
        #self.current_index = next_index.copy()
        for index in self.current_index:
            a = index[0]
            b = index[1]
                
            self.children[a].children[b].colored()
        self.check_collisions()
        
        if any(index[0] <=0 for index in self.current_index) or self.check_collisions():
            self.event.cancel()
            for index in self.current_index:
                self.static_colored.append(index)
            self.create_first_figure()

        else:
            #pass
            self.event = Clock.schedule_once(lambda dt: self.remove(), 0.3)
            #self.remove()

    def check_collisions(self):
        for static in self.static_colored:
            if any((index[0]-1, index[1]) == static  for index in self.current_index):
                print("Col")
                return True

    def move_one_down(self):
        for index in self.current_figure:
            self.return_btn(index).uncolor()
            new_index = (index[0], index[1]-1)
            print(new_index)
            self.return_btn(new_index).colored()
            self.current_figure[self.current_figure.index(index)] = new_index

    def create_first_figure(self):
        self.current_index = [0]*4
        self.current_figure = [0]*4
        print(self.current_index)
        self.start_x = random.randint(2,7)
        center_i = 18
        center_j = self.start_x
        num = random.randint(0,7)
        shape = self.all_shapes[num-1]
        print(shape)
        s_x = 5
        s_y = 18
        t_shape = [(s_x, s_y), (s_x, s_y+1), (s_x +1, s_y), (s_x -1, s_y), (s_x, s_y)]
        l1_shape = [(s_x, s_y), (s_x-1, s_y), (s_x , s_y+1), (s_x , s_y+2), (s_x -1, s_y+1)]
        l2_shape = [(s_x, s_y), (s_x+1, s_y), (s_x , s_y+1), (s_x , s_y+2), (s_x +1, s_y+1)]
        z1_shape = [(s_x, s_y), (s_x-1, s_y), (s_x , s_y-1), (s_x+1 , s_y-1), (s_x , s_y)]
        z2_shape = [(s_x, s_y), (s_x+1, s_y), (s_x , s_y-1), (s_x-1 , s_y-1), (s_x , s_y)]
        sq_shape = [(s_x, s_y), (s_x+1, s_y+1), (s_x , s_y+1), (s_x+1 , s_y), (s_x , s_y)]
        line_shape = [(s_x, s_y), (s_x, s_y-1), (s_x , s_y+1), (s_x , s_y+2), (s_x , s_y)]
        self.current_figure = line_shape
        for s in line_shape[:5]:
            self.return_btn(s).colored()
        for i in range(0, 8):
            self.move_one_down()
        for child in self.children:
            for btn in child.children:
                if self.get_index(btn) == (center_j, center_i):
                    print(self.get_index(btn))
                    #self.current_figure
                if (int(child.id) == center_i and int(btn.id) == center_j):
                    index = (int(child.id), (9- int(btn.id)))
                    self.current_index[0] = index
        if shape == "Z1":
            for child in self.children:
                for btn in child.children:
                    index = (int(child.id), (9- int(btn.id)))
                    if (int(child.id) == center_i and int(btn.id) == center_j -1):
                        self.current_index[1] = index
                        btn.colored()
                    elif (int(child.id) == center_i - 1 and int(btn.id) == center_j +1):
                        self.current_index[2] = index
                        btn.colored()
                    elif (int(child.id) == center_i - 1 and int(btn.id) == center_j):
                        self.current_index[3] = index
                        btn.colored()

        if shape == "Z2":
            for child in self.children:
                for btn in child.children:
                    index = (int(child.id), (9- int(btn.id)))
                    if (int(child.id) == center_i and int(btn.id) == center_j +1):
                        self.current_index[1] = index
                        btn.colored()
                    elif (int(child.id) == center_i - 1 and int(btn.id) == center_j -1):
                        self.current_index[2] = index
                        btn.colored()
                    elif (int(child.id) == center_i - 1 and int(btn.id) == center_j):
                        self.current_index[3] = index
                        btn.colored()

        if shape == "L1":
            for child in self.children:
                for btn in child.children:
                    index = (int(child.id), (9- int(btn.id)))
                    if (int(child.id) == center_i and int(btn.id) == center_j +1):
                        self.current_index[1] = index
                        btn.colored()
                    elif (int(child.id) == center_i -1  and int(btn.id) == center_j):
                        self.current_index[2] = index
                        btn.colored()
                    elif (int(child.id) == center_i - 2 and int(btn.id) == center_j):
                        self.current_index[3] = index
                        btn.colored()

        if shape == "L2":
            for child in self.children:
                for btn in child.children:
                    index = (int(child.id), (9- int(btn.id)))
                    if (int(child.id) == center_i and int(btn.id) == center_j - 1):
                        self.current_index[1] = index
                        btn.colored()
                    elif (int(child.id) == center_i -1  and int(btn.id) == center_j):
                        self.current_index[2] = index
                        btn.colored()
                    elif (int(child.id) == center_i - 2 and int(btn.id) == center_j):
                        self.current_index[3] = index
                        btn.colored()

        if shape == "Line":
            for child in self.children:
                for btn in child.children:
                    index = (int(child.id), (9- int(btn.id)))
                    if (int(child.id) == center_i+1 and int(btn.id) == center_j ):
                        self.current_index[1] = index
                        btn.colored()
                    elif (int(child.id) == center_i -1  and int(btn.id) == center_j):
                        self.current_index[2] = index
                        btn.colored()
                    elif (int(child.id) == center_i - 2 and int(btn.id) == center_j):
                        self.current_index[3] = index
                        btn.colored()

        if shape == "Square":
            for child in self.children:
                for btn in child.children:
                    index = (int(child.id), (9- int(btn.id)))
                    if (int(child.id) == center_i and int(btn.id) == center_j -1):
                        self.current_index[1] = index
                        btn.colored()
                    elif (int(child.id) == center_i+1  and int(btn.id) == center_j):
                        self.current_index[2] = index
                        btn.colored()
                    elif (int(child.id) == center_i+1 and int(btn.id) == center_j-1):
                        self.current_index[3] = index
                        btn.colored()

        if shape == "T":
            for child in self.children:
                for btn in child.children:
                    index = (int(child.id), (9- int(btn.id)))
                    if (int(child.id) == center_i -1 and int(btn.id) == center_j ):
                        self.current_index[1] = index
                        btn.colored()
                    elif (int(child.id) == center_i   and int(btn.id) == center_j -1):
                        self.current_index[2] = index
                        btn.colored()
                    elif (int(child.id) == center_i  and int(btn.id) == center_j +1):
                        self.current_index[3] = index
                        btn.colored()


        self.remove()
        self.keyboard.bind(on_key_down=self.on_keyboard_down)

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(keyboard, keycode, text, modifiers)
        self.move_side(keycode[1])
        if keycode[1] == "up":
            self.rotate()

            




class MyRow(GridLayout):
    def __init__(self, *args, **kwargs):
        super(MyRow, self).__init__(*args,**kwargs)
        self.cols = 10

class MyCol(Button):
    def __init__(self, color, *args, **kwargs):
        super(MyCol, self).__init__(*args,**kwargs)
        self.background_color= (1,0,0,1)
        self.color = color
        self.is_colored = False
    

    def colored(self):
        self.background_color = (0,1,0,1)
        self.is_colored = True

    def uncolor(self):
        self.background_color= (1,0,0,1)
        self.is_colored = False

    def on_press(self):
        print(self.parent.children.index(self), self.parent.parent.children.index(self.parent))


main = MainWindow()
left_border = GameWindow()
right_border = GameWindow()
game_screen =  GameWindow(size_hint_x = 1.4) 
game_screen.draw_grid()
game_screen.create_first_figure()
main.add_widget(left_border)  
main.add_widget(game_screen)
main.add_widget(right_border)


class TestApp(App):

    def build(self):
    
        return main
if __name__=="__main__":
    TestApp().run()
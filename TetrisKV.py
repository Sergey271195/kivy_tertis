from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen
import math
import random

class GameWindow(FloatLayout):
    def __init__(self, left, right, **kwargs):
        super(GameWindow, self).__init__(**kwargs)
        self.proper_colors = []
        self.current_index = []
        self.static_colored = []
        self.current_figure = []
        self.keyboard = Window.request_keyboard(None, self)
        self.score_window = left
        self.score = 0
        self.game_speed = 0.3
        self.level = 0
        self.score_label = Label(text = f"Score: {self.score} \nLevel: {self.level//300}", font_size = "20sp")
        self.score_window.add_widget(self.score_label)
        self.game_over_screen = GameOver(size_hint = (1,1), pos_hint= {"x": 0, "y": 0})

        #If you want to change the color of main screen
        with self.canvas.before:
            Color(0,0,0,1)
            self.rect = Rectangle(size = self.size, pos = self.pos)
        self.bind(size=self.update_rect)

        self.draw_grid()
        self.create_figure()
        self.right_window = right

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
    def get_score(self):
        return(self.score, self.level//300)

    def draw_grid(self):
        for i in range(0, 25):
            row = MyRow()
            row.size_hint = (1, .05)
            row.pos_hint = {'x': 0, 'y': 1.2 - i/20}
            for j in range(0, row.cols):
                col = MyCol()
                row.add_widget(col)
            self.add_widget(row)


    def get_index(self, btn):
        return(btn.parent.children.index(btn), btn.parent.parent.children.index(btn.parent))   

    def return_btn(self, index):
        return(self.children[index[1]].children[index[0]])       

    def remove_row(self):
        for row in self.children:
            if all(child.is_colored for child in row.children):
                self.score += 100
                self.score_label.text = f"Score: {self.score} \nLevel: {self.level//300}"
                for child in row.children:
                    row_num = self.get_index(child)[1]
                    child.uncolor()
                    for index in self.static_colored:
                        if self.get_index(child) == index[0]:
                            self.static_colored.remove(index)
                self.dropped = []
                for index in self.static_colored:
                    if index[0][1] >= row_num:
                        self.return_btn(index[0]).uncolor()
                        new_index = ((index[0][0], index[0][1]-1), index[1])
                        self.dropped.append(new_index)
                    else:
                        self.dropped.append(index)
                self.static_colored = self.dropped.copy()
                for index in self.static_colored:
                    self.return_btn(index[0]).colored(index[1])
                self.remove_row()


        
    def check_collisions_down(self):
        for static in self.static_colored:
            if any((index[0], index[1]-1) == static[0]  for index in self.current_figure[:4]):
                return True
        if any(index[1] == 0 for index in self.current_figure[:4]):
            return True
    
    def check_collisions_left(self):
        for static in self.static_colored:
            if any((index[0]+1, index[1]) == static[0]  for index in self.current_figure[:4]):
                return True
        if any(index[0] == 9 for index in self.current_figure[:4]):
            return True

    def check_collisions_right(self):
        for static in self.static_colored:
            if any((index[0]-1, index[1]) == static[0]  for index in self.current_figure[:4]):
                return True
        if any(index[0] == 0 for index in self.current_figure[:4]):
            return True

    def check_collisions_rotation(self, figure):
        if any(index[0] in figure for index in self.static_colored):
            return("No")
        elif any(new_index[0] < 0 for new_index in figure):
            return("Move left")
        elif any(new_index[0] > 9 for new_index in figure):
            return("Move right")
        else:
            return(True)

    def rotate(self):
        if (self.current_num != 0 and self.current_num != 7):
            self.next_figure = []
            for index in self.current_figure:
                otx = index[0] - self.current_figure[4][0]
                oty = index[1] - self.current_figure[4][1]
                new_x = -oty + self.current_figure[4][0]
                new_y = otx + self.current_figure[4][1]
                new_index = (new_x, new_y)
                self.next_figure.append(new_index)
            
            if self.check_collisions_rotation(self.next_figure) == True:
                for index in self.current_figure:
                    self.return_btn(index).uncolor()
                self.current_figure = self.next_figure.copy()
                self.draw()
            elif self.check_collisions_rotation(self.next_figure) == "Move left":
                print(self.check_collisions_rotation(self.next_figure))
                self.move_one_left()
                self.rotate()
            elif self.check_collisions_rotation(self.next_figure) == "Move right":
                print(self.check_collisions_rotation(self.next_figure))
                self.move_one_right()
                self.rotate()
            else:
                self.draw()


    def move_side(self, keycode):
        if keycode == "left":
            if not self.check_collisions_left():
                self.move_one_left()
                self.draw()
        if keycode == "right":
            if not self.check_collisions_right():
                self.move_one_right()
        if keycode == "up":
            self.rotate()
        if keycode == "down":
            self.play()
    
    
    def draw(self):
        for index in self.current_figure[:4]:
            self.return_btn(index).colored(self.current_num)

    def move_one_left(self):
        self.next_figure = []
        for index in self.current_figure:
            self.return_btn(index).uncolor()
            new_index = (index[0]+1, index[1])
            self.next_figure.append(new_index)
        self.current_figure = self.next_figure.copy()        

    def move_one_right(self):
        self.next_figure = []
        for index in self.current_figure:
            self.return_btn(index).uncolor()
            new_index = (index[0]-1, index[1])
            self.next_figure.append(new_index)
        self.current_figure = self.next_figure.copy()

    def move_one_down(self):
        self.next_figure = []
        for index in self.current_figure:
            self.return_btn(index).uncolor()
            new_index = (index[0], index[1]-1)
            self.next_figure.append(new_index)
        self.current_figure = self.next_figure.copy()

    def check_score(self):
        if self.score - self.level >= 300:
            self.game_speed-=0.05
            self.level = self.score
        self.score_label.text = f"Score: {self.score} \nLevel: {self.level//300}"

    def game_over(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        for row in self.children:
            for col in row.children:
                col.uncolor()
        self.add_widget(self.game_over_screen)
        self.game_over_screen.update()        
        self.event.cancel()
        self.score = 0
        self.game_speed = 0.3
        self.level = 0
        self.static_colored = []
        

    def play(self):
        self.check_score()
        for index in self.static_colored:
            if not self.return_btn(index[0]).is_colored:
                self.return_btn(index[0]).colored(index[1])
        if not self.check_collisions_down():
            self.move_one_down()
            self.draw()
        else:
            self.event.cancel()
            for index in self.current_figure[:4]:
                self.static_colored.append((index, self.current_num))
            if not any(index[0][1] > 18 for index in self.static_colored):
                self.remove_row()
                self.create_figure()
            else:
                self.game_over()

    def create_figure(self):
        s_x = random.randint(2,7)
        s_y = 22
        t_shape = [(s_x, s_y), (s_x, s_y+1), (s_x +1, s_y), (s_x -1, s_y), (s_x, s_y)]
        l1_shape = [(s_x, s_y), (s_x-1, s_y), (s_x , s_y+1), (s_x , s_y+2), (s_x -1, s_y+1)]
        l2_shape = [(s_x, s_y), (s_x+1, s_y), (s_x , s_y+1), (s_x , s_y+2), (s_x +1, s_y+1)]
        z1_shape = [(s_x, s_y), (s_x-1, s_y), (s_x , s_y-1), (s_x+1 , s_y-1), (s_x , s_y)]
        z2_shape = [(s_x, s_y), (s_x+1, s_y), (s_x , s_y-1), (s_x-1 , s_y-1), (s_x , s_y)]
        sq_shape = [(s_x, s_y), (s_x+1, s_y+1), (s_x , s_y+1), (s_x+1 , s_y), (s_x , s_y)]
        line_shape = [(s_x, s_y), (s_x, s_y-1), (s_x , s_y+1), (s_x , s_y+2), (s_x , s_y)]
        self.all_shapes = [t_shape, l1_shape, l2_shape, z1_shape, z2_shape, line_shape, sq_shape]
        self.current_num = random.randint(0,6)
        shape = self.all_shapes[self.current_num-1]        
        self.current_figure = shape
        self.event = Clock.schedule_interval(lambda dt: self.play(), self.game_speed)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.move_side(keycode[1])

class MyRow(GridLayout):
    def __init__(self, *args, **kwargs):
        super(MyRow, self).__init__(*args,**kwargs)
        self.cols = 10
        self.bind(size=self.update_rect)
        
    def update_rect(self, *args):
        with self.canvas.before:
            Color(0,0,0,0)
            self.rect = Rectangle(size = self.size, pos = self.pos) 

class MyCol(Button):
    def __init__(self, *args, **kwargs):
        super(MyCol, self).__init__(*args,**kwargs)
        self.background_color= (0,0,0,0)
        self.is_colored = False
        
    def colored(self, figure):          
        self.background_color = self.parent.parent.proper_colors[figure]
        self.is_colored = True

    def uncolor(self):
        self.background_color= (0,0,0,0)
        self.is_colored = False

class GameOver(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(GameOver, self).__init__(*args,**kwargs)
        self.orientation = "vertical"
        self.gg_label = Label(text = "Game Over", font_size = "20sp")
        self.score_label = Label(text = f"Your score:", font_size = "20sp")
        self.restart_btn = Button(text = "Restart", font_size = "20sp")
        self.restart_btn.bind(on_press = self.restart)
        self.add_widget(self.gg_label)
        self.add_widget(self.restart_btn)
        self.add_widget(self.score_label)
        

    def update(self):
        self.restart_btn.background_color = (0,1,1,1)
        self.score_label.text = f"Your score: {self.parent.score}"
    def restart(self, instance):
        self.parent.create_figure()
        self.parent.remove_widget(self)


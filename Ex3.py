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
import math
import random

style_color = (124/255,202/255,109/255,1)

class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        with self.canvas.before:
            Color(style_color[0],style_color[1],style_color[2],1)
            self.rect = Rectangle(size = self.size, pos = self.pos)
        self.bind(size=self.update_rect)
               
    def update_rect(self, *args):
        with self.canvas.before:
            Color(style_color[0],style_color[1],style_color[2],1)
            self.rect = Rectangle(size = self.size, pos = self.pos)
        
class ScoreWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(ScoreWindow, self).__init__(**kwargs)

class RightWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(RightWindow, self).__init__(**kwargs)

class GameWindow(FloatLayout):
    def __init__(self, left, right, **kwargs):
        super(GameWindow, self).__init__(**kwargs)
        self.current_index = []
        self.static_colored = []
        self.current_figure = None
        self.keyboard = Window.request_keyboard(None, self)
        self.score_window = left
        self.score = 0
        self.game_speed = 0.3
        self.level = 0
        self.score_label = Label(text = f"Score: {self.score} \nLevel: {self.level//300}")
        self.score_window.add_widget(self.score_label)

        #If you want to change the color of main screen
        with self.canvas.before:
            Color(0,0,0,1)
            self.rect = Rectangle(size = self.size, pos = self.pos)
        self.bind(size=self.update_rect)

    
        self.right_window = right
        self.img  = Image(source = "gg.jpg")
        #self.sound = SoundLoader.load('gg.MP3')

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        

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
                    if self.get_index(child) in self.static_colored:
                        self.static_colored.remove(self.get_index(child))
                self.dropped = []
                for index in self.static_colored:
                    if index[1] >= row_num:
                        self.return_btn(index).uncolor()
                        new_index = (index[0], index[1]-1)
                        self.dropped.append(new_index)
                    else:
                        self.dropped.append(index)
                self.static_colored = self.dropped.copy()
                for index in self.static_colored:
                    self.return_btn(index).colored()
                self.remove_row()


        
    def check_collisions_down(self):
        for static in self.static_colored:
            if any((index[0], index[1]-1) == static  for index in self.current_figure[:4]):
                return True
        if any(index[1] == 0 for index in self.current_figure[:4]):
            return True
    
    def check_collisions_left(self):
        for static in self.static_colored:
            if any((index[0]+1, index[1]) == static  for index in self.current_figure[:4]):
                return True
        if any(index[0] == 9 for index in self.current_figure[:4]):
            return True

    def check_collisions_right(self):
        for static in self.static_colored:
            if any((index[0]-1, index[1]) == static  for index in self.current_figure[:4]):
                return True
        if any(index[0] == 0 for index in self.current_figure[:4]):
            return True

    def check_collisions_rotation(self, figure):
        if any(new_index in self.static_colored for new_index in figure):
            return("No")
        elif any(new_index[0] < 0 for new_index in figure):
            return("Move left")
        elif any(new_index[0] > 9 for new_index in figure):
            return("Move right")
        else:
            return(True)


    def rotate(self):
        print(self.current_num)
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
            self.return_btn(index).colored()

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
        print(self.game_speed)
        if self.score - self.level >= 300:
            self.game_speed-=0.05
            self.level = self.score
            self.score_label.text = f"Score: {self.score} \nLevel: {self.level//300}"

    def play(self):
        self.check_score()
        for index in self.static_colored:
            if not self.return_btn(index).is_colored:
                self.return_btn(index).colored()
        if not self.check_collisions_down():
            self.move_one_down()
            self.draw()
        else:
            self.event.cancel()

            if any(index[1] > 18 for index in self.current_figure[:4]):
                self.right_window.add_widget(self.img)
                self.sound.play()
                self.score = 0
                self.game_speed = 0.3
                self.level = 0
                self.static_colored = []

            else:
                for index in self.current_figure[:4]:
                    self.static_colored.append((index, self.current_num))
                print(self.static_colored)
                self.remove_row()
                self.create_figure()

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
        self.all_shapes = [t_shape, l1_shape, l2_shape, z1_shape, z1_shape, line_shape, sq_shape]
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
        
    def colored(self):
        self.background_color = (0,1,0,1)
        self.is_colored = True

    def uncolor(self):
        self.background_color= (0,0,0,0)
        self.is_colored = False

main = MainWindow()
left_border = ScoreWindow()
right_border = RightWindow()
game_screen =  GameWindow(size_hint_x = 1.3, left = left_border, right = right_border) 
game_screen.draw_grid()
game_screen.create_figure()
main.add_widget(left_border)  
main.add_widget(game_screen)
main.add_widget(right_border)


class TestApp(App):

    def build(self):
    
        return main
if __name__=="__main__":
    TestApp().run()
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


#Window.size = (800,600)

class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

class MyButton(Button):
    def __init__(self, **args):
        super().__init__(**args)
        self.background_color= (1,0,0,1)
        self.pos_hint = {'x': 0.5, 'y': 0.95}


class MyFigure():
    def __init__(self, name, pre_rot, start_x, *args):
        self.all_btns = []
        self.name = name
        self.pre_rot = pre_rot
        self.start_x = start_x
        for i in range(0, 4):
            btn = MyButton(size_hint = (.1, .05))
            self.all_btns.append(btn)
        
        self.all_btns[2].pos_hint = {'x': float(start_x), 'y': 1.2}
        self.x = round(self.all_btns[2].pos_hint["x"],2)
        self.y = round(self.all_btns[2].pos_hint["y"], 2)

        if name == "T":
            self.all_btns[0].pos_hint["y"] = self.y +0.05 
            self.all_btns[0].pos_hint["x"] = self.x 
            self.all_btns[1].pos_hint["y"] = self.y 
            self.all_btns[1].pos_hint["x"] = self.x - 0.1
            self.all_btns[3].pos_hint["y"] = self.y 
            self.all_btns[3].pos_hint["x"] = self.x + 0.1

        else:
            self.all_btns[1].pos_hint["y"] = self.y - 0.05
            self.all_btns[1].pos_hint["x"] = self.x
            if name == "G1":
                self.all_btns[0].pos_hint["y"] = self.y 
                self.all_btns[0].pos_hint["x"] = self.x + 0.1
                self.all_btns[3].pos_hint["y"] = self.y - 0.1
                self.all_btns[3].pos_hint["x"] = self.x
            elif name == "G2":
                self.all_btns[0].pos_hint["y"] = self.y 
                self.all_btns[0].pos_hint["x"] = self.x - 0.1
                self.all_btns[3].pos_hint["y"] = self.y - 0.1
                self.all_btns[3].pos_hint["x"] = self.x
            elif name == "Square":
                self.all_btns[0].pos_hint["y"] = self.y 
                self.all_btns[0].pos_hint["x"] = self.x - 0.1
                self.all_btns[3].pos_hint["y"] = self.y - 0.05
                self.all_btns[3].pos_hint["x"] = self.x - 0.1
            elif name == "Line":
                self.all_btns[0].pos_hint["y"] = self.y + 0.05
                self.all_btns[0].pos_hint["x"] = self.x 
                self.all_btns[3].pos_hint["y"] = self.y - 0.1
                self.all_btns[3].pos_hint["x"] = self.x
            elif name == "Z1":
                self.all_btns[0].pos_hint["y"] = self.y 
                self.all_btns[0].pos_hint["x"] = self.x - 0.1
                self.all_btns[3].pos_hint["y"] = self.y - 0.05
                self.all_btns[3].pos_hint["x"] = self.x + 0.1
            elif name == "Z2":
                self.all_btns[0].pos_hint["y"] = self.y 
                self.all_btns[0].pos_hint["x"] = self.x + 0.1
                self.all_btns[3].pos_hint["y"] = self.y - 0.05
                self.all_btns[3].pos_hint["x"] = self.x - 0.1

        for i in range(0, pre_rot):
            self.rot()

    def rot(self):
        for btn in self.all_btns:
            otx = round(btn.pos_hint["x"],2) - self.x
            oty = round(btn.pos_hint["y"],2)- self.y
            btn.pos_hint = {'x': oty*2+self.x, 'y': -otx/2+self.y}

class Screen(FloatLayout):
    def __init__(self, left_border, right_border, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.current_btns = []
        self.next_btns = []
        self.temp = []
        self.num = 0
        self.all_names = ["Square", "Line", "Z1", "Z2", "G1", "G2", "T"]
        self.all_figures = []
        self.size = (Window.width/10, Window.height)
        self.pos = (Window.width/5, 0)
        self.keyboard = Window.request_keyboard(None, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)

        self.left_border = left_border
        self.right_border = right_border

        for i in range(0, 200):
            self.btn = Button(size_hint = (.1, .05), pos_hint = {'x': (i%10)/10, 'y': (i//10)/20}, id = f"{i//10, i%10}")
            self.btn.background_color = (1,0,1,1)
            self.add_widget(self.btn)

        
        
        self.create_first_figure()
        


    def check_collisions(self):
        for btn in self.current_btns:
            for button in self.all_figures:
                if ((round(btn.pos_hint["x"], 1) == (round(button.pos_hint["x"], 1)) and 
                (round(btn.pos_hint["y"], 2) <= (round(button.pos_hint["y"], 2)) + 0.05))):
                    #print("False")
                    return False
                else:
                    #print("Next")
                    pass
                    #continue
        #print("True")
            return True 
                    
                
    def create_next_figure(self):
        self.next_btns = []
        num = round(round(random.random(), 1)*6)
        pre_rot = round(round(random.random(), 1)*4)
        start_x = random.randint(2,7)/10
        next_name = self.all_names[num]
        self.next_figure = MyFigure(name = next_name, pre_rot = pre_rot, start_x = start_x)        
        for btn in self.next_figure.all_btns:
            self.add_widget(btn)
            self.next_btns.append(btn)
        self.event = Clock.schedule_interval(lambda dt: self.move_btn(), 0.3)

    def create_first_figure(self):
        num = round(round(random.random(), 1)*6)
        pre_rot = round(round(random.random(), 1)*4)
        start_x = random.randint(2,7)/10
        current_name = self.all_names[num]
        self.current_figure = MyFigure(name = current_name, pre_rot = pre_rot, start_x = start_x)        
        for btn in self.current_figure.all_btns:
            self.add_widget(btn)
            self.current_btns.append(btn)
        self.create_next_figure()

    def attach_figure(self):
        #self.current_btns = []
        self.temp = self.current_btns.copy()
        self.event.cancel()
        self.current_btns = []
        self.current_btns = self.next_btns.copy()
        for btn in self.temp:
            btn.pos_hint = {'x': round(btn.pos_hint["x"],2), 'y': round(btn.pos_hint["y"],2)}
            self.all_figures.append(btn)
        
        '''self.all_figures.append(self.current_figure)
        for btn in self.next_figure.all_btns:
            self.current_btns.append(btn)'''
        self.create_next_figure()
        


    def move_btn(self):  
        '''lowest  = min(self.current_btns[0].pos_hint["y"], self.current_btns[1].pos_hint["y"],
        self.current_btns[2].pos_hint["y"], self.current_btns[3].pos_hint["y"])
        self.check_collisions()
        if lowest >= 0.01:
            #self.keyboard.bind(on_key_down=self.on_keyboard_down)'''
        if (self.check_collisions() and not any((round(btn.pos_hint["y"], 2) <=0.01) for btn in self.current_btns)):
            #print("Down")
            self.move_one_down()
            '''for btn in self.current_btns:
                btn.pos_hint = {'x': round(btn.pos_hint["x"],2), 'y': round(btn.pos_hint["y"],2) - 0.05}'''
        else:
            print("Stop")
            '''for btn in self.current_btns:
                btn.pos_hint = {'x': round(btn.pos_hint["x"],2), 'y': round(btn.pos_hint["y"],2)}'''
            self.event.cancel()
            self.attach_figure()
            

                
        '''else:
            self.attach_figure()'''
            
    def move_one_left(self):
        for btn in self.current_btns:
            btn.pos_hint["x"]-=0.1 

    def move_one_right(self):
        for btn in self.current_btns:
            btn.pos_hint["x"]+=0.1

    def move_one_up(self):
        for btn in self.current_btns:
            btn.pos_hint = {'x': round(btn.pos_hint["x"],2), 'y': round(btn.pos_hint["y"],2) + 0.05}    

    def move_one_down(self):
        for btn in self.current_btns:
            btn.pos_hint = {'x': round(btn.pos_hint["x"],2), 'y': round(btn.pos_hint["y"],2) - 0.05} 

    def move_line(self, keycode):
        far_left = min(self.current_btns[0].pos_hint["x"], self.current_btns[1].pos_hint["x"],
        self.current_btns[0].pos_hint["x"], self.current_btns[3].pos_hint["x"])
        far_right = max(self.current_btns[0].pos_hint["x"], self.current_btns[1].pos_hint["x"],
        self.current_btns[0].pos_hint["x"], self.current_btns[3].pos_hint["x"])
        
        if (keycode == "up") and (self.current_figure.name != "Square"):
            x = round(self.current_btns[2].pos_hint["x"], 2)
            y = round(self.current_btns[2].pos_hint["y"], 2)
            for btn in self.current_btns:
                otx = round(btn.pos_hint["x"], 2) - x
                oty = round(btn.pos_hint["y"], 2) - y
                btn.pos_hint = {'x': oty*2+x, 'y': -otx/2+y}
            for btn in self.current_btns:
                if btn.pos_hint["x"] < 0:
                    self.move_one_right()
                elif btn.pos_hint["x"] > 0.9:
                    self.move_one_left()
                elif btn.pos_hint["y"] < 0:
                    self.move_one_up()
                

            
        if keycode == "left":
            if far_left > 0.05:
                for btn in self.current_btns:                             
                    btn.pos_hint = {'x': round(btn.pos_hint["x"], 2) - 0.1, 'y': round(btn.pos_hint["y"], 2)}
        
        if keycode == "right":
            if far_right < 0.85:
                for btn in self.current_btns:
                    btn.pos_hint = {'x': round(btn.pos_hint["x"], 2) + 0.1, 'y': round(btn.pos_hint["y"],2)}

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(keyboard, keycode, text, modifiers)
        self.move_line(keycode[1])
        #self.move_btn_side(keycode[1])

main = MainWindow()
left_border = GridLayout(size_hint_x = 0.5)
right_border = GridLayout(size_hint_x = 0.5) 
game_screen =  Screen(size_hint_x = 0.8, left_border = left_border, right_border = right_border)    
main.add_widget(left_border)  
main.add_widget(game_screen)
main.add_widget(right_border)


class TestApp(App):

    def build(self):
    
        return main
if __name__=="__main__":
    TestApp().run()
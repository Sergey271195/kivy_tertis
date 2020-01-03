import time
import threading
from multiprocessing import Process
from playsound import playsound
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.config import ConfigParser, Config
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen

from TetrisKV import GameWindow, MyCol, MyRow

on = True
i = 0
def playsound_btn(instance):
    global i, on
    i+=1
    print(i , on)
    if i/2 == 0:
        on = False
    else:
        on = True


def play_sound():
    global on
    print(on)
    while on:
        playsound("gg.mp3")


#Color scheme
black = (0,0,0,1)
red = (255,0,0,1)
blue = (0,0,255,1)
green = (0,255,0,1)
yellow = (255,255,0,1)
pink = (255,0,157,1)
orange = (255,128,0,1)
light_green = (102, 255, 102, 1)
violet = (102,0,204,1)
light_blue = (0,255,255,1)
colors_rgb  = [blue, red, green, yellow, pink, light_green, violet, light_blue]

proper_colors = []
for col in colors_rgb:
    color = [a/255 for a in col[:3]]
    color.append(col[3])
    proper_colors.append(color)

style_color = proper_colors[6]

class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.style_color = proper_colors[6]
        with self.canvas.before:
            Color(self.style_color[0],self.style_color[1],self.style_color[2],1)
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

Application = ScreenManager()
main = MainWindow()
left_border = ScoreWindow()
right_border = RightWindow()
game_screen =  GameWindow(size_hint_x = 1.4, left = left_border, right = right_border)
game_screen.proper_colors = proper_colors 
main.add_widget(left_border)
sound_btn = Button(text = "sound")
sound_btn.bind(on_press = playsound_btn)
left_border.add_widget(sound_btn)  
main.add_widget(game_screen)
main.add_widget(right_border)

class MyApp(App):

    def build(self):
        time.sleep(0.1)
        return main

if __name__ == "__main__":
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e:
        e.submit(play_sound)
        e.submit(MyApp().run())
        
    '''Game = Process(target=MyApp().run())
    Soundtrack = Process(target=play_sound)
    Game.start()
    Soundtrack.start()
    
    Soundtrack.join()
    Game.join()'''
    
    

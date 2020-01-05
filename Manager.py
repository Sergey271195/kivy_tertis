import time
import threading
from kivy.uix.image import Image
from kivy.uix.popup import Popup
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
from kivy.core.audio import SoundLoader

from TetrisKV import GameWindow, MyCol, MyRow
from db import BdManager
from StartingScreen import RegisterForm



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


class MyPopup(Popup):
    def __init__(self, source, screen, **kwargs):
        super().__init__(**kwargs)
        self.screen = screen
        self.title='Greetings, Friend!'
        self.source = source
        self.icon = Image(source = self.source)
        self.size_hint=(None, None)
        self.size=(400, 400) 
        self.auto_dismiss = False
        self.lbl = Label(font_size = "30sp")
        self.btn = Button(text = "START PLAYING", font_size = "18sp", size_hint_y = 0.3, size_hint_x = 1)
        self.btn.bind(on_press = self.to_next_screen)
        self.box = BoxLayout(padding = (20,20), orientation = "vertical")
        self.box.add_widget(self.icon)
        self.box.add_widget(self.lbl)
        self.box.add_widget(self.btn)
        self.add_widget(self.box)
    
    def to_next_screen(self, *args):
        self.dismiss()
        self.screen.switch_screen(self)
        self.screen.create_leaderboard()

class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.proper_colors = proper_colors
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
        self.orientation = "vertical"

class RightWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(RightWindow, self).__init__(**kwargs)

class Application(ScreenManager):
    def __init__(self, **kwargs):
        super(Application, self).__init__(**kwargs)

        #Starting Screen
        self.db = BdManager("Tetris.db", "Players")
        self.reg_form = RegisterForm()
        self.start = Screen(name = "Start")
        self.start.add_widget(self.reg_form)
        self.reg_form.submit.bind(on_press = self.to_login_screen)
        

        #Game Screen
        self.sound = SoundLoader.load("Main_theme.mp3")
        self.game = Screen(name = "Game")
        self.add_widget(self.start)
        self.add_widget(self.game)

        self.create_game_screen()

    def create_game_screen(self):
        self.main = MainWindow()
        self.left_border = ScoreWindow()
        self.right_border = RightWindow()
        self.game_screen =  GameWindow(size_hint_x = 1.4, left = self.left_border, right = self.right_border)
        self.game_screen.proper_colors = proper_colors 
        self.main.add_widget(self.left_border)
        self.main.add_widget(self.game_screen)
        self.main.add_widget(self.right_border)
        self.game.add_widget(self.main)
        self.game_screen.sound_btn.bind(on_press = self.play_music)
        self.game_screen.back_btn.bind(on_press = self.back)

    def play_music(self, instance):
        if instance.text == "Music off":
            instance.text = "Music on"
            self.sound.stop()
        else:
            instance.text = "Music off"
            self.sound.play()
            self.sound.loop = True

    def back(self, instance,*args):
        self.game.clear_widgets()
        self.switch_screen(instance)
        self.create_game_screen()
        if self.sound.state == "play":
            self.sound.stop()

    def switch_screen(self, instance):
        if self.current == "Start":
            self.current = "Game"
            #self.game_screen.define_next_figure()
            self.game_screen.create_figure()
        elif self.current == "Game":
            self.current = "Start"

    def to_login_screen(self, instance):
        self.firstname = self.reg_form.firstname_input.text.strip()
        self.lastname = self.reg_form.lastname_input.text.strip()
        if (self.lastname == "" or self.firstname == ""):
            pass
        else:
            self.img_source = self.reg_form.img.source
            self.popup = MyPopup(self.img_source, self)
            self.db.add_player(self.firstname, self.lastname)
            self.db.login(self.firstname, self.lastname)
            self.popup.lbl.text = f"Welcome {self.firstname} {self.lastname}"
            self.game_screen.img.source = self.img_source
            self.game_screen.firstname_label.text = f"{self.firstname}"
            self.game_screen.lastname_label.text = f"{self.lastname}"
            self.popup.open()

    def create_leaderboard(self):
        self.game_screen.pos_box.clear_widgets()
        self.game_screen.name_box.clear_widgets()
        self.game_screen.score_box.clear_widgets()
        for i in range(0, len(self.db.get_leaderboard_names()[:10])):
            self.game_screen.pos_box.add_widget(Label(text = f"{i+1}"))
        for name, lastname in self.db.get_leaderboard_names()[:10]:
            self.game_screen.name_box.add_widget(Label(text = f"{name} {lastname}"))
        for score in self.db.get_leaderboard_score()[:10]:
            self.game_screen.score_box.add_widget(Label(text = f"{score}"))



class MyApp(App):

    def build(self):
        return Application()


if __name__ == "__main__":
    MyApp().run()
    
    

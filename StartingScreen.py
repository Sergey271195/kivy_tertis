from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window, WindowBase
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen

class IconButton(ButtonBehavior, Image):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images = ['man.png', 'man_1.png', 'man_2.png', 'man_3.png']
        self.num = 0
        self.source = self.images[self.num]

    def on_press(self):
        self.num+=1
        if self.num == 4:
            self.num = 0
        self.source = self.images[self.num]

class MyTextInput(TextInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.padding_y = [self.height/2 - self.line_height/2,0]
        self.bind(size = self.update_font)
        self.font_size = "20sp"

    def update_font(self, *args):
        self.padding_y = [self.height/2 - self.line_height/2 ,0]




class RegisterForm(BoxLayout):
    def __init__(self, **kwargs):
        super(RegisterForm, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.frame = GridLayout(cols = 2)
        self.padding = (200,150,200,150)
        self.all_inputs = []
        self.submit = Button(text = "Submit", size_hint_y = 0.2)
        self.forms = BoxLayout(orientation = "vertical", spacing = (20))
        self.inputs = BoxLayout(orientation = "vertical", spacing = (20))
        self.photo = Label(text = '', size_hint_y = 2)
        self.firstname = Label(text = "Firstname", font_size = "18sp")
        self.lastname = Label(text = "Lastname", font_size = "18sp")

        self.img = IconButton(size_hint_y = 2)

        self.firstname_input = MyTextInput(multiline = False)
        self.lastname_input = MyTextInput(multiline = False)

        self.forms.add_widget(self.photo)
        self.forms.add_widget(self.firstname)
        self.forms.add_widget(self.lastname)

        self.inputs.add_widget(self.img)
        self.inputs.add_widget(self.firstname_input)
        self.inputs.add_widget(self.lastname_input)

        self.frame.add_widget(self.forms)
        self.frame.add_widget(self.inputs)
        self.add_widget(self.frame)
        self.add_widget(self.submit)
        self.spacing = 20
        self.bind(size = self.update_rect)
    
    def update_rect(self, *args):
        with self.canvas.before:
            self.img.rect = Rectangle(size = self.size, pos = self.pos, source = "bg.jpg")

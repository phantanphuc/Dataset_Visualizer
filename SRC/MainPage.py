from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout

from Labeler.Labeler import *

class MainScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("main.kv")

class MainApp(App):
    def build(self):
        return presentation

MainApp().run()
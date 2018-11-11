from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.treeview import TreeViewLabel
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.core.image import Image as CoreImage

from kivy.config import Config
# Config.set('graphics', 'fullscreen', 1)
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)
from Labeler.Labeler import *



class LoadDialog(FloatLayout):
	load = ObjectProperty(None)
	cancel = ObjectProperty(None)


class MainScreen(Screen):
	pass
class ScreenManagement(ScreenManager):
	pass

class MainApp(App):
	pass



if __name__ == '__main__':
	
	presentation = Builder.load_file("main.kv")
	MainApp().run()
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout

class LabelerManager:
	def __init__(self):
		self.path = '/'

	@staticmethod
	def getInstance():
		return LabelerManagerInstance

	def setPath(self, path):
		self.path = path
		Labeler_Labeling.path = path


LabelerManagerInstance = LabelerManager()

class Labeler(Screen):
    pass

class Labeler_ChooseFile(Screen):
    def start_labeling(self):
    	# print(self.ids['file_chooser'].path)
    	LabelerManager.getInstance().setPath(self.ids['file_chooser'].path)
    	print(self.ids)


class Labeler_Labeling(Screen):
	path = LabelerManager.getInstance().path

	def setLookPath(self):
		self.ids['listfile'].path = '/home/phucpt2/Desktop/visual/prj/Dataset_Visualizer/SRC/Labeler'

import os

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.treeview import TreeViewLabel
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Line, Rectangle

Builder.load_string("""
#:kivy 1.1.0

<LoadDialog>:
	BoxLayout:
		size: root.size
		pos: root.pos
		orientation: "vertical"
		FileChooserListView:
			id: filechooser
			path: '/home/phucpt2/Desktop/visual/prj/Dataset_Visualizer/Label'

		BoxLayout:
			size_hint_y: None
			height: 30
			Button:
				text: "Cancel"
				on_release: root.cancel()

			Button:
				text: "Load"
				on_release: root.load(filechooser.path, filechooser.selection)""")

Builder.load_file("kv/Labeler.kv")

class LoadDialog(FloatLayout):
	load = ObjectProperty(None)
	cancel = ObjectProperty(None)

class LabelerManager:
	def __init__(self):
		self.path = '/'
		self.labeled_data = {}
		self.label_classes = {}


	# Structure of labeled data:
	# {Key, (path, node)}
	#

	@staticmethod
	def getInstance():
		return LabelerManagerInstance

	def setPath(self, path):
		self.path = path
		self.labeled_data = {}
		Labeler_Labeling.path = path

	def restartLabelClasses(self):
		self.label_classes = {}

	def addToLabelClasses(self, key, value):
		self.label_classes['key'] = value

	def getPath(self):
		return self.path

	def generateTreeView(self, path, treeview):

		# "D:\dataset\img"

		for root, dirs, files in os.walk(path):
			for file in files:

				if root == path:
					tree_node = treeview.add_node(TreeViewLabel(text=file, is_open=True))

					# print(root)
					# print(dirs)
					# print(file)

					full_path = root + '/' + file

					self.labeled_data[file] = (full_path, tree_node)

					# treeview.add_node(TreeViewLabel(text='blah',  is_open=True), tree_node)
					

				else:
					break


	def updateCurrentImage(self, key, canvas):
		canvas.source = self.labeled_data[key][0]


LabelerManagerInstance = LabelerManager()

class Labeler(Screen):
	pass

class Labeler_ChooseFile(Screen):
	def start_labeling(self):
		LabelerManager.getInstance().setPath(self.ids['file_chooser'].path)
		print(self.ids)


class Labeler_Labeling(Screen):

	loadfile = ObjectProperty(None)

	path = LabelerManager.getInstance().path

	def on_parent(self, widget, parent):

		self.draw_canvas = self.ids['canvas_labeling']

		LabelerManager.getInstance().generateTreeView("D:\dataset\img", self.ids['treeview'])

		self.toref = 0

		self.ids['treeview'].hide_root = True
		self.ids['treeview'].bind(minimum_height=self.ids['treeview'].setter("height"))


		with self.draw_canvas.canvas:
			self.draw_canvas.bg = Rectangle(source='D:/dataset/img/testtt/asfasdasdas.png', 
					pos=self.draw_canvas.pos, size=self.draw_canvas.size)

		


	def setLookPath(self):
		with self.draw_canvas.canvas:

			temp = self.draw_canvas.size
			temp = (temp[0], temp[1] / 2)

			self.data = InstructionGroup()
			self.data.add(Rectangle(source='D:/dataset/img/person_009.png', 
					pos=self.draw_canvas.pos, size=temp, group='my_group'))

			self.draw_canvas.canvas.add(self.data)

			# self.draw_canvas.canvas.remove_group(data)

	def test2(self):
		self.draw_canvas.canvas.remove(self.data)
		self.canvas.remove(self.data)
		# self.draw_canvas.canvas.remove_group('my_group')
		pass


	def show_load(self):
		content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
		self._popup = Popup(title="Load file", content=content,
							size_hint=(0.9, 0.9))
		self._popup.open()


	def load(self, path, filename):
		with open(filename[0], 'r') as file:
			lines = file.readlines()
			label_arr = []
			LabelerManager.getInstance().restartLabelClasses()
			for line in lines:
				info = line.replace('\n', '').split(',')
				label_arr.append(info[0])
				LabelerManager.getInstance().addToLabelClasses(info[0], info[1])

			self.ids['label_spinner'].values = label_arr

			
				

		self.dismiss_popup()
	def dismiss_popup(self):
		self._popup.dismiss()


	undolist = []
	objects = []
	drawing = False

	def on_touch_up(self, touch):
		self.drawing = False

	def on_touch_move(self, touch):
		if self.drawing:
			self.points.append(touch.pos)
			self.obj.children[-1].points = self.points
		else:
			self.drawing = True
			self.points = [touch.pos]
			self.obj = InstructionGroup()
			self.obj.add(Color(1,0,0))
			self.obj.add(Line())
			self.objects.append(self.obj)
			self.canvas.add(self.obj)


	def undo(self):
		item = self.objects.pop(-1)
		self.undolist.append(item)
		self.canvas.remove(item)

	def redo(self):
		item = self.undolist.pop(-1)
		self.objects.append(item)
		self.canvas.add(item)

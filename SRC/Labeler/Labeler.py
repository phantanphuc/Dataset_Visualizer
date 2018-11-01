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
from kivy.uix.label import Label
from kivy.core.text import Label as CoreLabel
from kivy.core.window import Window

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
	# {Key, (path, node, [child])}
	# child {name, id, label, rect, node}

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
		self.label_classes[key] = value

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

					self.labeled_data[file] = (full_path, tree_node, [])

					# aa = treeview.add_node(TreeViewLabel(text='blah',  is_open=True), tree_node)
					# treeview.remove_node(aa)
				else:
					break


	def updateCurrentImage(self, key, canvas):
		# canvas = self.draw_canvas
		canvas.canvas.clear()
		with canvas.canvas:

			if True:

				with canvas.canvas:
					canvas.bg = Rectangle(source=self.labeled_data[key][0], 
							pos=canvas.pos, size=canvas.size)



			# self.draw_canvas.bg = Rectangle(source='/home/phucpt2/Desktop/visual/data/img/person_002.png', 
			# 		pos=self.draw_canvas.pos, size=self.draw_canvas.size)

	def registCurrentLabel(self, filename, rect, label, treeview): #label: text
		# child {name, id, label, rect, node}
		treenode = self.labeled_data[filename]

		curr_id = 0

		if len(tree_node[2]) > 0:
			curr_id = tree_node[2][-1]['id']

		child_node = {}


		child_node_tree = treenode[1].add_node(TreeViewLabel(text=label + ' ' + str(curr_id),  is_open=True), tree_node)

		child_node['name'] = label + ' ' + str(curr_id)
		child_node['id'] = curr_id
		child_node['label'] = self.label_classes[label]
		child_node['rect'] = rect
		child_node['node'] = child_node_tree

		treenode[2].append(child_node)


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

	def __init__(self, **kwargs):
		super(Labeler_Labeling, self).__init__(**kwargs)
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)


		Window.bind(on_resize=self.on_resize)

	def on_parent(self, widget, parent):

		self.draw_canvas = self.ids['canvas_labeling']

		LabelerManager.getInstance().generateTreeView("/home/phucpt2/Desktop/visual/data/img/", self.ids['treeview'])

		self.ids['treeview'].hide_root = True
		self.ids['treeview'].bind(minimum_height=self.ids['treeview'].setter("height"))


		with self.draw_canvas.canvas:
			self.draw_canvas.bg = Rectangle(source='/home/phucpt2/Desktop/visual/data/img/person_002.png', 
					pos=self.draw_canvas.pos, size=self.draw_canvas.size)

	


	def on_resize(self, window, width, height):

		pass		

		# with self.draw_canvas.canvas:
		# 	self.ids['canvas_labeling'].canvas.clear()
		# 	self.draw_canvas.bg = Rectangle(source='/home/phucpt2/Desktop/visual/data/img/person_003.png', 
		# 			pos=self.draw_canvas.pos, size=self.draw_canvas.size)

	def chooseImage(self):

		self.clearAllLabeledRect()

		if (self.ids['treeview'].selected_node != None):
			print(self.ids['treeview'].selected_node.text)
			LabelerManager.getInstance().updateCurrentImage(self.ids['treeview'].selected_node.text, self.draw_canvas)


	def setLookPath(self):

		

		self.loadChoosenImage()

			# self.draw_canvas.canvas.remove_group(data)

	def test2(self):
		with self.draw_canvas.canvas:
			print('test2')
			print(self.draw_canvas.canvas.remove(self.data))
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


	

	current_rect = 0
	rects = []
	drawing = False

	def on_touch_up(self, touch):
		self.drawing = False
		# registCurrentLabel(self, filename, rect, label, treeview):

		print(touch)
		print(self.ids['canvas_labeling'].pos)
		print(self.ids['canvas_labeling'].size)
		print(self.ids['canvas_labeling'].pos_hint)

		# LabelerManager.getInstance().registCurrentLabel(self.ids['treeview'].selected_node.text, self.drawing_rect, self.ids['label_spinner'].text, self.ids['treeview'])

	def on_touch_move(self, touch):
		if self.drawing:
			self.drawing_rect = (self.points[0], self.points[1], touch.pos[0] - self.points[0], touch.pos[1] - self.points[1])
			self.obj.children[-1].rectangle = self.drawing_rect
			# self.obj.children[-1].size = self.drawing_rect
			pass
		else:
			self.drawing = True
			self.points = touch.pos
			self.obj = InstructionGroup()
			self.obj.add(Color(1,0,0))
			# self.obj.add(LineRectangle(pos=touch.pos, size=(10, 10), opacity=0.2))
			

			label = CoreLabel(self.ids['label_spinner'].text, font_size=15)
			label.refresh()
			text = label.texture
			self.obj.add(Rectangle(size=text.size, pos=touch.pos, texture=text))
			self.obj.add(Line(rectangle = (touch.pos[0], touch.pos[1], 10, 10), width = 1.5))


			self.current_rect = self.obj
			self.rects.append(self.obj)
			self.canvas.add(self.obj)


	def undo(self):
		if len(self.rects) != 0:
			todel = self.rects.pop()
			self.canvas.remove(todel)


	def clearAllLabeledRect(self):
		for rect in self.rects:
			self.canvas.remove(rect)

		self.rects = []


	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None


	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		print(keycode)
		if keycode[1] == 'delete':
			print('bleh')

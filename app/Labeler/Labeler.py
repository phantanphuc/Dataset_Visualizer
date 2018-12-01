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
from kivy.uix.image import Image
import math
from kivy.config import Config


Builder.load_file("kv/Labeler.kv")
Builder.load_file("kv/labeler_popup.kv")

class LoadDialog(FloatLayout):
	load = ObjectProperty(None)
	cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
	save = ObjectProperty(None)
	text_input = ObjectProperty(None)
	cancel = ObjectProperty(None)

	def on_spinner_select(self, text):
		print(text)
		if text == 'XML':
			self.ids['output_format'].text = '$filename { $x $y $w $h $label}'
		if text == 'TEXT':
			self.ids['output_format'].text = \
				'<record>\n' \
				'\t<name>$filename</name>\n'\
				'{\t<object>$x $y $w $h $label</object>}\n'\
				'</record>'


class LabelerManager:
	def __init__(self):
		self.path = '/'
		self.labeled_data = {}
		self.label_classes = {}
		self.scale_factor = 1.0
		self.current_img_size = (0,0)
		self.current_mode = 1 # 0: add mode, 1: delete mode

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

	def getCurrentMode(self):
		return self.current_mode

	def generateTreeView(self, path, treeview):

		# "D:\dataset\img"
		self.labeled_data = {}
		iterator = treeview.iterate_all_nodes()
		try:
			for node in list(iterator):
				treeview.remove_node(node)
		except:
			pass

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

	def changeBackgroundImage(self, path, canvas):
		with canvas.canvas:

				current_canvas_size = canvas.size
				canvas.bg = Rectangle(source=path, pos=canvas.pos, 
					size= canvas.size)

				self.scale_factor = current_canvas_size[1] / canvas.bg.texture.size[1]
				canvas.bg.size = (canvas.bg.texture.size[0] * self.scale_factor, current_canvas_size[1])


	def updateCurrentImage(self, key, canvas, clicked_node):
		# canvas = self.draw_canvas self.ids['treeview'].selected_node
		canvas.canvas.clear()

		if key in self.labeled_data.keys():
			self.current_mode = 0

			self.changeBackgroundImage(self.labeled_data[key][0], canvas)

			# with canvas.canvas:

			# 	current_canvas_size = canvas.size
			# 	canvas.bg = Rectangle(source=self.labeled_data[key][0], pos=canvas.pos, 
			# 		size= canvas.size)

			# 	self.scale_factor = current_canvas_size[1] / canvas.bg.texture.size[1]
			# 	canvas.bg.size = (canvas.bg.texture.size[0] * self.scale_factor, current_canvas_size[1])

			treenode = self.labeled_data[key]
			# {Key, (path, node, [child])}
			# child {name, id, label, rect, node}

			objlist = []
			inv_map = {v: k for k, v in self.label_classes.items()}
			for node in treenode[2]:

				obj = InstructionGroup()
				obj.add(Color(1,0,0))
				label = CoreLabel(inv_map[node['label']], font_size=15)
				label.refresh()
				text = label.texture
				obj.add(Rectangle(size=text.size, pos=(node['rect'][0], node['rect'][1]), texture=text))
				obj.add(Line(rectangle = node['rect'], width = 1.5))
				objlist.append(obj)
				canvas.canvas.add(obj)

			return objlist

		else:
			self.current_mode = 1
			parent_key = clicked_node.parent_node.text

			self.changeBackgroundImage(self.labeled_data[parent_key][0], canvas)

			treenode = self.labeled_data[parent_key]
			# {Key, (path, node, [child])}
			# child {name, id, label, rect, node}

			objlist = []
			inv_map = {v: k for k, v in self.label_classes.items()}
			for node in treenode[2]:

				if node['name'] == key:

					obj = InstructionGroup()
					obj.add(Color(1,0,0))
					label = CoreLabel(inv_map[node['label']], font_size=15)
					label.refresh()
					text = label.texture
					obj.add(Rectangle(size=text.size, pos=(node['rect'][0], node['rect'][1]), texture=text))
					obj.add(Line(rectangle = node['rect'], width = 1.5))
					objlist.append(obj)
					canvas.canvas.add(obj)

			return objlist

			# self.draw_canvas.bg = Rectangle(source='/home/phucpt2/Desktop/visual/data/img/person_002.png', 
			# 		pos=self.draw_canvas.pos, size=self.draw_canvas.size)

	def registCurrentLabel(self, filename, rect, label, treeview, canvas): #label: text
		# child {name, id, label, rect, node}
		im_size = canvas.bg.size
		img_size = (im_size[0] * self.scale_factor, im_size[1] * self.scale_factor)

		base_point = canvas.pos
		relative_rect = (rect[0] - base_point[0], im_size[1] - (rect[1] - base_point[1]), 
				abs(rect[2] / self.scale_factor), abs(rect[3] / self.scale_factor ))


		treenode = self.labeled_data[filename]

		curr_id = 0

		if len(treenode[2]) > 0:
			curr_id = treenode[2][-1]['id'] + 1

		child_node = {}


		child_node_tree = treeview.add_node(TreeViewLabel(text=label + ' ' + str(curr_id),  is_open=True), treenode[1])

		child_node['name'] = label + ' ' + str(curr_id)
		child_node['id'] = curr_id
		child_node['label'] = self.label_classes[label]
		child_node['rect'] = rect
		child_node['relative_rect'] = relative_rect
		child_node['node'] = child_node_tree

		treenode[2].append(child_node)

	def saveToFile(self, path, format_str):
		with open(path, 'w') as fout:
			format_node_abstract = format_str[format_str.find('{') + 1:  format_str.find('}')]
			format_node_toreplace = format_str[format_str.find('{'):  format_str.find('}') + 1]

			for key, value in self.labeled_data.items():
				if len(value[2]) > 0:
					list_bb = ''
					for bounding_box in value[2]:
						relative_rect = bounding_box['relative_rect']
						format_node = format_node_abstract.replace('$x', str(relative_rect[0]))\
															.replace('$y', str(relative_rect[1]))\
															.replace('$w', str(relative_rect[2]))\
															.replace('$h', str(relative_rect[3]))\
															.replace('$label', str(bounding_box['label']))
						list_bb = list_bb + format_node
					towrite = format_str.replace('$filename', key).replace(format_node_toreplace, list_bb) + '\n'
					fout.write(towrite)


	def deleteCurrentLabel(self, canvas, key, clicked_node, treeview):
		

		# {Key, (path, node, [child])}
		# child {name, id, label, rect, node}

		if key not in self.labeled_data.keys():
			parent_key = clicked_node.parent_node.text
			parent_node = self.labeled_data[parent_key]

			del_index = 0

			for node in parent_node[2]:
				if node['name'] == key:
					treeview.remove_node(node['node'])
					break

				del_index = del_index + 1

			del parent_node[2][del_index]
			canvas.canvas.clear()

			self.changeBackgroundImage(parent_node[0], canvas)

			# with canvas.canvas:
			# 	canvas.bg = Rectangle(source=parent_node[0], pos=canvas.pos, size=canvas.size)

			return True
		return False

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


		

	def on_parent(self, widget, parent):

		self.just_delete = True
		self.draw_canvas = self.ids['canvas_labeling']
		self.drawing_rect = (0,0,0,0)
		# Window.bind(on_resize=self.on_resize)

		LabelerManager.getInstance().generateTreeView(LabelerManager.getInstance().getPath(), self.ids['treeview'])

		self.ids['treeview'].hide_root = True
		self.ids['treeview'].bind(minimum_height=self.ids['treeview'].setter("height"))


		with self.draw_canvas.canvas:
			self.draw_canvas.bg = Rectangle(source='D:/dataset/img/carsgraz_004.png', 
					pos=self.draw_canvas.pos)#, size=self.draw_canvas.size)

	
		


	# def on_resize(self, window, width, height):
	# 	print(self)

	# 	try:
	# 		with self.draw_canvas.canvas:
	# 			# self.ids['canvas_labeling'].canvas.clear()
	# 			self.draw_canvas.bg = Rectangle(source='/home/phucpt2/Desktop/visual/data/img/person_003.png', 
	# 					pos=self.draw_canvas.pos, size=self.draw_canvas.size)
	# 	except:
	# 		pass

	def chooseImage(self):

		self.clearAllLabeledRect()
		self.just_delete = False

		if (self.ids['treeview'].selected_node != None):


			self.rects = LabelerManager.getInstance().updateCurrentImage(
						self.ids['treeview'].selected_node.text, self.draw_canvas, self.ids['treeview'].selected_node)


	def setLookPath(self):
		pass

			# self.draw_canvas.canvas.remove_group(data)

	def test2(self):

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
		if self.ids['label_spinner'].text == '' or self.just_delete or LabelerManager.getInstance().getCurrentMode() == 1:
			return
		self.drawing = False
		mouse_loc = touch.pos

		im_loc = self.ids['canvas_labeling'].pos
		im_size = self.ids['canvas_labeling'].size

		if im_loc[0] < mouse_loc[0] and mouse_loc[0] < im_loc[0] + im_size[0] and im_loc[1] < mouse_loc[1] and mouse_loc[1] < im_loc[1] + im_size[1]:
			if self.drawing_rect[2] > 5:
				LabelerManager.getInstance().registCurrentLabel(self.ids['treeview'].selected_node.text, self.drawing_rect, self.ids['label_spinner'].text, self.ids['treeview'], self.draw_canvas)

	def on_touch_move(self, touch):

		if self.ids['label_spinner'].text == '' or self.just_delete or LabelerManager.getInstance().getCurrentMode() == 1:
			return

		if self.drawing:
			self.drawing_rect = (self.points[0], self.points[1], touch.pos[0] - self.points[0], touch.pos[1] - self.points[1])
			self.obj.children[-1].rectangle = self.drawing_rect
			# self.obj.children[-1].size = self.drawing_rect
			pass
		else:
			mouse_loc = touch.pos
			im_loc = self.ids['canvas_labeling'].pos
			im_size = self.ids['canvas_labeling'].size
			if im_loc[0] < mouse_loc[0] and mouse_loc[0] < im_loc[0] + im_size[0] and im_loc[1] < mouse_loc[1] and mouse_loc[1] < im_loc[1] + im_size[1]:
				self.drawing = True
				self.points = touch.pos
				self.obj = InstructionGroup()
				self.obj.add(Color(1,0,0))
				label = CoreLabel(self.ids['label_spinner'].text, font_size=15)
				label.refresh()
				text = label.texture
				self.obj.add(Rectangle(size=text.size, pos=touch.pos, texture=text))
				self.obj.add(Line(rectangle = (touch.pos[0], touch.pos[1], 5, 5), width = 1.5))
				self.current_rect = self.obj
				self.rects.append(self.obj)
				self.draw_canvas.canvas.add(self.obj)


	def undo(self):
		if len(self.rects) != 0:
			todel = self.rects.pop()
			self.draw_canvas.canvas.remove(todel)


	def clearAllLabeledRect(self):
		for rect in self.rects:
			self.draw_canvas.canvas.remove(rect)

		self.rects = []


	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None


	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		print(keycode)
		if keycode[1] == 'delete':

			# def deleteCurrentLabel(self, key, clicked_node, treeview):
			if LabelerManager.getInstance().deleteCurrentLabel(self.draw_canvas, self.ids['treeview'].selected_node.text, self.ids['treeview'].selected_node, self.ids['treeview']):
				self.just_delete = True


	def show_save(self):
		content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
		self._popup = Popup(title="Save file", content=content,
							size_hint=(0.9, 0.9))
		self._popup.open()


	def save(self, path, filename, format_string):
		if path in filename:
			LabelerManager.getInstance().saveToFile(filename, format_string)
		else:
			LabelerManager.getInstance().saveToFile(path + '/' + filename, format_string)
		self.dismiss_popup()

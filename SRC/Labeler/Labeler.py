import os

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.treeview import TreeViewLabel
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

class LoadDialog(FloatLayout):
	load = ObjectProperty(None)
	cancel = ObjectProperty(None)

class LabelerManager:
	def __init__(self):
		self.path = '/'
		self.labeled_data = {}


	# Structure of labeled data:
	# {Key, ()}
	#

	@staticmethod
	def getInstance():
		return LabelerManagerInstance

	def setPath(self, path):
		self.path = path
		Labeler_Labeling.path = path

	def getPath(self):
		return self.path

	def generateTreeView(self, path, treeview):

		# "D:\dataset\img"

		for root, dirs, files in os.walk(path):
			for file in files:

				if root == path:
					tree_node = treeview.add_node(TreeViewLabel(text=file, is_open=True))
					treeview.add_node(TreeViewLabel(text='blah',  is_open=True), tree_node)
					# print(root)
					# print(dirs)
					# print(file)

				else:
					break




LabelerManagerInstance = LabelerManager()

class Labeler(Screen):
	pass

class Labeler_ChooseFile(Screen):
	def start_labeling(self):
		LabelerManager.getInstance().setPath(self.ids['file_chooser'].path)
		print(self.ids)


class Labeler_Labeling(Screen):
	path = LabelerManager.getInstance().path

	def on_parent(self, widget, parent):

		LabelerManager.getInstance().generateTreeView("D:\dataset\img", self.ids['treeview'])

		self.toref = 0

		self.ids['treeview'].hide_root = True
		self.ids['treeview'].bind(minimum_height=self.ids['treeview'].setter("height"))



	def populate_tree_view(self, tree_view, parent, node):
		if parent is None:
			tree_node = tree_view.add_node(TreeViewLabel(text=node['node_id'],
														 is_open=True))
		else:
			tree_node = tree_view.add_node(TreeViewLabel(text=node['node_id'],
														 is_open=True), parent)

		for child_node in node['children']:
			self.populate_tree_view(tree_view, tree_node, child_node)

	def setLookPath(self):
		print(self.ids['treeview'].selected_node.text)
		print(self.ids['treeview'].selected_node.parent_node.text)
		# self.ids['treeview'].add_node(TreeViewLabel(text='blah',  is_open=True), self.ids['treeview'].selected_node)
		
	def show_load(self):
		content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
		self._popup = Popup(title="Load file", content=content,
							size_hint=(0.9, 0.9))
		self._popup.open()


	def load(self, path, filename):
		print(filename)
		self.dismiss_popup()
	def dismiss_popup(self):
		self._popup.dismiss()

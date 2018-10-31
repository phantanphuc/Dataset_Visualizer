from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.lang import Builder

Builder.load_string("""
#:kivy 1.1.0

<Root>:
	text_input: text_input

	BoxLayout:
		orientation: 'vertical'
		BoxLayout:
			size_hint_y: None
			height: 30
			Button:
				text: 'Load'
				on_release: root.show_load()
			Button:
				text: 'Save'
				on_release: root.show_save()

		BoxLayout:
			TextInput:
				id: text_input
				text: ''

			RstDocument:
				text: text_input.text
				show_errors: True

<LoadDialog>:
	BoxLayout:
		size: root.size
		pos: root.pos
		orientation: "vertical"
		FileChooserListView:
			id: filechooser

		BoxLayout:
			size_hint_y: None
			height: 30
			Button:
				text: "Cancel"
				on_release: root.cancel()

			Button:
				text: "Load"
				on_release: root.load(filechooser.path, filechooser.selection)

<SaveDialog>:
	text_input: text_input
	BoxLayout:
		size: root.size
		pos: root.pos
		orientation: "vertical"
		FileChooserListView:
			id: filechooser
			on_selection: text_input.text = self.selection and self.selection[0] or ''

		TextInput:
			id: text_input
			size_hint_y: None
			height: 30
			multiline: False

		BoxLayout:
			size_hint_y: None
			height: 30
			Button:
				text: "Cancel"
				on_release: root.cancel()

			Button:
				text: "Save"
				on_release: root.save(filechooser.path, text_input.text)""")
import os


class LoadDialog(FloatLayout):
	load = ObjectProperty(None)
	cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
	save = ObjectProperty(None)
	text_input = ObjectProperty(None)
	cancel = ObjectProperty(None)


class Root(FloatLayout):
	loadfile = ObjectProperty(None)
	savefile = ObjectProperty(None)
	text_input = ObjectProperty(None)

	def dismiss_popup(self):
		self._popup.dismiss()

	def show_load(self):
		content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
		self._popup = Popup(title="Load file", content=content,
							size_hint=(0.9, 0.9))
		self._popup.open()

	def load(self, path, filename):
		print(filename)
		self.dismiss_popup()

	def show_save(self):
		content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
		self._popup = Popup(title="Save file", content=content,
							size_hint=(0.9, 0.9))
		self._popup.open()

	

	def save(self, path, filename):
		with open(os.path.join(path, filename), 'w') as stream:
			stream.write(self.text_input.text)

		self.dismiss_popup()


class Editor(App):
	def build(self):
		return Root()




if __name__ == '__main__':
	Editor().run()
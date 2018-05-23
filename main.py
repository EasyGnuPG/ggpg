import os
import sys

import gi

gi.require_version('Gtk','3.0')
from gi.repository import Gtk, Gdk, Gio, GLib

class MainApp(Gtk.Application):

	def __init__(self, *args, **kwargs):

		super().__init__(application_id="apps.ggpg", flags=Gio.ApplicationFlags.FLAGS_NONE)
		self.window = None
		self.connect("startup", self.on_startup)
		self.connect("activate", self.on_activate)
		self.connect("shutdown", self.on_shutdown)

	def on_activate(self, data=None):
		#To allow only a single instance and raise any running isntances.
		if not self.window:
			#The startup signal is fired when the application starts
			#This should serve just as a fallback incase the Window wasn't initialized
			self.on_startup(self)

		self.window.present()



	def on_startup(self, data=None):
		#Sets up the window and connects widgets to callback functions

		self.window = Gtk.ApplicationWindow(application=self, title="EasyGnuPG")
		self.window.set_default_size(640,480)
		#TODO : Add support for widgets that need to be re-sized with the window
		self.window.set_border_width(10)
		self.window.connect('delete_event', self.on_delete_window)
		self.add_window(self.window)

		window_split = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

		statusbar = Gtk.Statusbar()
		window_split.pack_end(statusbar, False, False, 0)
		
		#This will be changed when writing callbacks
		context = statusbar.get_context_id("status")
		statusbar.push(context,"In development")

		center_split = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

		window_split.pack_end(center_split, True, True, 0)

		notebook = Gtk.Notebook()
		notebook.set_vexpand(True)
		center_split.pack_end(notebook, True, True, 0)

		page1 = Gtk.Box()
		page1.set_vexpand(True)
		page1.set_border_width(10)
		page1.add(Gtk.Button.new_with_label('Open a file to Encrypt'))
		notebook.append_page(page1, Gtk.Label('Encrypt'))
		page2 = Gtk.Box()
		page2.set_border_width(10)
		page2.add(Gtk.Button.new_with_label('Open an encrypted file to decrypt'))
		notebook.append_page(page2, Gtk.Label('Decrypt'))
		page3 = Gtk.Box()
		page3.set_border_width(10)
		page3.add(Gtk.Button.new_with_label('Sign a file'))
		notebook.append_page(page3, Gtk.Label('Signature'))
		page4 = Gtk.Box()
		page4.set_border_width(10)
		page4.add(Gtk.Button.new_with_label('Verify a signed file'))
		notebook.append_page(page4, Gtk.Label('Verify'))

		builder = Gtk.Builder()
		builder.add_from_file("uifiles/menu.xml")
		# builder.connect_signals(Handler())

		appmenu = builder.get_object('appmenu')
		self.set_app_menu(appmenu)
		menubar = builder.get_object('menubar')
		self.set_menubar(menubar)

		self.window.add(window_split)
		self.window.show_all()

	def on_shutdown(self, data=None):
		#Add cleanups like file saves, logs, errors etc
		pass

	def on_delete_window(self, widget, data= None):
		print(widget.get_size())


if __name__ == '__main__':
	app = MainApp()
	app.run(sys.argv)
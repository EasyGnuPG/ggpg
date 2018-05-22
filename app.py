import os
import sys

import gi

gi.require_version('Gtk','3.0')
from gi.repository import Gtk, Gdk, Gio, GLib

class MainApp(Gtk.Application):

	def __init__(self, *args, **kwargs):

		super().__init__(application_id="apps.ggpg", flags=Gio.ApplicationFlags.FLAGS_NONE)
		self.connect("startup", self.on_startup)
		# self.connect("activate", self.on_activate)
		self.connect("shutdown", self.on_shutdown)

	# def run(self, argv):

	# 	self.app.run(argv)

	def on_startup(self, data=None):

		window = Gtk.ApplicationWindow(application=self, title="EasyGnuPG")
		window.set_default_size(640,480)
		window.set_border_width(10)
		self.add_window(window)

		window_split = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

		# statusbar = Gtk.StatusBar()
		# window_split.pack_end(statusbar, False, False, 0)

		center_split = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

		window_split.pack_end(center_split, False, False, 0)

		builder = Gtk.Builder()
		builder.add_from_file("uifiles/menus.xml")
		# builder.connect_signals(Handler())

		appmenu = builder.get_object('appmenu')
		self.set_app_menu(appmenu)
		menubar = builder.get_object('menubar')
		self.set_menubar(menubar)

		window.add(window_split)
		window.show_all()

	def on_shutdown(self, data=None):
		#Add cleanups
		pass


if __name__ == '__main__':
	app = MainApp()
	app.run(sys.argv)
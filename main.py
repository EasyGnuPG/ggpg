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

		#Principal Container Box
		window_split = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

		#StatusBar
		statusbar = Gtk.Statusbar()
		window_split.pack_end(statusbar, False, False, 0)
		
		#This will be changed when writing callbacks
		context = statusbar.get_context_id("status")
		statusbar.push(context,"In development")

		#Display Container
		center_split = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
		window_split.pack_end(center_split, True, True, 0)

		#Main Command Widgets
		notebook = Gtk.Notebook()
		notebook.set_vexpand(True)
		center_split.pack_end(notebook, True, True, 6)

		page1 = Gtk.HBox()
		page1_innerbox = Gtk.VBox()
		page1_vbox = Gtk.VBox(spacing=6)
		page1_innerbox.set_center_widget(page1_vbox)
		file_button1 = Gtk.Button("Choose File")
		file_button1.connect("clicked", self.on_file_clicked)
		page1_vbox.pack_start(file_button1, False, False, 0)
		page1_vbox.pack_start(Gtk.Button.new_with_label('Encrypt File'), False, False, 0)
		page1.set_border_width(10)
		page1.set_center_widget(page1_innerbox)
		notebook.append_page(page1, Gtk.Label('Encrypt'))
		page2 = Gtk.HBox()
		page2_innerbox = Gtk.VBox()
		page2_vbox = Gtk.VBox(spacing=6)
		page2_innerbox.set_center_widget(page2_vbox)
		page2_vbox.pack_start(Gtk.Button.new_with_label('Open an encrypted file to decrypt'), False, False, 0)
		page2.set_border_width(10)
		page2.set_center_widget(page2_innerbox)
		notebook.append_page(page2, Gtk.Label('Decrypt'))
		page3 = Gtk.HBox()
		page3_innerbox = Gtk.VBox()
		page3_vbox = Gtk.VBox(spacing=6)
		page3_innerbox.set_center_widget(page3_vbox)
		page3_vbox.pack_start(Gtk.Button.new_with_label('Sign a file'), False, False, 0)
		page3.set_border_width(10)
		page3.set_center_widget(page3_innerbox)
		notebook.append_page(page3, Gtk.Label('Signature'))
		page4 = Gtk.HBox()
		page4_innerbox = Gtk.VBox()
		page4_vbox = Gtk.VBox(spacing=6)
		page4_innerbox.set_center_widget(page4_vbox)
		page4_vbox.pack_start(Gtk.Button.new_with_label('Verify Signature'), False, False, 0)
		page4.set_border_width(10)
		page4.set_center_widget(page4_innerbox)
		notebook.append_page(page4, Gtk.Label('Verify'))

		#Scroll View
		scroll_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		center_split.pack_end(scroll_box, True, True, 0)

		scrolled_contacts = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
		scrolled_contacts.set_min_content_width(self.window.get_size()[0]/4)
		scrolled_contacts.set_max_content_width(self.window.get_size()[0]/4)
		scrolled_contacts.set_min_content_height(self.window.get_size()[1]*0.4)
		scrolled_contacts.set_max_content_height(self.window.get_size()[1]*0.4)

		scroll_box.pack_start(scrolled_contacts, True, True, 0)
		#TreeView for Contacts
		contacts_view = Gtk.TreeView()
		contacts_model = Gtk.ListStore(str)
		contacts_view.set_model(contacts_model)
		contacts = Gtk.TreeViewColumn("Contacts")
		contacts_view.append_column(contacts)
		contact_cell = Gtk.CellRendererText()
		contacts.pack_start(contact_cell, False)
		contacts.add_attribute(contact_cell, "text", 0)
		self.populate_contacts(contacts_model)

		scrolled_contacts.add(contacts_view)

		scrolled_keys = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
		scrolled_keys.set_min_content_width(self.window.get_size()[0]/4)
		scrolled_keys.set_max_content_width(self.window.get_size()[0]/4)
		scrolled_keys.set_min_content_height(self.window.get_size()[1]*0.4)
		scrolled_keys.set_max_content_height(self.window.get_size()[1]*0.4)

		scroll_box.pack_start(scrolled_keys, True, True, 0)
		#TreeView for Keys
		keys_view = Gtk.TreeView()
		keys_model = Gtk.ListStore(str)
		keys_view.set_model(keys_model)
		keys = Gtk.TreeViewColumn("Keys")
		keys_view.append_column(keys)
		key_cell = Gtk.CellRendererText()
		keys.pack_start(key_cell, False)
		keys.add_attribute(key_cell, "text", 0)
		self.populate_keys(keys_model)

		scrolled_keys.add(keys_view)

		builder = Gtk.Builder()
		builder.add_from_file("uifiles/menu.xml")
		# builder.connect_signals(Handler())

		appmenu = builder.get_object('appmenu')
		self.set_app_menu(appmenu)
		menubar = builder.get_object('menubar')
		self.set_menubar(menubar)

		#Key Check

		self.window.add(window_split)
		self.window.show_all()
		self.expired_key_checks()
		self.is_expiring_key_check()

	def on_shutdown(self, data=None):
		#Add cleanups like file saves, logs, errors etc
		pass

	def on_delete_window(self, widget, data= None):
		print(widget.get_size())

	def populate_contacts(self, model):
		#Shift to separate package later
		model.clear()
		for item in range(1,11):
			item_iter = model.append(["Contact " + str(item)])

	def populate_keys(self, model):
		#TODO : link to key_checks
		model.clear()
		for item in range(1,11):
			item_iter = model.append(["Key " + str(item)])

	def expired_key_checks(self):
		#Expired Keys check
		#TODO : Change this to a loop
		dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING,
			Gtk.ButtonsType.NONE, "EasyGnuPG")
		dialog.format_secondary_text("Your key has expried on 26/5/2018.")
		dialog.add_button("Renew Key", 200)
		dialog.add_button("Delete Key", 300)
		response = dialog.run()
		if response == 200:
			#TODO : Add function here
			print("Renew Key Selcted")
			dialog.destroy()
		else:
			#TODO : Add function here
			print("Delete Key Selcted")
			dialog.destroy()

	def is_expiring_key_check(self):
		#Check for keys that are about to expire
		#TODO : Merge the two checks in a single loop
		dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING,
			Gtk.ButtonsType.NONE, "EasyGnuPG")
		dialog.format_secondary_text("Your key is due expirey on 26/5/2018.")
		dialog.add_button("Renew Key", 200)
		dialog.add_button("Not Now", 300)
		response = dialog.run()
		if response == 200:
			#TODO : Add function here
			print("Renew Key Selcted")
			dialog.destroy()
		else:
			#TODO : Add function here
			print("Not Now Selcted")
			dialog.destroy()

	def on_file_clicked(self, button):

		dialog = Gtk.FileChooserDialog("Please choose a file", self.window,
        	Gtk.FileChooserAction.OPEN,
        	(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        		Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			print("Open clicked")
			print("File selected: " + dialog.get_filename())
		elif response == Gtk.ResponseType.CANCEL:
			print("Cancel clicked")

		dialog.destroy()





if __name__ == '__main__':
	app = MainApp()
	app.run(sys.argv)
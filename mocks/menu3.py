import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Tab Menu")
        self.set_border_width(10)

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        self.page1.add(Gtk.Button.new_with_label('Encrypt!'))
        self.notebook.append_page(self.page1, Gtk.Label('EGPG'))

        self.page2 = Gtk.Box()
        self.page2.set_border_width(10)
        self.page2.add(Gtk.Label('Configure and manage GPG'))
        self.notebook.append_page(self.page2, Gtk.Label('Settings')
        )

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
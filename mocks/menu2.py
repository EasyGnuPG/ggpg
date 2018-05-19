import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class StackWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Stack Menu")
        # self.set_default_size(640,480)
        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        #Change this value to make it a gradual transition
        stack.set_transition_duration(1)
        
        button = Gtk.Button.new_with_label("Encrypt!")
        stack.add_titled(button, "button", "Button")
        
        label = Gtk.Label()
        label.set_markup("<big>Configure</big>")
        stack.add_titled(label, "label", "Settings")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        vbox.pack_start(stack_switcher, True, True, 0)
        vbox.pack_start(stack, True, True, 0)

win = StackWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

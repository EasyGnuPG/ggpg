"""
A similar pattern can be used with the file size to show progress as the file is being encrypted.
Need to perform some time tests to see if its possible. (Maybe for larger files)
"""


import threading
import time
import gi

gi.require_version('Gtk','3.0')
from gi.repository import GLib, Gtk, GObject


def app_main():
    win = Gtk.Window(default_height=50, default_width=300)
    win.connect("destroy", Gtk.main_quit)

    progress = Gtk.ProgressBar(show_text=True)
    
    vbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    vbox.add(progress)
    win.add(vbox)

    def update_progess(i):
        progress.set_fraction(float(i/100))
        return False

    def example_target():
        for i in range(101):
            GLib.idle_add(update_progess, i)
            time.sleep(0.1)
        print("Viola! Thread is complete!")
        Gtk.main_quit()

    win.show_all()

    thread = threading.Thread(target=example_target)
    thread.daemon = True
    thread.start()


if __name__ == "__main__":
    app_main()
    Gtk.main()
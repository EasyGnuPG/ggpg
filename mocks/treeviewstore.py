import gi

gi.require_version('Gtk','3.0')
from gi.repository import Gtk

class Tree(Gtk.Window):
   
   def __init__(self):

      super(Tree, self).__init__()
      self.set_title("Tree View mock")
      self.set_size_request(400,200)
      vbox = Gtk.VBox(False, 5)
      
      # create a TreeStore with one string column to use as the model
      store = Gtk.TreeStore(str)
      
      # add row
      row1 = store.append(None, ['Office'])
      
      #add child rows
      store.append(row1,['Dan Smith'])
      store.append(row1,['Rob Williams'])
      store.append(row1,['John Arch'])
      
      # add another row
      row2 = store.append(None, ['College'])
      store.append(row2,['Tim'])
      store.append(row2,['Jimmy'])
      
      # create the TreeView using treestore
      treeview = Gtk.TreeView(store)
      tvcolumn = Gtk.TreeViewColumn('Contacts')
      treeview.append_column(tvcolumn)
		
      cell = Gtk.CellRendererText()
      tvcolumn.pack_start(cell, True)
      tvcolumn.add_attribute(cell, 'text', 0)
      vbox.add(treeview)
		
      self.add(vbox)
      self.connect("destroy", Gtk.main_quit)
      self.show_all()

Tree()
Gtk.main()
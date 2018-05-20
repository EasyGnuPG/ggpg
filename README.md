Ggpg

A GUI application based on EasyGnuPG

# Requirements and Dependencies

- Python 3
- gobject-introspection
- Gtk+ version 3 or higher. (Stable release at the time of development was 3.22.30)
- Development is primarily Linux centric, using Python-Gtk3+ (PyGObject and Gtk3+)

# Setup

1. Setup on common Linux distributions
2. Setting up a `Virtual Environemnt`

##Dependencies

### Ubuntu / Debian

```
$ sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

### Fedora

```
$ sudo dnf install pygobject3 python3-gobject gtk3
```

### Arch Linux

```
$ sudo pacman -S python-gobject gobject-introspection gtk3
```

Other distros should be similar, but feel free to send a pull request with
updated dependencies if needed.
Also, if you face any issues with the above setup please open an issue or feel free to send in a pull request.

### Virtual Environment

Setup virtual environment (Optional - recommended)
```
$ pip install virtualenv
$ mkdir ggpg
$ virtualenv venv
$ cd ggpg
$ source venv/bin/activate
```
Installations inside the virtual environment:
```
$ pip install pygobject
$ pip install vext
$ pip install vext.gi
```
# Running the Application

Clone the git repository:
```
$ git clone https://github.com/EasyGnuPG/ggpg.git --branch gui-devel --single-branch
$ cd ggpg
$ python main.py
```

# Contributing

This project is part of my Google Summer of Code project for 2018. I would appretiate any help I can get and it would be much appretiated even if you just try out the application as it is in being developed.

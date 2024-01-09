from Cocoa import NSApplication, NSApp, NSStatusBar, NSMenu, NSMenuItem, NSObject, NSVariableStatusItemLength, NSOpenPanel, NSFileHandlingPanelOKButton
from PyObjCTools import AppHelper
from Foundation import NSSearchPathForDirectoriesInDomains, NSApplicationSupportDirectory, NSUserDomainMask
import threading
import socket
import os
import json

from TC_Server import TC_Server

class MenuBarApp(NSObject):
    def applicationDidFinishLaunching_(self, aNotification):
        self.selected_paths = []  # to store the selected paths
        self.initialize_status_bar()
        self.initialize_menu()
        self.TC_Server = TC_Server()

        self.json_path = self.initialize_json_storage()
        self.read_paths_from_json()


    def initialize_json_storage(self):
        # Get the Application Support directory path
        app_support_dir = NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory, NSUserDomainMask, True)[0]

        # Create a directory for TerminalCassette
        terminal_cassette_dir = os.path.join(app_support_dir, 'TerminalCassette')
        if not os.path.exists(terminal_cassette_dir):
            os.mkdir(terminal_cassette_dir)

        # Define the JSON file path
        json_path = os.path.join(terminal_cassette_dir, 'usr_paths.json')

        # Create a new JSON file if it doesn't exist
        if not os.path.exists(json_path):
            with open(json_path, 'w') as f:
                json.dump([], f)

        return json_path

    def initialize_status_bar(self):
        self.statusbar = NSStatusBar.systemStatusBar()
        self.statusitem = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)
        self.statusitem.setTitle_("🎹")

    def initialize_menu(self):
        self.menu = NSMenu.alloc().init()

        self.ip_address_item = self.add_menu_item(self.menu, "IP Address: Not Found", None, "")
        self.update_ip_address()
        self.add_paths_submenu()
        self.add_menu_item(self.menu, "Quit", "terminate:", "")

        self.statusitem.setMenu_(self.menu)

    def update_ip_address(self):
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            self.ip_address_item.setTitle_("IP Address: {}".format(ip_address))
        except Exception as e:
            print("Error fetching IP:", e)

    def add_menu_item(self, menu, title, action, keyEquivalent):
        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(title, action, keyEquivalent)
        menu.addItem_(menuitem)
        return menuitem

    def add_paths_submenu(self):
        self.paths_menu = NSMenu.alloc().init()
        self.add_menu_item(self.paths_menu, "Add Path", "addPath:", "")
        self.populate_paths()

        paths_menu_item = self.add_menu_item(self.menu, "Paths", None, "")
        paths_menu_item.setSubmenu_(self.paths_menu)

    def populate_paths(self):
        for item in self.selected_paths:
            self.add_menu_item(self.paths_menu, item, None, "")

    def addPath_(self, sender):
        panel = NSOpenPanel.alloc().init()
        panel.setCanChooseFiles_(False)
        panel.setCanChooseDirectories_(True)
        panel.setAllowsMultipleSelection_(False)

        clicked = panel.runModal()

        if clicked == NSFileHandlingPanelOKButton:
            url = panel.URL()
            path = url.fileSystemRepresentation()
            path = path.decode('utf-8')
            self.selected_paths.append(path)

            # Clear existing menu items except the "Add Path" item
            for _ in range(self.paths_menu.numberOfItems() - 1):
                self.paths_menu.removeItemAtIndex_(1)

            self.populate_paths()  # Repopulate the menu
            self.TC_Server.Library.add_path(path)
            self.write_paths_to_json()

    def read_paths_from_json(self):
        try:
            with open(self.json_path, "r") as f:
                self.selected_paths = json.load(f)
                for path in self.selected_paths:
                    self.TC_Server.Library.add_path(path)
        except FileNotFoundError:
            self.selected_paths = []
        except json.JSONDecodeError:
            print("Error decoding JSON file.")
            self.selected_paths = []
        except Exception as e:
            print("Error reading from JSON:", e)
            self.selected_paths = []

        self.populate_paths()

    def write_paths_to_json(self):
        try:
            with open(self.json_path, "w") as f:
                json.dump(self.selected_paths, f)
        except Exception as e:
            print("Error writing to JSON:", e)



def start_menu():
    app = NSApplication.sharedApplication()
    delegate = MenuBarApp.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()

start_menu()

import os
import re
import sys

bad_names = {'.DS_Store', 'Audio Files', 'Samples'}
substrings = ['.logicx', '.Spotlight', '.Trashes']
bad_names_pattern = re.compile('|'.join(map(re.escape, substrings)))

def is_valid_dir(entry):
    if not entry.is_dir():
        return False
    if entry.name.startswith('.'):
        return False
    if bad_names_pattern.search(entry.name):
        return False
    if entry.name in bad_names:
        return False
    return True

def is_good_file(entry):
    if entry.is_dir():
        return False
    if bad_names_pattern.search(entry.name):
        return False
    if entry.name.startswith('.'):
        return False
    return entry.name.endswith(('.aif', '.mp3', '.wav'))


class Track:
    def __init__(self, title, path, scan=False):
        self.title = title
        self.path = path

        self.root = None
        self.current = None
        self.next = None

class Cassette:
    def __init__(self, title, path, scan=False):
        self.title = title
        self.path = path

        self.root = None # Root Track obj
        self.current = None # Current Track obj
        self.next = None # Next Track obj
        self.child = None

        self._music_extract(self.path)


# ------------------
# Helpers
# ------------------



        

# ------------------
# Setters
# ------------------

    def addTrack(self, name, path):
        newTrack = Track(name, path, True)
        if self.root == None:
            self.current = newTrack
            self.root = newTrack
        else:
            self.current.next = newTrack
            self.current = newTrack


    def _music_extract(self, path):
        for item in os.scandir(path):
            if is_valid_dir(item):
                self._music_extract(item)
            if is_good_file(item):
                self.addTrack(item.name, item.path)


                
# ------------------
# Getters
# ------------------


    def get_all_tra(self):
        i = self.root
        titles =[]
        while i is not None:
            titles.append(i)
            i = i.next
        return titles

    def get_track(self, title, track=None):
        if not track:
            track = self.root

        if track.title == title:
            return track
        if track.next == None:
            return None

class Collection:
    def __init__(self, title, path):
        self.title = title
        self.path = path

        self.root = None # Root Cassette obj
        self.current = None # Current Cassette obj
        self.next = None # Next Cassette obj

        self._scan_collection()


# ------------------
# Helpers
# ------------------



# ------------------
# Setters
# ------------------

    def addCassette(self, name, path):
        newCassette = Cassette(name, path, True)
        if self.root == None:
            self.current = newCassette
            self.root = newCassette
        else:
            self.current.next = newCassette
            self.current = newCassette

    def _scan_collection(self):
        for entry in os.scandir(self.path):
            if is_valid_dir(entry):
                self.addCassette(os.path.basename(entry.name), entry.path)


# ------------------
# Getters
# ------------------

    def root(self):
        return self.root

    def get_all_cass(self):
        i = self.root
        titles =[]
        while i is not None:
            titles.append(i)
            i = i.next
        return titles

    def get_cassette(self, title, cassette=None):
        if not cassette:
            cassette = self.root

        if cassette.title == title:
            return cassette
        if cassette.next == None:
            return None
  
        return self.get_cassette(title, cassette.next)


class Library:
     
    def __init__(self, title, paths=[]):
        self.title = title
        self.paths = []

        self.collections = []
        self.currentCollection = None
        self.currentCassette = None
        self.status = None

    def flag(self):
        if self.status[:4] == "ERR:":
            return True
        else:
            return False

    def add_path(self, path):
        self.scan_path(path)


    def scan_path(self, path):
        name = path.split("/")[-1]
        self.status = f"Adding {path} as '{name}'..."
        if os.path.isdir(path):
            newCollection = Collection(name, path)
            self.collections.append(newCollection)
            self.paths.append(path)
            print(f"ADded {name}")
            self.status = f"Added {name}"
        else:
            self.status = "ERR: " + path + " is not a valid directory"


    def total_scan(self):
        self.collections = []
        for path in self.paths:
            self.scan_path(path)
                


    def Collections(self):
        return self.collections

    def Cassettes(self, choice):
        for collection in self.collections:
            if collection.title == choice:
                self.currentCollection = collection
                return self.currentCollection.get_all_cass()
        return None

    def Tracks(self, choice):
        self.currentCassette = self.currentCollection.get_cassette(choice)

        return self.currentCassette.get_all_tra()





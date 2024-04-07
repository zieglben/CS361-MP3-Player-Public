import os
import threading
import time
import shutil
import os

from tkinter import *
from tkinter import filedialog
from tinytag import TinyTag
from shutil import copyfile
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Entry, Button
from random import sample 

current_directory = os.getcwd()
print(current_directory)

# Define the directory you want to add
dir_to_add = os.getcwd() + "/Python MP3 Starter/bin"

print (dir_to_add)

# Add the directory to the PATH
os.environ["PATH"] = dir_to_add + os.pathsep + os.environ["PATH"]
#os.environ.setdefault('PYTHON_VLC_LIB_PATH', dir_to_add)

import vlc



class PlaylistSetup:
    def __init__(self, root, window, music_player):
        self.music_player = music_player
        self.window = window
        self.root = root
        self.initialize_gui()
        self.LoadPlaylist()
        self.load_main_library()
        self.music_player.playlist_setup = self
        
    def initialize_gui(self):
        
        #Create Window for p_list
        self.Frame_p_list = Frame(root, bd=0, relief=RIDGE)
        self.Frame_p_list.place(x=0, y=100, width=300, height=250)
        
        #Create LoadPlaylist Button for p_list
        self.loadplaylist_btn = Button(root, text="Load Playlist", width=12, height=2, font=("times new roman",10, "bold"), 
                             fg="Black", bg="#21b3de", command=self.click_LoadPlaylist)
        self.loadplaylist_btn.grid(row=1, column=1, padx=3, pady=58)
        
        #Create removePlaylist Button for p_list
        self.removePlaylist_btn = Button(root, text="Remove Playlist", width=12, height=2, font=("times new roman", 10, "bold"), 
                                         fg="Black", bg="#21b3de", command=self.removePlaylist)
        self.removePlaylist_btn.grid(row=1, column=2, padx=3, pady=58)

        #Create createPlaylist Button for p_list
        self.createPlaylist_btn = Button(root, text="Create Playlist", width=12, height=2, font=("times new roman", 10, "bold"), 
                                         fg="Black", bg="#21b3de", command=self.Create_forum)
        self.createPlaylist_btn.grid(row=1, column=3, padx=3, pady=58)
        
        self.Scroll2 = Scrollbar(self.Frame_p_list)
        self.p_list = Listbox(self.Frame_p_list, width=100, font=("Times new roman", 20),
                   bg="#333333", fg="grey", selectbackground="lightblue", cursor="hand2",
                   bd=0, yscrollcommand=self.Scroll2.set)
        
        #Add styles
        self.Scroll2.config(command=self.p_list.yview)
        self.Scroll2.pack(side=RIGHT, fill=Y)
        self.p_list.pack(side=LEFT, fill=BOTH)

    def LoadPlaylist(self):
        self.Clear_P_list()
        #Remove everything from the Listbox
        path = os.path.join(current_directory, "p_list")
        if path:
            os.chdir(path)
            playlists = os.listdir(path)
            library_exists = True

            try:
                index = playlists.index(".Library")
            except ValueError:
                print("Error: Library not found")
                index = -1
                library_exists = False
        
            if index < 0:
                os.mkdir(".Library")
                os.chdir(".Library")
                os.mkdir("songs_list")
            
                with open("description.txt", "w") as f:
                    f.write("Main library of song")
            
                os.chdir(path)
            
            self.p_list.insert(END,"Library")
            
            playlists = os.listdir(path)
            index = playlists.index(".Library")
            
            i=0
            for playlist in playlists:
                if i != index:
                    self.p_list.insert(END, playlist)
                i += 1
            os.chdir(path)
                
    def Clear_P_list(self):
        total_playlists = self.p_list.size()
        i=0
        while (i != total_playlists):
            self.p_list.delete(0)
            i = i+1
    
    def load_main_library(self):
         #Refresh the Listboxes
        self.window.clearPlaylistWindow()
        self.window.clearDetailsWindow()

        selected = ".Library"
            
        path = os.path.join(current_directory, "p_list", str(selected))
        os.chdir(path)
     
        global is_playlist_open
        is_playlist_open = True
        global playlist_open
        playlist_open = path
     
        #Fill Playlist Listboxes with selected playlist
        songs = os.listdir(str(os.path.join(path, "songs_list")))
        #List out each song in playlist folder
        for song in songs:
           if song.endswith(".mp3"):
               self.window.playlist.insert(END, song)

        #Fill Details Window with selected playlist 
        self.window.details.insert(END,"Playlist: " + selected[1:])
        description_path = os.path.join(path, "description.txt")
        if os.path.exists(description_path):
            with open(description_path, "r") as f:
               fileInput = f.readlines()
               count = 0
               for line in fileInput:
                   self.window.details.insert(END, "Description: " + line)
               #print(fileInput)
    
    #Triggers when user clicks open playlist        
    def click_LoadPlaylist(self):
     
        #Refresh the Listboxes
        self.window.clearPlaylistWindow()
        self.window.clearDetailsWindow()
     
        selected = self.p_list.get(ACTIVE)
        if selected == "Library":
            selected = ".Library"
        path = os.path.join(current_directory, "p_list", str(selected))
        os.chdir(path)
     
        global is_playlist_open
        is_playlist_open = True
        global playlist_open
        playlist_open = path
     
        #Fill Playlist Listboxes with selected playlist
        songs = os.listdir(str(os.path.join(path, "songs_list")))
        #List out each song in playlist folder
        for song in songs:
           if song.endswith(".mp3"):
               self.window.playlist.insert(END, song)

        #Fill Details Window with selected playlist 
        if selected == ".Library":
            self.window.details.insert(END,"Playlist: " + selected[1:])
        else:
            self.window.details.insert(END, "Playlist: " + selected)
        description_path = os.path.join(path, "description.txt")
        if os.path.exists(description_path):
            with open(description_path, "r") as f:
               fileInput = f.readlines()
               count = 0
               for line in fileInput:
                   self.window.details.insert(END, "Description: " + line)
               #print(fileInput)

    
    #Starts Creates New Playlist
    def Create_forum(self):
        #Hide p_list controls
        self.loadplaylist_btn.grid_remove()
        self.removePlaylist_btn.grid_remove()
        self.createPlaylist_btn.grid_remove()
    
        #Create all forum buttons
        self.back_btn = Button(self.root, text="Back", width=15, height=2, font=("times new roman",12, "bold"), 
                               fg="Black", bg="#21b3de", command=lambda: self.Destroy_forum(self.submit_btn, self.Frame_p_list1, self.entry1, self.entry2, self.back_btn, self.prompt1, self.prompt2, FALSE))
        self.back_btn.place(x=155, y=50)
    
        self.Frame_p_list1 = Frame(self.root, bg= "#333333", bd=2, relief=RIDGE)
        self.Frame_p_list1.place(x=0, y=100, width=300, height=250)
    
        self.prompt1 = Button(self.root, text="Title:", width=4, height=1, font=("times new roman",8, "bold"), 
                              fg="white", bg="grey")
        self.prompt1.place(x=35, y=110)

        self.prompt2 = Button(self.root, text="Description (optional):", width=17, height=1, font=("times new roman",8, "bold"), 
                              fg="white", bg="grey")
        self.prompt2.place(x=35, y=160)

        self.entry1 = Text(self.root, width=29, font=("times new roman",10, "bold"))
        self.entry1.place(x=35, y=135, height = 20)

        self.entry2 = Text(self.root, width=29, font=("times new roman",10, "bold")) 
        self.entry2.place(x=35, y=185, height = 100)

        self.submit_btn = Button(self.root, text="Submit", width=22, height=1, font=("times new roman",12, "bold"), 
                                 fg="Black", bg="#21b3de", command=lambda: self.Destroy_forum(self.submit_btn,self.Frame_p_list1, self.entry1, self.entry2, self.back_btn, self.prompt1, self.prompt2, TRUE))
        self.submit_btn.place(x=75, y=300)
    
    #Deletes selected file from p_list  
    def removePlaylist(self):
        selected = self.p_list.get(ACTIVE)
        if selected == "Library":
            return
        path1 = os.path.join(current_directory, "p_list", str(selected))
        path2 = os.path.join(current_directory, "p_list")
        os.chdir(os.path.join(path1, "songs_list"))
    
        songs = os.listdir(os.path.join(path1, "songs_list"))

        #Remove out each song in playlist folder
        if (selected != "Library"):
            for song in songs:
                os.remove(str(song))  

            os.chdir(path1)
            os.rmdir("songs_list")
            os.remove("description.txt")
        
            os.chdir(path2)
            os.rmdir(str(selected))
        
            global is_playlist_open
            global playlist_open
            is_playlist_open = False
            playlist_open = None
        
            #Refreshes the windows
            self.LoadPlaylist()
            self.window.clearPlaylistWindow()
            self.window.clearDetailsWindow()
            self.load_main_library()
        
    #Catches faulty forum values and deletes forum elements
    def Destroy_forum(self, submit_btn,Frame_p_list1, entry1, entry2, back_btn, prompt1, prompt2, sub):
        #Require title value for submit button

        title_formVal = str(entry1.get("1.0", "end-1c"))
        description_formVal = str(entry2.get("1.0", "end-1c"))
    
        #Require title value for submit button
        if (sub == FALSE or (title_formVal != "" and title_formVal != "Library")):
        
            #Create a playlist when there is a title value
            if (sub == TRUE and title_formVal):
                file_name = entry1.get("1.0", "end-1c")  # Retrieve the content of entry1 without the trailing newline
                #file_path = r"C:\Users\camer\Desktop\CS-361-Scrum-Samurais-\Python MP3 Starter\p_list\\" + title_formVal
                file_path = os.path.join(current_directory, "p_list", title_formVal)
            
                os.makedirs(file_path)
                os.chdir(file_path)
                with open("description.txt", "w") as f:
                    f.write(description_formVal)
                
                #f = open ("description.txt", "w")
                f.close
            
                os.mkdir("songs_list")

                self.LoadPlaylist()

            #Unhide all buttons
            self.loadplaylist_btn.grid(row=0, column=1)
            self.removePlaylist_btn.grid(row=0, column=2)
            self.createPlaylist_btn.grid(row=0, column=3)
        
            #Bring back Open loadplaylist_btn Button
            
            submit_btn.destroy()
            Frame_p_list1.destroy()
            entry1.destroy()
            entry2.destroy()
            back_btn.destroy()
            prompt1.destroy()
            prompt2.destroy()
        else:
            if (title_formVal == ""):
                messagebox.showerror('Input Error', 'Error: No title value')
            if (title_formVal == "Library"):
                messagebox.showerror('Input Error', 'Error: Reserved title value: Library')
        
class Window:
    def __init__(self, root, music_player):
        self.root = root
        self.root.title("Samurai's MP3 Player")
        self.root.geometry("920x600+290+85")
        self.root.configure(background='#212121')
        self.root.resizable(False, False)
         
       
        self.BassLevelOld = DoubleVar()
        self.MidLevelOld = DoubleVar()
        self.TrebleLevelOld = DoubleVar()
        
        self.BassLevelOld = self.MidLevelOld = self.TrebleLevelOld = 0.00

        
        self.music_player = music_player
        self.initialize_gui()

        
    def initialize_gui(self):
        self.image_icon = PhotoImage(file=os.path.join(current_directory, "imgs", "logo.png"))
        self.root.iconphoto(False, self.image_icon)
        
    
        
        self.play_image = PhotoImage(file=os.path.join(current_directory, "imgs", "play.png")).subsample(2,2)
        self.pause_image = PhotoImage(file=os.path.join(current_directory, "imgs", "pause.png"))
        
        self.play_pause_button = Button(self.root, image=self.play_image, bg="#0f1a2b", bd=0,
                                        command=self.music_player.toggle_play_pause_button)
        self.play_pause_button.place(x=155, y=400)
        
        self.button_stop = PhotoImage(file=os.path.join(current_directory, "imgs", "stop.png"))
        Button(self.root, image=self.button_stop, bg="#0f1a2b", bd=0,
               command=self.music_player.stop_button_click).place(x=90, y=400)


        self.button_shuffle = PhotoImage(file=os.path.join(current_directory, "imgs", "shuffle.png"))
        Button(self.root, image=self.button_shuffle, bg="#0f1a2b", bd=0,
               command=self.music_player.shuffle_button_click).place(x=200, y=340)
        
        # Create an IntVar variable
        self.loop_state = IntVar()
        self.button_skip = PhotoImage(file=os.path.join(current_directory, "imgs", "skip.png"))
        Button(self.root, image=self.button_skip, bg="#0f1a2b", bd=0,
               command=self.music_player.skip_button_click).place(x=230, y=400)
        
        self.button_rewind = PhotoImage(file=os.path.join(current_directory, "imgs", "rewind.png"))
        Button(self.root, image=self.button_rewind, bg="#0f1a2b", bd=0, 
               command=self.music_player.rewind_button_click).place(x=15,y=400)#self.music_player.rewind_button_click)

        self.frame_music = Frame(self.root, bd=2, relief=RIDGE)
        self.frame_music.place(x=330, y=350, width=560, height=250)

        self.scroll = Scrollbar(self.frame_music)
        self.playlist = Listbox(self.frame_music, width=100, font=("Times new roman", 10),
                                bg="#333333", fg="grey", selectbackground="lightblue", cursor="hand2",
                                bd=0, yscrollcommand=self.scroll.set)

        self.scroll.config(command=self.playlist.yview)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.playlist.pack(side=LEFT, fill=BOTH)

        self.music_details = Frame(self.root, bd=2, relief=RIDGE)
        self.music_details.place(x=600, y=10, width=250, height=250)

        self.details = Listbox(self.music_details, width=240, font=("Times new roman", 10),
                               bg="#333333", fg="white", selectbackground="lightblue", cursor="hand2",
                               bd=0, yscrollcommand=self.scroll.set)
        

        self.details.pack(side=RIGHT, fill=Y)
        self.music_player.details = self.details
        self.music_player.playlist = self.playlist
        
        from tkinter import DoubleVar, HORIZONTAL, Scale

        # Create a DoubleVar variable
        BassLevel = DoubleVar()

        self.BASSinput = Scale(self.root, resolution=.01, from_=-20.0, to=20.00, bg="#333333", fg="grey", orient=HORIZONTAL)
        # Place Spinbox widget
        self.BASSinput.set(0.00)
        self.BASSinput.place(x=70, y=500, width=100, height=30)
        # Create Label widget
        self.BASSlabel = Label (self.root, text="Bass", font=("times new roman", 12, "bold"), bg="#333333", fg="white")
        self.BASSlabel.place(x=0, y=500)

        # Create Spinbox widget for numerical input
        self.MIDinput = Scale(self.root,resolution=.01, from_=-20.0, to=20.00 ,bg="#333333", fg="grey", orient=HORIZONTAL)
        # Place Spinbox widget
        self.MIDinput.set(0.00)
        self.MIDinput.place(x=70, y=530, width=100, height=30)
        # Create Label widget
        self.MIDlabel = Label (self.root, text="Medium", font=("times new roman", 12, "bold"), bg="#333333", fg="white")
        self.MIDlabel.place(x=0, y=530)

        # Create Spinbox widget for numerical input
        self.TREBLEinput = Scale(self.root,resolution=.01, from_=-20.0, to=20.00 , bg="#333333", fg="grey", orient=HORIZONTAL)
        # Place Spinbox widget
        self.TREBLEinput.set(0.00)
        self.TREBLEinput.place(x=70, y=560, width=100, height=30)
        # Create Label widget
        self.TREBLElabel = Label (self.root, text="Treble", font=("times new roman", 12, "bold"), bg="#333333", fg="white")
        self.TREBLElabel.place(x=0, y=560)

    

                # Add other widgets to the Frame...
                # ...




        self.add_music_button = Button(self.root, text="Open Folder", width=15, height=2,
                                       font=("times new roman", 12, "bold"),
                                       fg="Black", bg="#21b3de", command=self.music_player.add_music)
        self.add_music_button.place(x=350, y=300)
        
    def update_play_pause_button_image(self):
        if self.music_player.playing:
            self.play_pause_button.config(image=self.pause_image)
            self.play_pause_button.config(command=self.music_player.toggle_play_pause_button)
        else:
            self.play_pause_button.config(image=self.play_image)
            self.play_pause_button.config(command=self.music_player.unpause_button_click)
        #self.play_pause_button.config(image=PhotoImage(file=image_path))


    #Removes all song in Playlist Listbox
    def clearPlaylistWindow(self):
        i = 0
        while(i != self.playlist.size()):
            self.playlist.delete(0)
    
    def clearDetailsWindow(self):
        i=0
        while (i != self.details.size()):
            self.details.delete(i)
    
class MusicPlayer:
    def __init__(self, root):

        # creating a basic vlc instance
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()
        
        # Create an equalizer
        self.equalizer = vlc.libvlc_audio_equalizer_new_from_preset(0)
        self.now_playing_thread = None

        #self.stop_timer = False
        #self.pause_timer = False
        global stop_timer 
        global pause_timer
        
        stop_timer = False
        pause_timer = False
                
        global filter_clicked
        filter_clicked = False
        
        self.playing = False 
        
        self.playlist = None
        self.details = None
        self.window = None
        self.playlist_setup = None
        self.master = None
        self.p_list = None
        self.shuffle = 0
        self.filter_entry = Entry(root, width=30)
        self.filter_entry.place(x=585, y=320)
        
        self.filter_button = Button(root, text="Search", command=self.filter_songs)
        self.filter_button.place(x=500, y=320)#pack(pady=10)



    def getequalizerinput(self, frequency):
        bass_input_value = int(self.window.BASSinput.get())
        mid_input_value = int(self.window.MIDinput.get())
        treble_input_value = int(self.window.TREBLEinput.get())
        if frequency == 'bass':
            return bass_input_value
        elif frequency == 'mid':
            return mid_input_value
        elif frequency == 'treble':
            return treble_input_value


    def media_ended(self, event):
        
        location = self.playlist.get(ACTIVE)
        print (location)
        location_active = int(location[0])
        size_playlist = self.playlist.size()
        

        print("Location: ", location_active)
        print(self.playlist.curselection())

        #for item in self.playlist.curselection():
        #    location_active = int(item)

        if size_playlist <= location_active + 1:
            if self.window.loop_state.get() == 1:
                location_active = 0
            else:
                self.stop_button_click()
                return
        else:
            location_active += 1    

        self.window.music_player.playing = False
        self.playlist.selection_clear(0, size_playlist - 1)
        self.playlist.selection_set(location_active)
        self.window.update_play_pause_button_image()
        self.window.playlist.activate(location_active)
        self.play_music()
       
    def add_music(self):
        global is_playlist_open
        global playlist_open
        path = filedialog.askdirectory()
        
        if is_playlist_open:
            path2 = os.path.join(playlist_open, "songs_list")
        #print("Song path: ", path)        
        if path:
            os.chdir(path)
            songs = [song for song in os.listdir(path) if song.endswith(".mp3")]

            if is_playlist_open:
                for song in songs:
                    self.playlist.insert(END, song)
                    
                    source_path = os.path.join(path, song)
                    destination_path = path2
                    
                    try:
                        shutil.copy2(source_path, destination_path)
                        #print(f"Successfully copied {song} to {path2})
                    except Exception as e:
                        print(f"Error copying {song} to {path}: {e}")
            
            elif not is_playlist_open:
                for song in songs:
                    self.playlist.insert(END, song)

    def filter_songs(self):
        global filter_clicked
        if self.playlist_setup:
            keyword = self.filter_entry.get().lower()
            selected_playlist = self.playlist.get(ACTIVE)                

            if selected_playlist:
                try:
                    path = os.path.join(current_directory, "p_list", playlist_open)
                    #print("Selected Playlist Path:", path)

                    # Verify if the playlist path exists
                    if not os.path.exists(path):
                        print(f"Error: Playlist path does not exist: {path}")
                        return

                    songs_path = os.path.join(path, "songs_list")

                # Verify if the songs_list path exists
                    if not os.path.exists(songs_path):
                        print(f"Error: songs_list path does not exist: {songs_path}")
                        return

                    songs = [song for song in os.listdir(songs_path) if song.endswith(".mp3")]

                    # Clear existing songs in the playlist and details window
                    self.playlist_setup.window.clearPlaylistWindow()
                    #self.playlist_setup.window.clearDetailsWindow()

                    # Display filtered songs in the playlist and details window
                    filter_clicked = True
                    for song in songs:
                        song_path = os.path.join(songs_path, song)
                        if self.matches_criteria(song_path, keyword):
                            # self.playlist_setup.p_list.insert(END, song)

                            # Insert song details into the details window
                            #print("filtering Song:", song)
                            self.playlist.insert(END, song)
                            
                            #self.display_song_details(song_path)

                    # Fill Details Window with selected playlist
                    #self.playlist.insert(END, song)#f"Selected Playlist: {selected_playlist}")

                except Exception as e:
                    print(f"An error occurred: {e}")
            elif filter_clicked:
                self.playlist_setup.click_LoadPlaylist()
            else:
                print("No playlist selected.")
        else:
            print("Playlist setup not initialized.")
    
    def matches_criteria(self, song_path, keyword):
        # tag = TinyTag.get(song_path)

        # # Check if tag is not None before accessing attributes
        # if tag is not None:
        #     return any(keyword in (info.lower() if info else "") for info in [tag.album, tag.title, tag.artist])

        # # Handle the case where TinyTag couldn't extract metadata
        # return False
        tag = TinyTag.get(song_path)
        #print(f"Tag Information - Title: {tag.title}, Album: {tag.album}, Artist: {tag.artist}")
        result = any(keyword in (info.lower() if info else "") for info in [tag.album, tag.title, tag.artist])
        #print(f"Matches criteria: {result}")  # Add this line
        return result
    
    def display_song_details(self, song_path):
        tag = TinyTag.get(song_path)
        print("Tag", tag)
        if tag is not None:
            details = f"Title: {tag.title}, Album: {tag.album}, Artist: {tag.artist}"
            self.playlist_setup.window.details.insert(END, details)
        else:
            print(f"Could not extract metadata for {song_path}")

    
    def shuffle_songs(self):
        current_list = self.playlist.get(0, END)
        new_list = sample(current_list, len(current_list))
        
        self.playlist.delete(0, END)
        for item in new_list:
            self.playlist.insert(END, item)
        self.playlist.activate(0);
        self.play_music()
    def skip_track(self):
        location_active = -1
        size_playlist = self.playlist.size()

        for item in self.playlist.curselection():
            location_active = int(item)

        if size_playlist <= location_active + 1:
            location_active = 0
        else:
            location_active += 1
        
        self.window.play_pause_button.config(command=self.toggle_play_pause_button)
        self.playlist.selection_clear(0, size_playlist - 1)
        self.playlist.selection_set(location_active)
        self.playlist.activate(location_active)
        self.play_music()
        
    def rewind_track(self):
        current_position = self.mediaplayer.get_time() / 1000
        location_active = -1
        size_playlist = self.playlist.size()
        
        for item in self.playlist.curselection():
            location_active = int(item)
            
        if current_position >= 3.5:
            self.window.play_pause_button.config(command=self.toggle_play_pause_button)
            self.playlist.selection_clear(0, size_playlist - 1)
            self.playlist.selection_set(location_active)
            self.playlist.activate(location_active)
            self.play_music()
            return
        
        if size_playlist <= location_active - 1:
            location_active = 0
        elif location_active <= 0:
            location_active = size_playlist - 1
        else:
            location_active -= 1
        
        self.window.play_pause_button.config(command=self.toggle_play_pause_button)
        self.playlist.selection_clear(0, size_playlist - 1)
        self.playlist.selection_set(location_active)
        self.playlist.activate(location_active)
        self.play_music()

#returns filtered audio must get position before calling and set position 
# and new active audio after calling must also delete temp.wav and output.wav after calling
#sliders should be set from .1 to 2.0 for each frequency to reduce or double the frequency volume
    def set_equalizer(self):
        # Set the gain for each band (0 to 100).
        bass_input_value = int(self.window.BASSinput.get())
        mid_input_value = int(self.window.MIDinput.get())
        treble_input_value = int(self.window.TREBLEinput.get())

        if (self.window.BassLevelOld == bass_input_value and
            self.window.MidLevelOld == mid_input_value and
            self.window.TrebleLevelOld == treble_input_value):
            return

        self.window.BassLevelOld = bass_input_value
        self.window.MidLevelOld = mid_input_value
        self.window.TrebleLevelOld = treble_input_value

        # Set the amplification value for the bass (first few bands)
        for i in range(0, 4):
            self.equalizer.set_amp_at_index(bass_input_value, i)

        # Set the amplification value for the mid (middle bands)
        for i in range(4, 7):
            self.equalizer.set_amp_at_index(mid_input_value, i)

        # Set the amplification value for the treble (last few bands)
        for i in range(7, 10):
            self.equalizer.set_amp_at_index(treble_input_value, i)

        # Assign the equalizer to the media player
        self.mediaplayer.set_equalizer(self.equalizer)


    def play_music(self):
        global is_playlist_open
        global playlist_open
        
        if is_playlist_open:
            os.chdir(os.path.join(playlist_open, "songs_list"))

        self.playing = True
        music_name = self.playlist.get(ACTIVE)
        
        try:
            music_details = TinyTag.get(music_name)
        except Exception as e:
            print("error finding details: ", e)
            music_details.title = None
            music_details.album = None
            music_details.artist = None
            
        # Clear details
        for i in range(5):
            self.details.delete(0)
            
        # Print new song details
        if music_details.title != None:
            self.details.insert(END, "Now Playing: " + music_details.title)
        else:
            self.details.insert(END, "Now Playing: " + self.playlist.get(ACTIVE))
        
        if music_details.artist != None:
            self.details.insert(END, "By: " + music_details.artist)
        else:
            self.details.insert(END, "By: Unknown")
            
        if music_details.artist != None:
            self.details.insert(END, "Album: " + music_details.album)
        else:
            self.details.insert(END, "Album: Unknown")

        self.set_equalizer()
        
        self.current_media = self.instance.media_new(self.playlist.get(ACTIVE))
        self.mediaplayer.set_media(self.current_media)
        self.mediaplayer.play()
        
        music_duration_min = int(music_details.duration // 60)
        music_duration_sec = int(music_details.duration % 60)
        music_duration_display = str(music_duration_min) + ":"

        if music_duration_sec < 10:
            music_duration_display += "0" + str(music_duration_sec)
        else:
            music_duration_display += str(music_duration_sec)

        if music_details.artist != None: 
            self.details.insert(END, "Length: " + music_duration_display)
        else:
            time.sleep(0.1)
            music_time = self.mediaplayer.get_length() / 1000
            min = int(music_time // 60)
            sec = int(music_time % 60)
            duration_display = str(min) + ":"
            if sec < 10:
                duration_display += "0" + str(sec)
            else:
                duration_display += str(sec)
            
            self.details.insert(END, "Length: " + duration_display)
        if (self.now_playing_thread == None):
            now_playing_thread = threading.Thread(target=self.now_playing)
            now_playing_thread.start()

# should we put the equalizer change check and function call here 
#or do we create a seperate thread for it?
#I feel like .5 seconds will be changing the equalizer as the sliders are adjusted
    def now_playing(self):
        global stop_timer
        global pause_timer
        old_position = 0
        self.details.insert(END, "0:00")
        while True:
            
            time.sleep(.5)

            self.set_equalizer()
            
            current_position = self.mediaplayer.get_time() / 1000

            now_playing_min = int(current_position // 60)
            now_playing_sec = int(current_position % 60)
            now_playing_display = str(now_playing_min) + ":"

            if now_playing_sec < 10:
                now_playing_display += "0" + str(now_playing_sec)
            else:
                now_playing_display += str(now_playing_sec)
            
            if now_playing_min != -1 and now_playing_display != self.details.get(4):
                self.details.delete(4)
                self.details.insert(END, now_playing_display)
                #print("Song Time: ", now_playing_display)
            elif current_position == old_position:
                now_playing_min = -1
            
            if stop_timer == True:
                stop_timer = False
                self.details.delete(4)
                if pause_timer:
                    pause_timer = False
                break

            if pause_timer == True:
                while pause_timer:
                    time.sleep(.5)
                    if stop_timer:
                        self.details.delete(4)
                        break

            if now_playing_min == -1:
                self.details.delete(4)
                break
    
            old_position = current_position
            if self.mediaplayer.get_length() <= current_position * 1000 + 1000:
                self.stop_button_click()
                self.media_ended(None)            
            
    def toggle_play_pause_button(self):
        if self.playing:
            self.pause_button_click()
        else:
            self.play_button_click()
    
    def stop_button_click(self):
        global stop_timer
        global pause_timer
        if self.playing == True:
            #if not stop_timer:
            stop_timer = True

            self.playing = False
            self.window.update_play_pause_button_image()
            self.window.play_pause_button.config(command=self.toggle_play_pause_button)
            self.mediaplayer.stop()
            
        elif self.playing != True and pause_timer == True:
            stop_timer = True

            self.playing = False
            self.window.update_play_pause_button_image()
            self.window.play_pause_button.config(command=self.toggle_play_pause_button)
            self.mediaplayer.stop()
        else:
            return

    def play_button_click(self):
        global stop_timer
        stop_timer = False
        
        if self.mediaplayer.is_playing():
            self.stop_button_click()
            self.play_music()
        else:
            self.play_music()
        self.window.update_play_pause_button_image()
    
    def shuffle_button_click(self):
        global stop_timer
        stop_timer = True
        self.playing = True
        
        self.shuffle_songs()
        self.window.update_play_pause_button_image()
    def skip_button_click(self):
        global stop_timer
        self.playing = True
        self.skip_track()
        self.window.update_play_pause_button_image()
    
    def rewind_button_click(self):
        global stop_timer
        self.playing = True
        self.rewind_track()
        self.window.update_play_pause_button_image()

    def pause_button_click(self):
        global pause_timer
        pause_timer = True
        
        self.mediaplayer.pause()
        self.playing = False
        self.window.update_play_pause_button_image()

    def unpause_button_click(self):
        global pause_timer
        pause_timer = False
        
        self.mediaplayer.play()
        self.playing = True
        self.window.update_play_pause_button_image()

if __name__ == "__main__":
    global is_playlist_open
    global playlist_open
    is_playlist_open = False
    playlist_open = None
        
    current_directory = os.path.dirname(os.path.abspath(__file__))
    root = Tk()
    music_player = MusicPlayer(root)
    window = Window(root, music_player)
    music_player.window = window
    playlist = PlaylistSetup(root, window, music_player)    
    
    root.mainloop()

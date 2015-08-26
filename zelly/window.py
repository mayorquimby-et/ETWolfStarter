import json
from os import startfile,getcwd,chdir
from os.path import isfile, join, isdir
from re import compile
#import tkinter
import tkinter.filedialog
import tkinter.font
import tkinter.messagebox
import tkinter.simpledialog

from tkinter import END,W,E,N,S,NORMAL,DISABLED
from zelly.update import WolfStarterUpdater
from zelly.serverdata import ServerData
from zelly.constants import * # @UnusedWildImport

FONT       = None
Config = {
          # WINDOW AND FRAME
          'WINDOW_BACKGROUND'          : WHITE,
          'WINDOW_BORDER'              : BLACK,
          'NAVBAR_BACKGROUND'          : DARK_GREY,
          'HEADER_BACKGROUND'          : WHITE,
          'SERVERLIST_BACKGROUND'      : WHITE,
          'SERVERDATA_BACKGROUND'      : WHITE,
          'SERVERSTATUS_BACKGROUND'    : WHITE,
          'ENTRY_BACKGROUND'           : LIGHT_GREY,
          'ENTRY_FOREGROUND'           : BLACK,
          'LIST_SELECT_FORE'           : WHITE,
          'LIST_SELECT_BACK'           : DARK_GREY,
          'BUTTON_BACKGROUND'          : DARK_GREY,
          'BUTTON_FOREGROUND'          : WHITE,
          'A_BUTTON_BACKGROUND'        : LIGHT_GREY,
          'A_BUTTON_FOREGROUND'        : BLACK,
          'BROWSE_BUTTON_BACKGROUND'   : DARK_GREY,
          'BROWSE_BUTTON_FOREGROUND'   : WHITE,
          'BROWSE_A_BUTTON_BACKGROUND' : LIGHT_GREY,
          'BROWSE_A_BUTTON_FOREGROUND' : BLACK,
          'servers'                    : join(getcwd(), 'servers.json'),
          'launchmod'                  : True,
          'showbasepath'               : False,
          'showhomepath'               : False,
          'showcommandline'            : False,
          'windowborder'               : False,
          }

clean_pattern = compile("(\^.)") #(\^[\d\.\w=\-]?)
def cleanstr(s):
    """Cleans color codes from an W:ET String"""
    return clean_pattern.sub("", s)

class MenuButton(tkinter.Button):
    """Flat styled button to be placed on navbar
    parent -- Should be Navbar
    column -- Placement from left to right
    row    -- Should probably always be 0 but added just incase"""
    def __init__(self, parent=None, column=0, row=0,sticky=W,cnf={}, **kw):
        tkinter.Button.__init__(self, parent, cnf, **kw)
        self.parent = parent
        #logfile("MenuButton: Making button with background %s" % Config['BUTTON_BACKGROUND'])
        self.config(
                    background=Config['BUTTON_BACKGROUND'],
                    foreground=Config['BUTTON_FOREGROUND'],
                    activebackground=Config['A_BUTTON_BACKGROUND'],
                    activeforeground=Config['A_BUTTON_FOREGROUND'],
                    borderwidth=0,
                    width=5,
                    height=1,
                    relief="flat",
                    padx=12,
                    cursor="hand2",
                )
        self.sticky = sticky
        self.row    = row
        self.column = column
        self.hide()
    def show(self):
        """Adds it self to the navbar grid"""
        self.grid(row=self.row, column=self.column, sticky=self.sticky)
    def hide(self):
        """Hides itself from the grid"""
        self.grid_forget()

class BrowseButton(tkinter.Button):
    """File browse button share similar style to MenuButtons""" 
    def __init__(self, master=None, dir_var=None, cnf={}, **kw):
        tkinter.Button.__init__(self, master, cnf, **kw)
        self.parent = master
        self.config(background=Config['BROWSE_BUTTON_BACKGROUND'],
                    foreground=Config['BROWSE_BUTTON_FOREGROUND'],
                    activebackground=Config['BROWSE_A_BUTTON_BACKGROUND'],
                    activeforeground=Config['BROWSE_A_BUTTON_FOREGROUND'],
                    borderwidth=0,
                    relief="flat",
                    padx=5,
                    cursor="hand2")

class NavBar(tkinter.Frame):
    """Flat styled menu bar should contain only MenuButtons"""
    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)
        self.MainWindow = parent
        logfile("LOADING...    NAVBAR")
        self.config(background=Config['NAVBAR_BACKGROUND'] , cursor="hand1")
        
        self.button_open     = MenuButton(self , BUTTON_OPEN     , text="Open..."    , command=self.MainWindow.openfile)
        self.button_saveas   = MenuButton(self , BUTTON_SAVE     , text="Save..."    , command=self.MainWindow.saveasfile)
        self.button_issues   = MenuButton(self , BUTTON_ISSUE    , 0 , E , text="Issue..."   , command=self.issue)
        self.button_donate   = MenuButton(self , BUTTON_DONATE   , 0 , E , text="Donate..."   , command=self.donate)
        self.button_minimize = MenuButton(self , BUTTON_MINIMIZE , 0 , E , text="Minimize"   , command=self.minimize)
        self.button_quit     = MenuButton(self , BUTTON_QUIT     , 0 , E , text="Quit"       , command=self.MainWindow.quit)
        self.button_update   = MenuButton(self , BUTTON_UPDATE   , 0 , E , text="Update"     , command=self.updatelink)
        self.button_settings = MenuButton(self , BUTTON_SETTINGS , 0 , E , text="Settings"   , command=self.settings)
        self.button_logwin   = MenuButton(self , BUTTON_TEST     , 0 , E , text="LogWindow"  , command=self.logwindow)
        self.versionlabel    = tkinter.Label(self,
                                     background=Config['BUTTON_BACKGROUND'],
                                     foreground=Config['BUTTON_FOREGROUND'],
                                     relief="flat",
                                     borderwidth=0,
                                     width=5,
                                     height=1,
                                     padx=12,
                                     text=WOLFSTARTER_VERSION
                                     )
        self.versionlabel.grid(column=LABEL_VERSION,row=0,sticky=E)
        self.columnconfigure(BUTTON_SETTINGS,weight=1)
        
        self.button_open.show()
        self.button_saveas.show()
        self.button_settings.show()
        self.button_issues.show()
        self.button_donate.show()
        if not Config['windowborder']:
            self.button_minimize.show()
            self.button_quit.show()
        self.button_logwin.show()
        def checkupdate():
            self.Updater = WolfStarterUpdater()
            if self.Updater.check():
                self.button_update.show()
            else:
                del self.Updater
        self.after(500, checkupdate)
        
        self.grid(column=FRAME_NAVBAR[0], row=FRAME_NAVBAR[0], sticky=N + W + E + S)
    def logwindow(self):
        LogWindow(self.MainWindow)
    def minimize(self):
        self.MainWindow.minimized = True
        self.MainWindow.overrideredirect(False)
        self.MainWindow.iconify()
    def issue(self):
        self.MainWindow.overrideredirect(False)
        self.MainWindow.focus_ignore = True
        ok = tkinter.messagebox.askyesno("Open issues page", "Would you like to go to the github issues page?",parent=self.MainWindow)
        self.MainWindow.focus_ignore = False
        self.MainWindow.overrideredirect(True)
        if ok:
            startfile(r"https://github.com/Zelly/ETWolfStarter/issues/new")
    def donate(self):
        print("Opening donate dialog")
        self.MainWindow.overrideredirect(False)
        self.MainWindow.focus_ignore = True
        ok = tkinter.messagebox.askyesno(title="Open donate page", message="Would you like to go to the paypal donate page?",parent=self.MainWindow)
        self.MainWindow.focus_ignore = False
        self.MainWindow.overrideredirect(True)
        if ok:
            startfile(r"https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=45BP8LRVZW7JC&lc=US&item_name=Zelly%20Github%20Donate&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted")
    def updatelink(self):
        print("Opening update dialog")
        self.MainWindow.overrideredirect(False)
        self.MainWindow.focus_ignore = True
        ok = tkinter.messagebox.askyesno(title="Open update download page", message="Would you like to go to the update download page?",parent=self.MainWindow)
        self.MainWindow.focus_ignore = False
        self.MainWindow.overrideredirect(True)
        if ok:
            startfile(self.Updater.getreleaseurl())
            exit(0) # Close because they can't update with it open
    def settings(self):
        self.MainWindow.ServerFrame.closewindow()
        Settings(self.MainWindow) # Mainframe here?

class HeaderFrame(tkinter.Frame):
    """Frame containing global parameters to be applied to all servers by default"""
    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)
        self.ServerFrame = parent
        
        self.config(background=Config['HEADER_BACKGROUND'])
        
        # Global ETPath
        self.etpath_var    = tkinter.StringVar()
        self.etpath_label  = tkinter.Label(self, text="ET: ", font=FONT, background=Config['HEADER_BACKGROUND'])
        self.etpath_entry  = tkinter.Entry(self, font=FONT, background=Config['ENTRY_BACKGROUND'], foreground=Config['ENTRY_FOREGROUND'], textvariable=self.etpath_var)
        self.etpath_browse = BrowseButton(self, text="Browse...", command=lambda :self.ServerFrame.getfilepath(self.etpath_var, self.updateconfig))
        
        self.etpath_entry.bind(sequence='<KeyRelease>', func=self.updateconfig)
        self.etpath_label.grid(  row=0 , column=0 , sticky=N + W)
        self.etpath_entry.grid(  row=0 , column=1 , sticky=N + W + E)
        self.etpath_browse.grid( row=0 , column=2 , sticky=N + E)
        
        # Global fs_basepath
        self.fs_basepath_var    = tkinter.StringVar()
        self.fs_basepath_label  = tkinter.Label(self, text="fs_basepath: ", font=FONT, background=Config['HEADER_BACKGROUND'])
        self.fs_basepath_entry  = tkinter.Entry(self, font=FONT, background=Config['ENTRY_BACKGROUND'], foreground=Config['ENTRY_FOREGROUND'], textvariable=self.fs_basepath_var)
        self.fs_basepath_browse = BrowseButton(self, text="Browse...", command=lambda :self.ServerFrame.getpath(self.fs_basepath_var, self.updateconfig))
        
        if Config['showbasepath']:
            self.fs_basepath_entry.bind(  sequence='<KeyRelease>', func=self.updateconfig)
            self.fs_basepath_label.grid(  row=1 , column=0 , sticky=N + W)
            self.fs_basepath_entry.grid(  row=1 , column=1 , sticky=N + W + E)
            self.fs_basepath_browse.grid( row=1 , column=2 , sticky=N + E)
        
        # Global fs_homepath
        self.fs_homepath_var    = tkinter.StringVar()
        self.fs_homepath_label  = tkinter.Label(self, text="fs_homepath: ", font=FONT, background=Config['HEADER_BACKGROUND'])
        self.fs_homepath_entry  = tkinter.Entry(self, font=FONT, background=Config['ENTRY_BACKGROUND'], foreground=Config['ENTRY_FOREGROUND'], textvariable=self.fs_homepath_var)
        self.fs_homepath_browse = BrowseButton(self, text="Browse...", command=lambda :self.ServerFrame.getpath(self.fs_homepath_var, self.updateconfig))
        
        if Config['showhomepath']:
            self.fs_homepath_entry.bind(sequence='<KeyRelease>', func=self.updateconfig)
            self.fs_homepath_label.grid(  row=2 , column=0 , sticky=N + W)
            self.fs_homepath_entry.grid(  row=2 , column=1 , sticky=N + W + E)
            self.fs_homepath_browse.grid( row=2 , column=2 , sticky=N + E)
        
        # Global Parameters
        self.parameters_var   = tkinter.StringVar()
        self.parameters_label = tkinter.Label(self, text="Parameters: ", font=FONT, background=Config['HEADER_BACKGROUND'])
        self.parameters_entry = tkinter.Entry(self, font=FONT, background=Config['ENTRY_BACKGROUND'], foreground=Config['ENTRY_FOREGROUND'], textvariable=self.parameters_var)
        
        self.parameters_entry.bind(sequence='<KeyRelease>', func=self.updateconfig)
        self.parameters_label.grid(row=3, column=0, sticky=N + W)
        self.parameters_entry.grid(row=3, column=1, sticky=N + W + E)
        
        if self.ServerFrame.MainWindow.ServerData.fs_basepath != None: self.fs_basepath_var.set(self.ServerFrame.MainWindow.ServerData.fs_basepath)
        if self.ServerFrame.MainWindow.ServerData.fs_homepath != None: self.fs_homepath_var.set(self.ServerFrame.MainWindow.ServerData.fs_homepath)
        if self.ServerFrame.MainWindow.ServerData.parameters != None: self.parameters_var.set(self.ServerFrame.MainWindow.ServerData.parameters)
        if self.ServerFrame.MainWindow.ServerData.ETPath != None: self.etpath_var.set(self.ServerFrame.MainWindow.ServerData.ETPath)
        
        self.grid_columnconfigure(1, minsize=400)
    def show(self):
        self.grid(row=FRAME_HEADER[0], column=FRAME_HEADER[1], sticky=N + W + E)
    def hide(self):
        self.grid_forget()
    def updateconfig(self, e):
        if self.fs_basepath_var.get() != None: self.ServerFrame.MainWindow.ServerData.fs_basepath = self.fs_basepath_var.get()
        if self.fs_homepath_var.get() != None: self.ServerFrame.MainWindow.ServerData.fs_homepath = self.fs_homepath_var.get()
        if self.etpath_var.get() != None: self.ServerFrame.MainWindow.ServerData.ETPath = self.etpath_var.get()
        if self.parameters_var.get() != None: self.ServerFrame.MainWindow.ServerData.parameters = self.parameters_var.get()

class ServerListFrame(tkinter.Frame):
    """Contains the server list"""
    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)
        self.ServerFrame = parent
        
        self.config(background=Config['SERVERLIST_BACKGROUND'], padx=5, pady=5)
        
        # Server List Titles
        self.servers_label = tkinter.Label(self, text="Title", font=FONT, background=Config['SERVERLIST_BACKGROUND'])
        self.servers       = tkinter.Listbox(self, width=25, relief="flat",
                                     borderwidth=0,
                                     font=FONT,
                                     selectbackground=Config['LIST_SELECT_BACK'],
                                     selectborderwidth=0,
                                     selectforeground=Config['LIST_SELECT_FORE'],
                                     exportselection=0,
                                     activestyle="none")
        
        self.servers.bind("<<ListboxSelect>>", self.selectserver)
        self.servers.bind("<Double-Button-1>", self.ServerFrame.joinserver)
        self.servers.bind("<MouseWheel>", self.OnMouseWheel)
        self.servers_label.grid(row=0, column=0, sticky=N + W + E)
        self.servers.grid(row=1, column=0, sticky=N + W + E)
        
        # Server Map
        self.servermap_label = tkinter.Label(self, text="Map", font=FONT, background=Config['SERVERLIST_BACKGROUND'])
        self.servermap       = tkinter.Listbox(self, width=10, relief="flat",
                                       borderwidth=0,
                                       font=FONT,
                                       selectbackground=Config['LIST_SELECT_BACK'],
                                       selectborderwidth=0,
                                       selectforeground=Config['LIST_SELECT_FORE'],
                                       exportselection=0,
                                       activestyle="none")
        
        self.servermap.bind("<<ListboxSelect>>", self.selectserver)
        self.servermap.bind("<Double-Button-1>", self.ServerFrame.joinserver)
        self.servermap.bind("<MouseWheel>", self.OnMouseWheel)
        self.servermap_label.grid(row=0, column=1, sticky=N + W + E)
        self.servermap.grid(row=1, column=1, sticky=N + W + E)
        
        # Server Players
        self.serverplayers_label = tkinter.Label(self, text="Players", font=FONT, background=Config['SERVERLIST_BACKGROUND'])
        self.serverplayers       = tkinter.Listbox(self, width=10, relief="flat",
                                           borderwidth=0,
                                           font=FONT,
                                           selectbackground=Config['LIST_SELECT_BACK'],
                                           selectborderwidth=0,
                                           selectforeground=Config['LIST_SELECT_FORE'],
                                           exportselection=0,
                                           activestyle="none")
        
        self.serverplayers.bind("<<ListboxSelect>>", self.selectserver)
        self.serverplayers.bind("<Double-Button-1>", self.ServerFrame.joinserver)
        self.serverplayers.bind("<MouseWheel>", self.OnMouseWheel)
        self.serverplayers_label.grid(row=0, column=2, sticky=N + W + E)
        self.serverplayers.grid(row=1, column=2, sticky=N + W + E)
        
        # Server Ping
        self.serverping_label = tkinter.Label(self, text="Ping", font=FONT, background=Config['SERVERLIST_BACKGROUND'])
        self.serverping       = tkinter.Listbox(self, width=10, relief="flat",
                                        borderwidth=0,
                                        font=FONT,
                                        selectbackground=Config['LIST_SELECT_BACK'],
                                        selectborderwidth=0,
                                        selectforeground=Config['LIST_SELECT_FORE'],
                                        exportselection=0,
                                        activestyle="none")
        
        self.serverping.bind("<<ListboxSelect>>", self.selectserver)
        self.serverping.bind("<Double-Button-1>", self.ServerFrame.joinserver)
        self.serverping.bind("<MouseWheel>", self.OnMouseWheel)
        self.serverping_label.grid(row=0, column=3, sticky=N + W + E)
        self.serverping.grid(row=1, column=3, sticky=N + W + E)
        
        self.grid_columnconfigure(0, weight=1)
    def show(self):
        self.grid(row=FRAME_SERVERLIST[0], column=FRAME_SERVERLIST[1], sticky=N + W)
    def hide(self):
        self.grid_forget()
    def clear(self):
        self.servers.selection_clear(0, END)
        self.servers.delete(0, END)
        self.servermap.selection_clear(0, END)
        self.servermap.delete(0, END)
        self.serverplayers.selection_clear(0, END)
        self.serverplayers.delete(0, END)
        self.serverping.selection_clear(0, END)
        self.serverping.delete(0, END)
    def add(self,Server=None):
        if not Server: return
        self.servers.insert(END       , Server['title'])
        self.servermap.insert(END     , Server['map'])
        self.serverplayers.insert(END , Server['players'])
        self.serverping.insert(END    , Server['ping'])
    def select(self,selectid=None):
        if selectid == None: return
        self.servers.select_clear(0, END)
        self.servermap.select_clear(0, END)
        self.serverplayers.select_clear(0, END)
        self.serverping.select_clear(0, END)
        
        self.servers.select_set(selectid)
        self.servermap.select_set(selectid)
        self.serverplayers.select_set(selectid)
        self.serverping.select_set(selectid)
    def get(self):
        if self.servers.curselection(): return self.servers.curselection()[0]
        if self.servermap.curselection(): return self.servermap.curselection()[0]
        if self.serverping.curselection(): return self.serverping.curselection()[0]
        if self.serverplayers.curselection(): return self.serverplayers.curselection()[0]
        return None
    def getfull(self):
        if self.servers.curselection(): return self.servers.curselection()
        if self.servermap.curselection(): return self.servermap.curselection()
        if self.serverping.curselection(): return self.serverping.curselection()
        if self.serverplayers.curselection(): return self.serverplayers.curselection()
        return None
    def OnMouseWheel(self, event):
        delta = event.delta*-1
        self.servers.yview("scroll", delta,"units")
        self.servermap.yview("scroll", delta,"units")
        self.serverping.yview("scroll", delta,"units")
        self.serverplayers.yview("scroll", delta,"units")
        return "break"
    def selectserver(self, e):
        selectid = self.get()
        if selectid == None: return
        
        Server = self.ServerFrame.MainWindow.ServerData.Servers[selectid]
        if not Server:
            logfile("selectserver: Error selecting server %d" % selectid)
            return
        
        logfile("selectserver: Selecting server %s" % Server['title'])

        self.select((selectid,))
        self.ServerFrame.ServerDataFrame.set(Server)
        
        self.ServerFrame.button_joinserver.show()
        self.ServerFrame.button_removeserver.show()
        self.ServerFrame.serverstatus()

        command_info = self.ServerFrame.getcommandline(selectid)
        if command_info and command_info[0]:
            self.ServerFrame.NoticeLabel.set(command_info[0].replace('+','\n+'))
            if Config['showcommandline']:
                self.ServerFrame.NoticeLabel.show()
            else:
                self.ServerFrame.NoticeLabel.hide()

class ServerDataFrame(tkinter.Frame):
    """Frame contains all server related frames"""
    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)
        self.ServerFrame = parent
        
        self.config(background=Config['SERVERDATA_BACKGROUND'])
        
        # Server title
        self.servertitle_var   = tkinter.StringVar()
        self.servertitle_label = tkinter.Label(self, text="Title: ", font=FONT, background=Config['SERVERDATA_BACKGROUND'])
        self.servertitle_entry = tkinter.Entry(self, font=FONT, background=Config['ENTRY_BACKGROUND'], foreground=Config['ENTRY_FOREGROUND'], textvariable=self.servertitle_var)
        
        self.servertitle_entry.bind( sequence='<KeyRelease>', func=self.updateserver)
        self.servertitle_label.grid( row=0, column=0, sticky=N + W)
        self.servertitle_entry.grid( row=0, column=1, sticky=N + W + E)
        
        # Server Password
        self.serverpassword_var   = tkinter.StringVar()
        self.serverpassword_label = tkinter.Label(self, text="Password: ", font=FONT, background=Config['SERVERDATA_BACKGROUND'])
        self.serverpassword_entry = tkinter.Entry(self, font=FONT, background=Config['ENTRY_BACKGROUND'], foreground=Config['ENTRY_FOREGROUND'], textvariable=self.serverpassword_var)
        
        self.serverpassword_entry.bind( sequence='<KeyRelease>', func=self.updateserver)
        
        # Server address
        self.serveraddress_var   = tkinter.StringVar()
        self.serveraddress_label = tkinter.Label(self, text="Address: ", font=FONT, background=Config['SERVERDATA_BACKGROUND'])
        self.serveraddress_entry = tkinter.Entry(self, font=FONT, background=Config['ENTRY_BACKGROUND'], foreground=Config['ENTRY_FOREGROUND'], textvariable=self.serveraddress_var)
        
        self.serveraddress_entry.bind( sequence='<KeyRelease>', func=self.updateserver)
        self.serveraddress_label.grid( row=2, column=0, sticky=N + W)
        self.serveraddress_entry.grid( row=2, column=1, sticky=N + W + E)
        
        # Server ETPath
        self.serveretpath_var    = tkinter.StringVar()
        self.serveretpath_label  = tkinter.Label(self, text="ET: ", font=FONT, background=Config['SERVERDATA_BACKGROUND'])
        self.serveretpath_entry  = tkinter.Entry(self, font=FONT, background=Config['ENTRY_BACKGROUND'], foreground=Config['ENTRY_FOREGROUND'], textvariable=self.serveretpath_var)
        self.serveretpath_browse = BrowseButton(self, text="Browse...", command=lambda :self.ServerFrame.getfilepath(self.serveretpath_var, self.updateserver))
        
        self.serveretpath_entry.bind(  sequence='<KeyRelease>', func=self.updateserver)
        self.serveretpath_label.grid(  row=3, column=0, sticky=N + W)
        self.serveretpath_entry.grid(  row=3, column=1, sticky=N + W + E)
        self.serveretpath_browse.grid( row=3, column=2, sticky=N + E)
        
        # Server fs_basepath
        self.serverfs_basepath_var    = tkinter.StringVar()
        self.serverfs_basepath_label  = tkinter.Label(self, text="fs_basepath: ", font=FONT, background=Config['SERVERDATA_BACKGROUND'])
        self.serverfs_basepath_entry  = tkinter.Entry(self, font=FONT, background=Config['ENTRY_BACKGROUND'], foreground=Config['ENTRY_FOREGROUND'], textvariable=self.serverfs_basepath_var)
        self.serverfs_basepath_browse = BrowseButton(self, text="Browse...", command=lambda :self.ServerFrame.getpath(self.serverfs_basepath_var, self.updateserver))
        
        if Config['showbasepath']:
            self.serverfs_basepath_entry.bind(  sequence='<KeyRelease>', func=self.updateserver)
            self.serverfs_basepath_label.grid(  row=4, column=0, sticky=N + W)
            self.serverfs_basepath_entry.grid(  row=4, column=1, sticky=N + W + E)
            self.serverfs_basepath_browse.grid( row=4, column=2, sticky=N + E)
        
        # Server fs_homepath
        self.serverfs_homepath_var    = tkinter.StringVar()
        self.serverfs_homepath_label  = tkinter.Label(self, text="fs_homepath: ", font=FONT, background=Config['SERVERDATA_BACKGROUND'])
        self.serverfs_homepath_entry  = tkinter.Entry(self, font=FONT, background=Config['ENTRY_BACKGROUND'], foreground=Config['ENTRY_FOREGROUND'], textvariable=self.serverfs_homepath_var)
        self.serverfs_homepath_browse = BrowseButton(self, text="Browse...", command=lambda :self.ServerFrame.getpath(self.serverfs_homepath_var, self.updateserver))
        
        if Config['showhomepath']:
            self.serverfs_homepath_entry.bind(  sequence='<KeyRelease>', func=self.updateserver)
            self.serverfs_homepath_label.grid(  row=5, column=0, sticky=N + W)
            self.serverfs_homepath_entry.grid(  row=5, column=1, sticky=N + W + E)
            self.serverfs_homepath_browse.grid( row=5, column=2, sticky=N + E)
        
        # Server extra parameters
        self.serverparams_var   = tkinter.StringVar()
        self.serverparams_label = tkinter.Label(self, text="Parameters: ", font=FONT, background=Config['SERVERDATA_BACKGROUND'])
        self.serverparams_entry = tkinter.Entry(self, font=FONT, background=Config['ENTRY_BACKGROUND'], foreground=Config['ENTRY_FOREGROUND'], textvariable=self.serverparams_var)
        
        self.serverparams_entry.bind( sequence='<KeyRelease>', func=self.updateserver)
        self.serverparams_label.grid( row=6, column=0, sticky=N + W)
        self.serverparams_entry.grid( row=6, column=1, sticky=N + W + E)
        self.grid_columnconfigure(1, minsize=400)
    def show(self):
        self.grid(row=FRAME_SERVERDATA[0], column=FRAME_SERVERDATA[1], sticky=N)
    def hide(self):
        self.grid_forget()
    def showpassword(self):
        self.serverpassword_label.grid(row=1, column=0, sticky=N + W)
        self.serverpassword_entry.grid(row=1, column=1, sticky=N + W + E)
    def hidepassword(self):
        self.serverpassword_label.grid_forget()
        self.serverpassword_entry.grid_forget()
    def set(self,Server=None):
        if not Server: return
        self.servertitle_var.set(Server['title'])
        self.serveraddress_var.set(Server['address'])
        self.serverpassword_var.set(Server['password'])
        self.serverparams_var.set(Server['parameters'])
        self.serverfs_basepath_var.set(Server['fs_basepath'])
        self.serverfs_homepath_var.set(Server['fs_homepath'])
        self.serveretpath_var.set(Server['ETPath'])
        self.show()
    def updateserver(self, e):
        selectid = self.ServerFrame.ServerListFrame.get()
        if selectid == None: return
        Server = self.ServerFrame.MainWindow.ServerData.Servers[selectid]
        if not Server:
            logfile("updateserver: Error updating server status %d" % selectid)
            return
        logfile("updateserver: Updating %s at %d" % ( Server['title'] , selectid ) )
        
        if self.servertitle_var.get() != None: Server['title'] = self.servertitle_var.get()
        if self.serveraddress_var.get() != None: Server['address'] = self.serveraddress_var.get()
        if self.serverpassword_var.get() != None: Server['password'] = self.serverpassword_var.get()
        if self.serverparams_var.get() != None: Server['parameters'] = self.serverparams_var.get()
        if self.serverfs_basepath_var.get() != None: Server['fs_basepath'] = self.serverfs_basepath_var.get()
        if self.serverfs_homepath_var.get() != None: Server['fs_homepath'] = self.serverfs_homepath_var.get()
        if self.serveretpath_var.get() != None: Server['ETPath'] = self.serveretpath_var.get()
        self.ServerFrame.refresh_list(selectid)
    def clear(self):
        self.servertitle_var.set('')
        self.serveraddress_var.set('')
        self.serverpassword_var.set('')
        self.serverparams_var.set('')
        self.serverfs_basepath_var.set('')
        self.serverfs_homepath_var.set('')
        self.serveretpath_var.set('')
    
class ServerStatusFrame(tkinter.Frame):
    """Contains actual serverdata information such as players and cvars"""
    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)
        self.ServerFrame = parent
        
        self.config(background=Config['SERVERSTATUS_BACKGROUND'])
        
        self.currentline = 1
        
        self.text = tkinter.Text(
                         self,
                         background=Config['SERVERSTATUS_BACKGROUND'],
                         font=FONT,
                         relief="flat",
                         wrap="none",
                         width=54,
                         height=35,
                         )

        self.text.tag_config("headerLine", foreground=Config['BUTTON_FOREGROUND'], background=Config['BUTTON_BACKGROUND'], underline=1)
        
        self.text.grid(sticky=W + N)
        
        self.text_scroll = tkinter.Scrollbar(self, command=self.text.yview, background=Config['BUTTON_BACKGROUND'])
        self.text.config(yscrollcommand=self.text_scroll.set)
        self.text_scroll.grid(row=0, column=1, sticky="ns")
    def show(self):
        print("Showing frame")
        self.grid(row=FRAME_SERVERSTATUS[0], column=FRAME_SERVERSTATUS[1], sticky=N + W, rowspan=4)
    def hide(self):
        self.grid_forget()
    def getlinenum(self):
        self.currentline += 1
        data = "%d.%d" % (self.currentline , 0)
        # logfile("Line data = %s right?" % data )
        return data
    def insertline(self, text, tag=None):
        self.text.config(state=NORMAL)
        if tag == None:
            self.text.insert(self.getlinenum(), text + '\n')
        else:
            self.text.insert(self.getlinenum(), text + '\n', tag)
        self.text.config(state=DISABLED)
    def clear(self):
        self.currentline = 0
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.config(state=DISABLED)
    
class NoticeLabel(tkinter.Label):
    def __init__(self, parent=None, cnf={}, **kw):
        tkinter.Label.__init__(self, parent, cnf, **kw)
        self.ServerFrame = parent
        self.textvar     = tkinter.StringVar(value="FS_Basepath and FS_Homepath are not required.\nThey will be set to the folder of you ET.exe if not specfied.")
        
        self.config(font=FONT,background=Config['WINDOW_BACKGROUND'],textvariable=self.textvar)
        
        #self.show()
    def set(self,message=""):
        self.textvar.set(message)
    def show(self):
        self.grid(row=LABEL_NOTICE[0], column=LABEL_NOTICE[1], sticky=N + W,rowspan=2)
    def hide(self):
        self.grid_forget()

class ServerFrame(tkinter.Frame):
    """Frame contains all server related frames"""
    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)
        self.MainWindow = parent
        
        self.config(background=Config['WINDOW_BACKGROUND'], padx=5, pady=5)
        
        self.HeaderFrame       = HeaderFrame(self)
        self.ServerListFrame   = ServerListFrame(self)
        self.ServerDataFrame   = ServerDataFrame(self)
        self.ServerStatusFrame = ServerStatusFrame(self)
        
        self.button_addserver    = MenuButton(self.MainWindow.navbar , BUTTON_ADD    , text="Add"        , command=self.addserver)
        self.button_removeserver = MenuButton(self.MainWindow.navbar , BUTTON_REMOVE , text="Remove"     , command=self.removeserver)
        #self.button_rcon         = MenuButton( self.parent.navbar , BUTTON_RCON , text="Rcon"       , command=parent.rcon)
        self.button_joinserver   = MenuButton(self.MainWindow.navbar , BUTTON_JOIN   , text="Join"       , command=self.joinserver)
        self.button_addserver.show()
        
        
        self.HeaderFrame.show()
        self.ServerListFrame.show()
        self.NoticeLabel = NoticeLabel(self)
        
        self.grid(sticky=W + S + N + E)
        
        self.after(100, self.create_server_list)
        
    def create_server_list(self):
        self.ServerStatusFrame.hide()
        self.ServerDataFrame.hide()
        self.ServerDataFrame.clear()
        self.button_joinserver.hide()
        self.button_removeserver.hide()
        for x in range(0, len(self.MainWindow.ServerData.Servers)):
            self.serverstatus(x)
        self.refresh_list(None)
        
    def refresh_list(self, selectid=None):
        self.ServerListFrame.clear()
        for Server in self.MainWindow.ServerData.Servers:
            self.ServerListFrame.add(Server)
        if selectid != None:
            self.ServerListFrame.select(selectid)
        
    # Buttons
    def addserver(self): # Leaving error checking up to the join command
        servertitle = tkinter.simpledialog.askstring("New Server Title", "Please insert a unique server title")
        if not servertitle or any(s['title'] == servertitle for s in self.MainWindow.ServerData.Servers):
            logfile("addserver: Invalid server title")
            return
        serveraddress = tkinter.simpledialog.askstring("New Server Address", "Please insert full server address.(unique)\nExample: 127.0.0.1:27960\nIf it is a hostname make sure you have the port at the end")
        if not serveraddress or any(s['address'] == serveraddress for s in self.MainWindow.ServerData.Servers):
            logfile("addserver: Invalid server address")
            return
        self.MainWindow.ServerData.add_server({'address':serveraddress, 'title':servertitle})
        self.create_server_list()
        self.ServerListFrame.select(END) # Select added server
        self.selectserver(None) # Get Server Data
    def removeserver(self):
        selectid = self.ServerListFrame.get()
        if selectid == None: return
        if not self.MainWindow.ServerData.Servers[selectid]:
            logfile("removeserver: Error updating server %d" % selectid)
            return
        del self.MainWindow.ServerData.Servers[selectid]
        self.create_server_list()
    def getcommandline(self,selectid=None):
        # TODO Move this to serverdata
        #selectid = self.ServerListFrame.get()
        if selectid == None: return
        Server = self.MainWindow.ServerData.Servers[selectid]
        if not Server:
            logfile("getcommandline: Error getting command line for server %d" % selectid)
            return
        # Generate Startup Line #
        etpath      = ''
        fs_basepath = ''
        fs_homepath = ''
        fs_game     = 'etmain' # Etmain by default if mod does not exist
        parameters  = ''
        address     = Server['address']
        password    = Server['password']
        
        # Check ET Path
        # This entry is required
        # If not exist then return None for command line
        if Server['ETPath']:
            etpath = Server['ETPath']
        else:
            etpath = self.MainWindow.ServerData.ETPath
        if not isfile(etpath):
            logfile("getcommandline: ET Path is not valid file")
            return None
        
        # Check for fs_basepath
        # This entry is not required
        # If not exist then do not add it to line ?
        if Server['fs_basepath']:
            fs_basepath = Server['fs_basepath']
        else:
            fs_basepath = self.MainWindow.ServerData.fs_basepath
        if not isdir(fs_basepath): fs_basepath = '' #will this work? or will it just default to wolfstarter directory
        #if not fs_basepath: fs_basepath = "/".join(etpath.replace('\\', '/').split("/")[0:-1])
        
        # Check for fs_homepath
        # This entry is not required
        # If not exist then do not add to line ?
        if Server['fs_homepath']:
            fs_homepath = Server['fs_homepath']
        else:
            fs_homepath = self.MainWindow.ServerData.fs_homepath
        if not isdir(fs_homepath): fs_homepath = ''
        #if not fs_homepath: fs_homepath = fs_basepath
        
        # Paramaters are extra parameters like exec configs or something.
        if self.MainWindow.ServerData.parameters: parameters = self.MainWindow.ServerData.parameters
        if Server['parameters']:
            if parameters: parameters += ' '
            parameters += Server['parameters']
        
            
        if Config['launchmod']:
            if "gamename" in Server['cvar']: fs_game = Server['cvar']['gamename']
            if fs_basepath:
                if not isdir(join(fs_basepath,fs_game)):
                    logfile("getcommandline: Mod path does not exist in basepath - setting to etmain")
                    fs_game = "etmain"
            else:
                etpathdir = "/".join(etpath.replace('\\', '/').split("/")[0:-1])
                if not isdir(join(etpathdir,fs_game)):
                    logfile("getcommandline: Mod path does not exist in et path - setting to etmain")
                    fs_game = "etmain"
        
        if not address:
            logfile("getcommandline: Address not valid")
            return
        if not isfile(etpath):
            logfile("getcommandline: ET Executable is not valid")
            return
        
        commandline = "\"%s\"" % etpath
        if fs_basepath and isdir(fs_basepath): commandline += " +set fs_basepath \"%s\"" % fs_basepath
        if fs_homepath and isdir(fs_homepath): commandline += " +set fs_homepath \"%s\"" % fs_homepath
        if fs_game and fs_game != "etmain": commandline += " +set fs_game %s" % fs_game
        
        if parameters: commandline += ' ' + parameters
        
        if password and "g_needpass" in Server['cvar'] and int(Server['cvar']['g_needpass']) == 1: commandline += ' +set password ' + password
        commandline += ' +connect ' + address
        
        # End command line generate #
        
        logfile("getcommandline: " + commandline)
        return (commandline,"/".join(etpath.replace('\\', '/').split("/")[0:-1]))
    def joinserver(self,e=None):
        selectid = self.ServerListFrame.get()
        if selectid == None: return
        command_info = self.getcommandline(selectid)
        if not command_info or not command_info[0] or not command_info[1]:
            logfile("joinserver: Couldn't find command line")
            LogWindow(self.MainWindow,"There was with your configuration. This error log should tell you what went wrong.")
            return
        cwd = getcwd()
        logfile("joinserver: Changing directory to %s" % command_info[1])
        chdir(command_info[1])
        logfile("joinserver: Joining server %s" % selectid)
        openprocess(command_info[0])
        logfile("joinserver: Returning directory to %s" % cwd)
        chdir(cwd)
    def serverstatus(self, selectid=None):
        specificserver = False
        if selectid == None:
            selectid = self.ServerListFrame.get()
        else:
            specificserver = True
        if not specificserver:
            self.ServerStatusFrame.clear()
            self.ServerStatusFrame.hide()
        if selectid == None: return
        
        Server = self.MainWindow.ServerData.Servers[selectid]
        
        if not Server:
            logfile("serverstatus: Error getting server playerlist %d" % selectid)
            return
        
        logfile("serverstatus: Getting serverstatus for %d (%s)" % (selectid, Server['title']))
        
        self.MainWindow.ServerData.getstatus(selectid)
        
        if Server['ping'] <= 0:
            logfile("serverstatus: Could not ping server")
            return
        
        if not specificserver:
            if "sv_hostname" in Server['cvar']:
                self.ServerStatusFrame.insertline("%s : %s" % ( "Server Name".ljust(11) , cleanstr(Server['cvar']['sv_hostname']).ljust(HEADERLENGTH) ) )
            if "mapname" in Server['cvar']:
                self.ServerStatusFrame.insertline("%s : %s" % ( "Map".ljust(11) , Server['cvar']['mapname'].ljust(HEADERLENGTH)) )
            if "gamename" in Server['cvar']:
                self.ServerStatusFrame.insertline("%s : %s" % ( "Mod".ljust(11), Server['cvar']['gamename'].ljust(HEADERLENGTH)) )
            self.ServerStatusFrame.insertline("%s : %s" % ( "Ping".ljust(11) , (str(Server['ping']) + 'ms').ljust(HEADERLENGTH)) )
            self.ServerStatusFrame.insertline('')
            self.ServerStatusFrame.insertline("%s %s %s" % ("Name".ljust(PLAYER_NAME_LENGTH) , "Ping".ljust(PLAYER_PING_LENGTH) , "Score".ljust(PLAYER_SCORE_LENGTH)), "headerLine")
        
        currentplayers = 0
        currentbots    = 0
        for Player in Server['playerlist']:
            if Player['ping'] == 0:
                currentbots += 1
            else:
                currentplayers += 1
            if not specificserver:
                name = cleanstr(Player['name'][:PLAYER_NAME_LENGTH]) if len(cleanstr(Player['name'])) > PLAYER_NAME_LENGTH else cleanstr(Player['name'])
                self.ServerStatusFrame.insertline("%s %s %s" % (name.ljust(PLAYER_NAME_LENGTH) , str(Player['ping']).ljust(PLAYER_PING_LENGTH) , str(Player['score']).ljust(PLAYER_SCORE_LENGTH)))
        Server['players'] = "%d/%d (%d)" % (currentplayers , int(Server['cvar']['sv_maxclients']) , currentbots)
        
        if not specificserver:
            self.ServerStatusFrame.insertline('')
            self.ServerStatusFrame.insertline('')
            self.ServerStatusFrame.insertline("%s | %s" % ("Cvar".ljust(HALFLEN) , "Value".ljust(HALFLEN)) , "headerLine")
            for Cvar in Server['cvar']:
                self.ServerStatusFrame.insertline("%s = %s" % (Cvar.ljust(HALFLEN) , Server['cvar'][Cvar].ljust(HALFLEN)))
            
        self.refresh_list(selectid)
        if not specificserver:
            if 'g_needpass' in Server['cvar'] and int(Server['cvar']['g_needpass']) == 1:
                self.ServerDataFrame.showpassword()
            else:
                self.ServerDataFrame.hidepassword()
            self.ServerStatusFrame.show()
    # Methods
    def getpath(self, browse_var=None, updatemethod=None):
        if not browse_var: return
        if not updatemethod: return
        currentdir = browse_var.get()
        if not currentdir or not isdir(currentdir):
            currentdir = getcwd()
        self.MainWindow.focus_ignore = True
        dir_path = tkinter.filedialog.askdirectory(parent=self, initialdir=currentdir, title="Navigate to your path")
        self.MainWindow.focus_ignore = False
        
        if dir_path and isdir(dir_path):
            browse_var.set(dir_path)
            updatemethod(self)
        else:
            logfile("getpath-dialog: Could not find directory path")
    def getfilepath(self, browse_var=None, updatemethod=None):
        if not browse_var: return
        if not updatemethod: return
        currentdir = browse_var.get()
        if not currentdir or not isdir(currentdir):
            currentdir = getcwd()
        self.MainWindow.focus_ignore = True
        file_path = tkinter.filedialog.askopenfilename(parent=self, initialdir=currentdir, title="Navigate to your your exe", filetypes=(("exe files", "*.exe"), ("All files", "*")),)
        self.MainWindow.focus_ignore = False
        
        if file_path and isfile(file_path):
            browse_var.set(file_path)
            updatemethod(self)
        else:
            logfile("getfilepath-dialog: Could not find filepath")
    def closewindow(self):
        self.button_addserver.destroy()
        self.button_removeserver.destroy()
        self.button_joinserver.destroy()
        for child in self.winfo_children():
            child.destroy()
        self.destroy()

class LogWindow(tkinter.Toplevel):
    def __init__(self, parent=None,labeltext="", cnf={}, **kw):
        tkinter.Toplevel.__init__(self, parent, cnf,**kw)
        self.MainWindow = parent
        self.config(background=Config['WINDOW_BACKGROUND'],padx=5,pady=5)
        self.title("Log Window")
        
        if labeltext:
            self.label = tkinter.Label(self,text=labeltext,background="#000000",foreground="#FF0000")
            self.label.grid(row=0,column=0,columnspan=2)
        
        self.textbox   = tkinter.Text(self,width=115,height=47)
        
        self.text_scroll = tkinter.Scrollbar(self, command=self.textbox.yview, background=Config['BUTTON_BACKGROUND'])
        self.textbox.config(yscrollcommand=self.text_scroll.set)
        self.text_scroll.grid(row=1, column=1, sticky="nse")
        
        with open('wolfstarter.log') as myfile:
            logdata=myfile.read()
        
        self.textbox.insert(END, logdata)
        self.textbox.yview(END)
        self.textbox.grid(row=1,column=0,sticky="W")
        self.grid()

class SettingCheckButton(tkinter.Checkbutton):
    def __init__(self, master=None, labeltext=None,row=0, cnf={}, **kw):
        tkinter.Checkbutton.__init__(self, master, cnf, **kw)
        
        self.Settings = master
        
        self.var = tkinter.IntVar()
        
        self.config(variable=self.var,background=Config['WINDOW_BACKGROUND'])
        self.label = tkinter.Label(self.Settings,text=labeltext,background=Config['WINDOW_BACKGROUND'])
        self.label.grid(row=row,column=0,sticky=W)
        
        self.grid(row=row,column=1,sticky=W)
    def get(self):
        if self.var.get() == 1:
            return True
        else:
            return False

class Settings(tkinter.Frame):
    """Sepearate window for settings"""
    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)
        
        self.MainWindow = parent
        
        self.config(background=Config['WINDOW_BACKGROUND'], padx=5, pady=5)
        
        self.label_info = tkinter.Label(self,text="The color options are only editable in wolfstarter.json",background=Config['WINDOW_BACKGROUND'])
        self.label_info.grid(sticky=W)
        
        self.launchmod    = SettingCheckButton(self,"Launches ET with the mod of the server instead of etmain",1)
        self.basepath     = SettingCheckButton(self,"Show the basepath text entry",2)
        self.homepath     = SettingCheckButton(self,"Show the homepath text entry",3)
        self.command      = SettingCheckButton(self,"Show the full command line text that will be sent to et executable",4)
        self.windowborder = SettingCheckButton(self,"Show the Windows's window border at all times",5)
        
        self.savebutton = MenuButton(self,0,6,text="save",command=self.closewindow)
        self.savebutton.show()
        
        if Config['launchmod']: self.launchmod.toggle()
        if Config['showbasepath']: self.basepath.toggle()
        if Config['showhomepath']: self.homepath.toggle()
        if Config['showcommandline']: self.command.toggle()
        if Config['windowborder']: self.windowborder.toggle()
        
        self.grid()
    def closewindow(self):
        Config['launchmod']       = self.launchmod.get()
        Config['showbasepath']    = self.basepath.get()
        Config['showhomepath']    = self.homepath.get()
        Config['showcommandline'] = self.command.get()
        Config['windowborder']    = self.windowborder.get()
        
        self.MainWindow.save_config()
        for child in self.winfo_children():
            child.destroy()
        self.MainWindow.ServerData   = ServerData()
        self.MainWindow.ServerData.load_serverfile(Config['servers'])
        self.MainWindow.ServerFrame = ServerFrame(self.MainWindow)
        
        if self.windowborder.get():
            self.MainWindow.overrideredirect(False)
        else:
            self.MainWindow.overrideredirect(True)
        
        self.destroy()

class Window(tkinter.Tk):
    def __init__(self , *args, **kwargs):
        global FONT # Do I need?
        self.focus_ignore = False
        self.minimized    = False
        self.load_config()
        
        tkinter.Tk.__init__(self)
        FONT              = tkinter.font.Font(family="Courier New", size=10)
        # self.bind("<FocusIn>"         , self.OnFocus)
        # self.bind("<FocusOut>"        , self.OnLostFocus)
        if not Config['windowborder']:
            self.overrideredirect(True)
        self.config(background=Config['WINDOW_BORDER'], padx=5, pady=5)  # Set padding and background color
        self.title("WolfStarter by Zelly")
        self.bind("<FocusIn>"         , self.OnFocus)
        self.bind("<FocusOut>"        , self.OnLostFocus)
        self.bind("<Configure>"       , self.OnConfigure)
        self.iconbitmap('WolfStarterLogo.ico')
        
        self.mainframe = tkinter.Frame(self,background=Config["WINDOW_BACKGROUND"])
        
        self.navbar = NavBar(self)
        
        # Bind the move window function
        self.navbar.bind("<ButtonPress-1>"   , self.StartMove)
        self.navbar.bind("<ButtonRelease-1>" , self.StopMove)
        self.navbar.bind("<B1-Motion>"       , self.OnMotion)
        
        self.mainframe.grid()
        
        self.ServerData   = ServerData()
        self.ServerData.load_serverfile(Config['servers'])
        self.ServerFrame = ServerFrame(self)
        
        self.mainloop()
    def load_config(self):
        logfile(str(" Loading config ").center(24,"-"))
        if not isfile(join(getcwd() , 'wolfstarter.json')):
            logfile("Config not found using default")
        else:
            with open(join(getcwd() , 'wolfstarter.json')) as configfile:
                jsondata = json.load(configfile)
            if jsondata:
                for key in jsondata:
                    if key in Config:
                        Config[key] = jsondata[key]
                        logfile(key.ljust(32) + " = " + str(jsondata[key]))
                    # Make sure to only do keys that exist.
        logfile(str(" Loaded config ").center(24,"-"))
    def save_config(self):
        self.ServerData.save_serverfile(Config['servers'])
        jsonfile = open(join(getcwd() , 'wolfstarter.json'), 'w')
        json.dump(Config, jsonfile, skipkeys=True, sort_keys=True, indent=4)
    # Opening and closing files and application
    def openfile(self):
        self.focus_ignore = True
        fname = tkinter.filedialog.askopenfilename(
                                                parent=self,
                                                initialdir=getcwd(),
                                                title="Select servers file",
                                                filetypes=(("json file", "*.json"), ("All files", "*")),
                                                )
        if not fname or not isfile(fname):
            tkinter.messagebox.showinfo(title="Invalid servers file", message="Servers file was not found", parent=self)
            self.focus_ignore = False
            logfile("Invalid Servers file was not found %s" % fname)
            return
        self.focus_ignore      = False
        Config['servers']      = fname
        self.ServerData        = ServerData()
        self.ServerData.load_serverfile(Config['servers'])
        logfile("Loaded Servers file: %s" % Config['servers'])
        if self.ServerFrame:
            self.ServerFrame.destroy()
        self.serversframe = ServerFrame(self)
    def saveasfile(self):
        self.focus_ignore = True
        fname = tkinter.filedialog.asksaveasfilename(
                                                parent=self,
                                                initialdir=getcwd(),
                                                title="Select servers file",
                                                filetypes=(("json file", "*.json"), ("All files", "*")),
                                                )
        if not fname:
            tkinter.messagebox.showinfo(title="Invalid servers file", message="Servers file was not found", parent=self)
            self.focus_ignore = False
            # self.parent.focus_force()
            logfile("saveasfile: Invalid Servers file was not found %s" % fname)
            return
        self.focus_ignore      = False
        Config['servers']      = fname
        self.ServerData.save_serverfile(Config['servers'])
        logfile("saveasfile: Saved servers file %s" % Config['servers'])
    def quit(self):
        self.save_config()
        self.destroy()
        
    # Moving application on screen
    def StartMove(self, event):
        self.x = event.x
        self.y = event.y
    def StopMove(self, event):
        self.x = None
        self.y = None
    def OnMotion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry("+%s+%s" % (x, y))
    def OnFocus(self, event):
        if Config['windowborder']: return # Ignore window focus events
        if self.minimized or self.focus_ignore: return
        w=self.focus_get()
        if w:
            self.overrideredirect(True)
            w.focus_force()
    def OnLostFocus(self, event):
        if Config['windowborder']: return # Ignore window focus events
        if self.minimized or self.focus_ignore: return
        if not self.focus_get(): self.overrideredirect(False)
        
    def OnConfigure(self,event):
        if Config['windowborder']: return # Ignore window focus events
        if self.minimized and not self.focus_get(): # If minimized, and window does not have focus and there is a new event.
            # Is most likely that the event is a maximize event, however the window isn't maximized until after this event.
            def task():
                if self.minimized and self.focus_get():
                    self.minimized = False
                    self.overrideredirect(True)
            self.after(50,task) # Do task after 50 ms (Basically after the window is maximized)
            
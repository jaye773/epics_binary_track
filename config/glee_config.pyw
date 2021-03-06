
# There are a few things I would like to add to this, but I am lacking
# the time to do so.  The biggest and best change would be to make the
# category entry box in the question editor be a Combobox from ttk.  
# This would make adding questions to existing categories significantly
# easier.  Making the question name editor be a Combobox as well would
# be nice for editing existing questions, but not as much so, I think.
# It would also be significantly more difficult to implement well.
# Buttons to check/uncheck all categories on the Choose Categories 
# tab would be nice, but the current implementation of the save 
# function would make that somewhat obnoxious to use, because every
# time a box is checked or unchecked, the whole configuration file is
# saved, which takes some time.  It would be particularly frustrating 
# for the users to use that button with a large number of categories.
# I suspect it will be more frustrating to check or uncheck a large
# number of categories manually as well, so that is certainly a 
# trade-off.  Unfortunately, I do not have time to implement that,
# debug it, and make sure it performs well.

# Next, a few notes.  The overall project is coded in Python 3.3.0.
# The modules we use are tkinter, json, and sys.  From tkinter 
# we use two sub modules called ttk and tix.  We only need stdout
# from sys for debug message printing purposes.  

# Tkinter is the graphical module.  It includes everything needed
# for the GUI itself (buttons, labels, entry boxes, etc.).  
# Included in tkinter is ttk, or Themed Tkinter.  ttk is a more
# modern extension of tkinter, allowing for more modern appearing
# applications.  We also use tix solely for the scrolled window
# with the user-defined categories on the second tab.  

# Json, or JavaScript Object Notation, is used for inter-program
# file standardization.  This config editor writes a large config
# file using json.  Because json is standardized, other programs
# in the binary racetrack suite can easily use the same config
# file without doing special file parsing.  The sys module is used
# solely for stdout, to help with a debug print in one part.

# To compile the program to exe, we use cx_Freeze version 4.3.1 for
# Python 3.3.  Theoretically, all future versions of Python and 
# cx_Freeze should work, but if any issues arise in future 
# maintenance, make sure these are the versions being used.  More
# documentation for compiling with cx_Freeze is included in the 
# file setup.py.  For Python 2.x, an older program called py2exe
# could be used, but unfortunately it is not fully compatible with
# Python 3.x.  

# Python is rather versatile and easy to work with, so we are using
# that.  It is also multi-platform, so if the school wants this to 
# run on multiple platforms (Mac OSX, Windows, or some Linux distro),
# making it work for those should be particularly easy.  A similarly
# portable language is Java, but at this point I pick Python solely
# from personal preference.  Python is just easier for me to work with.

# There are many GUI (graphical user interface) toolkits for Python,
# including PyQt, Pygame, PyGTK, PyGUI, and Tkinter.  We are using 
# Tkinter here because it is included in all modern Python
# distributions.  It is the standard Python GUI toolkit.  Adding 
# other toolkits would not be too difficult, but converting the 
# Python code to an executable file is a bit more of a hassle when
# using 3rd party software (such as PyQt).  

# The normal Python file extension is .py.  These can be opened and run
# in IDLE or another Python coding environment.  This file, however,
# should be a .pyw file.  This extension tells the Python environment
# to not display the console.  If we use .py, the GUI works fine, but
# a console for text output is also displayed.  .pyw files suppress
# the console, so only the GUI is displayed.

# imports
from tkinter import *
from tkinter import ttk 
from tkinter import messagebox
from tkinter import tix
import json
from sys import stdout

# Use a class for encapsulation.  It is not necessary, but it can help
# make the overall code much easier to work with, especially if another
# program ends up extending this module.  It is unlikely, but 
# encapsulation is good practice anyway.  
class glee_config(object):
	
	# This tuple is used to specify fonts in the labels and entry boxes
	# later.  Change these values to any standard font or font size
	# (right now it is Courier and size 18), but be warned that the GUI
	# is designed specifically around this font.  No other fonts have 
	# been tested, so weird things can happen.
	default_font = ("Courier", 18)
	
	# For those unfamiliar with OOP (object-oriented programming), the 
	# __init__ function is generally the part of the code where all 
	# variables that will be stored in the class are instantiated 
	# and initialized.  Thus, __init__ functions are often rather 
	# empty, bland, and long.  For those who are familiar with OOP 
	# languages such as C++ and Java, the __init__ function is the
	# constructor.  
	def __init__(self):
	
		# set up initial window.
		# In Tkinter, the root window is the primary window into which
		# everything else goes.  All the widgets go into frames (which
		# are also widgets), and all the frames go into potentially
		# more frames.  Eventually, all the top level frames are 
		# packed into the root window.  
		# Normally, the code would just be root = Tk().  However, in 
		# order to use the ScrolledWindow that we use later, we have
		# to use the special Tk in tix, so we need tix.Tk().  
		root = tix.Tk()
		root.title("Learning Racetrack Question Editor")
		# Geometry is important.  The first 1000x650 makes it 1000 
		# pixels wide and 650 tall.  +40 moves it 40 pixels from
		# the left side of the monitor, and +20 moves it 20 pixels
		# down from the top of the monitor.
		root.geometry('1000x650+40+20')
		# Because the geometry of the window is so important, we also 
		# want to assure that the geometry remains that way.  This 
		# window also does not look good if its width or height change,
		# so we need to make it not resizable.  Tkinter apps default
		# to being resizable in both width and height, so set those
		# both to false with the resizable function.
		root.resizable(width=FALSE, height=FALSE)
		root.rowconfigure(0, weight=1)
		root.columnconfigure(0,weight=1)
		
		# set up the notebook
		# A notebook can display multiple pages.  Each page must 
		# be a frame (or possibly some other frame-like widget).
		# Two things to note about the next line of code are we use
		# ttk.Notebook instead of just Notebook so we can use our
		# lovely modern themes.  The one argument for the 
		# Notebook initializer is the root window, so Tkinter knows
		# to put the Notebook into the root window.  
		# Call this notebook book for simplicity.  If we have other
		# notebooks, we would probably want to call it something 
		# else, but book is fine here.  
		book = ttk.Notebook(root)
		# pack tells the notebook to actually appear on the frame
		# on which it's supposed to appear (in book's case, it 
		# will appear on root).  The fill argument can be X, Y, or
		# BOTH.  This determines how the widget fills the frame it
		# is in.  My understanding of the expand argument is not 
		# complete, but as far as I can tell expand=1 tells the 
		# widget to expand the frame it is in in order to fill 
		# the frame that frame is in.  The =1 part is the weight
		# of the expansion; if another frame had expand=2 and would
		# conflict, it has priority.  
		# An alternate option would be to use a grid (instead of 
		# pack), which allows us to specify exactly where on a 
		# grid we want widgets.  Both allow us to put things exactly
		# where we want them, and they both seem to be fairly
		# common, but I prefer pack, mostly because it was the first
		# I used with Tkinter.
		book.pack(fill=BOTH,expand=1)
		
		# Make two frames and put them into the Notebook.  One frame
		# is for editing the questions and categories.  The other is 
		# to enable or disable the various categories (user defined
		# and built in).
		page_1_frame = ttk.Frame(book)
		page_1_frame.pack(fill=BOTH,expand=1)
		
		page_2_frame = ttk.Frame(book)
		page_2_frame.pack(fill=BOTH,expand=1)
		
		# Put the frames into the book.  This is an additional step
		# that is similar to packing but also required.  The text 
		#argument determines what displays in the tab for the frame.
		book.add(page_1_frame, text="Edit Questions")
		book.add(page_2_frame, text="Choose Categories")
		
		# set up category frame
		# This is a pretty standard frame setup.  Make a frame, give
		# it to its parent frame, and pack it.  In this case we want
		# it to be on the left side and fill its parent frame 
		# vertically.  Make sure it is a ttk.Frame rather than a 
		# Frame because ttk is themed.
		cat_frame = ttk.Frame(page_1_frame)
		cat_frame.pack(side=LEFT,fill=Y)
		# Create a label.  Labels are widgets used primarily to display
		# text.  They can also be used to display images, but in this 
		# case we are just displaying text with them.  Make the text
		# be "Categories" and give it the default font, as described
		# at the start of this class.  Pack it and give it some padding
		# to make it display more nicely.  Without some padding, some
		# widgets will encroach on each other, altering the seamless
		# appearance of the various frames.
		cat_label = ttk.Label(cat_frame, text="Categories", font=self.default_font)
		cat_label.pack(pady=3,padx=3)
		# load_cat_frame is used as a wrapper for the category buttons.
		# Pack the buttons onto the frame with side=LEFT.  Once we 
		# have this frame with things on it, we can pack it into the top 
		# of cat_frame, which puts it just under the Categories label.
		# This has the added benefit of centering the buttons under the
		# label.  Alternately, we could wrap this frame in yet another 
		# frame, pack the wrapper frame at the top, and pack this frame
		# to the left to get the buttons to be left-aligned.  We want
		# center for aesthetics in this case, though.
		load_cat_frame = ttk.Frame(cat_frame)
		load_cat_frame.pack(side=TOP)
		# Make two buttons.  Buttons, like most other widgets, should be
		# the ttk variants for the modern theme.  Pass it the frame, 
		# set the text variable, and give it a command.  Commands are 
		# functions that are called when the button is clicked.  We are
		# unable to pass any variables to the functions (aside from self
		# by referring to the function as self.cat_select, for example)
		# so they are generally built specifically for this purpose.
		# Another term for this type of function is a "call back".  
		load_cat_button = ttk.Button(load_cat_frame, text="Select Category", command=self.cat_select)
		load_cat_button.pack(side=LEFT)
		del_cat_button = ttk.Button(load_cat_frame, text="Delete Category", command=self.cat_delete)
		del_cat_button.pack(side=LEFT)
		
		# Scrollbars are a bit different from other widgets.  Most 
		# widgets just require packing, and buttons (as we will see
		# later) require a command or event to be set.  We want this
		# scrollbar to be associated with a listbox, which we will make
		# next.  Make the scrollbar like any other widget (pass it the 
		# frame we want to put it in) and pack it.  We want it to be
		# vertical, so set fill to Y.  We also want it to act like a 
		# standard scrollbar, so pack it to the right instead of the
		# left that we have been using.
		cat_scroll = Scrollbar(cat_frame)
		cat_scroll.pack(side=RIGHT, fill=Y)
		
		# A listbox displays a selectable list of items.  We only want
		# one item to be selectable at a time, which is nice because
		# that is the default mode.  There are two other modes that
		# change how many items are selectable at a time.  Like the
		# buttons, listboxes can have a command.  However, it is a 
		# special command called yscrollcommand.  Set yscrollcommand to
		# cat_scroll.set, and then set the cat_scroll's command to 
		# cat_box.yview.  This lets the scrollbar control the listbox,
		# and it lets the listbox control the scrollbar.  
		cat_box = Listbox(cat_frame, font=self.default_font, yscrollcommand=cat_scroll.set)
		cat_scroll.config(command=cat_box.yview)
		
		# Double click event is different than button presses, in that 
		# the function it calls has to accept an event object.  Because 
		# this is object-oriented, that would mean the function would 
		# have to accept self and the event object, and cat_select() 
		# only accepts self.  We could use a new function that does 
		# nothing but call cat_select(), but instead of that we just 
		# create a lambda function.  A lambda function is a temporary 
		# function that exists only during the time it is called.  
		# After that, it is gone.  Lambda functions are often used in 
		# locations like this, where a very short function is wanted 
		# for one specific purpose.  This double click event essentially
		# allows us to just double click on an item instead of using
		# the "select category" button to select it.  For convenience,
		# we leave the button in as well.  Unfortunately, there does
		# not seem to be a single click event, which would make using
		# this app a bit easier.
		cat_box.bind("<Double-Button-1>", lambda x:self.cat_select()) 
		cat_box.pack(side=TOP, fill=Y,expand=1)
		
		# set up input boxes
		# Most of the remaining code in the __init__ function is similar
		# to the code we have already seen, so it requires significantly
		# less documentation.  
		
		main_frame = ttk.Frame(page_1_frame)
		main_frame.pack(fill=BOTH,expand=1)
		
		# An Entry is a 1-line input box that defaults to 20 characters
		# long.  Fortunately, we want exactly 20 characters for these.
		# A Text is similar to an Entry, except it is potentially 
		# 2-dimensional, and so requires a different sort of indexing.
		# Otherwise, they are about the same in functionality.  
		title_frame = ttk.Frame(main_frame)
		title_frame.pack(fill=X)
		title_label = ttk.Label(title_frame, text="Question", font=self.default_font)
		title_label.pack(side=LEFT,pady=3,padx=3)
		title_entry = Text(title_frame, font=self.default_font, height=5, wrap='word')
		title_entry.pack(side=RIGHT)
		
		change_cat_frame = ttk.Frame(main_frame)
		change_cat_frame.pack(fill=X)
		change_cat_label = ttk.Label(change_cat_frame, text="Category", font=self.default_font)
		change_cat_label.pack(side=LEFT,pady=3,padx=3)
		change_cat_entry = ttk.Entry(change_cat_frame, font=self.default_font)
		change_cat_entry.pack(side=RIGHT)
		
		cor_ans_frame = ttk.Frame(main_frame)
		cor_ans_frame.pack(fill=X)
		cor_ans_label = ttk.Label(cor_ans_frame, text="Correct Answer", font=self.default_font)
		cor_ans_label.pack(side=LEFT,pady=3,padx=3)
		cor_ans_entry = ttk.Entry(cor_ans_frame, font=self.default_font)
		cor_ans_entry.pack(side=RIGHT)
		
		# For the alternate answers we need another container frame
		# and then two smaller frames.
		alt_ans_frame = ttk.Frame(main_frame)
		alt_ans_frame.pack(fill=X)
		
		alt_ans_left_frame = ttk.Frame(alt_ans_frame)
		alt_ans_left_frame.pack(side=LEFT, fill=Y)
		alt_ans_label = ttk.Label(alt_ans_left_frame, text="Alternate Answers", font=self.default_font)
		alt_ans_label.pack(side=TOP,pady=3,padx=3)
		# Change alt_ans_warning_label to say "Must have either 2 or 4 answers" 
		# if there are 1 or 3 answers including the alternates.
		alt_ans_warning_string = StringVar()
		alt_ans_warning_label = ttk.Label(alt_ans_left_frame, textvariable=alt_ans_warning_string, font=self.default_font)
		alt_ans_warning_label.config(foreground="red")
		alt_ans_warning_label.pack(pady=3,padx=3,side=TOP)
		
		alt_ans_right_frame = ttk.Frame(alt_ans_frame)
		alt_ans_right_frame.pack(side=RIGHT)
		alt_ans_1_entry = ttk.Entry(alt_ans_right_frame, font=self.default_font)
		alt_ans_1_entry.pack(pady=3)
		alt_ans_2_entry = ttk.Entry(alt_ans_right_frame, font=self.default_font)
		alt_ans_2_entry.pack(pady=3)
		alt_ans_3_entry = ttk.Entry(alt_ans_right_frame, font=self.default_font)
		alt_ans_3_entry.pack(pady=3)
		
		# set up frame for buttons 
		but_frame = ttk.Frame(main_frame)
		but_frame.pack(fill=X)
			
		# There is plenty of code here for a few extra buttons that we
		# removed.  Initially, there was a "save all" button.  Nothing
		# was saved to the file until the save all button was clicked.
		# However, it was requested that we remove that, so it is no 
		# longer there.  Its callback function is called everywhere 
		# data changes so data is always saved.  There were also undo
		# buttons, but since data is saved automatically, undo seemed 
		# a bit confusing, so those buttons were removed.  We still have
		# the select question, save question, new question, and delete
		# question buttons.
		load_quest_button = ttk.Button(but_frame, text="Select Question", command=self.quest_select)
		load_quest_button.pack(side=LEFT)
		save_button = ttk.Button(but_frame, text="Save Question", command=self.save_question)
		#save_button.config(font=self.default_font)
		save_button.pack(side=LEFT)
		#undo_button = ttk.Button(but_frame, text="Undo Change", command=self.undo_change)
		#undo_button.pack(side=LEFT)
		#undo_all_button = ttk.Button(but_frame, text="Undo All Changes", command=self.undo_all_changes)
		#undo_all_button.config(font=self.default_font)
		#undo_all_button.pack(side=LEFT)
		new_button = ttk.Button(but_frame, text="New Question", command=self.new_question)
		new_button.pack(side=LEFT)
		del_button = ttk.Button(but_frame, text="Delete Question", command=self.delete_question_func)
		del_button.pack(side=LEFT)
		#save_button = ttk.Button(but_frame, text="Save", command=self.save_all)
		#save_button.pack(side=LEFT)
		
		# set up frame for question selection
		quest_frame = ttk.Frame(main_frame)
		quest_frame.pack(side=LEFT,fill=BOTH,expand=1)
		
		quest_label = ttk.Label(quest_frame, text="Questions", font=self.default_font)
		quest_label.pack(pady=3,padx=3)
		quest_scroll = Scrollbar(quest_frame)
		quest_scroll.pack(fill=Y, side=RIGHT)
		
		quest_box = Listbox(quest_frame, font=self.default_font, yscrollcommand=quest_scroll.set)
		quest_scroll.config(command=quest_box.yview)
		quest_box.bind("<Double-Button-1>", lambda x:self.quest_select()) 	
		
		quest_box.pack(fill=BOTH, expand=1)
		
		# work on choose categories tab
		choose_cat_title_frame = ttk.Frame(page_2_frame)
		choose_cat_title_frame.pack(side=TOP)# fill=X)
		
		choose_cat_title = ttk.Label(choose_cat_title_frame, text="Select Categories", font=self.default_font)
		choose_cat_title.pack(side=TOP)
		
		default_cat_frame = ttk.Frame(page_2_frame)
		default_cat_frame.pack(side=LEFT, fill=Y)
		
		default_cat_buffer_frame = ttk.Frame(default_cat_frame)
		default_cat_buffer_frame.pack(side=TOP)
		
		default_cat_title = ttk.Label(default_cat_buffer_frame, text="Default Categories", font=self.default_font)
		default_cat_title.pack(side=TOP)
		
		user_cat_master_frame = ttk.Frame(page_2_frame)
		user_cat_master_frame.pack(fill=BOTH, expand=1)
		user_cat_title = ttk.Label(user_cat_master_frame, text="Custom Categories", font=self.default_font)
		user_cat_title.pack(side=TOP)
		
		user_cat_scroll_window = tix.ScrolledWindow(user_cat_master_frame, scrollbar="x")
		user_cat_scroll_window.pack(fill=BOTH, expand=1)
		
		user_cat_frame = user_cat_scroll_window.window
		
		builtin_cat_checkboxes = {}
		
		#choose_cat_frame = ttk.Frame(page_2_frame)
		#choose_cat_frame.pack(side=TOP)#, fill=X)

		# Give all the frames borders for debugging purposes.
		# Uncomment these lines to see where the various 
		# frames are.  Do not leave it uncommented, because
		# the app looks quite ugly with frames.
		#default_cat_frame.config(relief=SUNKEN)
		#choose_cat_title_frame.config(relief=SUNKEN)
		#user_cat_frame.config(relief=SUNKEN)
		#cat_frame.config(relief=SUNKEN)
		#main_frame.config(relief=SUNKEN)
		#title_frame.config(relief=SUNKEN)
		#change_cat_frame.config(relief=SUNKEN)
		#cor_ans_frame.config(relief=SUNKEN)
		#alt_ans_frame.config(relief=SUNKEN)
		#alt_ans_left_frame.config(relief=SUNKEN)
		#alt_ans_right_frame.config(relief=SUNKEN)
		#but_frame.config(relief=SUNKEN)
		
		# When the __init__ function ends, most of the variables
		# expire because they are local to the function.  Of 
		# course, they still exist because root eventually owns
		# them (or their parents, which in turn own them), but
		# we need a way to reference them.  Assign them to 
		# class variable versions for later access.
		self.root = root
		self.cat_box = cat_box
		self.save_button = save_button
		#self.undo_button = undo_button
		#self.undo_all_button = undo_all_button
		self.title_entry = title_entry
		self.change_cat_entry = change_cat_entry
		self.cor_ans_entry = cor_ans_entry
		self.alt_ans_warning_label = alt_ans_warning_label
		self.alt_ans_warning_string = alt_ans_warning_string
		self.alt_ans_1_entry = alt_ans_1_entry
		self.alt_ans_2_entry = alt_ans_2_entry
		self.alt_ans_3_entry = alt_ans_3_entry
		self.quest_box = quest_box
		self.builtin_cat_checkboxes = builtin_cat_checkboxes
		self.default_cat_buffer_frame = default_cat_buffer_frame
		self.user_cat_frame = user_cat_frame
		self.page_2_frame = page_2_frame
		
		# We need a few more variables that do not come from 
		# widgets.  Create some class variables and assign them
		# default values.  
		self.cat_selected = ""
		self.quest_selected = ""
		self.font_color="blue"
		self.builtin_categories = {}
		self.user_categories = {}
		self.user_cat_frames = []
		
		# Set up some styles used in the choose categories frame.
		# These can have any name, as long as the name ends in 
		# ".TCheckbutton" so the styles inherit the values from
		# the default TCheckbutton style.  All we want here is 
		# the background colors to be different.  
		sty = ttk.Style()
		self.sty_1 = "Emergency1.TCheckbutton"
		self.sty_2 = "Emergency0.TCheckbutton"
		sty.configure("Emergency1.TCheckbutton", background="white")
		sty.configure("Emergency0.TCheckbutton", background="#F0F0F0")
		
		self.fill_defaults()
		
		# Load the questions.txt file.		
		self.fname = "questions.txt"
		self.load_from_file(self.fname)

		# Initialize all the widgets.  These functions 
		# automatically use the values loaded from the 
		# questions.txt file.
		self.init_categories()
		self.init_default_checkboxes()
		self.init_user_checkboxes()
		
		# The mainloop is like a more standard app's main
		# function, and keeps the program running until 
		# the user exits it or it somehow crashes.
		root.mainloop()
		
	# init_default_checkboxes is used to fill (or refill) the 
	# checkboxes for the default categories according to 
	# the configuration file.  This is called in the initial
	# setup, but we do not need to call it anywhere else
	# because the default categories will never change.
	def init_default_checkboxes(self):
		for cat in sorted(self.builtin_categories):
			tmp_frame = ttk.Frame(self.default_cat_buffer_frame)
			tmp_frame.pack(side=TOP, fill=X)#, expand=1)
			#tmp_frame.config(relief=SUNKEN)
			b = ttk.Checkbutton(tmp_frame, text=cat, var=self.builtin_categories[cat])
			self.builtin_cat_checkboxes[cat] = b
			b.pack(side=LEFT)
		
	# init_user_checkboxes is called during the initial
	# setup and when a category is added or deleted.  Much
	# like init_default_checkboxes, it fills the checkboxes
	# for all user-defined categories.  
	def init_user_checkboxes(self):
		## Some test code to automatically generate 400 
		## categories named "category 1", "category 2", 
		## etc.  This is only for testing purposes, but
		## is quite useful for testing large numbers of
		## categories.  
		#for i in range(400):
			#x = "%6d"%i
			#self.questions["category " + x] = {}
			#self.questions["category " + x]["question " + str(i)] = [str(i), str(i), str(i), str(i)]
		#self.user_cat_frame.destroy()
		##self.user_cat_frame = ttk.Frame(self.page_2_frame)
		#user_cat_title = ttk.Label(self.user_cat_frame, text="Custom Categories", font=self.default_font)
		#user_cat_title.pack(side=TOP)
		print("init user checkboxes")
		
		# Clear all sub-frames.  The first time this function
		# is called, this does nothing.  Every other time, it 
		# removes all existing checkboxes so we can put them
		# back.  This might seem counter-intuitive, but we 
		# want all old versions out of our way so we can
		# put them all in in the right order.
		for frame in self.user_cat_frames:
			frame.destroy()
		
		# Destroying a frame does not remove the reference to
		# it, so self.user_cat_frames potentially contains a
		# bunch of dead references to frames.  Remove these
		# references by setting the list to a blank list.
		# The garbage collector will take care of the rest
		# for us.
		self.user_cat_frames = []
		
		# Make sure we have a BooleanVar to keep track of all
		# our categories.  The only time this should do anything
		# is if there is a new category.  This new category
		# should default to False.  We use a BooleanVar because
		# those are easy to trace with the callback function
		# trace_func.  This is called every time the variable
		# changes (or is "w"ritten to), which happens every time
		# the checkbox is clicked.  
		for cat in self.questions:
			if cat not in self.user_categories:
				self.user_categories[cat] = BooleanVar(value=False)
				self.user_categories[cat].trace(callback=self.trace_func, mode="w")
		
		# Experimentation showed that the best number of 
		# categories to display per column is 25.  Theoretically,
		# this should be more dynamic based on the size of the
		# font, but for the current version 25 is nice.
		CATEGORIES_PER_PAGE = 25
		i = 0
		f = None
		mod = 1
		
		# Iterate through every category.  We want to keep them
		# sorted so large lists of categories are much easier
		# for the user to read.  Otherwise, due to the nature
		# of dicts, the checkboxes would appear in a completely
		# random order each time.
		for cat in sorted(self.user_categories.keys()):
			# The mod variable is used to alternate colors in
			# the custom category display.  This line switches
			# it from 1 to 0 or 0 to 1.
			mod = (mod + 1) % 2
			
			# We already made a BooleanVar to keep track of all
			# new categories.  Now get rid of all extraneous
			# BooleanVars for categories that no longer exist.
			if cat not in self.questions:
				del self.user_categories[cat]
				print("should be deleting %s from self.user_categories"%cat)
				continue
			
			# i keeps track of the number of checkboxes we have
			# put on one column.  If that matches 
			# CATEGORIES_PER_PAGE, reset it to 0 and make a new
			# Frame to put checkboxes on.  Pack the new Frame
			# and append it to self.user_cat_frames.  Also,
			# create and pack a small Label to act as a border
			# between two columns.
			if i%CATEGORIES_PER_PAGE == 0:
				i = 0
				mod = 0
				f = ttk.Frame(self.user_cat_frame)
				self.user_cat_frames.append(f)
				f.pack(side=LEFT, fill=Y)
				#f.config(relief=SUNKEN)
				tmp_frm = ttk.Frame(self.user_cat_frame)
				tmp_frm.pack(side=LEFT)
				tmp_lbl = Label(tmp_frm, text="      ")
				tmp_lbl.pack()
				
			# Make a new small Frame to put our new Checkbutton
			# into.  Create the new Checkbutton and give it the
			# appropriate BooleanVar from self.user_categories.
			tmp_frame = ttk.Frame(f)
			tmp_frame.pack(side=TOP, fill=X)
			#tmp_frame.config(relief=SUNKEN)
			b = ttk.Checkbutton(tmp_frame, text=cat, var=self.user_categories[cat])
			
			# If mod is 0, we want to use one background for
			# checkbuttons.  Otherwise, use the other background.
			if (mod == 0):
				b.config(style="Emergency1.TCheckbutton")
			else:
				b.config(style="Emergency0.TCheckbutton")
			b.pack(side=LEFT)
			Label(tmp_frame, text="  ").pack(side=LEFT)
				
			i += 1 #
			
	# fill_defaults is a simple test function to fill a few examples
	# in the category and question listboxes for display testing.
	# It should never be used in production.
	def fill_defaults(self):
		print("filling defaults")
		for word in sorted(["English", "Math", "History", "Geography"]):
			self.cat_box.insert(END, word)
		for i in range(20):
			for word in ["1. 10x+3", "2. 52/3", "3. 5*5"]:
				self.quest_box.insert(END, word)
				
	# This function clears and then re-fills the category Listbox
	# in addition to clearing the question Listbox and all 
	# text entry forms.
	def init_categories(self):
		print("init categories")
		self.cat_box.delete(0, END)  # clear the category box
		self.quest_box.delete(0,END) # clear the question box
		# clear all the entry boxes
		self.cor_ans_entry.delete(0,END)
		self.alt_ans_1_entry.delete(0,END)
		self.alt_ans_2_entry.delete(0,END)
		self.alt_ans_3_entry.delete(0,END)
		self.title_entry.delete(0.0,END)
		self.change_cat_entry.delete(0,END)
		
		for key in sorted(self.questions.keys()):   # populate the category box with the categories
			self.cat_box.insert(END, key)
	
	# This function clears the question Listbox and sets the 
	# currently selected question to an empty string.
	def reset_questions(self):
		print("reset questions")
		self.quest_box.delete(0, END)
		self.quest_selected = ""
			
	# cat_select is the callback function for the select category
	# button.  
	def cat_select(self):
		print("cat select")
		# Make sure the user has actually selected something
		# in the Listbox.  If not, notify them.
		if len(self.cat_box.curselection()) == 0:
			if self.cat_selected == "":
				self.alt_ans_warning_string.set("Please click on\na category and click\nSelect Category.")
				self.alt_ans_warning_label.config(foreground="red")
				return			
		# Listboxes are a bit counter-intuitive.  Rather than
		# giving us the string the user has selected, it gives
		# us a tuple containing a string representing the index 
		# (for example, "1") of the item they have selected.
		# If multiple selections are enabled (in this case, they
		# are not) the tuple contains the indices of each 
		# selected item.  We can then use that index in the
		# Listbox's get function to get the selected string.
		select_index = self.cat_box.curselection()[0]
		category = self.cat_box.get(select_index)
		self.cat_selected = category
		self.fill_quest_box(category)
		self.reset_display()
		# When the user selects a new category, reset the 
		# selected question to a null string.
		self.quest_selected = ""
	
	# cat_delete is the callback function for the delete 
	# category button.  
	def cat_delete(self):
		print("cat delete")
		# messagebox.askyesno is a nifty function that displays
		# a dialog that prompts the user to click "yes" or "no". 
		# It returns True if the user clicks yes and False 
		# otherwise.  
		prompt = messagebox.askyesno("Delete Category?", "Are you sure you want to delete this category?\nAll questions in this category will be deleted!\nCategory: " + self.cat_selected)
		if prompt == True:
			del self.questions[self.cat_selected]
			# Display a message saying which category the
			# user is deleting.  Only display the first 20
			# characters of the category for space concerns.
			self.alt_ans_warning_string.set("Deleted category\n%s"%(self.cat_selected[:20]))
			self.alt_ans_warning_label.config(foreground="blue")
			# If we delete the selected category, remove the 
			# reference to its name here.  Set it to a null
			# string.
			self.cat_selected = ""
			self.init_categories()
			self.init_user_checkboxes()
			self.save_all()
	
	# This function reads all questions in a specific category
	# and inserts them into the question box.  
	def fill_quest_box(self, category):
		print("fill question box")
		self.reset_questions()
		# Make sure it is a valid category.  If for some reason
		# the category is not valid, do nothing.
		if category in self.questions:
			for question in sorted(self.questions[category].keys()):
				self.quest_box.insert(END, question)
	
	# reset_display removes all inputted text from the text boxes.
	def reset_display(self):
		print("reset display")
		self.title_entry.delete(0.0, END)
		self.change_cat_entry.delete(0,END)
		self.cor_ans_entry.delete(0,END)
		self.alt_ans_1_entry.delete(0,END)
		self.alt_ans_2_entry.delete(0,END)
		self.alt_ans_3_entry.delete(0,END)
	
	# quest_select is the callback function for the Select
	# Question button.  
	def quest_select(self, q=None):
		print("question select")
		self.reset_display()
		question = q
		# If no question is specified, make sure there is a 
		# selected category.  If not, display an informative
		# message and return.  If there is a selected 
		# category, check if there is a selected question.
		# If so, get it and set the selected question to that.
		# If not, display an informative message and return.
		if q == None:
			if self.cat_selected == "":
				self.alt_ans_warning_string.set("Please click on\na category and click\nSelect Category.")
				self.alt_ans_warning_label.config(foreground="red")
				return
			if len(self.quest_box.curselection()) == 0:
				self.alt_ans_warning_string.set("Click on a question\nbelow and then click\nSelect Question.")
				self.alt_ans_warning_label.config(foreground="red")
				return
			question = self.quest_box.get(self.quest_box.curselection()[0])
			self.quest_selected = question
		
		category = self.cat_selected
		
		print("Category: " + category + " Question: " + question)
		answers = self.questions[category][question]
		self.fill_answers(question, category, answers)
	
	# fill_answers fills the text boxes with the information
	# (answers, category, and question) of the specified
	# category and question.
	def fill_answers(self, question, category, answers):
		print("fill answers")
		self.title_entry.insert(END, question)
		self.change_cat_entry.insert(END, category)
		self.cor_ans_entry.insert(END, answers[0])
		self.alt_ans_1_entry.insert(END, answers[1])
		if len(answers) > 2:
			self.alt_ans_2_entry.insert(END, answers[2])
			self.alt_ans_3_entry.insert(END, answers[3])
	
	# save_question is the callback function for the save
	# question button.  
	def save_question(self):
		print("save question")
		question = self.title_entry.get(0.0, END).strip()
		category = self.change_cat_entry.get()
		print("(question, category)", (question, category))
		answers = [self.cor_ans_entry.get(), self.alt_ans_1_entry.get(), 
		           self.alt_ans_2_entry.get(), self.alt_ans_3_entry.get()]
		answers = [i for i in answers if i != ''] # clear all blank answers
		
		# Check to make sure the user has inputted the
		# necessary data.  Display appropriate messages
		# otherwise.
		if question == "":
			print("blank question.  Setting warning")
			self.alt_ans_warning_string.set("Must enter a \nquestion \nto save.")
			self.alt_ans_warning_label.config(foreground="red")
			return
		elif category == "":
			print("blank category.  Setting warning")
			self.alt_ans_warning_string.set("Must enter a \ncategory\nto save.")
			self.alt_ans_warning_label.config(foreground="red")
			return
		elif len(answers) == 3 or len(answers) < 2:  # 0, 1, or 3 answers; must have 2 or 4
			print("invalid number of answers: " + str(answers))
			self.alt_ans_warning_string.set("Must enter 2 or 4\nanswers to save.")
			self.alt_ans_warning_label.config(foreground="red")
			return
		# If the previous if statements were all false,
		# continue to saving the question.  Update the
		# question if it is editing an existing question,
		# create a new one if it is new, or change the 
		# category if that is necessary.
		elif self.cat_selected == "" or self.quest_selected == "":
			# check if the category or question name has not been selected.
			# If it has not, that means the question is new.	
			print("either category or question not selected. (category, question):", (self.cat_selected, self.quest_selected))
			self.insert_question(question, category, answers)
			self.init_categories()
			self.alt_ans_warning_string.set("New question saved!")
			self.alt_ans_warning_label.config(foreground=self.font_color)
		elif self.cat_selected == category and self.quest_selected == question:
			# we just have to change the answer
			print("just changing answer")
			self.insert_question(question, category, answers)
			self.alt_ans_warning_string.set("Answers changed!")
			self.alt_ans_warning_label.config(foreground=self.font_color)
		else:
			print("deleting and re-inserting")
			self.delete_question(self.quest_selected, self.cat_selected)
			self.quest_selected = question
			self.cat_selected = category
			self.insert_question(question, category, answers)
			self.alt_ans_warning_string.set("Question updated!")
			self.alt_ans_warning_label.config(foreground=self.font_color)
		
		self.cat_selected = ""
		self.quest_selected = ""
		self.init_categories()
		self.save_all()
			
	# insert_question stores the question in the dict
	# in the proper format, such that 
	# self.questions[category][question] == answers.
	def insert_question(self, question, category, answers):
		print("insert question")
		if category not in self.questions:
			self.questions[category] = {}
		self.questions[category][question] = answers
		self.init_categories()
		self.fill_quest_box(category)
		self.fill_answers(question, category, answers)
		self.quest_selected = question
		self.cat_selected = category
		
	# undo_change is the callback function for the 
	# undo change button.  However, it is deprecated,
	# because questions save automatically.  It simply
	# re-selects the selected question.
	def undo_change(self):
		self.quest_select(q=self.quest_selected)
		
	# undo_all_changes is the callback function for the
	# undo all changes button.  However, it is deprecated,
	# because questions save automatically.  It simply
	# reloads the configuration file.
	def undo_all_changes(self):
		self.alt_ans_warning_string.set("Reloading\nQuestions!")
		self.alt_ans_warning_label.config(foreground=self.font_color)
		self.load_from_file(self.fname)
		self.init_categories()
		self.quest_selected = ""
		self.cat_selected = ""
	
	# delete_question is a helper function to delete a 
	# question.
	def delete_question(self, question, category):
		print("delete question")
		# Remove the question from the category.
		del self.questions[category][question]
		# If the category is now empty, delete the 
		# category as well.
		if len(self.questions[category]) == 0:
			print("deleting")
			del self.questions[category]
			self.init_categories()
			self.init_user_checkboxes()
		
	# delete_question_func is the callback function for
	# the delete question button.  
	def delete_question_func(self):
		if self.cat_selected == "":
			self.alt_ans_warning_string.set("Please click on\na question and click\nSelect Question.")
			self.alt_ans_warning_label.config(foreground="red")
			return			
		prompt = messagebox.askyesno("Delete Question?", "Are you sure you want to delete this question?\nQuestion: " + self.quest_selected)
		
		if prompt == True:
			self.delete_question(self.quest_selected, self.cat_selected)
			category = self.cat_selected
			self.init_categories()
			self.cat_selected = category
			self.fill_quest_box(category)
			self.save_all()
	
	# new_question is the callback function for the
	# new questino button.  It resets all displays 
	# and 
	def new_question(self):
		self.reset_display()
		self.quest_selected = ""
		self.cat_selected = ""
		self.alt_ans_warning_string.set("Starting\na New\nQuestion!")
		self.alt_ans_warning_label.config(foreground=self.font_color)

	# save_all is the callback function for the save
	# all button.  However, that use is deprecated because 
	# this function is now called whenever information 
	# changes.  
	def save_all(self, refresh=True):
		fout = open(self.fname, "w")
		self.print_questions(f=fout)
		fout.close()
		if refresh:
			self.init_categories()
			self.init_user_checkboxes()
	
	# load_from_file is called automatically in the __init__
	# function.  
	def load_from_file(self, fname): # right now the filename is "sample.txt"
		f = open(fname, "r")
		# Read the dumped json dict.
		ret = json.load(f)
		# Split the dict into its various parts and
		# assign them to the appropriate variables.  Also,
		# initialize some variables.
		self.questions = ret["questions"]
		if "default categories" in ret:
			self.builtin_categories = ret["default categories"]
			for key in self.builtin_categories:
				self.builtin_categories[key] = BooleanVar(value=self.builtin_categories[key])
				self.builtin_categories[key].trace(callback=self.trace_func, mode="w")
		else:
			self.builtin_categories = {}
			for i in ["binary to decimal", "decimal to binary",
			          "addition", "subtraction", "multiplication", "division"]: 
				self.builtin_categories[i] = BooleanVar(value=False)
				self.builtin_categories[i].trace(callback=self.trace_func, mode="w")
		if "user categories" in ret:
			self.user_categories = ret["user categories"]
			for key in self.user_categories:
				self.user_categories[key] = BooleanVar(value=self.user_categories[key])
		else:
			pass
		for key in self.user_categories:
			self.user_categories[key].trace("w", self.trace_func)
	
	# trace_func is a callback function called whenever the
	# BooleanVars (used to keep track of whether the user 
	# wants specific categories to be displayed in the game)
	# are changed.  
	def trace_func(self, u, v, w):
		# Save all information to the file every time a 
		# BooleanVar changes.  Do not refresh.
		self.save_all(refresh=False)
		pass
	
	# print_questions is used to print questions to a file,
	# or, if a file is unspecified, to stdout.
	def print_questions(self, f=stdout):
		# Create an empty dict to store all data.
		dic = {}
		dic["questions"] = self.questions
		dic["default categories"] = {}# = self.builtin_categories
		for key in self.builtin_categories:
			dic["default categories"][key] = self.builtin_categories[key].get()
		dic["user categories"] = {}
		for key in self.user_categories:
			dic["user categories"][key] = self.user_categories[key].get()
			
		# Dump that dict using json to the specified
		# file.  If the file is stdout, this will print
		# to stdout.  Set indent to 2 for easy parsing.
		json.dump(dic, f, indent=2)

# Create the glee_config instance.  Since the mainloop is 
# run from within the __init__ function, this both creates
# and starts the app.
x = glee_config()

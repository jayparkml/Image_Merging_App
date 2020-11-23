import os
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import * #__all__
from tkinter import filedialog # sub module.
from PIL import Image

root = Tk()
root.title("MERGE IMAGE FILES BY JAY") # Title

# Add file
def add_file():
    files = filedialog.askopenfilenames(title="Choose Your Image File",\
        filetypes=(('PNG File', "*.png"), ("All Files", "*.*")),\
            initialdir =r"C:\Users\parks\Desktop\PythonWorkspace") #Initial directory setup

    # Selected file
    for file in files:
        list_file.insert(END, file)

# Del file
def del_file():
    list_file.curselection()
    for index in reversed(list_file.curselection()): # current selected in reverse order(index) :reversed=not touching original
        list_file.delete(index)

# Save path Function(Folder)
def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected == '': # when cancel pressed
        return
    #print(folder_selected)
    txt_dest_path.delete(0,END)
    txt_dest_path.insert(0,folder_selected)

# Image Merge Function
def merge_image():
    # print("Width : ", cmb_width.get())
    # print("Spacing : ", cmb_spacing.get())
    # print("File Format : ", cmb_format.get())

    try:
        # Width
        img_width = cmb_width.get()
        if img_width == 'Original':
            img_width = -1 # when -1, keep original width
        else:
            img_width = int(img_width)

        # Spacing
        img_spacing = cmb_spacing.get()
        if img_spacing == 'Small':
            img_spacing = 30
        elif img_spacing == 'Normal':
            img_spacing = 60
        elif img_spacing == 'Large':
            img_spacing = 90
        else:
            img_spacing = 0

        # Format
        img_format = cmb_format.get().lower() #PNG, JPG, BMP -> png, jpg, bmp

        images = [Image.open(x) for x in list_file.get(0, END)]

        # Image size handling
        image_sizes = [] # (width1, height1), (width2, height2), ....
        if img_width > -1:
            # width change
            image_sizes=[(int(img_width), int(img_width * x.size[1] / x.size[0])) for x in images]
        else:
            pass # Use original size
            image_sizes = [(x.size[0], x.size[1]) for x in images]

        # formula
        # 100 * 60 image -> width to 80 then height?
        # (original width) : (original height) = (changed width) : (changed height)
        # 100 : 60 = 80 : 48
        # x   :  y = x' : y'
        # y' = x'y/x -> apply this
        # x = width = x.size[0]
        # y = height = size[1]
        # x' = img_width
        # y' = img_width * size[1] / size[0]

        widths,heights = zip(*image_sizes)

        # max width, total_height of images
        max_width, total_height = max(widths), sum(heights)

        # prepare sketch book
        if img_spacing > 0: # image spacing option applied
            total_height += (img_spacing * (len(images) -1 ))
        result_img = Image.new("RGB",(max_width, total_height), (255,255,255)) # white background
        y_offset = 0 # y coord

        for idx, img in enumerate(images):
            # if width is not original, adjustment needed
            if img_width > -1:
                img = img.resize(image_sizes[idx])

            result_img.paste(img, (0,y_offset))
            y_offset += (img.size[1] + img_spacing) # add height of image + spacing
            
            progress = (idx + 1) / len(images) * 100 # % value
            p_var.set(progress)
            progressbar.update()

        # Format Option
        file_name = "Jay_Photo." + img_format
        dest_path = os.path.join(txt_dest_path.get(), file_name)
        result_img.save(dest_path)
        msgbox.showinfo("Notice", "Process completed")
    except Exception as err: # Error handling
        msgbox.showerror("Error", err)

#Start function
def start():
    # option value check
    # print("Width : ", cmb_width.get())
    # print("Spacing : ", cmb_spacing.get())
    # print("File Format : ", cmb_format.get())

    # file list check(Error Message)
    if list_file.size() == 0:
        msgbox.showwarning("Alarm", "There is no image file")
        return

    # Save path check
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("Alarm", "Please select save path")
        return

    # Merging image
    merge_image()

# File Frame(add, delete)
file_frame = Frame(root)
file_frame.pack(fill='x', padx=5, pady=5 ) # making gap

btn_add_file = Button(file_frame, padx=5, pady=5, width=12, text="Add File", command=add_file)
btn_add_file.pack(side='left')

btn_del_file = Button(file_frame, padx=5, pady=5, width=12,text="Delete File", command=del_file)
btn_del_file.pack(side='right')

# List frame , Scrollbar
list_frame = Frame(root)
list_frame.pack(fill='both', padx=5, pady=5 )

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side='right', fill='y')

list_file=Listbox(list_frame, selectmode='extended', height=15, yscrollcommand=scrollbar.set)
list_file.pack(side='left',fill='both',expand=True)
scrollbar.config(command=list_file.yview)

# Save path frame
path_frame = LabelFrame(root,text="Save Path")
path_frame.pack(fill='x', padx=5, pady=5, ipady=5)

txt_dest_path = Entry(path_frame) # if this was Text -> "1.0", END
txt_dest_path.pack(side='left', fill='x', expand=True, padx=5, pady=5, ipady=4) #ipady = height change of inner entry frame

btn_dest_path = Button(path_frame, text='Search', width=10, command=browse_dest_path)
btn_dest_path.pack(side='right', padx=5, pady=5 )

# Option frame
option_frame = LabelFrame(root, text='Option')
option_frame.pack(padx=5, pady=5, ipady=5)

# Width
# Width Option Label
lbl_width = Label(option_frame, text='Width',width=8)
lbl_width.pack(side='left', padx=5, pady=5 )

# Width Option Combobox
opt_width = ['Original', '1024','800','640']
cmb_width = ttk.Combobox(option_frame, state='readonly', values=opt_width, width=10)
cmb_width.current(0)
cmb_width.pack(side='left', padx=5, pady=5 )

# Spacing
# Spacing Option Label
lbl_spacing = Label(option_frame, text='Spacing',width=8)
lbl_spacing.pack(side='left', padx=5, pady=5 )

# Spacing Option Combobox
opt_spacing = ['None', 'Small','Normal','Large']
cmb_spacing = ttk.Combobox(option_frame, state='readonly', values=opt_spacing, width=10)
cmb_spacing.current(0)
cmb_spacing.pack(side='left', padx=5, pady=5 )

# File Format
# File Format Option Label
lbl_format = Label(option_frame, text='File Format',width=8)
lbl_format.pack(side='left', padx=5, pady=5 )

# File Format Option Combobox
opt_format = ['PNG', 'JPG','BMP']
cmb_format = ttk.Combobox(option_frame, state='readonly', values=opt_format, width=10)
cmb_format.current(0)
cmb_format.pack(side='left', padx=5, pady=5 )

# Progress bar
progress_frame = LabelFrame(root,text='Progress')
progress_frame.pack(fill='x', padx=5, pady=5, ipady=5)

p_var= DoubleVar()
progressbar = ttk.Progressbar(progress_frame, maximum=100, variable=p_var)
progressbar.pack(fill='x', padx=5, pady=5 )

# Action Frame
action_frame = Frame(root)
action_frame.pack(fill='x', padx=5, pady=5 )

btn_close = Button(action_frame, padx=5, pady=5, width=12, text="Close", command=root.quit)
btn_close.pack(side='right', padx=5, pady=5 )

btn_start = Button(action_frame, padx=5, pady=5, width=12, text="Start", command=start)
btn_start.pack(side='right', padx=5, pady=5 )




root.resizable(False, False) # screen's width, height resize X

root.mainloop() # let screen not closed


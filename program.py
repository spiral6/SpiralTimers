from tkinter import *
from datetime import datetime, timedelta
from winotify import Notification, audio
import pystray
from pystray import MenuItem as item
from PIL import Image
from timer import Timer, Weekday
import json
import re

current_time = datetime.now()
root = Tk()
root.title("Timers App")
root.iconbitmap("itstimetostop.ico")
root.wm_attributes("-topmost", True)
transparent_color = "black"
root.wm_attributes("-transparentcolor", "#1E1E1E")
root.configure(background=transparent_color)
root.resizable(False, False)

# Hide menu bar from window
# root.overrideredirect(True) 

# lbl_hw = Label()
# lbl_hw = Label(root, name="lbl_hw", text="Hello World!", foreground="white", background=transparent_color)
# lbl_hw.grid(column=0, row=0)

# btn_exit = Button(root, text="Quit", command=lambda: root.destroy(), foreground="white", background=transparent_color)
# btn_exit.grid(column=0, row=1)

# lbl_originaltime = Label(root, name="lbl_originaltime", text="", foreground="white", background=transparent_color)
# lbl_originaltime.grid()
lbl_originaltime = None

# lbl_reset = Label(root, name="lbl_reset", text="Next reset time is: ", foreground="white", background=transparent_color)
# lbl_reset.grid(column=0, row=4)

canvas = Canvas(root, background=transparent_color, bd=0, highlightthickness=0, relief='ridge')
canvas.grid()
# rect = canvas.create_rectangle(0, 0, 0, 50, fill="green")
# rect3 = canvas.create_rectangle(0, 0, 200, 50, fill="red")
# canvas.lift(rect)
# rect2 = canvas.create_rectangle(0, 55, 200, 105, fill="black")

ct_state = False
timers_array = []
reset_labels_array = []

def load_timers():
    timers_file = json.load(open('timers.json'))
    global timers_array
    for i in range(len(timers_file)):
        name = timers_file[i]["Name"]
        weekday = Weekday[timers_file[i]["Day"]]
        pattern = r"(\d{2}):(\d{2}) (\w+)"
        matches = re.search(pattern, timers_file[i]["Time"])
        hour = int(matches.group(1))
        minute = int(matches.group(2))
        meridiem = matches.group(3)

        if meridiem == "PM" and hour < 12:
            hour += 12

        timers_array.append(Timer(name, weekday.value, hour, minute))

    global reset_labels_array
    for timer in timers_array:
        new_reset = Label(canvas, text=timer.name + ": " + timer.determine_reset(), foreground="white", background=transparent_color)
        new_reset.grid(sticky=W)
        reset_labels_array.append(new_reset)

def systray():
    # root.withdraw()
    icon_image = Image.open("itstimetostop.ico")
    def quit(icon, item):
        icon.stop()
        root.quit()
    def show(icon, item):
        # icon.stop()
        root.after(0, root.deiconify())
    def clickthrough(icon, item):
        global ct_state
        global transparent_color
        ct_state = not item.checked
        if (ct_state):
            transparent_color = "#1E1E1E"
            # print("Window should be click through now.")
            root.overrideredirect(True) 
        else:
            transparent_color = "black"
            # print("Window should NOT be click through now.")
            root.overrideredirect(False) 
        
        def change_color():
            global transparent_color
            global reset_labels_array
            global lbl_originaltime
            root.configure(bg=transparent_color)
            canvas.configure(bg=transparent_color)
            lbl_originaltime.configure(bg=transparent_color)
            for widget in reset_labels_array:
                widget.configure(background = transparent_color)
            
        root.after(0, change_color)

    
    icon=pystray.Icon("Timers App", icon_image, "My System Tray Icon", menu=(
        item("Show app", show, default=True), 
        item("Click-through", clickthrough, checked=lambda item: ct_state), 
        item("Exit app", quit))
    )
    icon.run_detached()

def current_timer():
    current_time_local = datetime.now()
    dt_string = current_time_local.strftime("%A %B %d, %Y %I:%M:%S %p")
    global lbl_originaltime
    if lbl_originaltime is None:
        lbl_originaltime = Label(canvas, name="lbl_originaltime", text="", foreground="white", background=transparent_color)
        lbl_originaltime.grid()
    lbl_originaltime.configure(text="Current time: " + dt_string)

    root.after(100, current_timer)

def calculate_resets():
    current_time_local = datetime.now()
    global reset_labels_array
    for i in range(0, len(timers_array)):
        timer = timers_array[i]
        timer.delta = current_time_local - timer.reset
        if timer.delta.total_seconds() >= 0:
            reset_labels_array[i].configure(text=timer.name + ": " + timer.determine_reset())
            show_notification(timer.name, "Reset happened!")

    root.after(0, draw_timers())
    root.after(1000 * 60, calculate_resets)

def draw_timers():
    global reset_labels_array
    for i in range(0, len(reset_labels_array)):
        label = reset_labels_array[i] 
        # print(label.widgetName + " " + str(label.winfo_width()))
        x0 = label.winfo_x()
        y0 = label.winfo_y()
        x1 = label.winfo_x() + label.winfo_width()
        y1 = label.winfo_y() + label.winfo_height()
        rect1 = canvas.create_rectangle(x0, y0, x1, y1, fill="red")
        canvas.lift(rect1)

def show_notification(title="test", msg="test"):
    toast = Notification(app_id="Timers App",
                     title=title,
                     msg=msg)
    toast.set_audio(audio.Default, loop=False)
    toast.show()

root.after(0, load_timers)
root.after(0, current_timer)
root.after(0, systray)
root.after(1000, calculate_resets)

root.protocol('WM_DELETE_WINDOW', lambda: root.withdraw())
root.mainloop()

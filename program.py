from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta
# from win10toast_click import ToastNotifier
from winotify import Notification, audio
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageTk


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

lbl_hw = Label()
lbl_hw = Label(root, name="lbl_hw", text="Hello World!", foreground="white", background=transparent_color)
lbl_hw.grid(column=0, row=0)

# btn_exit = Button(root, text="Quit", command=lambda: root.destroy(), foreground="white", background=transparent_color)
# btn_exit.grid(column=0, row=1)

lbl_originaltime = Label(root, name="lbl_originaltime", text="", foreground="white", background=transparent_color)
lbl_originaltime.grid(column=0, row=3)

lbl_reset = Label(root, name="lbl_reset", text="Next reset time is: ", foreground="white", background=transparent_color)
lbl_reset.grid(column=0, row=4)

canvas = Canvas(root, background=transparent_color, bd=0, highlightthickness=0, relief='ridge')
canvas.grid(column=0, row=2)
rect = canvas.create_rectangle(0, 0, 0, 50, fill="green")
rect3 = canvas.create_rectangle(0, 0, 200, 50, fill="red")
canvas.lift(rect)
rect2 = canvas.create_rectangle(0, 55, 200, 105, fill="black")

ct_state = False

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
            print("Window should be click through now.")
        else:
            transparent_color = "black"
            print("Window should NOT be click through now.")
        root.after(0, change_color)

    
    icon=pystray.Icon("Timers App", icon_image, "My System Tray Icon", menu=(
        item("Show app", show, default=True), 
        item("Click-through", clickthrough, checked=lambda item: ct_state), 
        item("Exit app", quit))
    )
    icon.run_detached()

def change_color():
    global transparent_color
    global widgets_array
    root.configure(bg=transparent_color)

    widgets_array = [lbl_hw, lbl_reset, lbl_originaltime, canvas]
    for w in widgets_array:
        w.configure(background = transparent_color)
    # lbl_hw.configure(bg=transparent_color)
    # lbl_originaltime.configure(bg=transparent_color)
    # lbl_reset.configure(bg=transparent_color)
    # canvas.configure(bg=transparent_color)

def loop_timer():
    x0, y0, x1, y1 = canvas.coords(rect)
    new_coords = [x0, y0, x1 + 5, y1]
    if new_coords[2] > 200:
        new_coords[2] = 0
    canvas.coords(rect, new_coords)
    root.after(100, loop_timer)

def on_timer_load():
    current_time_local = datetime.now()
    dt_string = current_time_local.strftime("%A %B %d, %Y %I:%M:%S %p")
    global lbl_originaltime
    lbl_originaltime = Label(root, text=dt_string, foreground="white", background=transparent_color)
    lbl_originaltime.grid(column=0, row=3)

    # print(dt_string)
    root.after(100, on_timer_load)

def show_notification():
    toast = Notification(app_id="Timers App",
                     title="Winotify Test Toast",
                     msg="New Notification!")
    toast.set_audio(audio.Default, loop=False)
    toast.set_audio()
    toast.show()

def determine_reset():
    reset_day_offset = 1 - current_time.weekday() # 1 = Tuesday
    if reset_day_offset < 0:
        reset_day_offset += 7
    reset_hour_offset = 12 - current_time.time().hour
    reset_min_offset = 0 - current_time.time().minute
    reset_sec_offset = 0 - current_time.time().second
    reset_time = current_time + timedelta(days=reset_day_offset, hours=reset_hour_offset, minutes=reset_min_offset, seconds=reset_sec_offset)

    # reset_day_offset = 1 - current_time.weekday() # 1 = Tuesday
    # if reset_day_offset < 0:
    #     reset_day_offset += 7
    # reset_hour_offset = 4 - current_time.time().hour
    # reset_min_offset = 30 - current_time.time().minute
    # reset_sec_offset = 0 - current_time.time().second
    # reset_time = current_time + timedelta(days=reset_day_offset, hours=reset_hour_offset, minutes=reset_min_offset, seconds=reset_sec_offset)

    reset_str = reset_time.strftime("%A %B %d, %Y %I:%M:%S %p")
    # print(reset_str)
    global lbl_reset
    lbl_reset = Label(root, text="Next reset time is: " + reset_str, foreground="white", background=transparent_color)
    lbl_reset.grid(column=0, row=4)


def on_timer_reset():
    pass        

root.after(0, loop_timer)
root.after(0, on_timer_load)
root.after(0, determine_reset)
# root.after(0, show_notification)
root.after(0, systray)

root.protocol('WM_DELETE_WINDOW', lambda: root.withdraw())
root.mainloop()

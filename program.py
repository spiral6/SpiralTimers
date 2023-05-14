from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta
# from win10toast_click import ToastNotifier
from winotify import Notification, audio

current_time = datetime.now()

root = Tk()
root.title("Timers App")
root.wm_attributes("-topmost", True)
root.wm_attributes("-transparentcolor", "#1E1E1E")
root.configure(background="#1E1E1E")
# root.overrideredirect(True)

Label(root, text="Hello World!", foreground="white", background="#1E1E1E").grid(column=0, row=0)
Button(root, text="Quit", command=root.destroy, foreground="white", background="#1E1E1E").grid(column=0, row=1)

canvas = Canvas(root, background="#1E1E1E", bd=0, highlightthickness=0, relief='ridge')
canvas.grid(column=0, row=2)
rect = canvas.create_rectangle(0, 0, 200, 50, fill="green")
rect2 = canvas.create_rectangle(0, 55, 200, 105, fill="black")



def loop_timer():
    x0, y0, x1, y1 = canvas.coords(rect)
    new_coords = [x0, y0, x1 - 5, y1]
    if new_coords[2] < x0:
        new_coords[2] = 200
    canvas.coords(rect, new_coords)
    root.after(100, loop_timer)

def on_timer_load():
    current_time_local = datetime.now()
    dt_string = current_time_local.strftime("%A %B %d, %Y %I:%M:%S %p")
    Label(root, text=dt_string, foreground="white", background="#1E1E1E").grid(column=0, row=3)
    # print(dt_string)
    root.after(100, on_timer_load)

def show_notification():
    # wintoast = ToastNotifier()
    # wintoast.show_toast("Timers App", "Here's a notification: " + current_time.strftime("%A %B %d, %Y %I:%M:%S %p"), threaded=True, duration=None)
    toast = Notification(app_id="Timers App",
                     title="Winotify Test Toast",
                     msg="New Notification!")
    toast.set_audio(audio.Default, loop=False)
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
    print(reset_str)
    Label(root, text="Next reset time is: " + reset_str, foreground="white", background="#1E1E1E").grid(column=0, row=4)



def on_timer_reset():
    pass        

root.after(0, loop_timer)
root.after(0, on_timer_load)
root.after(0, determine_reset)
# root.after(0, show_notification)

root.mainloop()

# def main():
#     print("Hello world!")

# if __name__ == "__main__":
#     main()
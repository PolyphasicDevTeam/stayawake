import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Dashboard(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="StayAwake")
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.add(vbox)
        vbox.set_margin_top(30)
        vbox.set_margin_start(60) 
        vbox.set_margin_end(60) 
        
        title = Gtk.Label()
        title.set_markup("<span font_size='30720'>StayAwake</span>")
        vbox.add(title)
                
        config_label = Gtk.Label(label="Configuration file path:")
        config_path_entry = Gtk.Entry()
        config_path_entry.set_text("~/.config/stayawake/stayawake.conf")
        vbox.add(config_label)
        vbox.add(config_path_entry)

        schedule_box = Gtk.ListBox()
        schedule_label = Gtk.Label(label="Current Schedule")
        schedule_name = Gtk.Label(label="E2-shortened")
        schedule_times = Gtk.Label(label="21:30-01:00 05:00-05:20 12:50-13:10")
        schedule_box.add(schedule_label)
        schedule_box.add(schedule_name)
        schedule_box.add(schedule_times) 
        schedule_box.get_row_at_index(0).do_activate(schedule_box.get_row_at_index(0))
        vbox.add(schedule_box)

        status_box = Gtk.ListBox()
        status_label = Gtk.Label(label="Current Time")
        status_time = Gtk.Label(label="7 October 2018, 09:00")
        status_sleep_next = Gtk.Label(label="Next Sleep: Nap Noon")
        status_time_remaining = Gtk.Label(label="Time Remaining: 3h 40m")
        status_box.add(status_label)
        status_box.add(status_time)
        status_box.add(status_sleep_next)
        status_box.add(status_time_remaining)
        status_box.get_row_at_index(0).do_activate(status_box.get_row_at_index(0))
        vbox.add(status_box)
        
        activity_box = Gtk.ListBox()
        activity_label = Gtk.Label(label="Activity Monitor")
        activity_timer_label = Gtk.Label(label="25.7s / 180s")
        monitor_suspend_label = Gtk.Label(label="*Dangerous* Suspend Monitor")
        
        suspend_button_box = Gtk.Box()
        suspend_button_5 = Gtk.Button(label="5min")
        suspend_button_15 = Gtk.Button(label="15min")
        suspend_button_30 = Gtk.Button(label="30min")
        suspend_button_box.add(suspend_button_5)
        suspend_button_box.add(suspend_button_15)
        suspend_button_box.add(suspend_button_30)
        suspend_button_box.set_halign(Gtk.Align.CENTER)

        activity_box.add(activity_label)
        activity_box.add(activity_timer_label)
        activity_box.add(monitor_suspend_label)
        activity_box.add(suspend_button_box)
        activity_box.get_row_at_index(0).do_activate(activity_box.get_row_at_index(0))
        vbox.add(activity_box)

window = Dashboard()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()


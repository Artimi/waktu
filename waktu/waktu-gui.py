#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

from gi.repository import Gtk, Gdk, GLib, GObject
from waktu import Waktu
import category
from timetracker import TimeTracker

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas

from datetime import timedelta, date, datetime
import time

TIMERANGES = ['Den', 'Týden', 'Měsíc', 'Rok', 'Věčnost']
(COLUMN_TEXT, COLUMN_PIXBUF) = range(2)


class WaktuGui(Gtk.Window):
    def __init__(self):
        self.waktu = Waktu()
        self.waktu.restoreCategories()
        self.waktu.restoreTodolist()
        self.waktu.restoreStats()
        self.waktu.restoreConfiguration()
        self.waktu.restoreActivities()
        #self.waktu.getTodolist().fillTodolist()
        #self.waktu.getCategories().fillCategory()

        self.trackingCore = TimeTracker(self.waktu.getStats(), self.waktu.getCategories(), self.waktu.getActivities(), self.waktu.getConfiguration())

        self.gladefile = 'waktu2.glade'
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object('mainwindow')
        self.window.set_icon_from_file('icon.png')
        self.aboutdialog = None
        self.deleteDialog = None
        self.lastMovedActivityTime = 0
        # self.set_comboboxes()
        self.set_category_treeview()
        self.set_activity_treeview()
        self.set_todolist_treeview()
        self.set_statistics_treeview()

        self.category_treeview.drag_dest_add_text_targets()
        self.category_treeview.drag_source_add_text_targets()
        self.activityTreeview.drag_dest_add_text_targets()
        self.activityTreeview.drag_source_add_text_targets()

        self.set_settings_tab()
        self.set_statistic_graph()
        self.set_defaults()

        self.current_category = None
        self.window.show_all()


    def run_core(self):
        self.trackingCore.start()

    def set_comboboxes(self):
        self.timerange_liststore = Gtk.ListStore(int, str)
        for index,l in enumerate(TIMERANGES):
            self.timerange_liststore.append([index, l])
        self.timerange_combobox = self.builder.get_object('statistics_timerange_combobox')
        self.timerange_combobox.set_model(self.timerange_liststore)
        cell = Gtk.CellRendererText()
        self.timerange_combobox.pack_start(cell, True)
        self.timerange_combobox.add_attribute(cell, 'text', 1)
        self.timerange_combobox.set_active(0)

    def set_statistics_treeview(self):
        self.statistics_treeview = self.builder.get_object('statistics_treeview')
        self.update_statistics_treestrore()
        cat_column = Gtk.TreeViewColumn("Kategorie",Gtk.CellRendererText(),text =0)
        time_column = Gtk.TreeViewColumn("Čas", Gtk.CellRendererText(),text=1)
        plan_column = Gtk.TreeViewColumn("Plán", Gtk.CellRendererText(),text=2)
        cat_column.set_expand(True)
        time_column.set_expand(True)
        plan_column.set_expand(True)
        self.statistics_treeview.append_column(cat_column)
        self.statistics_treeview.append_column(time_column)
        self.statistics_treeview.append_column(plan_column)


    def set_category_treeview(self):
        self.category_treeview = self.builder.get_object('category_treeview')
        self.update_category_treestore()
        cell = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Kategorie", cell, text=0)
        select = self.category_treeview.get_selection()
        select.connect("changed", self.on_tree_selection_changed)
        self.category_treeview.append_column(column)
        self.category_treeview.expand_all()

        self.category_treeview.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY | Gdk.DragAction.MOVE)
        self.category_treeview.connect("drag-data-received", self.on_drag_data_received)

        self.category_treeview.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, [], Gdk.DragAction.MOVE)
        self.category_treeview.connect("drag-data-get", self.on_drag_data_get)

    def set_todolist_treeview(self):
        self.todolist_treeview = self.builder.get_object('todolist_treeview')
        self.update_todolist()
        category_column = Gtk.TreeViewColumn("Kategorie",Gtk.CellRendererText(),text =0)
        time_column = Gtk.TreeViewColumn("Čas", Gtk.CellRendererText(),text=1)
        category_column.set_expand(True)
        time_column.set_expand(True)
        self.todolist_treeview.append_column(category_column)
        self.todolist_treeview.append_column(time_column)

    def update_todolist(self, date_td=date.today()):
        todolist = self.waktu.getTodolist().findTodolist(date_td)
        if todolist is not None:
            plans = todolist.getPlans()
        self.todolist_treestore = Gtk.ListStore(str, str)
        if todolist is not None:
            for key, value in plans.items():
                self.todolist_treestore.append([key, str(value.strftime("%H:%M"))])
        self.todolist_treeview.set_model(self.todolist_treestore)
        #update calendar
        self.todolist_calendar = self.builder.get_object('todolist_calendar')
        self.todolist_calendar.clear_marks()
        todolists = self.waktu.getTodolist().getTodolists()
        for day in todolists.keys():
            if day.month == date_td.month:
                self.todolist_calendar.mark_day(int(day.day))
        #todolist_category_combobox
        self.builder.get_object('todolist_time_entry').set_text("")
        categories = self.waktu.getCategories().getCategories()
        todolist_category_comboboxtext = self.builder.get_object('todolist_category_comboboxtext')
        todolist_category_comboboxtext.get_model().clear()
        for cat in categories:
            todolist_category_comboboxtext.append_text(cat.name)

    def on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        drop_info = widget.get_dest_row_at_pos(x, y)

        if drop_info:
            text = data.get_text().split(":")
            model = widget.get_model()
            path, position = drop_info

            pathStr = path.to_string().split(":")

            category_iter = model.get_iter(pathStr[0])

            if not self.waktu.getCategories().findCategory(model[category_iter][0]).containsActivity(text[-1]):
                model.append(category_iter,[text[-1]])
                self.waktu.getCategories().findCategory(model[category_iter][0]).add_activity(text[-1])

            if len(text) == 2:
                category_name_src = text[0]
                self.waktu.getCategories().findCategory(category_name_src).delete_activity(text[-1])

            self.waktu.storeCategories()

    def on_drag_data_received_remove(self, widget, drag_context, x, y, data, info, time):
        drop_info = widget.get_dest_row_at_pos(x, y)

        if drop_info:
            path, position = drop_info
            category, text = data.get_text().split(":")

            self.waktu.getCategories().findCategory(category).delete_activity(text)
            self.waktu.storeCategories()

    def set_activity_treeview(self):
        self.activityTreeview = self.builder.get_object('activity_treeview')
        self.update_activity_treestore()
        cell = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Aktivity", cell, text=0)
        self.activityTreeview.append_column(column)
        self.activityTreeview.expand_all()

        self.activityTreeview.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, [], Gdk.DragAction.COPY)
        self.activityTreeview.connect("drag-data-get", self.on_drag_data_get)

        self.activityTreeview.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.MOVE)
        self.activityTreeview.connect("drag-data-received", self.on_drag_data_received_remove)


    def on_drag_data_get(self, widget, drag_context, data, info, time):
        if self.lastMovedActivityTime == time:
            return

        self.lastMovedActivityTime = time

        selected_model, selected_iter = widget.get_selection().get_selected()
        selected_path = widget.get_model().get_path(selected_iter)

        text = widget.get_model().get_value(selected_iter, 0)

        if widget == self.category_treeview:
            pathStr = selected_path.to_string().split(":")

            if len(pathStr) == 1:
                return

            category_iter = selected_model.get_iter(pathStr[0])
            text = selected_model[category_iter][0]+':'+text

        data.set_text(text, -1)

    def update_statistics_treestrore(self):
        pie_summary = self.waktu.getStats().get_pie_summary()
        todolist = self.waktu.getTodolist().findTodolist(date.today())
        self.statistics_liststore = Gtk.ListStore(str, str, str)
        for index in range(len(pie_summary['categories'])):
            cat = pie_summary['categories'][index]
            time_str = str(timedelta(seconds=int(pie_summary['values'][index])))
            plan_str = ""
            if todolist is not None:
                if todolist.getPlans().has_key(cat):
                    plan_str = str(todolist.getPlans()[cat])
            self.statistics_liststore.append([cat, time_str, plan_str])
        self.statistics_treeview.set_model(self.statistics_liststore)

    def update_category_treestore(self):
        self.categories = self.waktu.getCategories()
        self.category_treestore = Gtk.TreeStore(str)
        for cat in self.categories.getCategories():
            category_iter = self.category_treestore.append(None, [cat.name])
            for activity in cat.activities:
                self.category_treestore.append(category_iter, [activity])
        self.category_treeview.set_model(self.category_treestore)
        self.category_treeview.expand_all()

    def update_activity_treestore(self):
        self.activities = self.waktu.getActivities()
        activityListstore = Gtk.ListStore(str)
        for activity in self.activities.getActivities():
            activityListstore.append([activity])
        self.activityTreeview.set_model(activityListstore)
        self.activityTreeview.expand_all()


    def notify_strong(self, notification):
        dialog = Gtk.MessageDialog(self,
                0,
                Gtk.MessageType.WARNING,
                Gtk.ButtonsType.OK,
                "Warning")
        dialog.format_secondary_text(notification)
        dialog.run()
        dialog.destroy()

    def set_statistic_graph(self):
        self.graph_figure = Figure()
        self.graph_figure.set_facecolor('white')
        # f.add_axes([0.1,0.1,0.8,0.8])
        self.graph = self.graph_figure.add_subplot(111)
        self.graph.set_aspect('equal')
        self.update_statistic()
        self.graph_canvas = FigureCanvas(self.graph_figure)
        self.builder.get_object('scrolledwindow4').add_with_viewport(self.graph_canvas)

    def update_statistic(self):
        self.graph.clear()
        pie_summary = self.waktu.getStats().get_pie_summary()
        total = sum(pie_summary['values'])
        self.graph.pie(pie_summary['values'],
            labels=pie_summary['categories'],
            autopct=lambda pct: '{p: 2.1f}% ({v:s})'.format(p=pct, v=str(timedelta(seconds=int(pct*total/100.0)))),
            colors=['#B02B2C', '#C79810', '#6BBA70', '#356AA0', '#D15600', '#73880A', '#3F4C6B', '#D01F3C'])
        self.update_statistics_treestrore()

    def set_defaults(self):
        """Set the default values"""
        mode = self.waktu.configuration.getValue("mode")
        state = self.waktu.configuration.getValue("state")

        modeText = self.builder.get_object('modeTextView')
        if mode == 0:
            self.builder.get_object('radio_mode_tracking').set_active(True)
            modeText.set_buffer(self.builder.get_object('modeTextBufferTrack'))
        else:
            self.builder.get_object('radio_mode_learning').set_active(True)
            modeText.set_buffer(self.builder.get_object('modeTextBufferLearn'))

        state_toggle = self.builder.get_object('state_toggle')
        if state == 0:
            state_toggle.set_active(False)
            state_toggle.set_label("Sledovani vypnuto")
        else:
            state_toggle.set_active(True)
            state_toggle.set_label("Sledovani zapnuto")

    def set_settings_tab(self):
        """Bind signals to radiobuttons on settings tab"""
        track_button = self.builder.get_object('radio_mode_tracking')
        track_button.connect("toggled", self.on_button_toggled, 0)

        learn_button = self.builder.get_object('radio_mode_learning')
        learn_button.connect("toggled", self.on_button_toggled, 1)


    #Main window signals
    def on_window1_destroy(self, object, data=None):
        print "quit with cross"
        self.trackingCore.stop()
        Gtk.main_quit()

    #Settings tab signals
    def on_button_toggled(self, button, _mode):
        if not button.get_active():
            return

        modeText = self.builder.get_object('modeTextView')
        if _mode == 0:
            modeText.set_buffer(self.builder.get_object('modeTextBufferTrack'))
            self.trackingCore.mode.clear()
        else:
            modeText.set_buffer(self.builder.get_object('modeTextBufferLearn'))
            self.trackingCore.mode.set()

        self.waktu.getConfiguration().setValue('mode', _mode)

    def on_state_toggled(self, button=None):
        if button.get_active():
            _state = 1
            button.set_label("Sledovani zapnuto")
        else:
            _state = 0
            button.set_label("Sledovani vypnuto")

        if _state:
            self.trackingCore.track.set()
        else:
            self.trackingCore.track.clear()

        self.waktu.getConfiguration().setValue('state', _state)


    def on_gtk_about_clicked(self,  data=None):
        if self.aboutdialog == None:
            self.aboutdialog = self.builder.get_object('aboutdialog')
        print 'settngs about clicked'
        self.response = self.aboutdialog.run()
        self.aboutdialog.hide()

    def on_category_tab_activate(self, _notebook=None, _object=None, _order=None):
        if _order == 0: #tab Stats
            self.update_statistic()
        elif _order == 1: #tab Todolist
            self.update_todolist()
        elif _order == 2: #tab Category
            self.update_activity_treestore()
            self.update_category_treestore()
        elif _order == 3: #tab Settings
            pass

    def on_settings_delete_button_clicked(self,  data=None):
        if self.deleteDialog == None:
            self.deleteDialog = self.builder.get_object('delete_dialog')
        self.response = self.deleteDialog.run()
        self.deleteDialog.hide()

    def on_delete_confirm(self, data=None):
        self.waktu.clearAllData()
        self.update_statistic_graph()
        self.update_activity_treestore()

    def on_delete_discard(self, data=None):
        pass

#Statistics panel signals
    def on_statistics_timerange_combobox_changed(self, combobox, data=None):
        print combobox.get_active()

    def on_statistics_categoriesfilter_combobox_changed(self, combobox, data=None):
        pass

#Todolist panel signals
    def on_todolist_calendar_day_selected(self, calendar, data=None):
        year, month, day = calendar.get_date()
        month += 1 # workaround, get_date() returns -1 month
        date_str = str(year) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2)
        self.builder.get_object('todolist_date_entry').set_text(date_str)
        date_td = date(year, month, day)
        self.update_todolist(date_td)

    def on_todolist_add_button_clicked(self, button, data=None):
        date_str = self.builder.get_object('todolist_date_entry').get_text()
        cat_str = self.builder.get_object('todolist_category_comboboxtext').get_active_id()
        time_str = self.builder.get_object('todolist_time_entry').get_text()
        if date_str != "" and cat_str is not None and time_str != "":
            date_td = datetime.strptime(date_str,"%Y-%m-%d").date()
            time_td = datetime.strptime(time_str, "%H:%M").time()
            todolist = self.waktu.getTodolist().findTodolist(date_td)
            if todolist is not None:
                todolist.addPlan({cat_str : time_td})
            else:
                self.waktu.getTodolist().addTodolist({date_td : {cat_str : time_td}})
        else:
            self.notify_strong("Musíte zadat všechny údaje!")
        self.on_todolist_calendar_day_selected(self.builder.get_object('todolist_calendar'))

    def on_todolist_delete_button_clicked(self, button, data=None):
        date_str = self.builder.get_object('todolist_date_entry').get_text()
        cat_str = self.builder.get_object('todolist_category_comboboxtext').get_active_id()
        if date_str != "" and cat_str is not None:
            date_td = datetime.strptime(date_str,"%Y-%m-%d").date()
            todolist = self.waktu.getTodolist().findTodolist(date_td)
            if todolist is not None:
                if todolist.removePlan(cat_str) == False:
                    self.notify_strong("Na " + str(date_td) + " není naplánována činnost " + cat_str+".")
            else:
                self.notify_strong("Na " + str(date_td)+" není naplánována činnost " + cat_str+".")
        else:
            self.notify_strong("Musíte zadat datum a kategorii!")
        self.on_todolist_calendar_day_selected(self.builder.get_object('todolist_calendar'))


    def on_todolist_treeview_selection_changed(self, selection):
       model, treeiter = selection.get_selected()
       if treeiter is not None:
           self.builder.get_object('todolist_category_comboboxtext').set_active_id(model[treeiter][0])
           self.builder.get_object('todolist_time_entry').set_text(model[treeiter][1])

#Categories panel signals
    def on_category_add_button_clicked(self, button, data=None):
        c = category.Category()
        c.name = self.builder.get_object('category_name_entry').get_text()
        if c.name == "":
            self.notify_strong("Nebyl vložen žádný název kategorie.")
            return None
        tarif = self.builder.get_object('category_tarif_entry').get_text()
        unit = self.builder.get_object('category_unit_entry').get_text()
        if tarif != "" and unit != "":
           c.tarif = (tarif, unit)
        else:
            c.tarif = ()
        self.waktu.getCategories().addCategory(c)
        self.update_category_treestore()

    def on_category_edit_button_clicked(self, button, data=None):
        print "edit button clicked"
        c = category.Category()
        c.name = self.builder.get_object('category_name_entry').get_text()
        tarif = self.builder.get_object('category_tarif_entry').get_text()
        unit = self.builder.get_object('category_unit_entry').get_text()
        if tarif != "" and unit != "":
           c.tarif = (tarif, unit)
        else:
            c.tarif = ()

        """If there is no category selected, skip it"""
        if self.current_category == None:
            return

        self.waktu.getCategories().editCategory(self.current_category, c)
        self.update_category_treestore()

    def on_category_delete_button_clicked(self, button, data=None):
        name = self.builder.get_object('category_name_entry').get_text()
        self.waktu.getCategories().deleteCategory(name)
        self.update_category_treestore()
        #TODO: move activities in category.

    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter != None:
            parent = model.iter_parent(treeiter)
            if parent is not None:
                treeiter = parent
            category_name = model[treeiter][0]
            self.current_category = None
            for cat in self.categories.getCategories():
                if category_name == cat.name:
                    self.current_category = cat
            if self.current_category is not None:
                self.builder.get_object('category_name_entry').set_text(self.current_category.name)
                if self.current_category.tarif is not None:
                    self.builder.get_object('category_tarif_entry').set_text(str(self.current_category.tarif[0]))
                    self.builder.get_object('category_unit_entry').set_text(str(self.current_category.tarif[1]))
                else:
                    self.builder.get_object('category_tarif_entry').set_text("")
                    self.builder.get_object('category_unit_entry').set_text("")

if __name__ == '__main__':
    GObject.threads_init()
    main = WaktuGui()
    Gdk.threads_init()

    main.run_core()
    Gdk.threads_enter()
    Gtk.main()
    Gdk.threads_leave()


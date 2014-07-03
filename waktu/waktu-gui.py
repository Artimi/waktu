#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

import logging
from gi.repository import Gtk, Gdk, GObject
from waktu import Waktu
import category
from timetracker import TimeTracker

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas

from datetime import timedelta, date, datetime

TIMERANGES = ['Den', 'Týden', 'Měsíc', 'Rok', 'Věčnost']
(COLUMN_TEXT, COLUMN_PIXBUF) = range(2)


class WaktuGui(Gtk.Window):
    def __init__(self):
        self.waktu = Waktu()
        self.waktu.restoreCategories()
        self.waktu.restoreStats()
        self.waktu.restoreConfiguration()
        self.waktu.restoreActivities()

        self.trackingCore = TimeTracker(self.waktu.stats,
                                        self.waktu.categories,
                                        self.waktu.activities,
                                        self.waktu.configuration)

        self.gladefile = 'waktu.glade'
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
        for index, l in enumerate(TIMERANGES):
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
        cat_column = Gtk.TreeViewColumn("Kategorie", Gtk.CellRendererText(), text=0)
        time_column = Gtk.TreeViewColumn("Čas", Gtk.CellRendererText(), text=1)
        plan_column = Gtk.TreeViewColumn("Plán", Gtk.CellRendererText(), text=2)
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

    def on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        drop_info = widget.get_dest_row_at_pos(x, y)

        if drop_info:
            text = data.get_text().split(":")
            model = widget.get_model()
            path, position = drop_info

            pathStr = path.to_string().split(":")

            category_iter = model.get_iter(pathStr[0])

            if text[-1] not in self.waktu.categories.findCategory(model[category_iter][0]):
                model.append(category_iter, [text[-1]])
                self.waktu.categories.findCategory(model[category_iter][0]).add_activity(text[-1])

            if len(text) == 2:
                category_name_src = text[0]
                self.waktu.categories.findCategory(category_name_src).delete_activity(text[-1])

            self.waktu.storeCategories()

    def on_drag_data_received_remove(self, widget, drag_context, x, y, data, info, time):
        drop_info = widget.get_dest_row_at_pos(x, y)

        if drop_info:
            path, position = drop_info
            cat, text = data.get_text().split(":")

            self.waktu.categories.findCategory(cat).delete_activity(text)
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
            text = selected_model[category_iter][0] + ':' + text

        data.set_text(text, -1)

    def update_statistics_treestrore(self):
        pie_summary = self.waktu.stats.get_pie_summary()
        self.statistics_liststore = Gtk.ListStore(str, str, str)
        for index in range(len(pie_summary['categories'])):
            cat = pie_summary['categories'][index]
            time_str = str(timedelta(seconds=int(pie_summary['values'][index])))
            plan_str = ""
            self.statistics_liststore.append([cat, time_str, plan_str])
        self.statistics_treeview.set_model(self.statistics_liststore)

    def update_category_treestore(self):
        self.categories = self.waktu.categories
        self.category_treestore = Gtk.TreeStore(str)
        for cat in self.categories.categories:
            category_iter = self.category_treestore.append(None, [cat.name])
            for activity in cat.activities:
                self.category_treestore.append(category_iter, [activity])
        self.category_treeview.set_model(self.category_treestore)
        self.category_treeview.expand_all()

    def update_activity_treestore(self):
        self.activities = self.waktu.activities
        activityListstore = Gtk.ListStore(str)
        for activity in self.activities:
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
        pie_summary = self.waktu.stats.get_pie_summary()
        total = sum(pie_summary['values'])
        self.graph.pie(pie_summary['values'], labels=pie_summary['categories'],
                       autopct=lambda pct: '{p: 2.1f}% ({v:s})'.format(p=pct, v=str(timedelta(seconds=int(pct * total / 100.0)))),
                       colors=['#B02B2C', '#C79810', '#6BBA70', '#356AA0', '#D15600', '#73880A', '#3F4C6B', '#D01F3C'])
        self.update_statistics_treestrore()

    def set_defaults(self):
        """Set the default values"""
        mode = self.waktu.configuration["mode"]
        state = self.waktu.configuration["state"]

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
        logging.debug("quit with cross")
        self.trackingCore.stop()
        Gtk.main_quit()

    #Settings tab signals
    def on_button_toggled(self, button, mode):
        if not button.get_active():
            return

        modeText = self.builder.get_object('modeTextView')
        if mode == 0:
            modeText.set_buffer(self.builder.get_object('modeTextBufferTrack'))
            self.trackingCore.mode.clear()
        else:
            modeText.set_buffer(self.builder.get_object('modeTextBufferLearn'))
            self.trackingCore.mode.set()

        self.waktu.configuration['mode'] = mode

    def on_state_toggled(self, button=None):
        if button.get_active():
            state = 1
            button.set_label("Sledovani zapnuto")
        else:
            state = 0
            button.set_label("Sledovani vypnuto")

        if state:
            self.trackingCore.track.set()
        else:
            self.trackingCore.track.clear()

        self.waktu.configuration['state'] = state

    def on_gtk_about_clicked(self,  data=None):
        if self.aboutdialog is None:
            self.aboutdialog = self.builder.get_object('aboutdialog')
        logging.debug('settngs about clicked')
        self.response = self.aboutdialog.run()
        self.aboutdialog.hide()

    def on_category_tab_activate(self, notebook=None, obj=None, order=None):
        if order == 0:  # tab Stats
            self.update_statistic()
        elif order == 1:  # tab Category
            self.update_activity_treestore()
            self.update_category_treestore()
        elif order == 2:  # tab Settings
            pass

    def on_settings_delete_button_clicked(self,  data=None):
        if self.deleteDialog is None:
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
        logging.debug(combobox.get_active())

    def on_statistics_categoriesfilter_combobox_changed(self, combobox, data=None):
        pass

#Categories panel signals
    def on_category_add_button_clicked(self, button, data=None):
        c = category.Category()
        c.name = self.builder.get_object('category_name_entry').get_text()
        if c.name == "":
            self.notify_strong("Nebyl vložen žádný název kategorie.")
            return None
        self.waktu.categories.addCategory(c)
        self.update_category_treestore()

    def on_category_edit_button_clicked(self, button, data=None):
        logging.debug("edit button clicked")
        c = category.Category()
        c.name = self.builder.get_object('category_name_entry').get_text()

        # If there is no category selected, skip it
        if self.current_category is None:
            return

        self.waktu.categories.editCategory(self.current_category, c)
        self.update_category_treestore()

    def on_category_delete_button_clicked(self, button, data=None):
        name = self.builder.get_object('category_name_entry').get_text()
        self.waktu.categories.deleteCategory(name)
        self.update_category_treestore()

    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            parent = model.iter_parent(treeiter)
            if parent is not None:
                treeiter = parent
            category_name = model[treeiter][0]
            self.current_category = None
            for cat in self.categories.categories:
                if category_name == cat.name:
                    self.current_category = cat
            if self.current_category is not None:
                self.builder.get_object('category_name_entry').set_text(self.current_category.name)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format="%(levelname)s, %(asctime)s, %(message)s")
    GObject.threads_init()
    main = WaktuGui()
    Gdk.threads_init()

    main.run_core()
    Gdk.threads_enter()
    Gtk.main()
    Gdk.threads_leave()

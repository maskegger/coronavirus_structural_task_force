# script auto-generated by phenix.molprobity


from __future__ import absolute_import, division, print_function
from six.moves import cPickle as pickle
from six.moves import range
try :
  import gobject
except ImportError :
  gobject = None
import sys

class coot_extension_gui(object):
  def __init__(self, title):
    import gtk
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    scrolled_win = gtk.ScrolledWindow()
    self.outside_vbox = gtk.VBox(False, 2)
    self.inside_vbox = gtk.VBox(False, 0)
    self.window.set_title(title)
    self.inside_vbox.set_border_width(0)
    self.window.add(self.outside_vbox)
    self.outside_vbox.pack_start(scrolled_win, True, True, 0)
    scrolled_win.add_with_viewport(self.inside_vbox)
    scrolled_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

  def finish_window(self):
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window(self, *args):
    self.window.destroy()
    self.window = None

  def confirm_data(self, data):
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists(self, data):
    import gtk
    for data_key in self.data_keys :
      outlier_list = data[data_key]
      if outlier_list is None or len(outlier_list) == 0 :
        continue
      else :
        frame = gtk.Frame(self.data_titles[data_key])
        vbox = gtk.VBox(False, 2)
        frame.set_border_width(6)
        frame.add(vbox)
        self.add_top_widgets(data_key, vbox)
        self.inside_vbox.pack_start(frame, False, False, 5)
        list_obj = residue_properties_list(
          columns=self.data_names[data_key],
          column_types=self.data_types[data_key],
          rows=outlier_list,
          box=vbox)

# Molprobity result viewer
class coot_molprobity_todo_list_gui(coot_extension_gui):
  data_keys = [ "rama", "rota", "cbeta", "probe" ]
  data_titles = { "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes" }
  data_names = { "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"] }
  if (gobject is not None):
    data_types = { "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT] }
  else :
    data_types = dict([ (s, []) for s in ["rama","rota","cbeta","probe"] ])

  def __init__(self, data_file=None, data=None):
    assert ([data, data_file].count(None) == 1)
    if (data is None):
      data = load_pkl(data_file)
    if not self.confirm_data(data):
      return
    coot_extension_gui.__init__(self, "MolProbity to-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets(self, data_key, box):
    import gtk
    if data_key == "probe" :
      hbox = gtk.HBox(False, 2)
      self.dots_btn = gtk.CheckButton("Show Probe dots")
      hbox.pack_start(self.dots_btn, False, False, 5)
      self.dots_btn.connect("toggled", self.toggle_probe_dots)
      self.dots2_btn = gtk.CheckButton("Overlaps only")
      hbox.pack_start(self.dots2_btn, False, False, 5)
      self.dots2_btn.connect("toggled", self.toggle_all_probe_dots)
      self.dots2_btn.set_active(True)
      self.toggle_probe_dots()
      box.pack_start(hbox, False, False, 0)

  def toggle_probe_dots(self, *args):
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots(self, *args):
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui(coot_extension_gui):
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list(object):
  def __init__(self, columns, column_types, rows, box,
      default_size=(380,200)):
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)):
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns):
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      self.listmodel.get_model().append(row)
    self.listctrl.connect("cursor-changed", self.OnChange)
    sw = gtk.ScrolledWindow()
    w, h = default_size
    if len(rows) > 10 :
      sw.set_size_request(w, h)
    else :
      sw.set_size_request(w, 30 + (20 * len(rows)))
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    box.pack_start(sw, False, False, 5)
    inside_vbox = gtk.VBox(False, 0)
    sw.add(self.listctrl)

  def OnChange(self, treeview):
    import coot # import dependency
    selection = self.listctrl.get_selection()
    (model, tree_iter) = selection.get_selected()
    if tree_iter is not None :
      row = model[tree_iter]
      xyz = row[-1]
      if isinstance(xyz, tuple) and len(xyz) == 3 :
        set_rotation_centre(*xyz)
        set_zoom(30)
        graphics_draw()

def show_probe_dots(show_dots, overlaps_only):
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects):
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects):
      set_display_generic_object(object_number, 0)

def load_pkl(file_name):
  pkl = open(file_name, "rb")
  data = pickle.load(pkl)
  pkl.close()
  return data

data = {}
data['rama'] = []
data['omega'] = [('H', ' 147 ', 'PRO', None, (-0.979, 7.049999999999998, -2.33)), ('H', ' 149 ', 'PRO', None, (2.4909999999999997, 8.940999999999997, -7.058)), ('L', '   8 ', 'PRO', None, (-7.177999999999999, 36.824, -21.551)), ('L', '  95 ', 'PRO', None, (-5.048, 40.158, 0.813)), ('L', ' 141 ', 'PRO', None, (-9.185999999999998, 23.247, -30.951))]
data['rota'] = [('A', ' 382 ', 'VAL', 0.22373828974083673, (-9.305, 61.60599999999999, 28.211999999999993)), ('A', ' 450 ', 'ASN', 0.0, (5.364000000000001, 64.03899999999999, -2.698999999999999)), ('A', ' 469 ', 'SER', 0.26509314423705566, (17.275, 58.76199999999999, 7.095999999999999)), ('A', ' 478 ', 'THR', 0.24439551405186638, (27.157, 42.982, 0.766)), ('A', ' 493 ', 'GLN', 0.07683927454887035, (8.144, 54.606999999999985, -1.051)), ('H', ' 120 ', 'SER', 0.06318586932292251, (-7.061000000000002, -2.1189999999999993, -9.405999999999997)), ('H', ' 138 ', 'LEU', 0.23842719417378166, (-7.764000000000003, 0.487, -26.188999999999993)), ('H', ' 178 ', 'LEU', 0.0640880213064491, (-6.426999999999998, 7.369999999999998, -14.021)), ('L', '  14 ', 'PHE', 0.2080866082388881, (3.146999999999999, 31.294, -32.711)), ('L', '  22 ', 'THR', 0.05976976077863843, (-4.905, 41.80099999999999, -19.643)), ('L', '  33 ', 'LEU', 0.14841011395154718, (0.8720000000000002, 45.15099999999999, -9.576)), ('L', '  42 ', 'ASN', 0.1725916386054468, (8.128000000000004, 24.91399999999999, -11.519999999999996)), ('L', '  63 ', 'SER', 0.28309965757948696, (6.883000000000003, 44.699, -20.841)), ('L', ' 105 ', 'GLU', 0.10258647517345909, (-0.4269999999999998, 27.653, -25.737999999999996)), ('L', ' 162 ', 'SER', 0.2706883640820928, (-8.935, 14.831999999999997, -17.349))]
data['cbeta'] = []
data['probe'] = [(' A 449  TYR  HA ', ' A 494  SER  OG ', -0.663, (4.467, 59.68, -5.031)), (' H 129  LYS  H  ', ' H 129  LYS  HD3', -0.602, (-17.177, -5.11, -31.458)), (' L 213  GLU  HG3', ' L 213  GLU  O  ', -0.594, (-24.359, -7.32, -28.608)), (' A 503  VAL  HA ', ' A 506  GLN  HG3', -0.543, (-10.538, 56.347, -1.235)), (' L 125  LEU  O  ', ' L 183  LYS  HE2', -0.537, (-20.354, -6.255, -10.213)), (' H  29  VAL HG13', ' H  34  MET  HG3', -0.534, (12.942, 35.515, 5.641)), (' L  37  GLN  HB2', ' L  47  LEU HD11', -0.52, (6.212, 35.48, -17.168)), (' H  82  MET  HB3', ' H  82C LEU HD21', -0.515, (-0.457, 23.465, 7.975)), (' L  34  ALA  HB2', ' L  91  LEU HD11', -0.496, (3.864, 42.837, -7.696)), (' A 376  THR  HB ', ' A 435  ALA  HB3', -0.494, (-9.293, 59.781, 11.319)), (' L 145  LYS  HB3', ' L 197  THR  HB ', -0.494, (-19.593, 19.967, -26.626)), (' A 379  CYS  HB3', ' A 382  VAL HG23', -0.467, (-9.062, 61.588, 24.594)), (' L 142  ARG  NH1', ' L 163 BVAL HG21', -0.45, (-7.436, 20.956, -19.391)), (' H  82  MET  HE1', ' H 109  VAL HG21', -0.45, (2.611, 21.957, 4.285)), (' A 439  ASN  O  ', ' A 443  SER  OG ', -0.449, (-7.155, 63.835, -4.352)), (' L 113  PRO  HB3', ' L 139  PHE  HB3', -0.44, (-10.649, 16.06, -30.523)), (' A 431  GLY  HA2', ' A 515  PHE  CD2', -0.439, (-4.826, 63.989, 24.891)), (' A 493  GLN  HG3', ' H 334  HOH  O  ', -0.437, (6.737, 50.521, -2.381)), (' A 444 BLYS  NZ ', ' A 448  ASN  ND2', -0.432, (-0.628, 66.017, -4.281)), (' A 444 BLYS  HZ1', ' A 448  ASN  ND2', -0.423, (-0.707, 66.574, -4.084))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)

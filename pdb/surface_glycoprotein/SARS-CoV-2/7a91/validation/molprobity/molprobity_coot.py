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
data['omega'] = [('A', ' 527 ', 'PRO', None, (198.933, 203.51299999999998, 198.13)), ('D', ' 146 ', 'PRO', None, (202.415, 231.392, 271.655))]
data['rota'] = [('D', ' 432 ', 'ASN', 0.005907385433106919, (234.17100000000013, 245.157, 254.217)), ('D', ' 474 ', 'MET', 0.08450899926991229, (221.054, 217.21300000000005, 287.25)), ('D', ' 540 ', 'HIS', 0.13248169510438917, (231.63400000000013, 233.88999999999996, 251.81299999999993)), ('A', ' 336 ', 'CYS', 0.10938442148482935, (192.27, 199.528, 205.039)), ('A', ' 358 ', 'ILE', 0.0, (194.62, 193.383, 207.231)), ('A', ' 546 ', 'LEU', 0.03118623175882045, (209.809, 196.254, 191.435))]
data['cbeta'] = []
data['probe'] = [(' A 578  ASP  OD1', ' A 583  GLU  N  ', -0.734, (199.309, 188.706, 183.131)), (' A 362  VAL HG23', ' A 526  GLY  HA3', -0.638, (197.421, 200.77, 197.281)), (' D 168  TRP  HE1', ' D 502  SER  HB3', -0.602, (211.467, 222.967, 278.512)), (' A 393  THR  O  ', ' A 523  THR  OG1', -0.565, (199.095, 190.342, 201.518)), (' D 269  ASP  OD1', ' D 270  MET  N  ', -0.558, (214.992, 230.299, 273.437)), (' D  85  LEU  O  ', ' D  94  LYS  NZ ', -0.555, (224.727, 188.043, 254.11)), (' D 247  LYS  HB3', ' D 282  THR HG22', -0.543, (227.797, 241.989, 272.311)), (' D 261  CYS  HB2', ' D 488  VAL HG13', -0.532, (228.715, 230.338, 283.339)), (' D  32  PHE  CD1', ' D  76  GLN  HG2', -0.527, (206.797, 193.395, 251.277)), (' A 329  PHE  HE2', ' A 528  LYS  HD3', -0.507, (203.331, 202.846, 192.257)), (' D 402  GLU  HB3', ' D 518  ARG  HD3', -0.503, (220.441, 220.518, 257.63)), (' A 457  ARG  NH1', ' A 467  ASP  OD1', -0.5, (203.999, 181.303, 229.579)), (' A 503  VAL  HA ', ' A 506  GLN HE21', -0.475, (202.945, 211.017, 232.589)), (' D 204  ARG  HD2', ' D 219  ARG  O  ', -0.473, (228.534, 204.597, 268.02)), (' D 187  LYS  HB3', ' D 199  TYR  CD2', -0.466, (215.626, 203.954, 273.684)), (' D 177  ARG  HB3', ' D 178  PRO  HD3', -0.465, (209.983, 213.857, 287.715)), (' D 320  LEU  HB3', ' D 321  PRO  HD2', -0.465, (218.878, 218.401, 237.399)), (' D 457  GLU  HG2', ' D 513  ILE  HB ', -0.464, (224.03, 213.157, 268.103)), (' D 284  PRO  HB3', ' D 594  TRP  CH2', -0.458, (232.263, 243.548, 265.067)), (' D 476  LYS  O  ', ' D 480  MET  HG2', -0.457, (227.544, 217.476, 282.753)), (' A 418  ILE HD13', ' A 422  ASN HD22', -0.448, (205.314, 192.885, 230.61)), (' A 421  TYR  CD1', ' A 457  ARG  HB3', -0.446, (208.989, 185.333, 231.956)), (' D 439  LEU  HA ', ' D 439  LEU HD23', -0.442, (228.88, 235.92, 257.832)), (' D 291  ILE  O  ', ' D 291  ILE HG13', -0.436, (219.823, 241.516, 251.659)), (' D 455  MET  HB3', ' D 455  MET  HE3', -0.436, (225.435, 220.804, 275.204)), (' D 398  GLU  HG3', ' D 514  ARG  HG2', -0.435, (221.069, 212.438, 261.158)), (' D  93  VAL HG12', ' D  97  LEU HD12', -0.435, (218.715, 190.407, 249.791)), (' D 315  PHE  HA ', ' D 318  VAL HG12', -0.43, (220.624, 224.74, 239.111)), (' A 341  VAL HG23', ' A 356  LYS  HZ2', -0.429, (193.117, 197.171, 212.008)), (' D 308  PHE  CZ ', ' D 333  LEU HD22', -0.427, (206.402, 227.776, 246.16)), (' D 336  PRO  HG2', ' D 340  GLN  O  ', -0.425, (192.719, 227.341, 252.929)), (' A 431  GLY  HA3', ' A 513  LEU  O  ', -0.423, (206.102, 196.541, 211.745)), (' D 482  ARG HH21', ' D 489  GLU  CD ', -0.416, (225.168, 226.186, 288.133)), (' D 524  GLN  HG2', ' D 583  PRO  HG2', -0.415, (235.152, 220.818, 254.305)), (' D 230  PHE  HA ', ' D 233  ILE HG22', -0.414, (234.748, 221.413, 267.495)), (' A 409  GLN  OE1', ' A 418  ILE  HB ', -0.412, (209.436, 195.97, 229.013)), (' D 209  VAL HG11', ' D 565  PRO  HB3', -0.412, (230.068, 201.901, 253.297)), (' D 403  ALA  O  ', ' D 407  ILE HG23', -0.409, (224.403, 222.233, 251.382)), (' D  96  GLN  HG2', ' D 391  LEU  HB2', -0.409, (215.427, 198.231, 249.5)), (' D 529  LEU HD21', ' D 554  LEU HD22', -0.407, (226.77, 220.888, 244.536)), (' A 355  ARG  NH2', ' A 398  ASP  OD2', -0.407, (201.812, 190.886, 215.865)), (' A 382  VAL HG11', ' A 387  LEU  HB3', -0.407, (207.749, 200.771, 204.851)), (' D 215  TYR  HE2', ' D 568  LEU HD13', -0.401, (233.771, 204.428, 247.337)), (' D 527  GLU  OE1', ' D 583  PRO  HG3', -0.401, (237.174, 222.953, 252.747))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)

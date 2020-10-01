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
data['rama'] = [('A', ' 218 ', 'LYS', 0.009640764443272467, (-42.928000000000004, 24.941999999999986, -57.185)), ('A', ' 219 ', 'LEU', 0.015012821335479406, (-41.56799999999999, 28.157999999999987, -58.877999999999986)), ('A', ' 351 ', 'THR', 0.04808849921478914, (-11.017999999999994, 12.125999999999989, -50.139)), ('A', ' 484 ', 'VAL', 0.013274658562137371, (-32.541999999999994, 37.03299999999999, -80.69)), ('B', ' 103 ', 'VAL', 0.08884562351020737, (1.5830000000000002, -1.9320000000000057, -27.195999999999994))]
data['omega'] = []
data['rota'] = [('A', '   7 ', 'LEU', 0.25619477249024186, (6.410000000000008, 41.53099999999998, -61.962)), ('A', '  12 ', 'THR', 0.005158041233780662, (7.072000000000012, 46.61499999999999, -51.367)), ('A', '  46 ', 'ASN', 0.13645127703410093, (-2.0289999999999937, 54.78399999999998, -46.202)), ('A', '  51 ', 'ASN', 0.016424023657550083, (-2.8509999999999938, 64.94499999999996, -46.80499999999999)), ('A', '  81 ', 'PHE', 0.07394030621402883, (10.635000000000002, 64.964, -52.711999999999996)), ('A', '  86 ', 'ASN', 0.2409117156232396, (14.30900000000001, 58.71999999999997, -61.48299999999999)), ('A', ' 162 ', 'GLU', 0.036924452032724535, (-42.437000000000005, 26.172999999999984, -68.691)), ('A', ' 173 ', 'ARG', 0.0, (-31.098999999999997, 40.35499999999998, -71.29699999999998)), ('A', ' 209 ', 'VAL', 0.1094752847547471, (-39.52900000000001, 29.586999999999982, -71.897)), ('A', ' 255 ', 'THR', 0.0, (3.8419999999999987, -3.7510000000000154, -63.089999999999996)), ('A', ' 344 ', 'ASP', 0.07069628966351287, (-23.262000000000004, 7.486999999999989, -58.393999999999984)), ('A', ' 530 ', 'THR', 0.016319203132297844, (-30.632000000000005, 17.195999999999984, -79.828)), ('A', ' 572 ', 'ILE', 0.23865898505389885, (-23.007000000000005, 11.396999999999979, -90.51299999999999)), ('A', ' 592 ', 'ILE', 0.2410153740096111, (-31.792999999999992, 18.262999999999977, -103.68899999999996)), ('B', '   8 ', 'CYS', 0.1062193701804152, (7.549000000000003, 3.446999999999993, -33.46)), ('B', '  35 ', 'ILE', 0.24899346699064367, (-1.2750000000000012, -11.520000000000003, -31.58599999999999)), ('B', '  68 ', 'MET', 0.0016792065443564635, (4.605, -12.71100000000001, -55.07099999999999)), ('B', '  96 ', 'THR', 0.026876741948236457, (14.377000000000004, -0.7430000000000057, -39.748)), ('B', ' 103 ', 'VAL', 0.1484216708792606, (1.5830000000000002, -1.9320000000000057, -27.195999999999994)), ('B', ' 124 ', 'ASN', 0.08592932566820026, (-5.961, 12.010999999999992, -22.983999999999998)), ('B', ' 144 ', 'THR', 0.10069251578906847, (-20.057999999999996, 5.721999999999995, -38.382)), ('B', ' 179 ', 'ASN', 0.19652175754247908, (-27.367, 18.067999999999994, -30.415999999999993)), ('B', ' 188 ', 'THR', 0.222616091317195, (-35.162000000000006, 13.673999999999992, -57.683)), ('B', ' 192 ', 'LYS', 0.0, (-31.37600000000001, 13.286999999999988, -54.14099999999999)), ('B', ' 195 ', 'ILE', 0.04336114940904385, (-32.74300000000001, 20.838999999999988, -48.76099999999999)), ('B', ' 247 ', 'VAL', 0.20058364157586953, (12.902000000000001, 36.22, -21.124)), ('B', ' 264 ', 'SER', 0.11893996018283852, (-6.142999999999999, 45.357, -16.313)), ('B', ' 353 ', 'GLU', 0.20108055693798615, (-6.424999999999999, 40.118, -43.606)), ('B', ' 484 ', 'VAL', 0.003150532575091347, (-37.731999999999985, 8.332999999999993, -25.831999999999997)), ('B', ' 592 ', 'ILE', 0.28265948676952346, (-43.20899999999998, 24.895, -1.135))]
data['cbeta'] = [('A', ' 530 ', 'THR', ' ', 0.25786410666481946, (-31.805000000000007, 18.176999999999985, -79.815)), ('B', ' 279 ', 'THR', ' ', 0.2610903490880454, (-3.9589999999999974, 27.679999999999986, -20.675))]
data['probe'] = [(' B   2  VAL  N  ', ' B 801  HOH  O  ', -0.933, (1.64, 1.703, -48.947)), (' B  12  THR HG22', ' B  14  LEU  H  ', -0.885, (3.893, -0.525, -43.061)), (' B  12  THR HG21', ' B  25  LEU  O  ', -0.78, (3.429, -1.874, -40.553)), (' B 510  VAL HG21', ' B 541  TYR  CD1', -0.75, (-32.758, 34.096, -21.714)), (' B 279  THR  HB ', ' B 429  MET  HE2', -0.695, (-5.488, 27.217, -20.934)), (' A 510  VAL HG21', ' A 541  TYR  CD1', -0.66, (-26.35, 10.705, -80.283)), (' B  46  ASN  ND2', ' B 805  HOH  O  ', -0.655, (-0.169, -8.635, -54.705)), (' B 271  LYS  NZ ', ' B 806  HOH  O  ', -0.639, (1.95, 31.356, -15.897)), (' A 215  THR HG22', ' B 193  VAL HG21', -0.629, (-31.492, 20.605, -55.557)), (' B 195  ILE  O  ', ' B 195  ILE HG23', -0.622, (-34.284, 20.915, -47.147)), (' B 512  ILE  O  ', ' B 546  PHE  HA ', -0.593, (-33.993, 26.407, -15.254)), (' B 124  ASN  OD1', ' B 381  ASN  ND2', -0.574, (-7.504, 14.551, -25.553)), (' B 474 BMET  HG2', ' B 590  LEU  HB2', -0.563, (-38.538, 28.081, -3.197)), (' B 277  TYR  HA ', ' B 396  TYR  O  ', -0.562, (0.465, 30.323, -26.759)), (' B 280  LEU HD11', ' B 438  LEU  HG ', -0.56, (-8.977, 35.323, -18.112)), (' A 368  ALA  O  ', ' A 393  ALA  HA ', -0.558, (1.553, 14.08, -56.435)), (' A  60  VAL  HB ', ' A 871  HOH  O  ', -0.551, (-0.629, 57.721, -56.645)), (' B  12  THR  OG1', ' B  26  CYS  HA ', -0.547, (6.093, -0.988, -39.946)), (' B 425  VAL HG12', ' B 429  MET  HE3', -0.541, (-6.757, 25.389, -22.175)), (' A 445  PRO  HB3', ' A 468  SER  HB3', -0.539, (-17.971, 4.71, -91.928)), (' A 512  ILE  O  ', ' A 546  PHE  HA ', -0.539, (-25.902, 18.968, -87.284)), (' B 262  PHE  CE2', ' B 297  LEU HD12', -0.533, (-9.594, 47.266, -26.643)), (' A 519  ASN  HB3', ' A 530  THR HG23', -0.529, (-30.782, 20.262, -79.825)), (' B 220  ASN  O  ', ' B 223  ASP  OD2', -0.522, (-41.17, 16.347, -49.31)), (' B 474 AMET  SD ', ' B 495  VAL HG11', -0.522, (-40.898, 24.96, -6.27)), (' B   8  CYS  SG ', ' B  99  GLY  N  ', -0.516, (9.058, -0.281, -32.613)), (' A 277  TYR  HA ', ' A 396  TYR  O  ', -0.516, (3.109, 16.269, -65.887)), (' B 252  LEU  HB3', ' B 299  TYR  CD1', -0.513, (2.636, 41.823, -29.286)), (' A 352  LEU HD11', ' B 234  PRO  HD3', -0.512, (-7.789, 11.646, -44.117)), (' B 376  ILE HG22', ' B 400  GLY  HA3', -0.509, (-11.307, 27.196, -23.052)), (' A 565  ILE  HA ', ' A 572  ILE HD13', -0.502, (-19.614, 14.786, -88.097)), (' A 448  ILE HD13', ' A 565  ILE  O  ', -0.498, (-17.645, 11.903, -88.166)), (' A 518  GLN  HA ', ' A 518  GLN  OE1', -0.487, (-32.4, 25.807, -86.184)), (' B  69  SER  HB2', ' B  71  TYR  CE2', -0.485, (0.122, -16.044, -54.523)), (' B 477  LYS  NZ ', ' B 551  GLU  OE2', -0.484, (-33.68, 13.969, -4.264)), (' B 195  ILE  CG2', ' B 195  ILE  O  ', -0.48, (-34.175, 20.957, -47.387)), (' B 371  VAL HG23', ' B 393  ALA  HB2', -0.48, (-1.176, 31.226, -34.889)), (' A  13  SER  OG ', ' A  44  SER  OG ', -0.479, (2.814, 50.951, -48.248)), (' B   8  CYS  SG ', ' B  99  GLY  O  ', -0.479, (8.765, 0.392, -31.811)), (' A 139  LYS  O  ', ' A 143  GLU  HG2', -0.479, (-15.27, 36.461, -62.459)), (' B 304  ILE  HA ', ' B 370  ILE  O  ', -0.478, (-3.15, 35.69, -34.279)), (' B 386  VAL  O  ', ' B 390  ARG  HG2', -0.478, (-5.086, 22.604, -38.644)), (' A   5  CYS  SG ', ' A  26  CYS  N  ', -0.475, (6.289, 45.905, -57.455)), (' A  13  SER  O  ', ' A  44  SER  HA ', -0.474, (1.652, 50.15, -50.079)), (' A 151  ILE HG12', ' A 226  VAL HG22', -0.474, (-31.702, 39.648, -60.496)), (' A 367  THR  HA ', ' A 392  ARG  O  ', -0.474, (-0.398, 15.92, -53.785)), (' B 372  VAL HG13', ' B 399  ILE HD12', -0.468, (-8.289, 33.851, -26.923)), (' B 154  VAL HG12', ' B 221  VAL  HA ', -0.468, (-43.919, 14.903, -45.986)), (' A 451  THR HG21', ' A 585  LEU HD23', -0.467, (-15.36, 17.013, -93.45)), (' B 157  VAL  HA ', ' B 163  LEU HD23', -0.465, (-44.973, 18.312, -42.225)), (' B 372  VAL  CG1', ' B 399  ILE HD12', -0.462, (-8.552, 33.814, -27.499)), (' B  13  SER  HB2', ' B  92  LEU  HB2', -0.457, (6.578, -1.842, -47.217)), (' A  19  CYS  HB2', ' A  23  PRO  HD2', -0.456, (-3.895, 46.671, -59.585)), (' A 401  ASP  OD2', ' A 457  TYR  OH ', -0.455, (-8.629, 16.147, -82.186)), (' B 102  ASN  C  ', ' B 104  THR  H  ', -0.453, (1.738, -1.75, -24.889)), (' B 103  VAL  CG1', ' B 103  VAL  O  ', -0.452, (-0.156, -2.335, -28.443)), (' B 278  SER  HB2', ' B 436  MET  HE2', -0.451, (-1.503, 32.632, -21.675)), (' A 284  PRO  HA ', ' A 705  PO4  O2 ', -0.449, (-11.966, 12.93, -79.091)), (' A 504  PRO  O  ', ' A 507  ARG  HB2', -0.448, (-34.862, 5.452, -88.548)), (' B  12  THR HG22', ' B  14  LEU  N  ', -0.448, (3.433, -1.672, -43.117)), (' A 304  ILE  HA ', ' A 370  ILE  O  ', -0.446, (-2.933, 10.341, -59.177)), (' B  15  ARG  HG3', ' B  24  PHE  CD2', -0.444, (0.02, 1.736, -43.716)), (' B 154  VAL HG13', ' B 163  LEU HD22', -0.444, (-43.486, 16.393, -43.005)), (' B 420  GLU  OE1', ' B 427  ARG  NH1', -0.441, (-5.928, 14.702, -15.718)), (' A  12  THR HG21', ' A  26  CYS  HA ', -0.434, (7.543, 47.876, -54.883)), (' A 326  PRO  HG2', ' A 329  LYS  NZ ', -0.432, (-8.034, -2.078, -56.073)), (' B 343  PHE  CE2', ' B 345  LYS  HB2', -0.431, (-19.652, 41.88, -39.183)), (' A 519  ASN  HB3', ' A 530  THR  CG2', -0.43, (-31.318, 20.705, -79.906)), (' B 497  ARG  O  ', ' B 501  THR HG23', -0.43, (-48.082, 30.975, -11.535)), (' B 220  ASN  N  ', ' B 220  ASN  OD1', -0.428, (-42.458, 19.379, -49.576)), (' A 261  GLU  OE1', ' A 324  TYR  OH ', -0.425, (-10.569, -2.33, -72.115)), (' A 327  ILE HD11', ' A 345  LYS  O  ', -0.424, (-19.481, 1.974, -57.44)), (' B   7  LEU HD13', ' B 103  VAL HG22', -0.424, (2.444, -1.019, -30.262)), (' A 158  LEU HD21', ' A 164  HIS  ND1', -0.423, (-47.298, 31.271, -69.778)), (' B  31  TYR  CZ ', ' B  35  ILE HG21', -0.422, (2.516, -12.78, -32.565)), (' B 429  MET  O  ', ' B 433  GLY  HA2', -0.421, (-5.024, 24.443, -13.879)), (' A 531  GLN  HB2', ' A 531  GLN HE21', -0.419, (-27.019, 15.764, -78.533)), (' A 130  LEU  HA ', ' A 130  LEU HD23', -0.419, (1.381, 39.007, -64.275)), (' A 176  LEU HD22', ' A 200  PHE  HB2', -0.418, (-33.283, 31.143, -69.689)), (' A 255  THR HG23', ' A 300  PRO  HG3', -0.417, (1.276, -3.687, -60.986)), (' A 268  ASN  HB3', ' A 436  MET  SD ', -0.416, (2.585, 8.848, -73.038)), (' A  31  TYR  CE2', ' A  87  GLY  HA2', -0.416, (10.239, 56.138, -63.83)), (' B 280  LEU HD23', ' B 399  ILE HG12', -0.415, (-8.372, 34.103, -22.529)), (' A 280  LEU HD11', ' A 438  LEU  HG ', -0.415, (-2.303, 10.033, -76.306)), (' B  19  CYS  HB2', ' B  23  PRO  HD2', -0.413, (-5.986, -0.075, -37.884)), (' A 279  THR  HB ', ' A 429  MET  HE2', -0.411, (-0.571, 17.813, -73.865)), (' B 254  PRO  HB3', ' B 298  TYR  CE2', -0.407, (2.509, 44.961, -25.031)), (' B 343  PHE  CZ ', ' B 345  LYS  HB2', -0.406, (-19.897, 42.143, -38.721)), (' B 376  ILE  HA ', ' B 376  ILE HD12', -0.405, (-10.938, 25.243, -26.828)), (' A 512  ILE  HA ', ' A 531  GLN  O  ', -0.404, (-26.463, 19.058, -81.921)), (' A 158  LEU HD21', ' A 164  HIS  CE1', -0.402, (-47.38, 31.326, -70.456)), (' B 518  GLN  HA ', ' B 518  GLN  OE1', -0.401, (-39.66, 19.266, -18.529)), (' A 308  ALA  O  ', ' A 359  THR  HA ', -0.401, (-13.304, 18.688, -62.845)), (' A 254  PRO  HA ', ' A 298  TYR  O  ', -0.4, (4.0, 0.001, -63.828))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)

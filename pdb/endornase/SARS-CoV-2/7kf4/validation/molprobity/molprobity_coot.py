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
data['rama'] = [('D', ' 334 ', 'LYS', 0.044803834163348745, (58.594, 52.352, 88.34500000000001)), ('F', ' 226 ', 'LYS', 0.009275254213030265, (40.946999999999996, 9.183, -3.146))]
data['omega'] = []
data['rota'] = [('A', '   1 ', 'SER', 0.1773465504015756, (41.30399999999998, 52.677, 49.112)), ('A', ' 147 ', 'SER', 0.148735521791065, (31.499999999999993, 79.506, 75.288)), ('A', ' 148 ', 'VAL', 0.01820358548414157, (32.08, 81.014, 71.865)), ('A', ' 151 ', 'LEU', 0.2985414083553788, (27.48599999999999, 83.91300000000001, 70.41800000000002)), ('A', ' 173 ', 'LYS', 0.0, (31.50099999999999, 65.81100000000002, 78.048)), ('A', ' 188 ', 'GLN', 0.22318787274602073, (17.532999999999994, 82.062, 68.719)), ('A', ' 200 ', 'LEU', 0.11913422575048596, (12.763000000000002, 49.60799999999999, 78.79300000000002)), ('A', ' 201 ', 'GLN', 0.14690059831199792, (15.258000000000003, 46.979, 80.01)), ('A', ' 261 ', 'SER', 0.24886866150613335, (4.575, 41.313999999999986, 83.089)), ('A', ' 316 ', 'LYS', 0.12648984039377842, (-7.896, 70.924, 72.065)), ('A', ' 345 ', 'LEU', 0.0592340824060704, (-1.313, 61.501, 64.94600000000001)), ('B', '  38 ', 'VAL', 0.008010879063818222, (2.9459999999999993, 32.01400000000001, 34.138)), ('B', ' 147 ', 'SER', 0.1474301774791837, (12.020000000000003, 79.413, 15.434)), ('B', ' 151 ', 'LEU', 0.23912263175761778, (16.31299999999999, 83.904, 20.129)), ('B', ' 200 ', 'LEU', 0.08194842953249043, (30.827999999999992, 49.57300000000001, 11.880000000000003)), ('B', ' 201 ', 'GLN', 0.00542858475191789, (28.283999999999992, 46.997, 10.614000000000003)), ('B', ' 202 ', 'GLU', 0.014139520798221823, (25.658999999999992, 49.469, 9.226)), ('B', ' 226 ', 'LYS', 0.0, (45.04500000000001, 65.656, -3.3670000000000004)), ('B', ' 244 ', 'GLN', 0.23793228840090233, (51.22799999999999, 48.183000000000014, 17.952)), ('B', ' 316 ', 'LYS', 0.20353999086995161, (51.16800000000001, 71.209, 18.569)), ('C', '  34 ', 'LYS', 0.23769023421517818, (34.277999999999984, 21.287000000000006, 38.799)), ('C', '  96 ', 'ILE', 0.03591903468804358, (4.051, 25.614000000000008, 36.92)), ('C', ' 147 ', 'SER', 0.21569890151899052, (-4.29, 7.092, 13.769000000000002)), ('C', ' 148 ', 'VAL', 0.03149198324673487, (-5.75, 5.999999999999998, 17.082)), ('C', ' 200 ', 'LEU', 0.04661010259814608, (12.451999999999998, 38.115, 10.279000000000002)), ('C', ' 216 ', 'LEU', 0.24369503156906916, (7.926, 41.77900000000002, -7.006000000000002)), ('C', ' 236 ', 'VAL', 0.11551665895706843, (0.674, 43.878, 4.563)), ('C', ' 261 ', 'SER', 0.2517120749870879, (16.004, 48.726, 5.52)), ('C', ' 313 ', 'VAL', 0.0, (-20.150999999999996, 48.02, 6.823000000000001)), ('C', ' 315 ', 'SER', 0.07675539588361321, (-16.721999999999998, 48.893000000000015, 11.329)), ('C', ' 344 ', 'LYS', 2.523544646296132e-05, (-8.239999999999997, 43.84300000000001, 17.99)), ('D', '   1 ', 'SER', 0.21762835967696018, (23.759999999999998, 14.261, 47.42300000000001)), ('D', '  19 ', 'GLN', 0.0020467544534481146, (19.689, 6.662, 53.197)), ('D', ' 173 ', 'LYS', 0.014727655125278507, (35.653, 13.757, 78.381)), ('D', ' 181 ', 'LYS', 0.006777102376915845, (54.60800000000001, 15.623000000000003, 64.756)), ('D', ' 200 ', 'LEU', 0.06752893602077596, (30.631000000000004, 38.004, 80.001)), ('D', ' 201 ', 'GLN', 0.14189516808162306, (26.934, 37.094, 80.372)), ('D', ' 208 ', 'GLN', 0.18807676168915616, (38.002, 30.606, 95.401)), ('D', ' 219 ', 'ASP', 0.0020748800317795905, (40.0, 47.189, 98.10000000000001)), ('D', ' 227 ', 'LEU', 0.01521441148027353, (48.399999999999984, 42.479, 95.486)), ('D', ' 245 ', 'LEU', 0.07453845441096753, (39.54999999999998, 53.441, 79.223)), ('D', ' 257 ', 'ARG', 0.12091892422970588, (31.97999999999999, 45.603, 85.679)), ('D', ' 273 ', 'SER', 0.11512177507030089, (41.923, 33.839, 69.321)), ('D', ' 288 ', 'SER', 0.012139519630611596, (36.262, 54.25400000000001, 75.778)), ('D', ' 311 ', 'LEU', 0.0, (60.39699999999999, 44.881, 88.55800000000002)), ('D', ' 346 ', 'GLN', 0.20443254523428464, (52.853000000000016, 47.423000000000016, 68.351)), ('E', '  89 ', 'LYS', 0.06764672723582396, (7.914, 30.51300000000001, 63.818)), ('E', '  98 ', 'THR', 0.016319203132297844, (-4.648, 32.94, 49.337)), ('E', ' 121 ', 'VAL', 0.08214448273979805, (-10.405999999999997, 26.467, 53.928)), ('E', ' 147 ', 'SER', 0.11051371903186095, (-22.435999999999993, 29.05, 70.08900000000001)), ('E', ' 148 ', 'VAL', 0.23324352871862386, (-23.568, 28.462, 66.48800000000001)), ('E', ' 151 ', 'LEU', 0.07766367826579466, (-23.987, 22.802, 65.71000000000001)), ('E', ' 200 ', 'LEU', 0.046356239542778635, (11.937, 27.654000000000007, 78.692)), ('E', ' 202 ', 'GLU', 0.2569267280735701, (9.64, 32.359, 81.068)), ('E', ' 245 ', 'LEU', 0.01971706218035194, (21.265999999999995, 12.619, 77.431)), ('E', ' 264 ', 'GLU', 0.0007407821366026239, (21.619999999999994, 25.020999999999994, 74.588)), ('E', ' 314 ', 'VAL', 0.002100355050060898, (8.596, -5.143000000000002, 77.112)), ('E', ' 316 ', 'LYS', 0.10807512304706367, (4.655999999999999, -1.1880000000000004, 72.855)), ('E', ' 338 ', 'VAL', 0.06269875585688629, (8.289, 1.646, 83.164)), ('F', '   1 ', 'SER', 0.24122999590640176, (43.974999999999994, 48.966, 45.583)), ('F', '  31 ', 'VAL', 0.15550819234055535, (31.863999999999994, 47.08400000000001, 39.219)), ('F', '  33 ', 'THR', 0.08356806032379145, (32.95999999999999, 53.811, 38.27700000000001)), ('F', '  34 ', 'LYS', 0.01811329977514466, (31.699, 57.43, 38.025000000000006)), ('F', '  89 ', 'LYS', 0.06535917859218528, (35.672999999999995, 30.631, 26.999)), ('F', ' 110 ', 'LYS', 0.038298091683936046, (58.013, 34.285, 43.711)), ('F', ' 128 ', 'ASP', 0.00568178689236018, (63.022999999999996, 39.28, 31.828)), ('F', ' 151 ', 'LEU', 0.22173423213586863, (67.575, 23.292, 25.175000000000004)), ('F', ' 163 ', 'ASN', 0.18387369806449078, (42.67499999999998, 39.36400000000002, 24.104)), ('F', ' 173 ', 'LYS', 0.0, (54.816, 36.318, 16.978)), ('F', ' 200 ', 'LEU', 0.1656333851984676, (31.597999999999992, 27.952000000000012, 12.388000000000002)), ('F', ' 202 ', 'GLU', 0.007533172124172738, (33.562, 32.6, 9.935)), ('F', ' 206 ', 'ARG', 0.1612104109303466, (44.13799999999999, 26.438000000000006, 5.553)), ('F', ' 215 ', 'GLU', 0.015452449159156906, (33.873, 23.76, -2.982)), ('F', ' 219 ', 'ASP', 0.00692660042196872, (31.305, 12.606, -4.865000000000001)), ('F', ' 226 ', 'LYS', 0.293944045533587, (40.946999999999996, 9.183, -3.146)), ('F', ' 227 ', 'LEU', 0.009364198496520227, (39.335, 7.954000000000001, 0.12300000000000001)), ('F', ' 248 ', 'LEU', 0.014874637607717841, (29.776999999999994, 14.898, 11.708000000000002)), ('F', ' 250 ', 'LEU', 0.16470435830314764, (35.091, 17.336000000000006, 12.0)), ('F', ' 273 ', 'SER', 0.1490408606487177, (39.12, 21.724, 25.077)), ('F', ' 289 ', 'LYS', 0.22130113295659432, (22.326999999999995, 14.302000000000003, 18.451)), ('F', ' 303 ', 'VAL', 0.15294883852348912, (43.30299999999999, 12.388000000000003, 6.064)), ('F', ' 306 ', 'ILE', 0.26636243122796804, (42.408, 7.806000000000002, 9.018000000000002)), ('F', ' 309 ', 'GLN', 0.03167271557954461, (44.94299999999999, 2.785000000000001, 10.514)), ('F', ' 311 ', 'LEU', 0.002719551569652012, (40.895, -1.431, 9.087000000000002)), ('F', ' 318 ', 'VAL', 0.14669467845421416, (43.422, 4.565, 18.390000000000004)), ('F', ' 325 ', 'THR', 0.06690602842110638, (47.65899999999999, 15.157, 24.847)), ('F', ' 331 ', 'LEU', 0.07300029857885078, (37.584, 2.626, 15.264000000000001)), ('F', ' 334 ', 'LYS', 0.0, (32.712999999999994, -4.208, 9.263)), ('F', ' 335 ', 'ASP', 0.14019854453535371, (33.43, -6.338000000000001, 6.151000000000001)), ('F', ' 339 ', 'GLU', 0.04417820470252265, (31.914, 1.998, 9.426))]
data['cbeta'] = [('A', ' 148 ', 'VAL', ' ', 0.27994189720176105, (31.77799999999999, 80.25100000000002, 70.558)), ('B', ' 148 ', 'VAL', ' ', 0.2537465020716084, (12.080999999999998, 80.177, 20.129)), ('C', ' 148 ', 'VAL', ' ', 0.2702002212893354, (-5.417, 6.738, 18.395)), ('C', ' 236 ', 'VAL', ' ', 0.2921963547570186, (0.521, 42.56600000000001, 3.725)), ('E', '  98 ', 'THR', ' ', 0.2554503383436121, (-3.8389999999999995, 34.246, 49.546)), ('E', ' 338 ', 'VAL', ' ', 0.2521637940499738, (7.377, 2.807, 82.637)), ('F', '  31 ', 'VAL', ' ', 0.3008259865715451, (33.41399999999997, 46.88300000000001, 39.34700000000001)), ('F', '  53 ', 'VAL', ' ', 0.27122654529155255, (39.56499999999998, 38.559, 44.123000000000005)), ('F', ' 317 ', 'VAL', ' ', 0.26391641412406797, (40.744, 2.487, 21.69))]
data['probe'] = [(' B  96  ILE  CD1', ' B  96  ILE  CG1', -1.622, (23.767, 61.534, 37.469)), (' A 322  ILE  HB ', ' A 327  ILE HD13', -0.838, (8.798, 67.065, 71.294)), (' C 322  ILE  HB ', ' C 327  ILE HD13', -0.835, (-5.974, 33.259, 14.961)), (' D 322  ILE  HB ', ' D 327  ILE HD13', -0.804, (48.879, 32.298, 75.284)), (' C   1  SER  HB2', ' D   1  SER  HB2', -0.749, (22.311, 13.499, 45.323)), (' F 265  LEU HD23', ' F 280  ILE HG12', -0.747, (26.192, 20.794, 17.061)), (' A 209  MET  HE1', ' A 303  VAL HG21', -0.725, (6.39, 65.941, 88.701)), (' B 148  VAL HG13', ' B 151  LEU  HB2', -0.697, (14.562, 81.317, 20.245)), (' E 230  TYR  HA ', ' E 338  VAL HG13', -0.694, (6.638, 4.261, 84.559)), (' E 316  LYS  HE3', ' E 331  LEU HD23', -0.691, (2.59, 0.603, 76.881)), (' F 117  ALA  HB1', ' F 138  ARG  HE ', -0.683, (59.173, 21.366, 44.032)), (' D 151  LEU HD22', ' D 186  VAL HG11', -0.657, (55.597, 11.502, 69.938)), (' F  77  VAL HG22', ' F 141  VAL HG11', -0.635, (52.114, 24.376, 31.428)), (' B   1  SER  HB2', ' E   1  SER  HB2', -0.63, (0.226, 51.008, 43.031)), (' F 148  VAL HG13', ' F 151  LEU  HB2', -0.628, (66.418, 25.673, 25.333)), (' D 244  GLN  HA ', ' D 288  SER  O  ', -0.609, (39.117, 55.602, 75.71)), (' D 240  PHE  CZ ', ' D 257  ARG  HD2', -0.581, (34.439, 49.46, 83.301)), (' F  50  PRO  HD2', ' F  53  VAL  CG1', -0.57, (37.385, 36.855, 44.43)), (' A   1  SER  HB2', ' F   1  SER  HB2', -0.568, (43.075, 51.199, 46.941)), (' F 248  LEU HD11', ' F 254  LEU  HG ', -0.567, (28.594, 19.851, 11.917)), (' E  98  THR  CG2', ' E 101  VAL  HB ', -0.562, (-4.798, 36.606, 49.178)), (' F 318  VAL HG11', ' F 341  PHE  HE1', -0.555, (41.516, 5.697, 14.905)), (' F  77  VAL  CG2', ' F 141  VAL HG11', -0.545, (51.976, 24.492, 31.183)), (' D 313  VAL  O  ', ' D 333  CYS  HB2', -0.538, (60.098, 48.282, 84.904)), (' A 322  ILE  HB ', ' A 327  ILE  CD1', -0.537, (9.149, 67.45, 71.104)), (' E  98  THR HG23', ' E 101  VAL  HB ', -0.529, (-5.287, 36.772, 49.547)), (' E 127  VAL  HB ', ' E 130  GLN  HG3', -0.514, (-15.094, 36.615, 58.71)), (' F 127  VAL  HB ', ' F 130  GLN  HG3', -0.514, (58.756, 36.462, 31.881)), (' B 127  VAL  HB ', ' B 130  GLN  HG3', -0.514, (7.723, 70.647, 26.733)), (' A 127  VAL  HB ', ' A 130  GLN  HG3', -0.509, (36.012, 70.354, 63.578)), (' C 127  VAL  HB ', ' C 130  GLN  HG3', -0.508, (3.692, 8.331, 26.659)), (' C 240  PHE  CZ ', ' C 257  ARG  HD2', -0.507, (8.378, 49.25, 6.832)), (' F 319  LYS  HB3', ' F 326  GLU  HG2', -0.504, (46.706, 8.468, 22.645)), (' D 127  VAL  HB ', ' D 130  GLN  HG3', -0.5, (39.799, 8.47, 63.829)), (' A 300  ASP  HA ', ' A 303  VAL HG22', -0.5, (6.615, 65.882, 86.761)), (' F 135  ARG HH21', ' F 148  VAL HG22', -0.499, (68.245, 28.307, 28.07)), (' F  31  VAL HG23', ' F  42  LEU  HB2', -0.496, (34.197, 48.005, 37.024)), (' C 266  GLU  HB3', ' C 279  PHE  HB3', -0.491, (9.153, 48.031, 21.313)), (' F 337  HIS  HB3', ' F 843  HOH  O  ', -0.491, (36.464, -0.582, 2.889)), (' D 266  GLU  HB3', ' D 279  PHE  HB3', -0.489, (34.122, 47.893, 68.681)), (' A 266  GLU  HB3', ' A 279  PHE  HB3', -0.481, (4.35, 46.391, 66.071)), (' C 207  SER  O  ', ' C 211  ILE HG12', -0.48, (6.271, 31.136, -3.086)), (' F 303  VAL  O  ', ' F 307  LYS  HB2', -0.477, (45.04, 9.301, 5.743)), (' F  50  PRO  HD2', ' F  53  VAL HG11', -0.476, (38.053, 36.514, 44.855)), (' B 266  GLU  HB3', ' B 279  PHE  HB3', -0.465, (39.675, 46.415, 24.018)), (' C  79  ILE HG12', ' C  99  ILE HD12', -0.463, (1.105, 17.627, 34.816)), (' B 148  VAL HG12', ' B 179  TYR  CZ ', -0.461, (14.928, 79.113, 19.22)), (' E  71  ILE HD13', ' E 323  ASP  HB3', -0.46, (-3.238, 21.478, 68.165)), (' F 200  LEU HD11', ' F 254  LEU  HB3', -0.458, (30.315, 23.097, 12.111)), (' E 135  ARG HH21', ' E 148  VAL HG12', -0.458, (-24.406, 28.216, 62.763)), (' F 265  LEU HD22', ' F 278  TYR  CG ', -0.458, (28.192, 22.011, 18.787)), (' D 322  ILE  HB ', ' D 327  ILE  CD1', -0.454, (48.903, 32.756, 74.968)), (' B 226  LYS  HG3', ' B 226  LYS  O  ', -0.453, (45.213, 67.783, -2.017)), (' E 266  GLU  HB3', ' E 279  PHE  HB3', -0.448, (20.679, 21.047, 68.196)), (' F  71  ILE HD13', ' F 323  ASP  HB3', -0.446, (46.798, 21.526, 22.661)), (' B 246  GLY  HA2', ' B 700  CIT  O1 ', -0.444, (49.703, 53.936, 15.627)), (' A 300  ASP  O  ', ' A 303  VAL HG22', -0.444, (6.72, 67.057, 86.057)), (' A 104  MET  HE2', ' F  25  SER  OG ', -0.443, (29.482, 53.819, 43.227)), (' B  71  ILE HD13', ' B 323  ASP  HB3', -0.439, (27.327, 66.456, 20.396)), (' D  12  LYS  HE3', ' D  18  GLN HE21', -0.437, (18.586, 7.289, 61.041)), (' B 226  LYS  CG ', ' B 226  LYS  O  ', -0.436, (45.405, 67.455, -2.379)), (' D 163  ASN  ND2', ' E 279  PHE  CZ ', -0.436, (25.277, 18.764, 68.024)), (' F 266  GLU  HB3', ' F 279  PHE  HB3', -0.435, (23.083, 21.596, 22.732)), (' F  31  VAL HG22', ' F  43  PHE  HB3', -0.434, (34.137, 45.462, 36.746)), (' F 318  VAL  CG1', ' F 341  PHE  HE1', -0.434, (41.265, 5.906, 15.574)), (' A 246  GLY  HA2', ' A 700  CIT  O2 ', -0.433, (-6.173, 53.768, 75.05)), (' C  12  LYS  HE3', ' C  18  GLN  HG3', -0.431, (24.057, 8.131, 30.539)), (' F 334  LYS  HA ', ' F 334  LYS  HD3', -0.43, (32.889, -5.702, 10.126)), (' A  12  LYS  HE3', ' A  18  GLN  HG3', -0.43, (46.945, 52.962, 62.784)), (' F   0  MET  HA ', ' F 844  HOH  O  ', -0.428, (47.431, 47.428, 43.582)), (' C 322  ILE  HB ', ' C 327  ILE  CD1', -0.423, (-5.548, 32.638, 15.922)), (' F  75  LEU HD13', ' F 141  VAL HG21', -0.423, (53.314, 23.542, 28.636)), (' E 121  VAL HG22', ' E 123  PHE  CZ ', -0.422, (-13.95, 28.054, 53.968)), (' E  10  VAL HG21', ' E  22  VAL HG11', -0.421, (4.242, 56.025, 54.289)), (' E  79  ILE HG23', ' E 121  VAL  HB ', -0.419, (-9.078, 27.94, 52.121)), (' F 248  LEU  CD1', ' F 254  LEU  HG ', -0.416, (28.576, 19.04, 12.435)), (' B  84  VAL  CG2', ' B 101  VAL HG11', -0.416, (11.348, 60.118, 34.676)), (' A   0  MET  HA ', ' A 846  HOH  O  ', -0.415, (41.106, 56.912, 51.514)), (' A 330  MET  O  ', ' A 341  PHE  HA ', -0.414, (-4.322, 64.626, 74.923)), (' D  84  VAL  CG2', ' D 101  VAL HG11', -0.411, (33.724, 17.605, 56.243)), (' E  84  VAL  CG2', ' E 101  VAL HG11', -0.409, (-3.484, 37.763, 52.72)), (' B 232  PHE  O  ', ' B 236  VAL HG22', -0.408, (44.524, 57.586, 6.167)), (' C  84  VAL  CG2', ' C 101  VAL HG11', -0.405, (10.058, 17.86, 34.174)), (' B 104  MET  HE1', ' E 804  HOH  O  ', -0.403, (13.165, 55.282, 49.555)), (' A  84  VAL  CG2', ' A 101  VAL HG11', -0.402, (32.262, 60.043, 56.089))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)

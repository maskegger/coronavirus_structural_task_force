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
data['rama'] = [('F', ' 116 ', 'THR', 0.005082383675772536, (18.183, 116.98699999999998, 2.358)), ('H', ' 133 ', 'GLY', 0.011581762833121234, (5.611999999999997, 70.082, 20.855))]
data['omega'] = [('C', ' 147 ', 'PRO', None, (58.34699999999999, 90.397, 55.12000000000001)), ('C', ' 149 ', 'PRO', None, (53.36199999999999, 94.056, 54.44400000000002)), ('D', '   8 ', 'PRO', None, (24.49299999999999, 86.8, 65.146)), ('D', '  95 ', 'PRO', None, (39.359, 95.432, 80.13000000000002)), ('D', ' 141 ', 'PRO', None, (27.547999999999988, 83.161, 43.756000000000014)), ('F', ' 147 ', 'PRO', None, (19.389, 113.56100000000002, 5.285000000000002)), ('F', ' 149 ', 'PRO', None, (23.056, 110.86, 9.533)), ('G', '   8 ', 'PRO', None, (12.62, 81.273, 19.752000000000002)), ('G', '  95 ', 'PRO', None, (15.263, 81.326, -2.928000000000001)), ('G', ' 141 ', 'PRO', None, (11.491, 93.926, 32.084)), ('H', ' 147 ', 'PRO', None, (17.834999999999994, 65.164, 60.036000000000016)), ('H', ' 149 ', 'PRO', None, (13.059999999999995, 68.781, 58.31900000000002)), ('L', '   8 ', 'PRO', None, (-17.316000000000003, 62.224999999999994, 60.782)), ('L', '  95 ', 'PRO', None, (-7.139, 70.779, 79.15100000000001)), ('L', ' 141 ', 'PRO', None, (-8.714, 58.22, 40.386))]
data['rota'] = [('A', ' 354 ', 'ASN', 0.1099018235978261, (-20.604999999999986, 93.035, 96.096)), ('A', ' 444 ', 'LYS', 0.28780078237371637, (-31.414, 79.279, 81.82900000000002)), ('A', ' 494 ', 'SER', 0.002592353334614467, (-20.404000000000003, 86.4, 79.821)), ('B', ' 346 ', 'ARG', 0.035210616495261804, (20.758, 111.745, 99.435)), ('B', ' 354 ', 'ASN', 0.10251671198719851, (30.271999999999995, 117.002, 100.36700000000002)), ('B', ' 390 ', 'LEU', 0.28256036532967155, (42.55699999999998, 109.97599999999997, 120.537)), ('C', '   1 ', 'GLU', 0.28440787131907896, (39.681, 117.13500000000002, 59.563)), ('C', '  92 ', 'CYS', 0.23630175404235673, (46.13000000000001, 104.393, 67.481)), ('C', ' 129 ', 'LYS', 0.01264111424249432, (43.39799999999999, 85.953, 21.234)), ('C', ' 178 ', 'LEU', 0.14641331193246102, (50.133, 87.961, 45.494)), ('C', ' 179 ', 'SER', 0.12051158317992203, (48.54899999999999, 88.90699999999998, 42.183)), ('D', '  11 ', 'LEU', 0.2407813817473018, (24.86999999999999, 86.621, 58.138)), ('D', '  33 ', 'LEU', 0.22373438066684986, (28.454, 99.863, 74.67800000000003)), ('D', ' 108 ', 'ARG', 0.0025459384424564285, (22.718, 89.1, 45.47900000000001)), ('E', ' 408 ', 'ARG', 0.02248554824124267, (15.005999999999991, 70.784, -16.141)), ('E', ' 434 ', 'ILE', 0.07667842441656987, (13.688999999999997, 60.361999999999995, -19.588)), ('E', ' 514 ', 'SER', 0.16741967997486923, (21.536999999999992, 59.98599999999997, -27.891000000000005)), ('F', '  13 ', 'GLN', 0.004571007190233685, (15.929, 109.242, -6.023)), ('F', '  18 ', 'LEU', 0.20565692888977338, (23.433000000000003, 102.973, -8.813)), ('F', '  64 ', 'LYS', 0.2328020236321522, (14.72, 90.35, -11.437000000000003)), ('F', '  92 ', 'CYS', 0.23635185537434744, (28.845, 91.28, -0.757)), ('F', ' 178 ', 'LEU', 0.08478053298622991, (14.637000000000002, 111.738, 17.185)), ('F', ' 179 ', 'SER', 0.10942597124750028, (14.633999999999997, 112.607, 20.907)), ('F', ' 186 ', 'SER', 0.14444155290459088, (15.834999999999997, 118.105, 40.466000000000015)), ('F', ' 191 ', 'THR', 0.04054383537091509, (21.848999999999993, 125.957, 39.314)), ('G', '  19 ', 'VAL', 0.035176057067691724, (20.360999999999994, 78.408, 25.397000000000006)), ('G', '  33 ', 'LEU', 0.21594757808725412, (20.939999999999994, 74.996, 6.803000000000001)), ('G', '  48 ', 'ILE', 0.09673724066073576, (27.456, 76.727, 11.68)), ('G', ' 105 ', 'GLU', 0.04409360423679659, (19.311, 89.695, 25.3)), ('G', ' 142 ', 'ARG', 0.030626883592615745, (11.536999999999999, 95.315, 27.281000000000006)), ('H', '  18 ', 'LEU', 0.17922275092490528, (15.964, 72.90900000000002, 73.46800000000003)), ('H', '  92 ', 'CYS', 0.24301893431448426, (3.1289999999999996, 79.384, 68.773)), ('H', ' 128 ', 'SER', 0.20833854721420608, (11.379999999999997, 65.39, 25.961)), ('H', ' 129 ', 'LYS', 0.18913771314577715, (13.294999999999995, 67.289, 23.28900000000001)), ('H', ' 178 ', 'LEU', 0.08616307646741976, (12.452, 63.12899999999999, 48.432)), ('H', ' 179 ', 'SER', 0.11759345737041693, (11.76, 64.29, 44.848)), ('L', '  33 ', 'LEU', 0.18544169140961186, (-15.922, 75.458, 70.80200000000002))]
data['cbeta'] = [('C', ' 178 ', 'LEU', ' ', 0.28319447249372737, (50.28499999999999, 89.247, 46.359000000000016)), ('F', ' 116 ', 'THR', ' ', 0.2613080569893482, (19.379999999999995, 116.925, 1.384))]
data['probe'] = [(' C 133  GLY  HA2', ' G  81  GLU  HB3', -0.718, (32.639, 89.096, 22.967)), (' H  82  MET  HE2', ' H  82C LEU HD21', -0.71, (11.025, 69.435, 73.541)), (' L 209  PHE  HZ ', ' L 482  HOH  O  ', -0.673, (18.091, 53.453, 34.711)), (' L 186  TYR  HE1', ' L 482  HOH  O  ', -0.669, (18.655, 52.647, 34.962)), (' D 108  ARG  HG2', ' D 109  THR  N  ', -0.634, (23.006, 88.907, 42.847)), (' G  20  THR  HB ', ' H 190  GLY  HA3', -0.626, (16.507, 75.906, 23.423)), (' D 145 ALYS  HB3', ' D 197  THR  HB ', -0.574, (34.225, 74.272, 40.185)), (' C 215  SER  HB2', ' C 218  ARG  HD2', -0.568, (55.934, 89.907, 18.322)), (' B 346 BARG  NH1', ' B 509  ARG  NH2', -0.528, (20.91, 108.297, 98.194)), (' D 108  ARG  HG2', ' D 109  THR  H  ', -0.522, (22.889, 89.721, 42.789)), (' A 489 BTYR  OH ', ' H  94  ARG  NH1', -0.518, (-5.033, 90.095, 69.848)), (' D  40  PRO  HB3', ' D 165  GLU  HG3', -0.512, (38.642, 92.984, 52.573)), (' L  40  PRO  HB3', ' L 165  GLU  HG3', -0.509, (-0.545, 68.011, 52.12)), (' E 433  VAL  C  ', ' E 434  ILE HD13', -0.506, (13.961, 61.181, -22.262)), (' L  37  GLN  HB2', ' L  47  LEU HD11', -0.505, (-11.223, 74.937, 57.93)), (' E 365  TYR  H  ', ' E 388  ASN HD21', -0.501, (11.339, 51.474, -31.091)), (' A 383  SER  HB2', ' A 386  LYS  HB2', -0.497, (-11.936, 77.723, 116.079)), (' B 383  SER  O  ', ' B 385  THR  O  ', -0.497, (41.642, 102.547, 115.355)), (' G 145  LYS  HE3', ' G 147  GLN  HB2', -0.495, (-1.871, 101.439, 26.044)), (' F 127  SER  OG ', ' F 130  SER  OG ', -0.494, (7.628, 117.052, 36.546)), (' E 514  SER  HB2', ' E 738  HOH  O  ', -0.486, (23.17, 60.017, -25.333)), (' C 126  PRO  HG2', ' C 213  PRO  HB3', -0.471, (47.929, 91.686, 25.963)), (' F 128  SER  HB3', ' F 214  LYS  O  ', -0.463, (8.301, 124.505, 36.255)), (' H  82  MET  CE ', ' H  82C LEU HD21', -0.455, (10.701, 69.35, 73.708)), (' A 359  SER  HA ', ' A 524  VAL HG22', -0.454, (-20.247, 94.348, 112.994)), (' D  78  LEU HD11', ' D 104  LEU HD21', -0.45, (24.146, 94.526, 55.468)), (' B 348  ALA  HB2', ' B 354  ASN HD22', -0.449, (27.174, 116.456, 98.897)), (' F  29  VAL HG13', ' F  34  MET  HG3', -0.447, (33.376, 87.215, -7.029)), (' L 132  VAL HG22', ' L 482  HOH  O  ', -0.447, (17.797, 53.553, 36.364)), (' L 145 BLYS  HB3', ' L 197  THR  HB ', -0.443, (-1.005, 49.069, 38.547)), (' D  37  GLN  HB2', ' D  47  LEU HD11', -0.44, (29.137, 99.682, 61.382)), (' C  29  VAL HG13', ' C  34  MET  HG3', -0.435, (46.998, 111.161, 72.371)), (' F  13  GLN  HB3', ' F  13  GLN HE21', -0.434, (14.014, 110.808, -7.179)), (' L 132  VAL  CG2', ' L 482  HOH  O  ', -0.431, (17.579, 53.212, 36.403)), (' E 371  SER  OG ', ' E 373  SER  OG ', -0.43, (6.731, 53.241, -17.392)), (' B 360  ASN  H  ', ' B 523  THR  HB ', -0.43, (35.381, 120.516, 118.928)), (' B 455  LEU HD22', ' B 493  GLN  HG3', -0.427, (32.315, 110.845, 80.599)), (' B 357  ARG  HD3', ' B 844  HOH  O  ', -0.427, (33.228, 123.732, 111.288)), (' A 455  LEU HD22', ' A 493  GLN  HG3', -0.426, (-13.573, 86.235, 77.693)), (' B 449  TYR  HA ', ' B 494  SER  OG ', -0.426, (22.718, 109.908, 85.482)), (' C 192  GLN  HG2', ' C 194  TYR  CZ ', -0.425, (45.167, 100.794, 28.929)), (' D 202  SER  HB2', ' H 212  GLU  OE2', -0.424, (22.95, 74.801, 31.488)), (' C 127  SER  HB3', ' C 130  SER  HB3', -0.424, (43.736, 87.196, 25.793)), (' C 215  SER  HB2', ' C 218  ARG HH11', -0.422, (55.21, 89.766, 18.216)), (' H  29  VAL HG13', ' H  34  MET  HG3', -0.422, (3.136, 86.447, 73.664)), (' D  34  ALA  HB2', ' D  91  LEU HD11', -0.421, (31.465, 102.228, 72.42)), (' A 348  ALA  HB2', ' A 354  ASN HD22', -0.418, (-23.287, 92.498, 93.887)), (' C  11  LEU  HB2', ' C 147  PRO  HG3', -0.418, (58.738, 91.988, 58.389)), (' L  34  ALA  HB2', ' L  91  LEU HD11', -0.418, (-12.39, 77.859, 69.892)), (' D 105  GLU  HG2', ' D 106  ILE  N  ', -0.417, (27.05, 89.09, 51.079)), (' C 192  GLN  HG3', ' C 193  THR  N  ', -0.417, (47.699, 102.382, 28.332)), (' E 455  LEU HD22', ' E 493  GLN  HG3', -0.414, (28.943, 71.735, -2.869)), (' D 183  LYS  O  ', ' D 187  GLU  HG3', -0.41, (60.448, 73.82, 31.474)), (' G 145  LYS  HB3', ' G 197  THR  HB ', -0.41, (0.955, 98.526, 28.569)), (' B 346 BARG HH12', ' B 509  ARG  NH2', -0.407, (20.485, 107.913, 97.767)), (' G 142 BARG  CZ ', ' G 163  VAL HG21', -0.406, (10.673, 98.64, 22.75)), (' F   4  LEU HD21', ' F  27  PHE  HZ ', -0.404, (35.129, 88.022, -1.38)), (' F  22  CYS  HB3', ' F  78  LEU  HB3', -0.404, (31.723, 92.396, -5.137)), (' L  54 ALEU  HG ', ' L  58  VAL  HB ', -0.402, (-15.531, 82.69, 58.554)), (' C  82  MET  HE1', ' C 109  VAL HG21', -0.4, (55.083, 96.833, 66.472))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)

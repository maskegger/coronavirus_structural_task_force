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
data['rama'] = [('A', '  44 ', 'SER', 0.015562322571028749, (3.2580000000000036, 52.82699999999999, -50.46499999999999)), ('A', ' 195 ', 'ILE', 0.006426795665209347, (-32.14799999999999, 29.213, -54.965)), ('A', ' 219 ', 'LEU', 0.02042380073495634, (-39.282, 30.243, -59.09399999999999)), ('A', ' 228 ', 'THR', 0.025386378912247924, (-21.72399999999999, 35.1, -59.79899999999999)), ('A', ' 258 ', 'ILE', 0.05264856424038943, (1.6949999999999914, -3.4299999999999926, -68.344)), ('A', ' 339 ', 'ARG', 0.033076909067508625, (-23.995999999999995, 23.392, -59.165)), ('A', ' 484 ', 'VAL', 0.008041185578924701, (-31.034, 39.108, -80.833)), ('B', ' 161 ', 'ARG', 0.013892944885864622, (-44.31199999999998, 24.563, -38.132)), ('B', ' 221 ', 'VAL', 0.04917525905094541, (-44.47999999999999, 14.793000000000001, -48.40999999999999))]
data['omega'] = []
data['rota'] = [('A', '  11 ', 'GLN', 0.28489143303023023, (12.208000000000002, 45.363, -53.317)), ('A', '  12 ', 'THR', 0.0, (9.87399999999999, 48.428, -52.85499999999998)), ('A', '  35 ', 'ILE', 0.057893145376768824, (5.560999999999991, 58.58400000000002, -67.08599999999998)), ('A', '  46 ', 'ASN', 0.0053190856307272025, (0.8279999999999896, 56.251000000000005, -47.261999999999986)), ('A', '  49 ', 'VAL', 0.2052923938349619, (-1.273000000000006, 62.637, -52.42799999999999)), ('A', '  69 ', 'SER', 0.05359990173019469, (4.790000000000003, 64.477, -45.696999999999996)), ('A', '  74 ', 'SER', 0.21635793495554767, (1.273999999999992, 74.79, -54.68199999999999)), ('A', '  76 ', 'LYS', 0.05195958505283973, (5.424999999999995, 72.208, -50.863)), ('A', '  81 ', 'PHE', 0.0830721723017218, (12.49499999999999, 66.99400000000003, -53.496)), ('A', '  92 ', 'LEU', 0.013932929232524533, (12.190999999999995, 52.43100000000001, -50.089)), ('A', ' 147 ', 'LEU', 0.09010999413658981, (-21.737000000000002, 43.8, -62.139999999999986)), ('A', ' 156 ', 'GLU', 0.0658726039800596, (-44.605999999999995, 34.813, -63.78999999999999)), ('A', ' 157 ', 'VAL', 0.24117860497376542, (-44.425999999999995, 30.92200000000001, -64.16999999999999)), ('A', ' 163 ', 'LEU', 0.08634887104118621, (-41.193, 31.507000000000012, -67.543)), ('A', ' 169 ', 'VAL', 0.04477336845077072, (-34.00499999999999, 49.018, -67.274)), ('A', ' 173 ', 'ARG', 0.03746063164003343, (-29.021000000000004, 42.76700000000001, -70.54199999999999)), ('A', ' 225 ', 'PHE', 0.12217514121618507, (-30.752000000000002, 36.18600000000001, -60.070999999999984)), ('A', ' 226 ', 'VAL', 0.029404970700852573, (-27.175999999999988, 37.704, -60.545999999999985)), ('A', ' 230 ', 'HIS', 0.06381310608423245, (-16.619, 35.14, -57.563)), ('A', ' 247 ', 'VAL', 0.038955457421640693, (18.19599999999999, 11.079000000000004, -67.419)), ('A', ' 255 ', 'THR', 0.08192803134755713, (5.780999999999999, -2.1310000000000002, -64.248)), ('A', ' 289 ', 'SER', 0.26228798044090595, (-8.409000000000008, 9.303000000000004, -71.82099999999998)), ('A', ' 307 ', 'THR', 0.25111045872640914, (-7.885000000000002, 17.627000000000006, -63.135)), ('A', ' 340 ', 'VAL', 0.2873432329445559, (-25.113999999999994, 20.581000000000007, -61.636)), ('A', ' 353 ', 'GLU', 0.0, (-7.557000000000001, 8.451, -51.992)), ('A', ' 392 ', 'ARG', 0.0003061420788363293, (2.939, 20.276000000000007, -55.547)), ('A', ' 485 ', 'SER', 0.20904369223214092, (-27.452999999999996, 38.105, -82.029)), ('A', ' 495 ', 'VAL', 0.1587125282053352, (-33.25899999999999, 20.680000000000007, -95.63299999999998)), ('A', ' 502 ', 'ARG', 0.2632804523244769, (-35.37100000000001, 9.776999999999997, -97.07599999999996)), ('A', ' 508 ', 'LYS', 0.0185030259645488, (-30.63499999999999, 8.633000000000006, -83.89599999999999)), ('A', ' 530 ', 'THR', 0.022407417409790117, (-29.320000000000014, 19.242000000000008, -79.658)), ('A', ' 531 ', 'GLN', 0.03005462183405537, (-25.795999999999992, 20.446000000000005, -78.99399999999999)), ('A', ' 551 ', 'GLU', 0.019751980788604954, (-20.851999999999997, 32.46800000000001, -92.52699999999999)), ('A', ' 592 ', 'ILE', 0.05960311263312392, (-31.647999999999996, 19.71900000000001, -103.483)), ('B', '   2 ', 'VAL', 0.029404970700852573, (4.421999999999996, 3.508000000000001, -47.306)), ('B', '   9 ', 'ASN', 0.2803524302347367, (7.828, 6.283000000000002, -36.261)), ('B', '  11 ', 'GLN', 0.13026903386917832, (9.155999999999999, 3.4550000000000036, -41.499)), ('B', '  12 ', 'THR', 0.0, (6.729999999999996, 0.7859999999999996, -42.948)), ('B', '  49 ', 'VAL', 0.22658791737800937, (-5.173000000000002, -11.864000000000006, -48.17899999999999)), ('B', '  65 ', 'LEU', 0.1838314508070323, (4.454999999999998, -15.150999999999996, -49.144999999999996)), ('B', '  69 ', 'SER', 0.044188433823957894, (1.8779999999999957, -13.409000000000002, -54.075999999999986)), ('B', '  73 ', 'LYS', 0.0, (-1.601000000000007, -22.640999999999984, -45.16799999999999)), ('B', '  74 ', 'SER', 0.1449836032296557, (-4.14, -24.353, -47.588)), ('B', '  76 ', 'LYS', 0.011209368777083511, (0.9249999999999998, -21.771000000000008, -50.02499999999999)), ('B', '  92 ', 'LEU', 0.015047567003117684, (9.238999999999995, -2.977999999999998, -45.92599999999999)), ('B', '  95 ', 'ASN', 0.0, (15.913999999999994, -3.331999999999997, -40.684)), ('B', ' 160 ', 'ASP', 0.13221015781569337, (-46.20100000000001, 25.795, -41.289)), ('B', ' 162 ', 'GLU', 0.26184400377741673, (-45.517, 20.935000000000002, -37.531)), ('B', ' 169 ', 'VAL', 0.05076793086767403, (-36.971, 0.42100000000000115, -40.047999999999995)), ('B', ' 187 ', 'VAL', 0.00920533199147572, (-35.916, 13.476, -54.517999999999994)), ('B', ' 188 ', 'THR', 0.2466664332281125, (-34.727999999999994, 14.605000000000004, -58.08299999999999)), ('B', ' 193 ', 'VAL', 0.21912331317316466, (-30.77500000000001, 18.644999999999996, -53.70699999999999)), ('B', ' 194 ', 'GLN', 0.0968419454313664, (-29.627999999999986, 20.202000000000005, -50.331999999999994)), ('B', ' 195 ', 'ILE', 0.007559012805214254, (-32.61199999999999, 22.048000000000002, -48.821)), ('B', ' 201 ', 'GLU', 0.0637978266465929, (-38.918, 18.41400000000001, -31.246)), ('B', ' 219 ', 'LEU', 0.030688504372573398, (-41.408, 21.152000000000008, -47.793)), ('B', ' 220 ', 'ASN', 0.04179734708777854, (-43.58299999999999, 18.435, -49.23599999999998)), ('B', ' 247 ', 'VAL', 0.09333155948743574, (12.834, 36.193, -20.768999999999995)), ('B', ' 256 ', 'LEU', 0.07417842517811374, (2.9649999999999936, 52.99500000000001, -25.304)), ('B', ' 257 ', 'ASN', 0.011700964397570813, (-0.6579999999999986, 54.10700000000001, -24.508999999999993)), ('B', ' 258 ', 'ILE', 0.12324599574140734, (-3.7669999999999995, 52.036, -23.9)), ('B', ' 259 ', 'SER', 0.0013399975614447612, (-7.256999999999995, 52.817, -22.636999999999997)), ('B', ' 261 ', 'GLU', 0.21400312784234785, (-10.542000000000002, 49.659000000000006, -20.137999999999998)), ('B', ' 275 ', 'GLN', 0.09015435774001368, (5.621999999999995, 32.07300000000001, -23.524)), ('B', ' 289 ', 'SER', 0.18306463519682292, (-13.854, 38.669, -25.156)), ('B', ' 307 ', 'THR', 0.27029214413808333, (-10.59, 31.102, -33.679)), ('B', ' 353 ', 'GLU', 0.00024199859283106624, (-6.226999999999999, 40.945000000000014, -43.381)), ('B', ' 458 ', 'ASP', 0.0015214292670138493, (-11.526999999999994, 27.15299999999999, -5.209999999999998)), ('B', ' 484 ', 'VAL', 0.25117065863307, (-37.39699999999999, 8.415000000000003, -25.115)), ('B', ' 486 ', 'SER', 0.05874016083299942, (-35.383, 13.226000000000004, -22.036999999999995)), ('B', ' 495 ', 'VAL', 0.17540965777057504, (-44.15200000000001, 25.214000000000006, -8.605)), ('B', ' 508 ', 'LYS', 0.011670026117723343, (-39.244, 38.38499999999999, -18.178))]
data['cbeta'] = [('A', ' 484 ', 'VAL', ' ', 0.28170314575432015, (-30.86599999999999, 39.08400000000001, -79.26799999999999)), ('A', ' 545 ', 'ILE', ' ', 0.2983289052401628, (-27.673000000000002, 16.38600000000001, -88.675)), ('A', ' 592 ', 'ILE', ' ', 0.29585102910736544, (-32.825, 19.087000000000003, -102.64899999999997)), ('B', ' 275 ', 'GLN', ' ', 0.259753991011744, (4.9150000000000045, 31.318999999999996, -22.366)), ('B', ' 545 ', 'ILE', ' ', 0.2905546286928749, (-37.23099999999999, 30.226, -13.611))]
data['probe'] = [(' A 158  LEU HD11', ' A 164  HIS  CE1', -0.828, (-44.563, 32.727, -71.346)), (' B 505  ALA  O  ', ' B 508  LYS  HE3', -0.777, (-39.51, 40.072, -14.517)), (' B 226  VAL HG21', ' B 701  JG4  C02', -0.77, (-29.448, 10.092, -45.798)), (' A 158  LEU HD21', ' A 164  HIS  CE1', -0.76, (-45.251, 33.409, -70.511)), (' A 158  LEU HD21', ' A 164  HIS  HE1', -0.738, (-44.938, 32.725, -70.541)), (' A 326  PRO  CG ', ' A 329  LYS  HZ1', -0.715, (-6.641, 0.228, -58.384)), (' A 326  PRO  HG2', ' A 329  LYS  HZ1', -0.694, (-6.245, 0.541, -58.022)), (' A 326  PRO  HB2', ' A 329  LYS  HZ2', -0.676, (-7.619, 1.077, -56.753)), (' A 333  ILE  HB ', ' A 358  CYS  HB2', -0.66, (-12.376, 16.85, -56.676)), (' B 498  GLU  HG3', ' B 502  ARG HH21', -0.644, (-46.62, 30.146, -5.232)), (' A 158  LEU HD11', ' A 164  HIS  HE1', -0.628, (-44.741, 32.664, -70.844)), (' B 333  ILE  HB ', ' B 358  CYS  HB2', -0.625, (-11.736, 32.513, -41.491)), (' B 510  VAL HG21', ' B 541  TYR  CD1', -0.597, (-32.82, 34.24, -21.47)), (' B 279  THR  HB ', ' B 429  MET  HE3', -0.583, (-5.542, 27.611, -20.276)), (' A 326  PRO  HB2', ' A 329  LYS  NZ ', -0.582, (-7.359, 0.678, -57.276)), (' A 202  LYS  HA ', ' A 209  VAL HG23', -0.574, (-35.389, 32.707, -74.067)), (' B 259  SER  HB2', ' B 261  GLU  HG3', -0.574, (-10.211, 51.538, -22.353)), (' A 451  THR HG21', ' A 585  LEU HD23', -0.569, (-14.635, 18.487, -93.865)), (' A 279  THR  HB ', ' A 429  MET  HE3', -0.568, (1.448, 19.469, -74.88)), (' A 510  VAL HG21', ' A 541  TYR  CD1', -0.567, (-24.426, 12.919, -80.151)), (' A 480  ILE HG21', ' A 550  THR HG22', -0.566, (-26.89, 34.233, -90.456)), (' A 363  LEU HD22', ' A 391  LEU HD21', -0.565, (-5.229, 19.425, -57.124)), (' B 451  THR HG21', ' B 585  LEU HD23', -0.564, (-25.501, 27.412, -6.326)), (' B  13  SER  HB2', ' B  92  LEU  HB2', -0.561, (7.273, -1.535, -47.335)), (' B 252  LEU  HB3', ' B 299  TYR  CD1', -0.556, (2.819, 42.13, -28.853)), (' B 445  PRO  HD2', ' B 448  ILE HD12', -0.551, (-26.797, 35.759, -10.329)), (' A 332  ARG  HG2', ' A 343  PHE  HB3', -0.541, (-17.454, 12.017, -59.909)), (' A 445  PRO  HD2', ' A 448  ILE HD12', -0.534, (-16.731, 10.699, -89.551)), (' B 363  LEU HD22', ' B 391  LEU HD21', -0.53, (-6.512, 29.122, -38.971)), (' B 226  VAL HG11', ' B 701  JG4  S04', -0.528, (-27.228, 10.521, -44.843)), (' A 533  VAL HG11', ' A 560  ARG  HG3', -0.526, (-17.314, 24.023, -83.485)), (' A 263  SER  HA ', ' A 266  VAL HG13', -0.524, (3.019, 0.315, -73.434)), (' A 198  TYR  HE2', ' A 211  TYR  HD1', -0.52, (-35.764, 28.145, -63.466)), (' A 519  ASN  HB3', ' A 530  THR  CG2', -0.52, (-30.057, 22.77, -79.826)), (' B   7  LEU HD21', ' B 106  PHE  HB2', -0.516, (-0.553, 2.363, -30.25)), (' B 183  THR  OG1', ' B 228  THR  OG1', -0.51, (-27.46, 17.724, -42.961)), (' B 486  SER  HB3', ' B 517  SER  HB2', -0.51, (-37.791, 15.332, -22.283)), (' A 163  LEU  HG ', ' A 211  TYR  CD2', -0.507, (-38.591, 29.055, -66.385)), (' B  21  ARG  HD3', ' B 140  ALA  HB2', -0.506, (-11.22, 8.033, -38.255)), (' A 139  LYS  NZ ', ' A 813  HOH  O  ', -0.505, (-10.907, 30.467, -62.807)), (' A 326  PRO  CD ', ' A 329  LYS  HZ1', -0.501, (-6.702, 0.483, -58.517)), (' B 297  LEU HD11', ' B 324  TYR  HB3', -0.497, (-9.95, 47.637, -29.148)), (' B 474 BMET  CG ', ' B 590  LEU  HB2', -0.497, (-38.338, 27.746, -2.927)), (' A 280  LEU HD11', ' A 438  LEU  HG ', -0.496, (-0.928, 12.006, -77.347)), (' B 226  VAL HG21', ' B 701  JG4  C03', -0.495, (-29.112, 10.267, -45.584)), (' A   7  LEU HD21', ' A 106  PHE  HB2', -0.494, (5.793, 45.077, -66.216)), (' A 297  LEU HD11', ' A 324  TYR  HB3', -0.491, (-6.359, 0.673, -66.553)), (' B 533  VAL HG11', ' B 560  ARG  HG3', -0.486, (-25.715, 22.687, -17.543)), (' A 504  PRO  O  ', ' A 507  ARG  HB2', -0.484, (-34.051, 7.419, -88.389)), (' B 480  ILE HG21', ' B 550  THR HG22', -0.484, (-36.449, 12.235, -13.822)), (' B 157  VAL HG21', ' B 220  ASN  HA ', -0.483, (-44.846, 18.551, -48.128)), (' A 448  ILE HD11', ' A 572  ILE  CG2', -0.482, (-18.772, 12.975, -90.789)), (' B 195  ILE  O  ', ' B 195  ILE HG23', -0.48, (-34.323, 22.222, -47.287)), (' A 409  ARG  NH2', ' A 422  PHE  O  ', -0.478, (-6.057, 31.556, -73.13)), (' A 326  PRO  HD2', ' A 329  LYS  HZ1', -0.475, (-6.571, 0.873, -58.134)), (' A 326  PRO  CG ', ' A 329  LYS  NZ ', -0.47, (-7.117, 0.703, -57.561)), (' A 534  ASP  OD2', ' A 801  HOH  O  ', -0.468, (-19.586, 26.27, -80.564)), (' B 511  PHE  HB3', ' B 530  THR HG22', -0.465, (-38.231, 28.07, -20.168)), (' B 184  GLY  HA3', ' B 195  ILE HG22', -0.464, (-34.079, 19.797, -46.771)), (' B  19  CYS  HB2', ' B  23  PRO  HD2', -0.463, (-5.611, 1.077, -38.308)), (' A 313  ALA  HB2', ' A 375  GLU  OE1', -0.463, (-13.088, 18.311, -70.306)), (' B 474 BMET  HG2', ' B 590  LEU  HB2', -0.462, (-38.694, 27.894, -2.231)), (' A  19  CYS  HB2', ' A  23  PRO  HD2', -0.462, (-1.534, 48.33, -60.431)), (' B 477  LYS  HE2', ' B 551  GLU  OE2', -0.457, (-33.442, 13.731, -5.287)), (' B 386  VAL  O  ', ' B 390  ARG  HG2', -0.455, (-5.013, 23.126, -38.481)), (' A 139  LYS  HG2', ' A 232  VAL HG22', -0.454, (-10.833, 36.671, -61.207)), (' B 448  ILE HD11', ' B 572  ILE  CG2', -0.453, (-28.937, 33.695, -9.834)), (' A 467  LYS  NZ ', ' A 809  HOH  O  ', -0.453, (-12.234, 10.771, -98.327)), (' A 376  ILE HG22', ' A 400  GLY  HA3', -0.452, (-4.861, 19.911, -74.378)), (' B 376  ILE HG22', ' B 400  GLY  HA3', -0.45, (-11.085, 27.53, -22.447)), (' A 363  LEU  O  ', ' A 390  ARG  HD3', -0.448, (-7.404, 23.569, -55.003)), (' A  39  HIS  NE2', ' A 111  THR HG22', -0.446, (-3.281, 52.129, -67.216)), (' A 185  TYR  HA ', ' A 194  GLN  N  ', -0.444, (-31.254, 32.994, -53.204)), (' A 326  PRO  HD2', ' A 329  LYS  NZ ', -0.443, (-6.878, 1.329, -58.035)), (' A 512  ILE  O  ', ' A 546  PHE  HA ', -0.439, (-24.957, 20.578, -86.983)), (' A 139  LYS  O  ', ' A 143  GLU  HG2', -0.438, (-12.598, 38.559, -62.863)), (' A 120  TYR  CE2', ' A 409  ARG  HG2', -0.436, (-9.388, 36.758, -73.118)), (' A 448  ILE HD11', ' A 572  ILE HG22', -0.435, (-19.058, 12.601, -90.599)), (' B 539  SER  O  ', ' B 567  ARG  HD3', -0.434, (-25.93, 32.954, -20.003)), (' B   7  LEU HD12', ' B 103  VAL HG22', -0.433, (3.055, -0.875, -30.091)), (' A 456  VAL HG23', ' A 457  TYR  CE2', -0.432, (-6.843, 18.903, -86.824)), (' B 120  TYR  CE2', ' B 409  ARG  HG2', -0.43, (-16.088, 11.812, -25.893)), (' B 280  LEU HD11', ' B 438  LEU  HG ', -0.43, (-8.617, 35.644, -18.014)), (' B  12  THR  OG1', ' B  26  CYS  HA ', -0.429, (6.144, -0.211, -39.625)), (' A 561  PHE  CD2', ' A 581  LEU HD22', -0.428, (-14.431, 23.432, -91.682)), (' B  39  HIS  NE2', ' B 111  THR HG22', -0.427, (-9.481, -3.517, -32.732)), (' B 561  PHE  CD2', ' B 581  LEU HD22', -0.427, (-25.063, 22.909, -8.441)), (' B 192  LYS  H  ', ' B 192  LYS  HD2', -0.426, (-28.861, 13.765, -54.602)), (' B 226  VAL HG11', ' B 701  JG4  C03', -0.425, (-27.93, 10.52, -45.05)), (' B  52  ALA  HB1', ' B  75  HIS  CD2', -0.425, (-5.632, -21.325, -53.424)), (' B 448  ILE HD11', ' B 572  ILE HG22', -0.424, (-29.359, 33.801, -9.443)), (' B 331  SER  OG ', ' B 347  LYS  O  ', -0.421, (-11.975, 39.221, -44.728)), (' B 456  VAL HG23', ' B 457  TYR  CE2', -0.42, (-16.55, 28.341, -11.147)), (' A 480  ILE  CG2', ' A 550  THR HG22', -0.419, (-27.319, 33.695, -90.23)), (' B  31  TYR  CE2', ' B  35  ILE HD13', -0.419, (3.552, -11.417, -31.358)), (' B 377  SER  O  ', ' B 406  PRO  HA ', -0.418, (-15.49, 21.447, -23.512)), (' A 539  SER  O  ', ' A 567  ARG  HD3', -0.417, (-17.869, 14.635, -79.614)), (' A 326  PRO  CB ', ' A 329  LYS  NZ ', -0.416, (-7.631, 0.345, -57.389)), (' B 158  LEU  CD1', ' B 164  HIS  ND1', -0.416, (-49.439, 15.308, -39.579)), (' A 127  THR HG23', ' A 130  LEU  H  ', -0.414, (6.597, 38.621, -66.592)), (' A 378  MET  O  ', ' A 407  ALA  HB2', -0.412, (-10.742, 27.75, -71.05)), (' A 472  PHE  HB3', ' A 590  LEU  HG ', -0.411, (-24.84, 14.329, -98.656)), (' A 446  ALA  HB3', ' A 467  LYS  HG3', -0.41, (-12.08, 6.712, -95.651)), (' A  12  THR  OG1', ' A  26  CYS  HA ', -0.406, (9.852, 48.693, -56.015)), (' B 303  ARG  NH1', ' B 353  GLU  O  ', -0.405, (-4.657, 38.777, -41.612)), (' A 480  ILE HG12', ' A 550  THR HG22', -0.404, (-26.484, 33.296, -90.871)), (' A 162  GLU  HG2', ' A 210  VAL HG22', -0.404, (-39.256, 26.85, -71.771)), (' B 512  ILE  O  ', ' B 546  PHE  HA ', -0.402, (-34.159, 26.125, -15.035)), (' B 378  MET  O  ', ' B 407  ALA  HB2', -0.4, (-16.088, 20.596, -27.819)), (' B 357  PHE  CD1', ' B 357  PHE  N  ', -0.4, (-11.452, 37.207, -37.818))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)

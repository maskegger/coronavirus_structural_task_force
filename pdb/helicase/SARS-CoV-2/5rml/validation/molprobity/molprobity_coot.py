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
data['rama'] = [('A', '   6 ', 'VAL', 0.011489457270162786, (3.8759999999999932, 41.202, -59.788)), ('A', '   9 ', 'ASN', 0.04604771225757094, (9.183999999999987, 40.045, -57.734)), ('A', '  45 ', 'VAL', 0.026687929766541704, (-0.26899999999999924, 51.631999999999984, -45.50699999999999)), ('A', '  48 ', 'TYR', 0.02573583468939113, (-0.5970000000000075, 58.42500000000001, -51.90999999999998)), ('A', '  60 ', 'VAL', 0.06221796372859533, (1.0270000000000001, 60.37500000000001, -57.969999999999985)), ('A', ' 195 ', 'ILE', 0.005456614357542525, (-34.18899999999999, 28.477000000000004, -54.27899999999999)), ('A', ' 218 ', 'LYS', 0.039520222300979777, (-43.158, 25.246, -56.38899999999999)), ('A', ' 249 ', 'ILE', 0.004633871975061841, (10.64299999999999, 6.926, -64.049)), ('A', ' 283 ', 'PRO', 0.08519797863716924, (-8.210000000000008, 14.011000000000006, -81.781)), ('A', ' 351 ', 'THR', 0.0, (-10.822000000000006, 12.548000000000004, -50.772)), ('A', ' 484 ', 'VAL', 0.009961687730311183, (-32.75100000000001, 37.811000000000014, -80.621)), ('B', '  10 ', 'SER', 0.0036726578094709874, (9.198999999999995, 3.275000000000002, -37.725)), ('B', '  27 ', 'CYS', 0.0005532525088377538, (6.227999999999996, -5.328000000000005, -38.709)), ('B', '  45 ', 'VAL', 0.04794874001559266, (0.5879999999999947, -1.9799999999999986, -51.04599999999999)), ('B', '  51 ', 'ASN', 0.020406203136399823, (-5.399000000000002, -14.45700000000001, -53.654)), ('B', '  97 ', 'CYS', 0.006996619364626038, (11.265999999999996, -1.5310000000000024, -36.862)), ('B', ' 161 ', 'ARG', 0.021690932477227514, (-43.253, 24.468000000000004, -38.131)), ('B', ' 189 ', 'LYS', 0.013377232694771802, (-35.526999999999994, 12.280000000000001, -61.153)), ('B', ' 283 ', 'PRO', 0.05828199525237578, (-15.484999999999998, 32.17, -15.631))]
data['omega'] = []
data['rota'] = [('B', '  27 ', 'CYS', 0.012204796803416684, (6.227999999999996, -5.328000000000005, -38.709)), ('B', '  35 ', 'ILE', 0.07005541459732982, (-1.6170000000000035, -11.451, -31.889)), ('B', '  95 ', 'ASN', 0.20883529938660714, (14.821999999999994, -4.397999999999998, -40.802)), ('B', '  96 ', 'THR', 0.0011255109601909978, (13.973999999999993, -0.8159999999999972, -39.50299999999999)), ('B', '  97 ', 'CYS', 0.09982853127328654, (11.265999999999996, -1.5310000000000024, -36.862)), ('B', ' 103 ', 'VAL', 0.02880123025429473, (1.1709999999999976, -1.8119999999999985, -27.073)), ('B', ' 104 ', 'THR', 0.13819621126015086, (-1.655000000000002, -2.0539999999999994, -24.487)), ('B', ' 155 ', 'ARG', 0.25038151484488924, (-45.552, 11.526000000000003, -44.162)), ('B', ' 179 ', 'ASN', 0.2949261373151912, (-27.601999999999997, 17.74, -30.198999999999995)), ('B', ' 188 ', 'THR', 0.029761658929751487, (-35.457, 14.018, -57.716)), ('B', ' 191 ', 'SER', 0.12091897823888141, (-30.958000000000006, 11.450000000000003, -57.23199999999999)), ('B', ' 192 ', 'LYS', 0.0, (-31.524000000000008, 13.843000000000004, -54.201)), ('B', ' 215 ', 'THR', 0.006932179086506341, (-33.789, 27.939999999999998, -44.078999999999986)), ('B', ' 247 ', 'VAL', 0.16744862960042567, (12.592999999999995, 36.218, -21.108999999999998)), ('B', ' 259 ', 'SER', 0.03902745244870687, (-7.255000000000001, 52.584, -22.82999999999999)), ('B', ' 289 ', 'SER', 0.004019992775283754, (-13.927, 38.303, -25.534999999999997)), ('B', ' 293 ', 'ILE', 0.024592354626547866, (-10.126999999999995, 41.84400000000001, -28.792999999999992)), ('B', ' 327 ', 'ILE', 0.23310623945410666, (-13.715000000000003, 46.83600000000001, -39.93599999999999)), ('B', ' 359 ', 'THR', 0.11366334517770357, (-14.292999999999997, 28.241, -37.273)), ('B', ' 486 ', 'SER', 0.1846509508862434, (-35.793000000000006, 13.071000000000002, -22.036999999999992)), ('B', ' 513 ', 'SER', 0.2138813032084923, (-33.73499999999999, 23.010000000000005, -17.506)), ('B', ' 592 ', 'ILE', 0.25569407528631416, (-43.507999999999996, 24.81, -0.6839999999999999)), ('A', '  12 ', 'THR', 0.17218025847604995, (7.286999999999993, 46.819, -52.124)), ('A', '  26 ', 'CYS', 0.0760006250287874, (8.01799999999999, 47.744, -57.496999999999986)), ('A', '  69 ', 'SER', 0.16169282769778004, (3.453000000000001, 63.226, -45.60999999999999)), ('A', ' 127 ', 'THR', 0.1954873462059378, (5.411999999999993, 36.114000000000004, -68.77399999999999)), ('A', ' 156 ', 'GLU', 0.12804143128013157, (-46.660999999999994, 34.319, -63.919)), ('A', ' 173 ', 'ARG', 0.24571199395675347, (-31.060000000000002, 40.995, -71.06)), ('A', ' 183 ', 'THR', 0.2014956431209716, (-29.721, 31.969, -59.006)), ('A', ' 255 ', 'THR', 0.18637771281929819, (3.8759999999999923, -3.178000000000008, -63.57499999999999)), ('A', ' 259 ', 'SER', 0.2734010113904847, (-3.1310000000000073, -6.096, -69.961)), ('A', ' 411 ', 'LEU', 0.06617095894797141, (-16.597000000000016, 39.391000000000005, -72.824)), ('A', ' 485 ', 'SER', 0.024136630890036277, (-29.117, 36.948, -81.707)), ('A', ' 502 ', 'ARG', 0.0, (-36.538000000000004, 8.285, -97.14099999999998)), ('A', ' 517 ', 'SER', 0.11861681817134004, (-32.88300000000001, 28.252999999999993, -81.12)), ('A', ' 530 ', 'THR', 0.02447880688123405, (-31.015999999999984, 17.773, -79.691)), ('A', ' 531 ', 'GLN', 0.26271704336190255, (-27.419000000000008, 18.948000000000008, -78.95399999999998)), ('A', ' 551 ', 'GLU', 0.0833322418513454, (-22.528000000000006, 31.319000000000006, -92.448))]
data['cbeta'] = [('A', ' 534 ', 'ASP', ' ', 0.25433402812463235, (-20.357, 24.287, -77.377))]
data['probe'] = [(' A  59  ASP  OD1', ' A  61  THR  OG1', -0.956, (-0.014, 62.155, -62.766)), (' B   5  CYS  HG ', ' B 702   ZN ZN  ', -0.911, (5.895, 0.314, -35.766)), (' A 145  PHE  HD2', ' A 701  VXD CL1 ', -0.798, (-21.063, 41.013, -68.688)), (' A 534  ASP  OD2', ' A 802  HOH  O  ', -0.791, (-21.524, 25.165, -80.646)), (' B 401  ASP  OD2', ' B 457  TYR  OH ', -0.777, (-16.741, 28.629, -15.208)), (' B   5  CYS  SG ', ' B 702   ZN ZN  ', -0.763, (5.567, 0.862, -35.304)), (' B  12  THR  CG2', ' B  26  CYS  HA ', -0.762, (6.057, -1.508, -40.034)), (' A 368  ALA  O  ', ' A 393  ALA  HA ', -0.752, (1.65, 14.196, -57.341)), (' A 447  GLU  HA ', ' A 945  HOH  O  ', -0.746, (-14.618, 10.434, -96.862)), (' A  13  SER  OG ', ' A  44  SER  HB2', -0.727, (3.478, 51.109, -49.115)), (' B   8  CYS  SG ', ' B  99  GLY  N  ', -0.726, (9.554, -0.543, -32.777)), (' B  12  THR HG21', ' B  25  LEU  O  ', -0.722, (3.452, -1.853, -40.547)), (' B  12  THR HG21', ' B  26  CYS  HA ', -0.716, (5.132, -1.02, -39.651)), (' B   7  LEU HD12', ' B 103  VAL HG22', -0.71, (1.831, -1.257, -30.36)), (' B 508  LYS  HD3', ' B 920  HOH  O  ', -0.704, (-36.258, 41.402, -17.95)), (' B 279  THR  HB ', ' B 429  MET  HE2', -0.7, (-5.603, 27.291, -20.697)), (' B 124  ASN HD22', ' B 421  TYR  HA ', -0.694, (-8.901, 14.616, -21.224)), (' B  34  VAL  O  ', ' B  40  LYS  NZ ', -0.691, (-4.994, -11.243, -33.529)), (' B 177  ASN  HB3', ' B 516  ASN  ND2', -0.689, (-34.122, 17.209, -26.473)), (' B   7  LEU  CD1', ' B 103  VAL HG22', -0.669, (1.394, -0.961, -30.074)), (' B   2  VAL  N  ', ' B 805  HOH  O  ', -0.656, (1.833, 2.226, -48.982)), (' B 376  ILE HG22', ' B 400  GLY  HA3', -0.651, (-11.173, 27.541, -22.978)), (' A 269  TYR  OH ', ' A 294  GLY  HA3', -0.647, (-3.657, 3.409, -70.51)), (' A 411  LEU HD21', ' A 701  VXD  C1 ', -0.647, (-18.281, 38.338, -68.835)), (' A 327  ILE  O  ', ' A 803  HOH  O  ', -0.646, (-16.355, 2.204, -55.256)), (' A 200  PHE  N  ', ' A 804  HOH  O  ', -0.642, (-32.166, 30.438, -68.618)), (' B  44  SER  N  ', ' B  46  ASN  O  ', -0.635, (-1.634, -3.977, -47.955)), (' A  60  VAL  HB ', ' A 906  HOH  O  ', -0.632, (-0.28, 58.223, -57.066)), (' A 145  PHE  CD2', ' A 701  VXD CL1 ', -0.631, (-21.442, 40.977, -69.188)), (' A 235  LEU HD21', ' A 382  TYR  CE2', -0.624, (-7.932, 32.778, -61.047)), (' B 474 BMET  HG2', ' B 590  LEU  HB2', -0.622, (-38.759, 28.504, -2.681)), (' B 377  SER  O  ', ' B 406  PRO  HA ', -0.621, (-16.159, 20.711, -23.663)), (' B 252  LEU  HB3', ' B 299  TYR  CD1', -0.615, (3.085, 41.971, -29.373)), (' B 333  ILE  HB ', ' B 358  CYS  SG ', -0.611, (-11.97, 30.945, -41.7)), (' B 306  TYR  HB3', ' B 317  LEU HD13', -0.606, (-11.922, 35.321, -32.715)), (' B 542  ASP  OD1', ' B 569  LYS  HE3', -0.604, (-29.942, 41.316, -18.172)), (' A 350  SER  O  ', ' A 352  LEU  N  ', -0.603, (-10.542, 9.752, -50.405)), (' B 417  LEU  HA ', ' B 881  HOH  O  ', -0.602, (-14.217, 11.916, -18.09)), (' B 344  ASP  HB3', ' B 968  HOH  O  ', -0.6, (-22.473, 36.886, -43.871)), (' B  14  LEU  HB2', ' B  25  LEU  O  ', -0.592, (2.436, -1.879, -40.602)), (' B 277  TYR  HA ', ' B 396  TYR  O  ', -0.59, (0.109, 30.312, -26.703)), (' B  61  THR  O  ', ' B  62  GLN  NE2', -0.59, (-2.512, -17.948, -38.854)), (' A 519  ASN  HB3', ' A 530  THR HG23', -0.589, (-30.96, 21.235, -79.354)), (' B  83  LEU  O  ', ' B  90  PHE  N  ', -0.582, (4.81, -10.74, -42.372)), (' B 270  GLN  O  ', ' B 274  MET  HG3', -0.578, (4.623, 38.208, -22.645)), (' B 510  VAL HG21', ' B 541  TYR  CD1', -0.578, (-32.606, 34.674, -21.678)), (' A 519  ASN  HB3', ' A 530  THR  CG2', -0.577, (-31.336, 20.915, -79.808)), (' A 275  GLN  O  ', ' A 395  HIS  ND1', -0.568, (6.806, 13.052, -64.205)), (' B  50  CYS  SG ', ' B  71  TYR  HA ', -0.563, (-3.949, -17.5, -50.4)), (' A 296  ALA  O  ', ' A 300  PRO  HA ', -0.559, (-2.314, 1.399, -61.582)), (' A 510  VAL HG21', ' A 541  TYR  CD1', -0.555, (-26.579, 11.484, -80.156)), (' A 276  LYS  O  ', ' A 395  HIS  HA ', -0.554, (4.443, 15.184, -64.0)), (' A 367  THR  HA ', ' A 392  ARG  O  ', -0.552, (-0.51, 16.159, -54.307)), (' A 537  GLN  OE1', ' A 563  VAL HG21', -0.548, (-14.99, 20.337, -79.704)), (' B   8  CYS  C  ', ' B  10  SER  H  ', -0.547, (8.372, 4.415, -35.644)), (' A   4  ALA  O  ', ' A  24  PHE  HB2', -0.547, (3.764, 42.972, -55.281)), (' A 512  ILE  O  ', ' A 546  PHE  HA ', -0.546, (-26.211, 19.692, -87.191)), (' A 163  LEU HD23', ' A 211  TYR  CD2', -0.535, (-40.146, 28.311, -65.384)), (' A 370  ILE  HA ', ' A 395  HIS  O  ', -0.532, (1.02, 12.683, -61.932)), (' A 249  ILE  O  ', ' A 249  ILE HG22', -0.532, (9.35, 5.937, -62.56)), (' B 470  GLN  NE2', ' B 543  TYR  OH ', -0.525, (-34.985, 41.875, -9.569)), (' B 510  VAL HG21', ' B 541  TYR  CG ', -0.525, (-32.269, 34.422, -20.95)), (' B 425  VAL  CG1', ' B 429  MET  HE3', -0.521, (-6.762, 25.574, -22.31)), (' A 585  LEU HD22', ' A 587  PHE  CZ ', -0.52, (-18.537, 15.483, -93.781)), (' A 281  GLN  HG3', ' A 402  PRO  HD2', -0.519, (-4.673, 18.958, -79.706)), (' B 280  LEU HD11', ' B 438  LEU  HG ', -0.517, (-9.305, 35.59, -18.289)), (' A 323  LYS  HG2', ' A 324  TYR  CE1', -0.515, (-12.731, -0.737, -69.731)), (' A 277  TYR  HA ', ' A 396  TYR  O  ', -0.515, (2.55, 16.509, -66.539)), (' B 502  ARG  NH2', ' B 826  HOH  O  ', -0.515, (-44.88, 29.148, -4.73)), (' B  17  GLY  HA3', ' B  41  LEU HD23', -0.507, (-8.155, -5.048, -43.175)), (' B  35  ILE  O  ', ' B  35  ILE HD12', -0.505, (-1.46, -12.163, -29.578)), (' B 480  ILE HD13', ' B 550  THR HG22', -0.504, (-36.154, 12.624, -12.378)), (' A 538  GLY  HA2', ' A 706  PO4  O4 ', -0.503, (-15.15, 13.703, -76.658)), (' B 519  ASN  CB ', ' B 869  HOH  O  ', -0.503, (-36.495, 23.44, -23.992)), (' A  37  THR  OG1', ' A  39  HIS  HB2', -0.501, (-2.292, 53.244, -65.538)), (' A  64  TYR  O  ', ' A  70  TYR  HA ', -0.501, (3.634, 64.322, -50.748)), (' A   7  LEU HD13', ' A 103  VAL HG22', -0.501, (5.977, 45.585, -65.462)), (' B   6  VAL  CG1', ' B 978  HOH  O  ', -0.5, (-0.823, 5.716, -37.874)), (' A 411  LEU  N  ', ' A 411  LEU HD23', -0.499, (-17.682, 38.251, -71.907)), (' A 533  VAL HG11', ' A 560  ARG  HG3', -0.497, (-19.056, 23.334, -83.044)), (' B 593  PRO  HG2', ' B 826  HOH  O  ', -0.495, (-45.451, 28.173, -4.369)), (' B 425  VAL HG12', ' B 429  MET  HE3', -0.491, (-7.014, 25.142, -21.951)), (' B 455  LEU  HG ', ' B 456  VAL HG13', -0.491, (-19.029, 23.627, -8.61)), (' B  15  ARG  HA ', ' B  23  PRO  O  ', -0.491, (-1.97, 0.344, -41.041)), (' A   4  ALA  O  ', ' A  24  PHE  CB ', -0.491, (3.919, 43.122, -55.101)), (' A 558  VAL HG13', ' A 954  HOH  O  ', -0.49, (-12.407, 27.981, -89.593)), (' A  63  LEU  HB3', ' A  83  LEU HD12', -0.49, (2.744, 62.278, -54.458)), (' B  27  CYS  HB3', ' B 966  HOH  O  ', -0.49, (7.612, -5.98, -40.927)), (' B 115  THR  HA ', ' B 411  LEU  O  ', -0.489, (-20.641, 5.339, -25.492)), (' A   5  CYS  SG ', ' A  26  CYS  HB3', -0.489, (8.409, 45.809, -58.675)), (' A 369  ASP  O  ', ' A 394  LYS  HB2', -0.488, (3.892, 12.064, -59.45)), (' B  66  GLY  HA3', ' B  77  PRO  CG ', -0.487, (3.266, -19.696, -52.918)), (' B  44  SER  C  ', ' B  46  ASN  N  ', -0.486, (-0.33, -3.472, -50.091)), (' A 586  GLN  NE2', ' A 818  HOH  O  ', -0.482, (-11.131, 16.751, -97.395)), (' A 167  TRP  CZ3', ' A 174  PRO  HD2', -0.482, (-31.695, 39.107, -68.664)), (' B   8  CYS  SG ', ' B  98  VAL  HB ', -0.481, (10.211, 1.055, -32.959)), (' B 288  LYS  O  ', ' B 291  PHE  HB3', -0.481, (-10.782, 37.647, -23.616)), (' A 462  LYS  HA ', ' A 852  HOH  O  ', -0.481, (-5.864, 8.233, -91.718)), (' B 343  PHE  HA ', ' B 814  HOH  O  ', -0.477, (-23.015, 38.719, -39.45)), (' A 289  SER  HB2', ' A 811  HOH  O  ', -0.477, (-12.458, 9.251, -73.552)), (' A 130  LEU HD12', ' A 933  HOH  O  ', -0.476, (4.716, 40.309, -69.001)), (' A  19  CYS  HB2', ' A  23  PRO  HD2', -0.476, (-3.771, 47.011, -60.06)), (' B  12  THR HG21', ' B  26  CYS  CA ', -0.476, (5.036, -1.749, -39.555)), (' A 376  ILE HG12', ' A 425  VAL HG11', -0.476, (-3.48, 20.641, -71.353)), (' B   7  LEU HD12', ' B 103  VAL  CG2', -0.475, (2.288, -1.301, -30.112)), (' B 160  ASP  O  ', ' B 161  ARG  CB ', -0.473, (-44.391, 25.832, -37.963)), (' A 151  ILE HG12', ' A 226  VAL HG22', -0.471, (-31.25, 40.193, -60.435)), (' B 551  GLU  HB3', ' B 873  HOH  O  ', -0.47, (-29.801, 12.987, -6.913)), (' A 351  THR HG22', ' A 849  HOH  O  ', -0.469, (-7.512, 14.557, -49.906)), (' B 585  LEU HD22', ' B 587  PHE  CE2', -0.467, (-28.582, 29.129, -6.507)), (' A 238  PRO  CB ', ' A 904  HOH  O  ', -0.467, (4.704, 28.611, -62.834)), (' B  31  TYR  CE2', ' B  87  GLY  HA2', -0.466, (5.506, -11.566, -33.294)), (' B 220  ASN  N  ', ' B 220  ASN  OD1', -0.466, (-42.531, 19.415, -49.542)), (' A  18  ALA  O  ', ' A  39  HIS  CE1', -0.466, (-6.519, 50.502, -63.455)), (' B   7  LEU HD21', ' B 106  PHE  HB2', -0.464, (-0.542, 2.548, -30.324)), (' A 550  THR  HB ', ' A 552  THR HG23', -0.464, (-24.447, 32.972, -89.621)), (' A 318  CYS  HB3', ' A 343  PHE  CD2', -0.464, (-17.705, 7.706, -62.463)), (' A 235  LEU HD21', ' A 382  TYR  CZ ', -0.463, (-8.375, 32.116, -60.131)), (' A 367  THR HG22', ' A 392  ARG  HB3', -0.463, (1.167, 17.804, -52.803)), (' B  71  TYR  CD2', ' B  77  PRO  HD3', -0.462, (0.434, -19.429, -53.044)), (' A  34  VAL  HA ', ' A  39  HIS  O  ', -0.46, (-0.683, 55.545, -63.859)), (' B 152  ALA  HB2', ' B 167  TRP  CZ3', -0.46, (-36.127, 9.881, -38.366)), (' B  13  SER  O  ', ' B  44  SER  HA ', -0.459, (1.284, -2.051, -46.401)), (' A 585  LEU HD22', ' A 587  PHE  CE2', -0.458, (-18.661, 16.035, -94.155)), (' B 477  LYS  NZ ', ' B 551  GLU  OE2', -0.456, (-33.989, 14.029, -4.356)), (' B   9  ASN  O  ', ' B  10  SER  C  ', -0.455, (8.462, 4.572, -38.777)), (' A 152  ALA  HB2', ' A 167  TRP  CE3', -0.455, (-34.469, 38.883, -66.919)), (' A 152  ALA  HB2', ' A 167  TRP  CZ3', -0.452, (-34.249, 38.121, -66.547)), (' B 215  THR  OG1', ' B 216  THR  N  ', -0.451, (-35.199, 28.345, -45.828)), (' A  44  SER  O  ', ' A  45  VAL  C  ', -0.45, (-1.528, 52.441, -46.741)), (' A 352  LEU  CD1', ' B 234  PRO  HD3', -0.449, (-7.475, 11.329, -44.664)), (' B  55  CYS  SG ', ' B  57  VAL HG23', -0.447, (-9.32, -19.24, -46.941)), (' A 280  LEU HD11', ' A 438  LEU  HG ', -0.447, (-2.647, 10.984, -76.987)), (' A 307  THR  HA ', ' A 358  CYS  O  ', -0.447, (-11.052, 16.691, -62.03)), (' B  15  ARG  HD3', ' B  24  PHE  CE2', -0.446, (-1.608, 3.109, -44.723)), (' B 263  SER  HA ', ' B 266  VAL HG23', -0.446, (-3.867, 47.351, -19.604)), (' A 158  LEU HD11', ' A 164  HIS  CE1', -0.445, (-46.778, 31.731, -70.616)), (' A 140  ALA  HA ', ' A 232  VAL HG21', -0.442, (-13.127, 38.761, -61.184)), (' A  93  TYR  O  ', ' A  94  LYS  O  ', -0.438, (14.539, 48.966, -53.087)), (' A 490  ARG  HD2', ' A 990  HOH  O  ', -0.437, (-38.925, 29.444, -90.827)), (' B  27  CYS  CB ', ' B 966  HOH  O  ', -0.437, (7.685, -5.481, -40.765)), (' B 533  VAL HG11', ' B 560  ARG  HG3', -0.436, (-26.073, 22.631, -17.715)), (' A 106  PHE  HD1', ' A 130  LEU HD21', -0.436, (1.72, 42.745, -65.347)), (' B 475  PHE  CZ ', ' B 477  LYS  HE2', -0.435, (-34.589, 16.238, -2.14)), (' B 511  PHE  HB3', ' B 530  THR HG22', -0.434, (-38.568, 27.595, -20.567)), (' B  26  CYS  O  ', ' B  27  CYS  C  ', -0.434, (5.579, -4.518, -37.265)), (' A 309  CYS  HB3', ' A 978  HOH  O  ', -0.429, (-14.211, 25.007, -66.191)), (' A 456  VAL HG23', ' A 457  TYR  CE2', -0.428, (-8.44, 17.674, -86.315)), (' B 490  ARG  N  ', ' B 491  PRO  CD ', -0.423, (-43.944, 17.645, -13.082)), (' A 358  CYS  HB3', ' A 363  LEU HD23', -0.423, (-10.808, 17.611, -57.917)), (' A 200  PHE  HZ ', ' A 225  PHE  CD2', -0.423, (-35.762, 32.553, -63.757)), (' B 557  ASN  HB2', ' B 985  HOH  O  ', -0.422, (-22.627, 15.236, -15.344)), (' A 304  ILE  HA ', ' A 370  ILE  O  ', -0.422, (-2.761, 11.303, -59.743)), (' A 127  THR HG22', ' A 130  LEU  HB2', -0.421, (3.679, 38.399, -67.281)), (' A 329  LYS  HE2', ' A 354  GLN  OE1', -0.421, (-5.956, 1.773, -55.889)), (' A 352  LEU HD11', ' B 234  PRO  CD ', -0.42, (-7.214, 12.058, -44.262)), (' A 115  THR  HA ', ' A 411  LEU  O  ', -0.419, (-15.254, 41.196, -75.014)), (' B 254  PRO  HB3', ' B 298  TYR  CE2', -0.419, (1.999, 45.359, -24.789)), (' A 582  TYR  OH ', ' A 589  SER  HB2', -0.418, (-22.97, 17.784, -102.514)), (' A 311  HIS  ND1', ' A 359  THR HG21', -0.417, (-17.822, 18.823, -61.998)), (' B  14  LEU  O  ', ' B  24  PHE  HA ', -0.417, (0.278, 0.977, -41.544)), (' B  63  LEU  HB3', ' B  83  LEU HD12', -0.417, (-1.064, -14.258, -45.676)), (' B 103  VAL HG12', ' B 107  ASN  ND2', -0.417, (-1.576, -4.332, -28.041)), (' B 367  THR  HA ', ' B 392  ARG  O  ', -0.417, (1.148, 30.779, -38.615)), (' A 445  PRO  HD2', ' A 448  ILE HD12', -0.416, (-18.062, 9.626, -89.493)), (' B 512  ILE  O  ', ' B 546  PHE  HA ', -0.415, (-34.182, 26.155, -15.025)), (' B 179  ASN  HA ', ' B 179  ASN HD22', -0.413, (-26.312, 18.896, -30.232)), (' A 353  GLU  HA ', ' A 353  GLU  OE2', -0.413, (-9.539, 5.955, -51.209)), (' B 451  THR HG21', ' B 585  LEU HD23', -0.413, (-25.461, 27.864, -6.011)), (' A 107  ASN  O  ', ' A 111  THR  OG1', -0.413, (-3.628, 48.616, -69.978)), (' B 115  THR  O  ', ' B 412  LEU HD12', -0.413, (-19.474, 6.035, -21.965)), (' B 129  ARG  HA ', ' B 129  ARG  HD2', -0.413, (0.602, 11.088, -33.236)), (' B 402  PRO  O  ', ' B 419  PRO  HB3', -0.412, (-13.504, 21.287, -16.426)), (' A 350  SER  O  ', ' A 353  GLU  HG2', -0.411, (-11.708, 8.799, -50.753)), (' A 241  VAL HG12', ' A 992  HOH  O  ', -0.41, (3.372, 24.598, -59.363)), (' A  34  VAL  O  ', ' A  40  LYS  NZ ', -0.41, (0.666, 58.471, -65.908)), (' B 386  VAL  O  ', ' B 390  ARG  HG2', -0.41, (-5.749, 22.991, -39.075)), (' A 456  VAL HG23', ' A 457  TYR  CD2', -0.409, (-7.857, 17.662, -86.82)), (' B  31  TYR  CZ ', ' B  87  GLY  HA2', -0.408, (5.587, -11.974, -33.329)), (' B 480  ILE HD11', ' B 927  HOH  O  ', -0.408, (-36.859, 14.149, -9.343)), (' A  16  CYS  O  ', ' A  22  ARG  HA ', -0.407, (-4.104, 48.28, -57.525)), (' A 540  GLU  HA ', ' A 567  ARG  O  ', -0.407, (-20.365, 10.659, -81.742)), (' B 243  GLN  HG3', ' B 244  GLU  N  ', -0.407, (6.487, 26.498, -23.495)), (' B 554  HIS  ND1', ' B 815  HOH  O  ', -0.405, (-26.002, 15.019, -18.387)), (' B  28  LYS  CB ', ' B  97  CYS  SG ', -0.404, (9.039, -4.339, -35.357)), (' A  77  PRO  HB2', ' A 937  HOH  O  ', -0.404, (8.8, 71.983, -46.221)), (' B   9  ASN  O  ', ' B  10  SER  O  ', -0.403, (7.625, 4.899, -38.73)), (' B 539  SER  O  ', ' B 567  ARG  HD3', -0.403, (-26.223, 32.776, -20.019)), (' A 238  PRO  HG3', ' A 904  HOH  O  ', -0.402, (5.086, 27.945, -62.059)), (' B  12  THR HG22', ' B  13  SER  N  ', -0.402, (4.899, -0.933, -43.335)), (' A  21  ARG  O  ', ' A  22  ARG  HB2', -0.402, (-5.89, 45.128, -55.594)), (' B 152  ALA  HB2', ' B 167  TRP  CH2', -0.401, (-36.464, 10.56, -38.348)), (' B 445  PRO  HB3', ' B 468  SER  HB3', -0.401, (-28.271, 40.1, -7.591)), (' B   8  CYS  HB3', ' B  10  SER  HB2', -0.401, (8.513, 2.157, -35.556)), (' A 585  LEU  HA ', ' A 585  LEU HD23', -0.401, (-16.106, 17.598, -94.94)), (' B  20  ILE HD11', ' B 137  THR  O  ', -0.401, (-13.244, 5.658, -34.756))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)

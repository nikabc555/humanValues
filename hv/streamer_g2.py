# encoding:cp1251

# simple processors
def s_text(mode):
  def s_text_to_stream(obj):
    assert(isinstance(obj, str)), 'type=%s' % str(type(obj))
    return obj
  def s_text_from_stream(text):
    return text

  if mode == Streamer.mode_to_stream:
    return s_text_to_stream
  else:
    return s_text_from_stream

def s_int(mode):
  def s_int_to_stream(obj):
    assert(isinstance(obj, int)), 'type=%s' % str(type(obj))
    return str(obj)
  def s_int_from_stream(text):
    return int(text.strip())

  if mode == Streamer.mode_to_stream:
    return s_int_to_stream
  else:
    return s_int_from_stream

def s_float(mode):
  def s_float_to_stream(obj):
    assert(isinstance(obj, float) or isinstance(obj, int)), 'type=%s' % str(type(obj))
    return str(obj)
  def s_float_from_stream(text):
    return float(text.strip())

  if mode == Streamer.mode_to_stream:
    return s_float_to_stream
  else:
    return s_float_from_stream


class Streamer:
  mode_to_stream = 1
  mode_from_stream = 2

  #types of elems
  type_simple = 1
  type_struct = 2
  type_array_of_simple = 3
  type_array_of_struct = 4

  class Collector:
    class Elem_Pre:
      pass

    def __init__(self, mode):
      self.fs = []
      self.mode = mode
      
      self.s_text = s_text
      self.s_float = s_float
      self.s_int = s_int

    def mode_is_to_stream(self):
      return self.mode == Streamer.mode_to_stream

    def mode_is_from_stream(self):
      return self.mode == Streamer.mode_from_stream

    def add_simple(self, name, func):
      f = self.Elem_Pre()
      f.type = Streamer.type_simple
      f.name = name
      f.func = func(self.mode)
      self.fs += [f]

    def add_struct(self, name, creator):
      f = self.Elem_Pre()
      f.type = Streamer.type_struct
      f.name = name
      f.creator = creator
      self.fs += [f]

    def add_array_of_simple(self, name, func):
      f = self.Elem_Pre()
      f.type = Streamer.type_array_of_simple
      f.name = name
      f.func = func(self.mode)
      self.fs += [f]

    def add_array_of_struct(self, name, creator):
      f = self.Elem_Pre()
      f.type = Streamer.type_array_of_struct
      f.name = name
      f.creator = creator
      self.fs += [f]

    def add_text_fixFormat(self, name):
      f = self.Elem_Pre()
      f.type = Streamer.type_simple
      f.name = name
      f.func = s_text(self.mode)
      f.fixFormat = True
      self.fs += [f]

    def add_onRead(self, name, func):
      for f in self.fs:
        if f.name == name:
          f.onRead = func
          return
      raise NameError, 'unknown elenment; name=' + name

  class Elem_Hot:
    pass

  class RecursiveHelper:
    def __init__(self, owner):
      self.owner = owner

    def streaming(self, r):
      return r.elems

  def __init__(self, driver, obj, parent=None):
    self.obj = obj
    self.level = 0 if parent == None else parent.level + 1
    self.parent = parent
    self.driver = driver
    self.recursive = self.RecursiveHelper(self)

  def addon_reg(self, func):
    if self.mode != self.mode_from_stream:
      raise NameError, 'wrong mode: ' + str(self.mode)
    class AddonReg:
      def __init__(self, reg):
        self.reg = reg
    a = AddonReg(func)
    self.streaming(self.mode, a)

  def streaming(self, mode, adding_info=None):
    g = self.Collector(mode)
    if adding_info == None:
      self.obj.streamer_g1_reg(g)
    else:
      adding_info.reg(g)

    elems = []

    for f in g.fs:
      t = f.type
      elem = self.Elem_Hot()
      elem.type = t
      elem.name = f.name
      elem.level = self.level
      elem.owner = self.obj
      elem.onRead = getattr(f, 'onRead', None)
      elem.streamer = self
      elem.fixFormat =  getattr(f, 'fixFormat', False)
      if t == self.type_simple:
        elem.streamer = f.func
      elif t == self.type_struct:
        obj = None
        if mode == self.mode_to_stream:
          obj = getattr(elem.owner, elem.name)
        else:
          obj = f.creator()
          setattr(elem.owner, elem.name, obj)
        r = Streamer(self.recursive, obj, self)
        elem.streamer = r
        elem.childs = r.streaming(mode)
        elem.creator = f.creator
      elif t == self.type_array_of_simple:
        elem.streamer = f.func
      elif t == self.type_array_of_struct:
        def streamer(a):
          obj = a
          r = Streamer(self.recursive, obj, self)
          return r.streaming(mode)

        elem.streamer = streamer
        elem.creator = f.creator
      else:
        raise NameError, 'wrong'

      elems += [elem]

    if adding_info == None:
      self.elems = elems
      self.mode = mode
      return self.driver.streaming(self)
    else:
      self.elems += elems

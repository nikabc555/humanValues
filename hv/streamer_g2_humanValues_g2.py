import txt_funcs as txt

class HumanValues:
  def __init__(self, stream, use_spaces=True):
    self.stream = stream
    self.use_spaces = use_spaces

  def sym_startOfSingleString(self):
    return ':'

  def is_startOfSingleString(self, a):
    return a == self.sym_startOfSingleString()

  def sym_startOfMultiString(self):
    return '+'
    
  def sym_startOfMultiString_fixFormat(self):
    return '@'
    
  def sym_startOfMultiString_startPoint(self):
    return '%'

  def is_startOfMultiString(self, a):
    return a in [self.sym_startOfMultiString(), self.sym_startOfMultiString_fixFormat(), self.sym_startOfMultiString_startPoint()]

  def sym_endOfMultiString(self):
    return '^'

  def is_endOfMultiString(self, a):
    return a == self.sym_endOfMultiString()

  def sym_arrayElem(self):
    return '*'

  def is_arrayElem(self, a):
    return a == self.sym_arrayElem()

  def sym_vk(self):
    return '\n'

  def sym_space(self):
    return ' '
    
  def sym_space_opt(self):
    return ' ' if self.use_spaces else ''
    
  def sym_arrayElem_empty(self):
    return ''

  def is_vk(self, a):
    return ord(a) in [10, 13]

  def is_eng(self, a):
    b = ord(a)
    if b >= 0x41 and b <= 0x5A:
      return True
    if b >= 0x61 and b <= 0x7A:
      return True
    return False

  def is_digit(self, a):
    b = ord(a)
    return b >= 0x30 and b <= 0x39

  def is_space(self, a):
    return a == ' '

  def is_allow_sym_for_name(self, a):
    return a == '_'
    
  def is_comment(self, a):
    return a in [';', '#']

  def spaces(self, level):
    if not self.use_spaces:
      return ''
    spaces = ''
    for i in range(level * 2):
      spaces += ' '
    return spaces

  def streaming(self, r):
    if r.mode == r.mode_to_stream:
      self.to_stream(r)
    else:
      self.from_stream(r)

  def to_stream(self, r):
    def rec(elems, level=0):
      spaces = self.spaces(level)
      for e in elems:
        t = e.type
        if t == r.type_simple:
          attr = getattr(e.owner, e.name)
          assert(attr is not None), 'name=' + e.name + '; type=' + str(type(attr))
          v_fixFormat = e.fixFormat
          text = e.streamer(attr)
          if not v_fixFormat:
            text = text.strip()
          x = spaces + e.name
          self.stream.write_bulk(x)
          self.__write_text_ext(text, spaces, e, v_fixFormat)
        elif t == r.type_struct:
          x = spaces + e.name + self.sym_startOfMultiString() + self.sym_vk()
          self.stream.write_bulk(x)
          rec(e.childs, level + 1)
          x = spaces + self.sym_endOfMultiString() + self.sym_vk()
          self.stream.write_bulk(x)
        elif t == r.type_array_of_simple:
          x = spaces + e.name + self.sym_startOfMultiString() + self.sym_vk()
          self.stream.write_bulk(x)
          ar = getattr(e.owner, e.name)
          if ar is None:
            raise NameError, 'array not inited; name=%s' % e.name
          for a in ar:
            x = spaces + self.spaces(1) + self.sym_arrayElem_empty()
            self.stream.write_bulk(x)
            text = e.streamer(a).strip()
            self.__write_text_ext(text, spaces + self.spaces(1), e, False)
          x = spaces + self.sym_endOfMultiString() + self.sym_vk()
          self.stream.write_bulk(x)
        elif t == r.type_array_of_struct:
          ar = getattr(e.owner, e.name)
          x = spaces + e.name + self.sym_startOfMultiString() + self.sym_vk()
          self.stream.write_bulk(x)
          for a in ar:
            childs = e.streamer(a)
            x = spaces + self.spaces(1) + self.sym_arrayElem_empty() + self.sym_startOfMultiString() + self.sym_vk()
            self.stream.write_bulk(x)
            rec(childs, level + 2)
            x = spaces + self.spaces(1) + self.sym_endOfMultiString() + self.sym_vk()
            self.stream.write_bulk(x)
          x = spaces + self.sym_endOfMultiString() + self.sym_vk()
          self.stream.write_bulk(x)
        else:
          raise NameError, 'wrong'

    rec(r.elems, 0)
    self.stream.toStart()
    text = self.stream.read_bulk()

  def from_stream(self, r):
    rm_top = 1
    rm_inner_struct = 2
    rm_inner_array_simple = 3
    rm_inner_array_struct = 4

    def read(elems, rm, cur_r):

      step_findName = 1
      step_readName = 2
      step_readOneString = 3
      step_readManyStrings_unknown = 4
      step_readManyStrings_struct = 5
      step_readManyStrings_array_simple = 6
      step_readManyStrings_array_struct = 7
      step_readManyStrings_simple = 8
      step_readManyStrings_simple__find_close_str = 9
      step_skipString = 10

      step = step_findName

      def elemMustHaveManyStrings(elem):
        return elem.type in [r.type_struct, r.type_array_of_simple, r.type_array_of_struct]

      def elemReaded_oneString(elem, text):
        if rm == rm_inner_array_simple:
          at = getattr(elem.owner, elem.name, None)
          if at is None:
            at = []
            setattr(elem.owner, elem.name, at)
          at += [elem.streamer(text)]
        else:
          setattr(elem.owner, elem.name, elem.streamer(text))

      def onRead(elem):
        value = getattr(elem.owner, elem.name, None)
        if value is None: # new!!!
          if step in [step_readManyStrings_array_struct, step_readManyStrings_array_simple]:
            setattr(elem.owner, elem.name, [])
          else:
            raise Exception, 'what can I do?'
        func = getattr(elem, 'onRead', None)
        if func != None:
          func(elem.name, value, cur_r)

      tempo = ''
      tempo2 = ''
      text = ''
      lines = []
      start = None
      alast = None
      name = ''
      cur_elem = None
      fixedFormat = False
      startPoint = False

      reinit = True
      
      cur_str_close = ''

      while not self.stream.isEnd():
        pos = self.stream.pos()
        a = self.stream.read()

        if reinit:
          reinit = False
          tempo = ''
          tempo2 = ''
          text = ''
          name = ''
          cur_elem = None
          step = step_findName
          lines = []
          cur_str_close = ''
          fixedFormat = False
          startPoint = False

        if step == step_findName:
          if self.is_eng(a) or self.is_digit(a):
            name = a
            step = step_readName
          elif self.is_space(a) or self.is_vk(a):
            pass
          elif self.is_endOfMultiString(a) and (rm in [rm_inner_struct, rm_inner_array_simple, rm_inner_array_struct]):
            return
          elif self.is_arrayElem(a) and rm in [rm_inner_array_simple, rm_inner_array_struct]:
            name += a
            step = step_readName
          elif self.is_comment(a):
            step = step_skipString
          elif (self.is_startOfSingleString(a) or self.is_startOfMultiString(a)) and rm in [rm_inner_array_simple, rm_inner_array_struct]:
            step = step_readName
            name = self.sym_arrayElem()
            self.stream.seek(-1, self.stream.seek_from_cur)
            continue
          else:
            raise NameError, 'wrong sym: ' + a + ('; rm=%d' % (rm))
        elif step == step_readName:
          nextStep = None
          if self.is_eng(a) or self.is_digit(a) or self.is_allow_sym_for_name(a):
            name += a
          elif self.is_startOfSingleString(a):
            nextStep = step_readOneString
          elif self.is_startOfMultiString(a):
            if a == self.sym_startOfMultiString_fixFormat():
              fixedFormat = True
              nextStep = step_readManyStrings_simple__find_close_str
            elif a == self.sym_startOfMultiString_startPoint():
              startPoint = True
              nextStep = step_readManyStrings_simple__find_close_str
            else:
              nextStep = step_readManyStrings_unknown
          else:
            raise NameError, 'wrong sym: %s (%d)\n readedName=%s' % (a, ord(a), name)

          if nextStep != None:
            if rm == rm_inner_array_simple:
              if name != self.sym_arrayElem():
                raise NameError, 'wrong: ' + name
              cur_elem = elems
              if nextStep == step_readManyStrings_unknown:
                nextStep = step_readManyStrings_simple__find_close_str
            elif rm == rm_inner_array_struct:
              obj = elems.creator()
              at = getattr(elems.owner, elems.name, None)
              if at is None:
                at = []
                setattr(elems.owner, elems.name, at)
              childs = elems.streamer(obj)
              read(childs, rm_inner_struct, cur_r)
              if obj != childs[0].owner:
                raise NameError, "WTF"
              at += [obj]
              reinit = True
            else:
              for e in elems:
                if e.name == name:
                  cur_elem = e
                  if nextStep == step_readOneString and elemMustHaveManyStrings(e):
                    raise NameError, 'wrong type; name=' + name
                  if nextStep == step_readManyStrings_unknown:
                    start = pos + 1
                    if e.type == r.type_struct:
                      nextStep = step_readManyStrings_struct
                    elif e.type == r.type_array_of_simple:
                      nextStep = step_readManyStrings_array_simple
                    elif e.type == r.type_array_of_struct:
                      nextStep = step_readManyStrings_array_struct
                    elif e.type == r.type_simple:
                      nextStep = step_readManyStrings_simple__find_close_str
                      tempo2 = ''
                      cur_str_close = ''
                    else:
                      raise Exception, 'wtf'
                  break
            if cur_elem is None and not reinit:
              raise NameError, "unregged name: " + name
            step = nextStep
        elif step == step_readOneString:
          if text == '' and self.is_space(a):
            pass
          elif self.is_vk(a):
            elemReaded_oneString(cur_elem, text.strip())
            reinit = True
            onRead(cur_elem)
          else:
            text += a
        elif step == step_readManyStrings_struct:
          read(cur_elem.childs, rm_inner_struct, cur_r)
          reinit = True
          onRead(cur_elem)
        elif step == step_readManyStrings_array_simple:
          read(cur_elem, rm_inner_array_simple, cur_r)
          reinit = True
          onRead(cur_elem)
        elif step == step_readManyStrings_array_struct:
          read(cur_elem, rm_inner_array_struct, cur_r)
          reinit = True
          onRead(cur_elem)
        elif step == step_readManyStrings_simple:
          tempo += a
          if self.is_vk(a):
            if tempo.strip() == cur_str_close:
              lines = txt.get_lines_from_text(text, not fixedFormat)
              x = ''
              g = len(lines)
              for l in lines:
                g -= 1
                if startPoint:
                  if len(l) > 1:
                    x += l[1:]
                else:
                  x += l
                if g > 0:
                  x += self.sym_vk()
              if not fixedFormat and not startPoint:
                x = x.strip()
              elemReaded_oneString(cur_elem, x)
              reinit = True
              onRead(cur_elem)
            else:
              text += tempo
              tempo = ''
        elif step == step_readManyStrings_simple__find_close_str:
          if self.is_vk(a):
            cur_str_close = tempo2.strip()
            tepmo2 = ''
            if cur_str_close == '':
              cur_str_close = self.sym_endOfMultiString()
            step = step_readManyStrings_simple
          else:
            tempo2 += a
        elif step == step_skipString:
          if self.is_vk(a):
            step = step_findName
        else:
          raise NameError, 'appl err; step=' + str(step)

      if step == step_readOneString:
        elemReaded_oneString(cur_elem, text.strip())
        onRead(cur_elem)
        step = step_findName

      if step != step_findName and not reinit:
        raise NameError, 'wrong step on end: ' + str(step)

    read(r.elems, rm_top, r)

    
  def __write_text_ext(self, text, spaces, e, fixFormat):
    lines = txt.get_lines_from_text(text, not fixFormat)
    x = ''
    if len(lines) == 1 and not fixFormat:
      x = self.sym_startOfSingleString() + self.sym_space_opt() + lines[0]
    else:
      cur_close_str = self.sym_endOfMultiString()
      repeat = False
      guard = 10
      serv_sym = self.sym_startOfMultiString() if not fixFormat else self.sym_startOfMultiString_fixFormat()
      while True:
        ins = ''
        if repeat:
          ins = ' %s ' % cur_close_str
        repeat = False
        x = serv_sym + ins + self.sym_vk()
        for l in lines:
          if l == cur_close_str: #forbidden string
            if guard == 0:
              raise Exception, "can't make close string"
            cur_close_str += self.sym_endOfMultiString()
            repeat = True
            guard -= 1
            break
        if repeat:
          continue
        pref = ''
        if not fixFormat:
          pref = spaces + self.spaces(1)
        for l in lines:
          x += pref + l + self.sym_vk()
        x += spaces + cur_close_str
        break
    x += self.sym_vk()
    self.stream.write_bulk(x)

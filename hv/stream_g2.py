# encoding:cp1251

class Stream:
  seek_from_start = 1
  seek_from_cur = 2
  seek_from_end = 3

  def read(self):
    raise NameError, 'i'

  def write(self, a):
    raise NameError, 'i'

  def seek(self, pos, mode=seek_from_start):
    raise NameError, 'i'

  def read_bulk(self, size=0):
    raise NameError, 'i'

  def write_bulk(self, text):
    raise NameError, 'i'

  def size(self):
    raise NameError, 'i'

  def pos(self):
    raise NameError, 'i'

  def rest(self):
    return self.size() - self.pos()

  def isEnd(self):
    res = self.pos() >= self.size()
    return res

  def toEnd(self):
    self.seek(0, self.seek_from_end)

  def toStart(self):
    self.seek(0, self.seek_from_start)

  def record_to_stream(self, stream_other, size=None):
    if size is None:
      size = self.rest()

    if self.pos() + size > self.size():
      raise NameError, 'wrong'

    stream = stream_other

    max = 1024
    rest = size
    while rest > 0:
      text_size = max if rest >= max else rest
      text = self.read_bulk(text_size)
      stream.write_bulk(text)
      rest -= text_size

  def copy_from_stream(self, stream_other, size=None):
    stream_other.record_to_stream(self, size)

  def release(self):
    pass


class Stream_File(Stream):
  mode_readOnly = 'rb'
  mode_writeOnly = 'wb'
  mode_writeAndRead = 'wb+'
  mode_appendAndRead = 'rb+'

  def __init__(self, filename, mode, buf_size=2*1024*1024):
    self.file = open(filename, mode, buf_size)
    self.file_size = None
    self.seek(0)
    
  def __del__(self):
    self.release()

  def read(self):
    if self.isEnd():
      raise NameError, 'wrong'
    a = self.file.read(1)
    return a

  def write(self, a):
    assert(len(a) == 1)
    self.file.write(a)
    self.file_size = None

  def seek(self, pos, mode=Stream.seek_from_start):
    m = 0
    if mode == Stream.seek_from_start:
      pass
    elif mode == Stream.seek_from_cur:
      m = 1
    elif mode == Stream.seek_from_end:
      m = 2
    else:
      raise NameError, 'wrong'
    a = self.file.seek(pos, m)

  def read_bulk(self, size=None):
    if size == 0:
      return ''
    if size is None:
      size = self.rest()
    res = self.file.read(size)
    return res

  def write_bulk(self, text):
    self.file.write(text)
    self.file_size = None

  def size(self):
    if self.file_size is None:
      cur = self.pos()
      self.seek(0, Stream.seek_from_end)
      self.file_size = self.file.tell()
      self.seek(cur, Stream.seek_from_start)
    return self.file_size

  def pos(self):
    return self.file.tell()

  def release(self):
    if self.file is not None:
      self.file.close()
      self.file = None


class Stream_Buf(Stream):
  def __init__(self, buf=None):
    if buf == None:
      buf = ''
    self.buf = buf
    self.p = 0

  def read(self):
    k = self.p
    self.p += 1
    return self.buf[k]

  def write(self, a):
    assert(len(a) == 1)
    isEnd = self.isEnd()
    k = self.p
    self.p += 1
    if isEnd:
      self.buf += a
    else:
      self.buf[k] = a

  def seek(self, pos, mode=Stream.seek_from_start):
    def check_pos():
      if self.p < 0 or self.p > self.size():
        raise NameError, 'wrong; pos=' + str(self.p)

    if mode == Stream.seek_from_start:
      self.p = pos
    elif mode == Stream.seek_from_cur:
      self.p += pos
    elif mode == Stream.seek_from_end:
      self.p = self.size() + pos
    else:
      raise NameError, 'wrong'
    check_pos()

  def read_bulk(self, size=None):
    if size == 0:
      return ''
    if size is None:
      size = self.rest()
    k = self.p
    self.p += size
    return self.buf[k:k + size]

  def write_bulk(self, text):
    buf = self.buf[0:self.p]
    buf += text
    self.buf = buf
    self.p += len(text)

  def size(self):
    return len(self.buf)

  def pos(self):
    return self.p

  def release(self):
    self.buf = None
    self.p = None


class Stream_UnderStream(Stream):
  def __init__(self, stream, start, alast):
    if alast < start:
      raise NameError, 'wrong'

    self.__stream = stream
    self.__start = start
    self.__alast = alast
    self.__stream.seek(self.__start)

  def read(self):
    if not self.isEnd():
      return self.__stream.read()

  def write(self, a):
    raise NameError, 'only read'

  def seek(self, pos, mode=Stream.seek_from_start):
    if mode == Stream.seek_from_start:
      pos += self.__start
      size = self.size()
      if pos < 0 or pos >= size:
        raise NameError, 'wrong pos: %d; size=%d; start=%d; alast=%d' % (pos, size, self.__start, self.__alast)
      self.__stream.seek(pos, Stream.seek_from_start)
    else:
      raise NameError, "not impl"

  def read_bulk(self, size=None):
    rest = self.rest()
    if size == 0:
      return ''
    if size is None:
      size = rest
    if rest == 0:
      raise NameError, 'wrong'
    if size > rest:
      raise NameError, 'wrong'
    if rest - size > self.__alast:
      raise NameError, 'wrong; rest=%d; size=%d; alast=%d' % (rest, size, self.__alast)
    return self.__stream.read_bulk(size)

  def write_bulk(self, text):
    raise NameError, 'only read'

  def size(self):
    return self.__alast - self.__start

  def pos(self):
    res = self.__stream.pos() - self.__start
    if res < 0 or res > self.__alast:
      raise NameError, 'stream was used outside'
    return res

  def toEnd(self):
    self.seek(self.size(), Stream.seek_from_start)

  def toStart(self):
    self.seek(0, self.seek_from_start)

  def record_to_stream(self, stream_other, size=None):
    if size == None:
      size = self.rest()

    if self.pos() + size > self.size():
      raise NameError, 'wrong'

    stream = stream_other

    max = 1024
    rest = size
    while rest > 0:
      text_size = max if rest >= max else rest
      text = self.read_bulk(text_size)
      stream.write_bulk(text)
      rest -= text_size

  def copy_from_stream(self, stream_other, size=None):
    raise NameError, 'only read'

  def release(self):
    self.__stream = None

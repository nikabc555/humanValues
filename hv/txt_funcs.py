def get_lines_from_text(text, trim_lines):
  lines = []
  line = ''
  lastVk = None
  for a in text:
    if ord(a) in [10, 13]:
      if lastVk is not None:
        if lastVk != a:
          lastVk = None
          continue
        else:
          lines += ['']
      else:
        ln = line
        if trim_lines:
          ln = ln.strip()
        lines += [ln]
        line = ''
        lastVk = a
    else:
      lastVk = None
      line += a

  if trim_lines:
    line = line.strip()
  if line != '':
    lines += [line]

  res = []
  pre = []
  top = True
  for l in lines:
    if l == '':
      if top:
        continue
      else:
        pre += [l]
    else:
      if top:
        top = False
      else:
        res += pre
        pre = []
      res += [l]

  if len(res) == 0:
    res += ['']
  return res
  
def trim_by_lines(text):
  return get_lines_from_text(text, trim_lines=True)

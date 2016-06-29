import streamer_g2_humanValues_g2 as shv
import streamer_g2 as sga
import stream_g2 as ssa

def text_to_object(text, object):
  stream = ssa.Stream_Buf(text)
  hv = shv.HumanValues(stream)
  sr = sga.Streamer(hv, object)
  sr.streaming(sr.mode_from_stream)

def object_to_text(object, add_spaces=True):
  stream = ssa.Stream_Buf()
  hv = shv.HumanValues(stream, add_spaces)
  sr = sga.Streamer(hv, object)
  sr.streaming(sr.mode_to_stream)
  stream.toStart()
  text = stream.read_bulk()
  return text

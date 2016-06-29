use_spaces = True

def test():
  def text_to_object(text, object):
    import hv.hv as x
    return x.text_to_object(text, object)

  def object_to_text(object):
    import hv.hv as x
    global use_spaces
    
    return x.object_to_text(object, use_spaces)
    
  def test_1():
    do_print = False
  
    class A:
      def __init__(self):
        self.a = None
        self.b = None
        self.c = None
        
      def streamer_g1_reg(self, rg):
        rg.add_simple('a', rg.s_text)
        rg.add_array_of_simple('b', rg.s_text)
        rg.add_array_of_simple('c', rg.s_text)
        
        
    class B:
      def __init__(self):
        self.aa = None
        self.bb = None
        self.cc = None
        self.dd = None
        
      def streamer_g1_reg(self, rg):
        rg.add_struct('aa', A)
        rg.add_array_of_struct('bb', A)
        rg.add_simple('cc', rg.s_text)
        rg.add_array_of_simple('dd', rg.s_int)
        
    object = B()
    
    a = A()
    a.a = 'hello'
    a.b = ['jambo', 'zizmo', 'ffg abc']
    a.c = ['police', 'red', '9284 fff jj k', 'pp', '']
    object.aa = a
    
    ar = []
    
    a = A()
    a.a = 'kraski fg'
    a.b = ['pol', 'gvjedui', 'vjdie']
    a.c = ['oj38954 gef5', '', '', '', '']
    ar += [a]
    
    a = A()
    a.a = 'jdhrg348 3o4it'
    a.b = ['ewefwe']
    a.c = []
    ar += [a]
    
    a = A()
    a.a = ''
    a.b = []
    a.c = []
    ar += [a]
    
    a = A()
    a.a = 'krwegr wg eg aski fg'
    a.b = ['pol', 'gvjedui', 'vjdie', '', 'fbwuef3']
    a.c = ['oj38954 gef5', 'weoew9 3983 ']
    ar += [a]
    
    object.bb = ar
    
    object.cc = 'kilimandjaro'
    
    object.dd = [1,5,3,3,67545,45456,342]
    
    text = object_to_text(object)
    del(object)

    if do_print:
      print text
    
    res = B()
    text_to_object(text, res)
    
    # CHECK # 
    
    a = A()
    a.a = 'hello'
    a.b = ['jambo', 'zizmo', 'ffg abc']
    a.c = ['police', 'red', '9284 fff jj k', 'pp', '']
    assert(res.aa.a == a.a)
    assert(res.aa.b == a.b)
    assert(res.aa.c == a.c)
    
    assert(len(res.bb) == 4)
    
    a = A()
    a.a = 'kraski fg'
    a.b = ['pol', 'gvjedui', 'vjdie']
    a.c = ['oj38954 gef5', '', '', '', '']
    assert(res.bb[0].a == a.a)
    assert(res.bb[0].b == a.b)
    assert(res.bb[0].c == a.c)
    
    a = A()
    a.a = 'jdhrg348 3o4it'
    a.b = ['ewefwe']
    a.c = []
    assert(res.bb[1].a == a.a)
    assert(res.bb[1].b == a.b)
    assert(res.bb[1].c == a.c), '\n' + str(res.bb[1].c) + '\n' + str(a.c)
    
    a = A()
    a.a = ''
    a.b = []
    a.c = []
    assert(res.bb[2].a == a.a)
    assert(res.bb[2].b == a.b)
    assert(res.bb[2].c == a.c)
    
    a = A()
    a.a = 'krwegr wg eg aski fg'
    a.b = ['pol', 'gvjedui', 'vjdie', '', 'fbwuef3']
    a.c = ['oj38954 gef5', 'weoew9 3983']
    assert(res.bb[3].a == a.a)
    assert(res.bb[3].b == a.b)
    assert(res.bb[3].c == a.c), '\n' + str(res.bb[3].c) + '\n' + str(a.c)
    
    assert(res.cc == 'kilimandjaro')
    assert(res.dd == [1,5,3,3,67545,45456,342])
    
    if do_print:
      for p in dir(res.aa):
        print p
      
      print '-'
        
      for p in dir(res):
        print p
        
  def test_2():
    do_print = False
    
    class I:
      def __init__(self, v=None):
        self.n = v
        
      def streamer_g1_reg(self, rg):
        rg.add_simple('n', rg.s_int)
  
    class A:
      def __init__(self):
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None
        self.i = None
        
      def streamer_g1_reg(self, rg):
        rg.add_simple('a', rg.s_text)
        rg.add_simple('b', rg.s_float)
        rg.add_array_of_simple('c', rg.s_float)
        rg.add_array_of_simple('d', rg.s_float)
        rg.add_array_of_simple('e', rg.s_int)
        rg.add_array_of_simple('f', rg.s_text)
        rg.add_simple('g', rg.s_int)
        rg.add_array_of_struct('h', I)
        rg.add_array_of_struct('i', I)
      
    a = A()
    a.a = 'hello\nhow do you do?\nwhat`s new?'
    a.b = 15.78
    a.c = []
    a.d = [1, 2, 3.5, 60.8]
    a.e = [7, 777, 84, 56, 0, 33, 2]
    a.f = ['re', 'be']
    a.g = 84
    a.h = [I(5)]
    a.i = []
    
    text = object_to_text(a)
    del(a)
    
    if do_print:
      print text
    
    r = A()
    text_to_object(text, r)
    
    assert(r.a == 'hello\nhow do you do?\nwhat`s new?')
    assert(r.b == 15.78)
    assert(r.c == [])
    assert(r.d == [1, 2, 3.5, 60.8])
    assert(r.e == [7, 777, 84, 56, 0, 33, 2])
    assert(r.f == ['re', 'be'])
    assert(r.g == 84)
    assert(len(r.h) == 1)
    assert(r.h[0].n == 5)
    assert(r.i == [])
    
  def test_3(do_print=False):
    class K:
      def __init__(self, text=None):
        self.a = text
    
      def streamer_g1_reg(self, rg):
        rg.add_simple('a', rg.s_text)
  
    class J:
      def streamer_g1_reg(self, rg):
        rg.add_simple('a', rg.s_text)
        rg.add_array_of_struct('b', K)
        rg.add_struct('c', K)
  
    class I:
      def streamer_g1_reg(self, rg):
        rg.add_simple('a', rg.s_text)
        rg.add_simple('b', rg.s_float)
        rg.add_simple('c', rg.s_int) 
        rg.add_array_of_simple('d', rg.s_float)
        rg.add_array_of_simple('e', rg.s_float)
        rg.add_array_of_simple('f', rg.s_int)
        rg.add_array_of_simple('g', rg.s_text)
        rg.add_simple('h', rg.s_int)
        rg.add_struct('i', J)
  
    class A:
      def streamer_g1_reg(self, rg):
        rg.add_simple('a', rg.s_text)
        rg.add_simple('b', rg.s_float)
        rg.add_array_of_simple('c', rg.s_float)
        rg.add_array_of_simple('d', rg.s_float)
        rg.add_array_of_simple('e', rg.s_int)
        rg.add_array_of_simple('f', rg.s_text)
        rg.add_simple('g', rg.s_int)
        rg.add_array_of_struct('h', I)
        rg.add_array_of_struct('i', J)
        rg.add_array_of_struct('j', K)
        rg.add_struct('k', I)
        rg.add_struct('l', J)
        rg.add_struct('m', K)
    
    ###
    a = A()
    a.a = 'abc def ghi jkl\nhello'
    a.b = 123.789
    a.c = [1,2,3.4,5.67,8.901]
    a.d = [4.56,7.89,34,23.23,23,12,14.5,0,0,0.1]
    a.e = [685,347,32647,2353,2,7,5,3]
    a.f = ['',' ','jerenu','werewy787= jfi5v\nmnr84nr\n\njeu4urhf','trete','gd dhfg  \nhhre','442']
    a.g = 89
    a.h = []
    i = I()
    i.a = 'hrllo'
    i.b = 1
    i.c = 342
    i.d = [9.9,10.10,10.9,9.10]
    i.e = [43.3424,5654,453.454,0]
    i.f = [6,7,3,57,45,3465,546547,994,22,0,797,346,34634]
    i.g = ['hgf', 'trtrtr', 'ttr343y5h rg grtrtg \n\n\n\ngjgr98jekgre ergkrjg984jrgkrgjr', 'a']
    i.h = 7891
    i.i = J()
    i.i.a = 'police'
    i.i.b = [K('jello'), K('kueko'), K(';'), K("krusf")]
    i.i.c = K('lop')
    a.h += [i]
    i = I()
    i.a = 'kwhfv893'
    i.b = 39484.93
    i.c = 38392
    i.d = []
    i.e = [9,5,53]
    i.f = [95]
    i.g = ['a','b','c']
    i.h = 34934
    i.i = J()
    i.i.a = 'noser'
    i.i.b = [K(''), K('222'), K('123'), K("3rfb  ttg5\nkkror9\njkio")]
    i.i.c = K('jiji')
    a.h += [i]
    i = I()
    i.a = '84  i348934n  iu\n'
    i.b = 1.09
    i.c = 49
    i.d = [1.1,2.1,3.21]
    i.e = [9034903.9,0,0.115]
    i.f = [0,0,0,0,0,0,0,1]
    i.g = ['d','f','g rehrejgrerer ee', 'ry37bf83']
    i.h = 88
    i.i = J()
    i.i.a = 'poiceman'
    i.i.b = [K('78865uj'), K(''), K(' '), K("kwv uer834 hfre74nb4  \n erjher84 jjdk32"), K('[]')]
    i.i.c = K('jGGGHHJde')
    a.h += [i]
    a.i = []
    j = J()
    j.a = 'vanutz'
    j.b = [K('232145g r'), K('43mrf  jr83482 dw2'), K('slimpl'), K("surf"), K("ppp")]
    j.c = K('zz')
    a.i += [j]
    j = J()
    j.a = '3tz'
    j.b = [K('321')]
    j.c = K('zznrg rt954')
    a.i += [j]
    j = J()
    j.a = 'karrr nn'
    j.b = []
    j.c = K('321')
    a.i += [j]
    j = J()
    j.a = 'kokl;'
    j.b = [K('roga i kopita'), K('shemcuhiz^'), K('3r3tel'), K("4o489fj"), K(" vir9rnf e"), K("!!")]
    j.c = K('tmt')
    a.i += [j]
    a.j = [K('lop; +12 = 13'), K('snoop chchye')]
    i = I()
    i.a = 'jokpl'
    i.b = 88.9
    i.c = 13
    i.d = [16.9]
    i.e = [0.123,0.416,9]
    i.f = [85985,49384,487402,48373]
    i.g = ['yotig', 'rtgnri49', 'fkjfi8r', '']
    i.h = 1
    i.i = J()
    i.i.a = 'jijiko'
    i.i.b = [K('123'), K('12hb fgrg45'), K('3t5y5 53yt54'), K("nfkfg94 4nfu rjr \n kak")]
    i.i.c = K('jGGGHHJde')
    a.k = i
    j = J()
    j.a = 'jombo'
    j.b = [K('pogoda'), K('vbfudfme83'), K('!^!@#b87'), K("BO#*&#gbv 48 f "), K(" *U@**# 7t32"), K("233")]
    j.c = K('r   944jkjk 8804')
    a.l = j
    a.m = K('ll;;::')
    
    class C:
      def streamer_g1_reg(self, rg):
        rg.add_simple('a', rg.s_text)
        rg.add_struct('b', A)
        rg.add_simple('c', rg.s_text)
        
    
    tx = object_to_text(a)
    
    c = C()
    c.a = tx
    c.b = a
    c.c = 'hello!\n^\n123\n^^\n'
    
    full_tx = object_to_text(c)
    
    if do_print:
      print full_tx
      
    del(c)
    del(a)
    d = C()
    text_to_object(full_tx, d)
    a = d.b
    
    assert(a.a == 'abc def ghi jkl\nhello')
    assert(a.b == 123.789)
    assert(a.d == [4.56,7.89,34,23.23,23,12,14.5,0,0,0.1])
    assert(a.e == [685,347,32647,2353,2,7,5,3])
    assert(a.f == ['','','jerenu','werewy787= jfi5v\nmnr84nr\n\njeu4urhf','trete','gd dhfg\nhhre','442'])
    assert(a.g == 89)
    assert(len(a.h) == 3)
    assert(a.h[0].a == 'hrllo')
    assert(a.h[0].b == 1)
    assert(a.h[0].c == 342)
    assert(a.h[0].d == [9.9,10.10,10.9,9.10])
    assert(a.h[0].e == [43.3424,5654,453.454,0])
    assert(a.h[0].f == [6,7,3,57,45,3465,546547,994,22,0,797,346,34634])
    assert(a.h[0].g == ['hgf', 'trtrtr', 'ttr343y5h rg grtrtg\n\n\n\ngjgr98jekgre ergkrjg984jrgkrgjr', 'a'])
    assert(a.h[0].h == 7891)
    assert(a.h[0].i.a == 'police')
    assert(len(a.h[0].i.b) == 4)
    assert(a.h[0].i.b[0].a == 'jello')
    assert(a.h[0].i.b[1].a == 'kueko')
    assert(a.h[0].i.b[2].a == ';')
    assert(a.h[0].i.b[3].a == 'krusf')
    assert(a.h[0].i.c.a == 'lop')
    
    assert(a.h[1].a == 'kwhfv893')
    assert(a.h[1].b == 39484.93)
    assert(a.h[1].c == 38392)
    assert(a.h[1].d == [])
    assert(a.h[1].e == [9,5,53])
    assert(a.h[1].f == [95])
    assert(a.h[1].g == ['a','b','c'])
    assert(a.h[1].h == 34934)
    assert(a.h[1].i.a == 'noser')
    assert(len(a.h[1].i.b) == 4)
    assert(a.h[1].i.b[0].a == '')
    assert(a.h[1].i.b[1].a == '222')
    assert(a.h[1].i.b[2].a == '123')
    assert(a.h[1].i.b[3].a == '3rfb  ttg5\nkkror9\njkio')
    assert(a.h[1].i.c.a == 'jiji')
    
    assert(a.h[2].a == '84  i348934n  iu')
    assert(a.h[2].b == 1.09)
    assert(a.h[2].c == 49)
    assert(a.h[2].d == [1.1,2.1,3.21])
    assert(a.h[2].e == [9034903.9,0,0.115])
    assert(a.h[2].f == [0,0,0,0,0,0,0,1])
    assert(a.h[2].g == ['d','f','g rehrejgrerer ee', 'ry37bf83'])
    assert(a.h[2].h == 88)
    assert(a.h[2].i.a == 'poiceman')
    assert(len(a.h[2].i.b) == 5)
    assert(a.h[2].i.b[0].a == '78865uj')
    assert(a.h[2].i.b[1].a == '')
    assert(a.h[2].i.b[2].a == '')
    assert(a.h[2].i.b[3].a == 'kwv uer834 hfre74nb4\nerjher84 jjdk32')
    assert(a.h[2].i.b[4].a == '[]')
    assert(a.h[2].i.c.a == 'jGGGHHJde')
    
    assert(len(a.i) == 4)
    assert(a.i[0].a == 'vanutz')
    assert(len(a.i[0].b) == 5)
    assert(a.i[0].b[0].a == '232145g r')
    assert(a.i[0].b[1].a == '43mrf  jr83482 dw2')
    assert(a.i[0].b[2].a == 'slimpl')
    assert(a.i[0].b[3].a == 'surf')
    assert(a.i[0].b[4].a == 'ppp')
    assert(a.i[0].c.a == 'zz')
    
    assert(a.i[1].a == '3tz')
    assert(len(a.i[1].b) == 1)
    assert(a.i[1].b[0].a == '321')
    assert(a.i[1].c.a == 'zznrg rt954')
    
    assert(a.i[2].a == 'karrr nn')
    assert(len(a.i[2].b) == 0)
    assert(a.i[2].c.a == '321')
    
    assert(a.i[3].a == 'kokl;')
    assert(len(a.i[3].b) == 6)
    assert(a.i[3].b[0].a == 'roga i kopita')
    assert(a.i[3].b[1].a == 'shemcuhiz^')
    assert(a.i[3].b[2].a == '3r3tel')
    assert(a.i[3].b[3].a == '4o489fj')
    assert(a.i[3].b[4].a == 'vir9rnf e')
    assert(a.i[3].b[5].a == '!!')
    assert(a.i[3].c.a == 'tmt')
    
    assert(len(a.j) == 2)
    assert(a.j[0].a == 'lop; +12 = 13')
    assert(a.j[1].a == 'snoop chchye')
    
    assert(a.k.a == 'jokpl')
    assert(a.k.b == 88.9)
    assert(a.k.c == 13)
    assert(a.k.d == [16.9])
    assert(a.k.e == [0.123,0.416,9])
    assert(a.k.f == [85985,49384,487402,48373])
    assert(a.k.g == ['yotig', 'rtgnri49', 'fkjfi8r', ''])
    assert(a.k.h == 1)
    assert(a.k.i.a == 'jijiko')
    assert(len(a.k.i.b) == 4)
    assert(a.k.i.b[0].a == '123')
    assert(a.k.i.b[1].a == '12hb fgrg45')
    assert(a.k.i.b[2].a == '3t5y5 53yt54')
    assert(a.k.i.b[3].a == 'nfkfg94 4nfu rjr\nkak')
    assert(a.k.i.c.a == 'jGGGHHJde')
    
    assert(a.l.a == 'jombo')
    assert(len(a.l.b) == 6)
    assert(a.l.b[0].a == 'pogoda')
    assert(a.l.b[1].a == 'vbfudfme83')
    assert(a.l.b[2].a == '!^!@#b87')
    assert(a.l.b[3].a == 'BO#*&#gbv 48 f')
    assert(a.l.b[4].a == '*U@**# 7t32')
    assert(a.l.b[5].a == '233')
    assert(a.l.c.a == 'r   944jkjk 8804')
    
    assert(a.m.a == 'll;;::')
    
    assert(d.c == 'hello!\n^\n123\n^^'), '\n%s' % d.c
  
  def test_4():
    class A:
      def __init__(self):
        self.a = None
        self.b = None
        
      def streamer_g1_reg(self, rg):
        rg.add_simple('a', rg.s_text)
        rg.add_array_of_simple('b', rg.s_text)
        
    text = '''
      a: hello
      b+
        *: how do you do?
        *: abc
      ^
    '''
  
    a = A()
    text_to_object(text, a)
    
    assert(a.a == 'hello')
    assert(a.b == ['how do you do?', 'abc'])
    
    del(a)
    
    text = '''
      # comment
      a: hello2
      # comment
      b+
        # comment
        
        # comment
        *: how do you do? www
        
        # comment
        *: abcdef
        # comment
      ^
      # comment
      ; comment
      ; comment
      ; comment
    '''
  
    a = A()
    text_to_object(text, a)
    
    assert(a.a == 'hello2')
    assert(a.b == ['how do you do? www', 'abcdef'])
    
    del(a)
    
    text = '''
      a+ @@@
        abcd
        efgh
      @@@
      b+
        *+ ko
          rfjnf
          94732
        ko
        *: rr12
      ^
    '''
    
    a = A()
    text_to_object(text, a)
    assert(a.a == 'abcd\nefgh'), a.a
    assert(a.b == ['rfjnf\n94732', 'rr12'])
    
    del(a)
    
  def test_5():
    class A:
      def __init__(self):
        self.a = None
        self.b = None
        self.c = None
        
      def streamer_g1_reg(self, rg):
        rg.add_simple('a', rg.s_text)
        rg.add_simple('b', rg.s_text)
        rg.add_text_fixFormat('c')
        
    text = '''
a@ &
  |a|b|c|
     1 2
&
b@
a
 b
  c
   d
    e
^
    '''
  
    a = A()
    text_to_object(text, a)
    
    assert(a.a == '  |a|b|c|\n     1 2'), a.a
    assert(a.b == 'a\n b\n  c\n   d\n    e'), a.b
    assert(a.c is None)
    
    del(a)
    
    text = '''
        a% &
           >  |a|b|c|
          >     1 2
        &
        b%
        .a
        . b
        .  c
        .   d
        .    e
        ^
    '''
  
    a = A()
    text_to_object(text, a)
    
    assert(a.a == '  |a|b|c|\n     1 2'), a.a
    assert(a.b == 'a\n b\n  c\n   d\n    e'), a.b
    assert(a.c is None)
    
    del(a)
    
    a = A()
    a.a = 'hello\njoke'
    a.b = 'ww\n  aa  \n  bb \n '
    a.c = ' 1\n  2\n   3\n'
  
    text = object_to_text(a)
    exp = ''
    
    global use_spaces
    if use_spaces:
      exp = '''a+
  hello
  joke
^
b+
  ww
  aa
  bb
^
c@
 1
  2
   3
^
'''
    else:
      exp = '''a+
hello
joke
^
b+
ww
aa
bb
^
c@
 1
  2
   3
^
'''

    assert(text == exp), '\n%s<>\n%s' % (text, exp)
  
  def test_6():
    class A:
      def __init__(self):
        self.a = None
        
      def streamer_g1_reg(self, rg):
        rg.add_array_of_simple('a', rg.s_text)
        
    text = '''
        a+
          : 1
          : 45
          : hello
          +
            text
            number 2
          ^
          + &
            jj
            number 3
          &
        ^
    '''
    
    a = A()
    text_to_object(text, a)
    
    assert(a.a == ['1', '45', 'hello', 'text\nnumber 2', 'jj\nnumber 3']), a.a
    assert(a.a[3] == '''text
number 2'''), a.a[3]

  
  
  
  test_1()
  test_2()
  test_3()
  test_4()
  test_5()
  test_6()
  
for i in range(2):
  use_spaces = i == 0
  test()
  
print 'all tests done'

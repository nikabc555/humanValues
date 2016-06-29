# encoding:cp1251

import hv.hv as hv

class A:
  def streamer_g1_reg(self, rg): # регистрация полей
    rg.add_simple('a', rg.s_text) # текстовое поле
    rg.add_simple('b', rg.s_int) # целочисленное поле
    rg.add_simple('c', rg.s_float) # поле числа с плавающей точкой
    rg.add_array_of_simple('d', rg.s_text) # массив текстовых полей
    rg.add_array_of_simple('e', rg.s_int) # массив целочисленных полей
    rg.add_array_of_simple('f', rg.s_float) # массив полей чисел с плавающей точкой

class B:
  def streamer_g1_reg(self, rg): # регистрация полей
    rg.add_struct('aa', A) # поле-структура A
    rg.add_array_of_struct('bb', A) # массив полей-структур A
    
b = B()

b.aa = A()
b.aa.a = 'hello'
b.aa.b = 123
b.aa.c = 12.98
b.aa.d = ['abc', 'def', 'ghi']
b.aa.e = [5,6,7,7,8]
b.aa.f = [1.2, 3.9, 55.667]
    
r = A()
r.a = 'qwerty'
r.b = 0
r.c = 9.33
r.d = ['"""', '@']
r.e = [765,3,34,0,72]
r.f = [22.2, 33.3, 44.441]

s = A()
s.a = 'asdfg\nzxcvb'
s.b = 6634
s.c = 0.0
s.d = ['zzz', 'zzzxxx\nj789', '@@@']
s.e = [84873, 3838, 261]
s.f = [9.99]

b.bb = [r, s]
    
text = hv.object_to_text(b)

g = B()
hv.text_to_object(text, g)

text2 = hv.object_to_text(g, True)
#text2 = hv.object_to_text(g, False)

assert(text2 == text), text2

print text
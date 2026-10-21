#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function #,unicode_literals

# average timings
_pfxst= ("~#", "~$", "~:")
_pfxsl= ["~#", "~$", "~:"]
_pfxsd= dict.fromkeys( _pfxst)
_lpfxst= _pfxst*20
_lpfxsl= _pfxsl*20

c_pfx_check = dict(
    f_tuple=        lambda x: x[:2] in ("~#", "~$", "~:")   #0.0864 %avg=216 # 3
  , f_list=         lambda x: x[:2] in ["~#", "~$", "~:"]   #0.0868 %avg=217 # 4
  , f_tuple_global= lambda x: x[:2] in _pfxst               #0.0886 %avg=222 # 5
  , f_list_global=  lambda x: x[:2] in _pfxsl               #0.0912 %avg=228 # 6
  , f_dict_global=  lambda x: x[:2] in _pfxsd               #0.0763 %avg=191 # 2
  , f_tuple_global20= lambda x: x[:2] in _lpfxst            #0.6506 %avg=1630
  , f_list_global20=  lambda x: x[:2] in _lpfxsl            #0.6340 %avg=1589
  , f_one_by_one=   lambda x: x[0]=='~' and x[1] in "#$:"   #0.0399          # 1 fastest
    )

if 0:
 from transit.rolling_cache import encode_i2key_map, encode_key, SUB, MAP_AS_ARR
 c_encode_i2key = dict(
    f_map = lambda x: encode_i2key_map[ len( x) ]   #.054    fastest
  , f_func= lambda x: encode_key( len( x) )         #.143
    )

 c_is_cache_key= dict(
    f_org = lambda name: len(name) and (name[0] == SUB and name != MAP_AS_ARR)  # 73
  , f_nolen= lambda name: name and (name[0] == SUB and name != MAP_AS_ARR)      # 66 fastest
    )


#just def func -> class.@staticmethod -> slower!
def func1( x): return x and x != 'asd' and len(x)
class klas1:
    func1 = staticmethod( func1)
c_func_glob_vs_staticmethod= dict(
    f_glob_func=   lambda x: func1(x)               # 0.0695          fastest
  , f_staticmethd= lambda x: klas1.func1(x)         # 0.0845 %avg=121
    )


def for_loop(x):
    for a in x:
        if len(a)>9: return True
    return False
c_for_loop_vs_gen_for = dict(
    for_loop = lambda x: for_loop(x)                    #0.1882          fastest
  , gen_loop = lambda x: any( [len(a)>9 for a in x ])   #0.2767 %avg=147
    )


d = dict( a=1, b=2, c=35)
d_get = d.get
c_dictget_vs_dict_subscr = dict(
    dictgetattr_get = lambda x: d.get(x)                #0.0457 %avg=119
  , dictfuncget     = lambda x: d_get(x)                #0.0430 %avg=112
  , dictin_dictsubscr   = lambda x: x in d and d[x]     #0.0431 %avg=112
  , dictsubscr          = lambda x: d[ 'a']             #0.0383          fastest
    )


l = [ 1, 2, 3]
l_get = l.__getitem__
c_listget_vs_list_subscr = dict(
    listgetattr_get = lambda x: l.__getitem__(len(x)%3) #0.0726 %avg=144
  , listfuncget     = lambda x: l_get(len(x)%3)         #0.0743 %avg=148
  , listsubscr      = lambda x: l[len(x)%3]             #0.0501          fastest
    )


class property_vs_funccall:
    def func( me):
        if 'z' in me.__class__.__name__: return 123
        return me.__class__
    prop = property( func)
_g = property_vs_funccall()
c_property_vs_funccall = dict(
    property = lambda x: _g.prop        #0.069          fastest
  , funccall = lambda x: _g.func()      #0.076 %avg=109
    )


_abc = ('a','b','c')
c_a_in_abc_vs_a_eq_b_or = dict(
    x_in_str   = lambda x: x in 'abc'                       #0.0357          # 1 fastest
  , x_in_tuple = lambda x: x in ('a','b','c')               #0.0484 %avg=135 # 3
  , x_in_tuple_global= lambda x: x in _abc                  #0.0502 %avg=140 # 4
  , x_eq_a_or  = lambda x: x == 'a' or x =='b' or x == 'c'  #0.0444 %avg=124 # 2
    )


from collections import namedtuple
class plain:
    def __init__(me, x,y):
        me.x=x
        me.y=y
class slots:
    __slots__=['x','y']
    def __init__(me, x,y):
        me.x=x
        me.y=y
xy = namedtuple( 'xy', ['x','y'])

#comment dataclasses for py2
from dataclasses import dataclass
@dataclass
class datakl:
   x: int
   y: int
@dataclass(frozen=True)
class dataklfrz:
   x: int
   y: int
@dataclass(slots=True)
class dataklslt:
   x: int
   y: int
@dataclass(slots=True,frozen=True)
class datakl_s_f:
   x: int
   y: int

c_tuple_vs_slots = dict(
    slots= lambda x: slots( len(x), 4-len(x))                       #0.1206 %avg=185 # 4
  , plain= lambda x: plain( len(x), 4-len(x))                       #0.1262 %avg=194 # 6
  , tuple= lambda x: ( len(x), 4-len(x))                            #0.0650 %avg=    # 1 fastest
  , dict = lambda x: dict( x=len(x), y=4-len(x))                    #0.1224 %avg=188 # 5
  , namedtuple= lambda x: xy( len(x), 4-len(x))                     #0.2366 %avg=363 # 8
  , slots_kw        = lambda x: slots( x=len(x), y=4-len(x))        #0.2435 %avg=374 #10
  , slots_kw1       = lambda x: slots( len(x), y=4-len(x))          #0.2393 %avg=368 # 9
  , plain_kw        = lambda x: plain( x=len(x), y=4-len(x))        #0.2541 %avg=391 #11
  , dict_literal    = lambda x: { 'x':len(x), 'y':4-len(x)}         #0.1091 %avg=167 # 2 fastest2
  , dataclass       = lambda x: datakl( len(x), 4-len(x))           #0.1270 %avg=195 # 7
  , dataclass_frozen= lambda x: dataklfrz( len(x), 4-len(x))        #0.2690 %avg=413 #14
  , dataclass_kw    = lambda x: datakl( x=len(x), y=4-len(x))       #0.2542 %avg=391 #12
  , dataclass_slots = lambda x: dataklslt( len(x), 4-len(x))        #0.1186 %avg=182 # 3
  , dataclass_slots_frozen = lambda x: datakl_s_f( len(x),4-len(x)) #0.2605 %avg=400 #13
    )


objs = dict( (k,c_tuple_vs_slots[k]('z')) for k in '''
  slots                 #0.0627 %avg=102
  plain                 #0.0614 %avg=100
  namedtuple            #0.0610          -fastest
  dataclass             #0.0615 %avg=101
  dataclass_slots       #0.0631 %avg=103 -slowest~
  dataclass_frozen      #0.0616 %avg=100
'''.split() if k[0].isalpha() and k in c_tuple_vs_slots)
c_obj_attr_access = dict( (k, lambda x,  j=o: getattr( j, 'x')) for k,o in objs.items())


def afunc( a, b, c, d): return a+b+c+d
def afunc2( a, b, c, d, **ignore): return a+b+c+d
def afunc3( a, b, c, d, e=None  ): return a+b+c+d
c_funccall_args_vs_kargs= dict(
    args= lambda x: afunc( x,x,x,x)                         #0.1339           # 1 fastest
  , kargs= lambda x: afunc( a=x,b=x,c=x,d=x)                #0.1547 %avg=115  # 3
  , args_kargs= lambda x: afunc( x,b=x,c=x,d=x)             #0.1536 %avg=114  # 2
  , kargs_ignored= lambda x: afunc2( a=x,b=x,c=x,d=x, e=x)  #0.2318 %avg=173  # 6
  , kargs_default= lambda x: afunc3( a=x,b=x,c=x,d=x, e=x)  #0.1608 %avg=120  # 5
  , kargs_default1= lambda x: afunc3( a=x,b=x,c=x,d=x)      #0.1555 %avg=116  # 4
  )


def dictloop( x):
    r = {}
    for k in range( 75): r[k] = k*3
    return r
c_dictcomp_vs_dict_gen_tuples_vs_loop = dict(
    dictcomp = lambda x: { k:k*3 for k in range( 75)}               #2.51 %avg=    fastest
  , dict_gen_tuples= lambda x: dict( (k,k*3) for k in range( 75))   #4.77 %avg=189
  , dict_listcomp  = lambda x: dict( [(k,k*3) for k in range( 75)]) #4.25 %avg=168
  , dictloop = dictloop                                             #2.55 %avg=101 fastest2
  )


def listloop1( x):
    r = []
    for k in range( 75): r.append( k*3)
    return r
def listloop2( x):
    r = []
    r_append = r.append
    for k in range( 75): r_append( k*3)
    return r
c_listcomp_vs_list_gen_vs_loop= dict(
    listcomp = lambda x: [ k*3 for k in range( 75)]         #1.398           # 1  fastest
  , list_gen = lambda x: list( k*3 for k in range( 75))     #2.465 %avg=176  # 4
  , listloop1 = listloop1                                   #1.711 %avg=122  # 2  fastest2
  , listloop2 = listloop2                                   #2.001 %avg=143  # 3
  )


###############

TARGET = None
#TARGET = c_dictget_vs_dict_subscr

import sys
TARGET = TARGET or sys.argv[1:] and sys.argv[1]

from this import s as txt
words = txt.split()
import timeit
def runner(f): return [ f( w) for w in words ]

ttt = namedtuple( 'ttt', ['min','max','avg'])

for name,target in globals().copy().items():
    if not name.startswith( 'c_'): continue
    if TARGET:
        if TARGET!=name if isinstance( TARGET, str) else (TARGET is not target): continue
    print( '::::', name, '::::')
    res = {}
    for k,f in target.items():
        r = sorted(timeit.repeat( lambda: runner(f), number= 5000))
        res[k] = ttt( min= r[0], max= r[-1], avg= sum(r)/len(r))
    rsorted = sorted( res, key= lambda k: res[k].avg )  #was .min
    for k,r in res.items():
        avg_ratio = 100*r.avg/res[rsorted[0]].avg
        avg_ratio = int(avg_ratio) if avg_ratio != 100 else ' '
        avg_index = 1+rsorted.index(k)
        print( ' {k:<22} avg={r.avg:<9.6f} min={r.min:<9.6f} max={r.max:<9.6f}  %avg={avg_ratio:3}  #{avg_index:2}'.format(**locals()) )

# vim:ts=4:sw=4:expandtab

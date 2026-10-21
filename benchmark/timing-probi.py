#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from __future__ import print_function #,unicode_literals

_pfxst= ("~#", "~$", "~:")
_pfxsl= ["~#", "~$", "~:"]
_pfxsd= dict.fromkeys( _pfxst)
_lpfxst= _pfxst*20
_lpfxsl= _pfxsl*20
c_pfx_check = dict(
    f_tuple=        lambda x: x[:2] in ("~#", "~$", "~:")   #.106
  , f_list=         lambda x: x[:2] in ["~#", "~$", "~:"]   #.107
  , f_tuple_global= lambda x: x[:2] in _pfxst               #.108
  , f_list_global=  lambda x: x[:2] in _pfxsl               #.109
  , f_dict_global=  lambda x: x[:2] in _pfxsd               #.097  fastest2
  , f_tuple_global20= lambda x: x[:2] in _lpfxst            #.617
  , f_list_global20=  lambda x: x[:2] in _lpfxsl            #.635
  , f_one_by_one=   lambda x: x[0]=='~' and x[1] in "#$:"   #.059  fastest
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

#just def func -> class.staticmethod -> 10% slower! XXX
def func1( x): return x and x != 'asd' and len(x)
class klas1:
    func1 = staticmethod( func1)
c_func_glob_vs_staticmethod= dict(
    f_glob_func=   lambda x: func1(x)               # 83     fastest
  , f_staticmethd= lambda x: klas1.func1(x)         # 97
    )

def for_loop(x):
    for a in x:
        if len(a)>9: return True
    return False
c_for_loop_vs_gen_for = dict(
    for_loop = lambda x: for_loop(x)                    #.177   fastest
  , gen_loop = lambda x: any( [len(a)>9 for a in x ])   #.332
    )

d = dict( a=1, b=2, c=35)
d_get = d.get
c_dictget_vs_dict_subscr = dict(
    dictgetattr_get = lambda x: d.get(x)                # 75
  , dictfuncget     = lambda x: d_get(x)                # 51    fastest?
  , dictin_dictsubscr   = lambda x: x in d and d[x]     # 52    fastest?
  , dictsubscr          = lambda x: d[ 'a']             # 45
    )

l = [ 1, 2, 3]
l_get = l.__getitem__
c_listget_vs_list_subscr = dict(
    listgetattr_get = lambda x: l.__getitem__(len(x)%3) # 76
  , listfuncget     = lambda x: l_get(len(x)%3)         # 73
  , listsubscr      = lambda x: l[len(x)%3]             # 58
    )

class property_vs_funccall:
    def func( me):
        if 'z' in me.__class__.__name__: return 123
        return me.__class__
    prop = property( func)
_g = property_vs_funccall()
c_property_vs_funccall = dict(
    property = lambda x: _g.prop        # 101
  , funccall = lambda x: _g.func()      #  87   fastest
    )

_abc = ('a','b','c')
c_a_in_abc_vs_a_eq_b_or = dict(
    x_in_str   = lambda x: x in 'abc'                       # 437   fastest
  , x_in_tuple = lambda x: x in ('a','b','c')               # 610
  , x_in_tuple_global= lambda x: x in _abc                  # 585
  , x_eq_a_or  = lambda x: x == 'a' or x =='b' or x == 'c'  # 596
    )

from collections import namedtuple
from dataclasses import dataclass
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
    slots= lambda x: slots( len(x), 4-len(x))                       #.15    0.1216 0.1211 fastest4
  , plain= lambda x: plain( len(x), 4-len(x))                       #.162   0.1281 0.1273
  , tuple= lambda x: ( len(x), 4-len(x))                            #.078   0.0649 0.0655 fastest
  , dict = lambda x: dict( x=len(x), y=4-len(x))                    #.124   0.1224 0.1233 fastest5
  , namedtuple= lambda x: xy( len(x), 4-len(x))                     #.22    0.2363 0.2350
  , dataclass = lambda x: datakl( len(x), 4-len(x))                 #.159   0.1287 0.1276
  , dataclass_frozen= lambda x: dataklfrz( len(x), 4-len(x))        #.33    0.2696 0.2666
  , dataclass_kw    = lambda x: datakl( x=len(x), y=4-len(x))       #.?     0.2552 0.2502
  , slots_kw        = lambda x: slots( x=len(x), y=4-len(x))        #?      0.2447 0.2441
  , slots_kw1       = lambda x: slots( len(x), y=4-len(x))          #?      0.2405 0.2387
  , plain_kw        = lambda x: plain( x=len(x), y=4-len(x))        #?
  , dict_literal    = lambda x: { 'x':len(x), 'y':4-len(x)}         #?      0.1084 0.1103 fastest2
  , dataclass_slots = lambda x: dataklslt( len(x), 4-len(x))        #?      0.1204 0.1214 fastest3
  , dataclass_slots_frozen = lambda x: datakl_s_f( len(x),4-len(x)) #?      0.2577 0.2604
    )













objs = dict( (k,c_tuple_vs_slots[k]('z')) for k in '''
  slots                 #0.05554 0.06392 -slowest~
  plain                 #0.05456 0.06082
  namedtuple            #0.05245 0.06024
  dataclass             #0.05481 0.06159
  dataclass_slots       #0.05585 0.06272 -slowest~
  dataclass_frozen      #0.05467 0.06089
'''.split() if k[0].isalpha())
c_obj_attr_access = dict( (k, lambda x,*,j=o: getattr( j, 'x')) for k,o in objs.items())

def dictloop( x):
    r = {}
    for k in range( 75): r[k] = k*3
    return r
c_dictcomp_vs_dict_gen_tuples_vs_loop = dict(
    dictcomp = lambda x: { k:k*3 for k in range( 75)}               #2.94       fastest
  , dict_gen_tuples= lambda x: dict( (k,k*3) for k in range( 75))   #6.0  +90%
  , dict_listcomp  = lambda x: dict( [(k,k*3) for k in range( 75)]) #5.37 +80%
  , dictloop = dictloop                                             #3.10       fastest2
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
    listcomp = lambda x: [ k*3 for k in range( 75)]         # 1.04 100%     fastest
  , list_gen = lambda x: list( k*3 for k in range( 75))     # 1.8  +80%
  , listloop1 = listloop1                                   # 1.17 +10%     fastest2
  , listloop2 = listloop2                                   # 1.75 +50% WTF
  )

def afunc( a, b, c, d): return a+b+c+d
def afunc2( a, b, c, d, **ignore): return a+b+c+d
def afunc3( a, b, c, d, e=None  ): return a+b+c+d
c_funccall_args_vs_kargs= dict(
    args= lambda x: afunc( x,x,x,x)                         # .13   fastest
  , kargs= lambda x: afunc( a=x,b=x,c=x,d=x)                # .15   fastest2
  , kargs_ignored= lambda x: afunc2( a=x,b=x,c=x,d=x, e=x)  #.247   slow
  , kargs_default= lambda x: afunc2( a=x,b=x,c=x,d=x, e=x)  #.247   same
  )

###############

TARGET = None
#TARGET = c_dictcomp_vs_dict_gen_tuples_vs_loop
#TARGET = c_listcomp_vs_list_gen_vs_loop
#TARGET = c_dictget_vs_dict_subscr

import sys
TARGET = TARGET or sys.argv[1:] and sys.argv[1]

from this import s as txt
words = txt.split()
import timeit
def runner(f): return [ f( w) for w in words ]

@dataclass
class ttt:
    min: float
    max: float
    avg: float

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
        print( f' {k:<22} avg={r.avg:<9.6f} min={r.min:<9.6f} max={r.max:<9.6f}  %avg={avg_ratio:3}  #{avg_index:2}' )

# vim:ts=4:sw=4:expandtab

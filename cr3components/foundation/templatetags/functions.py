# ref http://djangosnippets.org/snippets/2189/

import inspect
from functools import partial
from django.template import TemplateSyntaxError



def isiterable(obj):
    '''
    Check if arg is iterable. Object is iterable when implements metod __iter__.
    '''
    return hasattr(obj, '__iter__')

def isstring(obj):
    '''
    Check whether `obj` is a string instance, i.e. str or unicode instance.
    '''
    return isinstance(obj, basestring)



_ARGS_TYPES = (_BOTH, _ARGS_ONLY, _KWARGS_ONLY) = (0, 1, 2)
def _parse_args_and_kwargs(parser, bits_iter, sep=",", tagname=None, type=_BOTH,
                          stop_test=lambda bit: False, return_stop_bit=False):
    '''
    :param type: indicates to support _ARGS_ONLY, _KWARGS_ONLY or _BOTH.
    '''
    assert type in _ARGS_TYPES, "'type' argument must be one of: _BOTH, _ARGS_ONLY, _KWARGS_ONLY."
    args_only, kwargs_only = (type == _ARGS_ONLY), (type == _KWARGS_ONLY)
    args = []
    kwargs = {}
    tagname = " '%s'" % tagname if tagname else ""
    bit_test = stop_test if inspect.isfunction(stop_test) else\
               (lambda bit: bit in stop_test) if (isiterable(stop_test) and not isstring(stop_test)) else\
               (lambda bit: bit == stop_test)
    stop_bit = None
    for bit in bits_iter:
        if bit_test(bit):
            # if we would like to stop on the bit that passes the test:
            #bits_iter = itertools.chain((bit,), bits_iter)
            stop_bit = bit
            break
        for arg in bit.split(sep):
            if '=' in arg:
                if args_only:
                    raise TemplateSyntaxError("Tag%s does not support kwargs arguments." % tagname)
                k, v = arg.split('=', 1)
                k = str(k.strip())
                if k in kwargs:
                    raise TemplateSyntaxError("Duplicate key '%s' in%s tag kwargs." % (k, tagname))
                kwargs[k] = parser.compile_filter(v)
            elif arg:
                if kwargs_only:
                    raise TemplateSyntaxError("Tag%s does not support non-kwargs arguments." % tagname)
                args.append(parser.compile_filter(arg))
    ret = (args,) if args_only else\
          (kwargs,) if kwargs_only else\
          (args, kwargs)
    if return_stop_bit:
        ret += (stop_bit,)
    if len(ret) == 1:
        return ret[0]
    return ret

parse_args_and_kwargs = partial(_parse_args_and_kwargs, type=_BOTH)
parse_args_and_kwargs.__name__ = 'parse_args_and_kwargs'
parse_args_and_kwargs.__doc__ =\
'''
Parses bits created form token "arg1,key1=val1, arg2 , ..." after splitting
contents.

:param sep: Single bit separator; by default ",".
:rtype sep: str

:param stop_test: Optional test to stop parsing earlier. This can be one of:
 * single string with keyword to stop on
 * list of string keywords to stop on
 * function which takes only current bit of `bits_iter` as an argument and
   returns boolean value.
Attention: `bits_iter` will be stopped after the bit that passes the test.
           To obtain the stop bit use `return_stop_bit` flag and capture the
           additional return value.
:rtype stop_test: str or list or callable

:returns: List of args and dictionary of kwargs with values compiled with the
          parser.compile_filter() function. If `return_stop_bit` is True then
          also the the last bit at which parsing stopped (see `stop_test`).
:rtype: tuple(list, dict [, basestring or None])
'''
parse_args = partial(_parse_args_and_kwargs, type=_ARGS_ONLY)
parse_args.__name__ = 'parse_args'
parse_args.__doc__ =\
'''
Parses bits created form token "arg1,arg2 , ...", after splitting contents. See
`parse_args_and_kwargs` for params details.

:returns: List of args with values compiled with the parser.compile_filter()
          function. If `return_stop_bit` is True then also the the last bit at
          which parsing stopped (see `stop_test`).
:rtype: list or tuple(list, basestring or None)
'''
parse_kwargs = partial(_parse_args_and_kwargs, type=_KWARGS_ONLY)
parse_kwargs.__name__ = 'parse_kwargs'
parse_kwargs.__doc__ =\
'''
Parses bits created form token "key1=val1, key2=val2, ...", after splitting
contents. See parse_args_and_kwargs` for params details.

:returns: Dictionary of kwargs with values compiled with the
          parser.compile_filter() function. If `return_stop_bit` is True then
          also the the last bit at which parsing stopped (see `stop_test`).
:rtype: dict or tuple(dict, basestring or None)
'''

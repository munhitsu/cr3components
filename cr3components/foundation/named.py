"""
a wrapper on eventlet to have some working version of named
"""

try:
    from eventlet.api import named
except ImportError:
    def named(name):
        """Return an object given its name.
    
        The name uses a module-like syntax, eg::
    
          os.path.join
    
        or::
    
          mulib.mu.Resource
        """
        toimport = name
        obj = None
        import_err_strings = []
        while toimport:
            try:
                obj = __import__(toimport)
                break
            except ImportError, err:
                # print 'Import error on %s: %s' % (toimport, err)  # debugging spam
                import_err_strings.append(err.__str__())
                toimport = '.'.join(toimport.split('.')[:-1])
        if obj is None:
            raise ImportError('%s could not be imported.  Import errors: %r' % (name, import_err_strings))
        for seg in name.split('.')[1:]:
            try:
                obj = getattr(obj, seg)
            except AttributeError:
                dirobj = dir(obj)
                dirobj.sort()
                raise AttributeError('attribute %r missing from %r (%r) %r.  Import errors: %r' % (
                    seg, obj, dirobj, name, import_err_strings))
        return obj

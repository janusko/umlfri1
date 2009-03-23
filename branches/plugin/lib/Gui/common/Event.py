from lib.Depend.gtk2 import gobject

import sys


def event(obj, *args):
    """
        event(obj, event)
        or
        event(type), where type is one of ('load', )
    """
    def tmp(fnc):
        if len(args) > 0:
            event = args[0]
            params = args[1:]
        else:
            event = None
            params = args
        if not hasattr(fnc, 'events'):
            def tmp2(self, *args, **kw_args):
                try:
                    return fnc(self, *args, **kw_args)
                except Exception, e:
                    exccls, excobj, tb = sys.exc_info()
                    self.application.DisplayException(exccls, excobj, tb)

            fncx = tmp2
            fncx.events = []
        else:
            fncx = fnc
        fncx.events.append((obj, event, params))
        return fncx

    return tmp

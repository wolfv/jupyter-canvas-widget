from ._version import version_info, __version__

from .raw_canvas import *

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'fastcanvas',
        'require': 'fastcanvas/extension'
    }]

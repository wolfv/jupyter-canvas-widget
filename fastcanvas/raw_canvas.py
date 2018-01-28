import ipywidgets as widgets
from traitlets import Unicode
from traittypes import Array

import logging
import numpy as np
import math

try:
	from io import BytesIO as StringIO # python3
except:
	from StringIO import StringIO # python2

from base64 import b64encode
import warnings

# Code extracted from maartenbreddels ipyvolume
def array_to_binary(ar, obj=None, force_contiguous=True):
	if ar is None:
		return None
	if ar.dtype.kind not in ['u', 'i', 'f']:  # ints and floats
		raise ValueError("unsupported dtype: %s" % (ar.dtype))
	if ar.dtype == np.float64:  # WebGL does not support float64, case it here
		ar = ar.astype(np.float32)
	if ar.dtype == np.int64:  # JS does not support int64
		ar = ar.astype(np.int32)
	if force_contiguous and not ar.flags["C_CONTIGUOUS"]:  # make sure it's contiguous
		ar = np.ascontiguousarray(ar)
	return {'buffer': memoryview(ar), 'dtype': str(ar.dtype), 'shape': ar.shape}

def binary_to_array(value, obj=None):
	return np.frombuffer(value['data'], dtype=value['dtype']).reshape(value['shape'])

ndarray_serialization = dict(to_json=array_to_binary, from_json=binary_to_array)

@widgets.register
class RawCanvas(widgets.DOMWidget):
    """An example widget."""
    _view_name = Unicode('RawCanvasView').tag(sync=True)
    _model_name = Unicode('RawCanvasModel').tag(sync=True)
    _view_module = Unicode('fastcanvas').tag(sync=True)
    _model_module = Unicode('fastcanvas').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    data = Array(default_value=None, allow_none=True).tag(sync=True, **ndarray_serialization)

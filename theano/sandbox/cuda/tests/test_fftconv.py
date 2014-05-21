import unittest
import numpy

import theano

# Skip tests if cuda_ndarray is not available.
from nose.plugins.skip import SkipTest
import theano.sandbox.cuda as cuda_ndarray
if cuda_ndarray.cuda_available == False:
    raise SkipTest('Optional package cuda disabled')

if theano.config.mode == 'FAST_COMPILE':
    mode_with_gpu = theano.compile.mode.get_mode('FAST_RUN').including('gpu')
else:
    mode_with_gpu = theano.compile.mode.get_default_mode().including('gpu')

def TestConv2dFFT(unittest.TestCase):
    def setUp(self):
        self._prev = theano.confg.enable_conv2d_fft
        theano.confg.enable_conv2d_fft = True

    def tearDown(self):
        theano.confg.enable_conv2d_fft = self._prev

    def test_valid(self):
        inputs_shape = (5, 3, 7, 6)
        filters_shape = (2, 3, 3, 3)

        inputs_val = numpy.random.random(inputs_shape).astype('float32')
        filters_val = numpy.random.random(filters_shape).astype('float32')

        inputs = shared(inputs_val)
        filters = shared(filters_val)

        conv = theano.tensor.nnet.conv.conv2d(inputs, filters)

        f_ref = theano.function([], conv)
        f_fft = theano.function([], conv, mode=mode_with_gpu)

        res_ref = f_ref()
        res_fft = f_fft()

        numpy.testing.assert_allclose(res_ref, res_fft)

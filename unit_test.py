from PIL import Image, ImageDraw
import _matrix
import numpy

class TestClass:
    def compare_helper(self,A,B):
        for i in range(len(A)):
            for j in range(len(A[i])):
                if (A[i][j] != B[i][j]):
                    return 0
        return 1

    '''Test for zero-length 2-vector (invalid input)'''
    def test_generate_cipher(self):
        origin = Image.open('testing/message.png')
        origin = origin.convert('1')
        width=origin.size[0]*2
        height=origin.size[1]*2
        pix = numpy.array(origin)
        _m1 = _matrix.Matrix(pix)
        out_image_B = Image.new('1', (width, height))
        b = numpy.array(out_image_B)
        _m2 = _matrix.Matrix(numpy.array(Image.open('testing/secret.png').convert('1')))
        _m3 = _matrix.Matrix(b)
        res = _matrix.generate_cipher(_m1,_m2,_m3,int(width/2),int(height/2))
        res = numpy.asarray(_matrix.to_matrix(res))
        target = numpy.array(Image.open('testing/ciphered.png').convert('1'))
        assert self.compare_helper(res,target) == 1
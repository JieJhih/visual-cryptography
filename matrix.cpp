#include "matrix.h"

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <algorithm>
namespace py = pybind11;

// There are 6 possible patterns. The four digits represent 4x4 pixel blocks
const std::array<std::array<double, 4>, 6>  pattern = {{{1,1,0,0},{1,0,1,0},{0,1,1,0},{1,0,0,1},{0,1,0,1},{0,0,1,1}}};
const int min = 0;
const int max = 5;
bool Matrix::operator==(const Matrix &other) {
  if (m_row != other.m_row || m_col != other.m_col) {
    return false;
  }
  for (size_t i = 0; i < m_row*m_col; ++i) {
      if ((*this)(i/m_row, i%m_col) != other(i/m_row, i%m_col)) {
        return false;
      }
  }
  return true;
}

std::pair<Matrix,Matrix> generate(const Matrix &origin, Matrix &message, Matrix &secret, int width, int height) {
  srand( time(NULL) );
/*
  These relate to the xor and overlay diagrams above
  For every black or white pixel in the original image
  the loop below replaces them systematically with
  a pattern.
  Black pixels get replaced with pattern and 'anti-pattern'
  to create a mixed black pixel on the final overlaid image
*/
  for(int x=0; x<height; x++) {
    for(int y=0; y<width; y++) {
      double pixel = origin(x,y);
      std::array<double,4> pat = pattern[rand() % (max - min + 1) + min];
      message(x*2,y*2) = pat[0];
      message(x*2+1, y*2) = pat[1];
      message(x*2, y*2+1) = pat[2];
      message(x*2+1, y*2+1) = pat[3];

      if(pixel == 0) {
        secret(x*2,y*2) = 1-pat[0];
        secret(x*2+1, y*2) = 1-pat[1];
        secret(x*2, y*2+1) = 1-pat[2];
        secret(x*2+1, y*2+1) = 1-pat[3];
      } else {
        secret(x*2,y*2) = pat[0];
        secret(x*2+1, y*2) = pat[1];
        secret(x*2, y*2+1) = pat[2];
        secret(x*2+1, y*2+1) = pat[3];
      }
    }
  }
  return std::pair<Matrix,Matrix>(message,secret);
}

inline size_t Boundary(size_t n, size_t root) {
  if(n>root)
    return root;
    return n;
}

Matrix generate_cipher(const Matrix &origin, Matrix &message, Matrix &secret, int width, int height) {
    for(int x=0; x<height; x++) {
    for(int y=0; y<width; y++) {
      double s = origin(x,y);
      double m = message(x/2,y/2);
      double color;
      double pixel = origin(x,y);
      std::array<double,4> pat;
      pat[0] = message(x*2,y*2);
      pat[1] = message(x*2+1, y*2);
      pat[2] = message(x*2, y*2+1);
      pat[3] = message(x*2+1, y*2+1);
      if((m > 0 && s > 0) || (m == 0 && s == 0)) {
        color = 0;
      } else {
        color = 1;
      }
      if(pixel == 0) {
        secret(x*2,y*2) = 1-pat[0];
        secret(x*2+1, y*2) = 1-pat[1];
        secret(x*2, y*2+1) = 1-pat[2];
        secret(x*2+1, y*2+1) = 1-pat[3];
      } else {
        secret(x*2,y*2) = pat[0];
        secret(x*2+1, y*2) = pat[1];
        secret(x*2, y*2+1) = pat[2];
        secret(x*2+1, y*2+1) = pat[3];
      }
    }
  }
  return secret;
}

py::array_t<bool> to_matrix(const Matrix &m)
{

    size_t N = m.nrow();
    size_t M = m.ncol();
    
    py::array_t<bool, py::array::c_style> arr({N, M});
    auto ra = arr.mutable_unchecked();
  
    for (size_t i = 0; i < N; i++)
    {
        for (size_t j = 0; j < M; j++)
        {
            ra(i, j) = (bool)m(i,j);
        }
    }

    return arr;
}


PYBIND11_MODULE(_matrix, m) {
  m.def("generate_cipher", &generate_cipher);
  m.def("generate", &generate);
  m.def("to_matrix", &to_matrix);

  py::class_<Matrix>(m, "Matrix")
      .def(py::init<size_t, size_t>())
      .def(py::init<const std::vector<std::vector<double>> &>())
      .def_property_readonly("nrow", &Matrix::nrow)
      .def_property_readonly("ncol", &Matrix::ncol)
      .def("__eq__", &Matrix::operator==)
      .def("__getitem__",
           [](const Matrix &m, std::array<double, 2> i) { return m(i[0], i[1]); })
      .def("__setitem__", [](Matrix &m, std::array<double, 2> i, double v) {
        m(i[0], i[1]) = v;
      });
} 
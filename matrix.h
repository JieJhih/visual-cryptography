#ifndef MATRIX_H_
#define MATRIX_H_

#include <cstddef>
#include <vector>

class Matrix {
    public:
        Matrix(size_t row, size_t col) : m_row(row), m_col(col), m_buffer(row , std::vector <double> (col, 0)) {}
        Matrix(const std::vector<std::vector<double>> &m) {
              m_row = m.size();
              m_col = m[0].size();
              m_buffer.clear();
              for(size_t i=0; i<m_row; i++) {
                m_buffer.push_back(std::vector<double>(0,0));
                for(size_t j=0; j<m_col; j++) {
                  m_buffer[i].push_back(m[i][j]);
                }
              }
                                  
        }
        size_t nrow() const { return m_row; }
        size_t ncol() const { return m_col; }
        double *buffer() { return &m_buffer[0][0]; }
        const double *buffer() const { return &m_buffer[0][0]; }

        bool operator==(const Matrix &other);
        double & operator() (size_t r, size_t c) {
		    return m_buffer[r][c];
	    }
        const double & operator() (size_t r, size_t c) const {
		    return m_buffer[r][c];
	    }

    private:
        size_t m_row;
        size_t m_col;
        std::vector<std::vector<double> > m_buffer;
};

std::pair<Matrix,Matrix> generate(const Matrix &origin, Matrix &message, Matrix &secret, int width, int height);
Matrix generate_cipher(const Matrix &origin, Matrix &message, Matrix &secret, int width, int height);

#endif 
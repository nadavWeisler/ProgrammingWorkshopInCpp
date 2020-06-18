#include "Matrix.h"

#define INVALID_MATRIX_ERROR "ERROR: invalid matrix"
#define INVALID_INPUT_ERROR "ERROR: invalid input"
#define SIZE_ERROR "ERROR: matrix size is invalid for this operation"
#define INVALID_READ_ERROR "ERROR: unable to read your file"
#define DEFAULT_ROWS 1
#define DEFAULT_COLS 1
#define DEFAULT_VALUE 0

/**
 * Constructs Matrix rows * cols
 * Inits all elements to 0
 */
Matrix::Matrix(int rows, int cols)
{
	if (rows <= 0 || cols <= 0)
	{
		std::cerr << INVALID_MATRIX_ERROR << std::endl;
		exit(EXIT_FAILURE);
	}
	this->_dims = new MatrixDims();
	this->_dims->rows = rows;
	this->_dims->cols = cols;
	this->_mat = new float[rows * cols];
	for (int i = 0; i < rows * cols; ++i)
	{
		this->_mat[i] = DEFAULT_VALUE;
	}
}

/**
 * Constructs 1*1 Matrix
 * Inits the single element to 0
 */
Matrix::Matrix() : Matrix(DEFAULT_ROWS, DEFAULT_COLS)
{

}

/**
 * Copy constructor
 * @param otherMatrix	Matrix
 */
Matrix::Matrix(const Matrix& otherMatrix) : Matrix(otherMatrix.getRows(), otherMatrix.getCols())
{
	for (int i = 0; i < this->_dims->cols * this->_dims->rows; ++i)
	{
		this->_mat[i] = otherMatrix._mat[i];
	}
}

/**
 * Matrix destructor
 */
Matrix::~Matrix()
{
	delete[] this->_mat;
	this->_mat = nullptr;
	delete this->_dims;
	this->_dims = nullptr;
}

/**
 * returns the amount of rows as int
 * @return	amount of rows as int
 */
int Matrix::getRows() const
{
	return this->_dims->rows;
}

/**
 * returns the amount of cols as int
 * @return	amount of cols as int
 */
int Matrix::getCols() const
{
	return this->_dims->cols;
}

/**
 * Transforms a matrix into a column vector
 * @return	Matrix
 */
Matrix& Matrix::vectorize()
{
	this->_dims->rows *= this->_dims->cols;
	this->_dims->cols = 1;
	return *this;
}

/**
 * Prints matrix elements, no return value.
 */
void Matrix::plainPrint() const
{
	for (int row = 0; row < this->_dims->rows; ++row)
	{
		for (int col = 0; col < this->_dims->cols; ++col)
		{
			std::cout << (*this)(row, col) << " ";
		}
		std::cout << std::endl;
	}
}

/**
 * Assignment
 * @param otherMatrix	Matrix
 * @return				this
 */
Matrix& Matrix::operator=(const Matrix& otherMatrix)
{
	if (this != &otherMatrix)
	{
		this->_dims->rows = otherMatrix.getRows();
		this->_dims->cols = otherMatrix.getCols();
		delete[] (this->_mat);
		this->_mat = new float[otherMatrix.getRows() * otherMatrix.getCols()];
		for (int i = 0; i < otherMatrix.getCols() * otherMatrix.getRows(); ++i)
		{
			this->_mat[i] = otherMatrix._mat[i];
		}
	}

	return *this;
}

/**
 * Matrix multiplication
 * @param otherMatrix	Matrix
 * @return				Matrix
 */
Matrix Matrix::operator*(const Matrix& otherMatrix) const
{
	if (this->_dims->cols != otherMatrix.getRows())
	{
		std::cerr << SIZE_ERROR << std::endl;
		exit(EXIT_FAILURE);
	}

	Matrix newMatrix(this->_dims->rows, otherMatrix.getCols());
	for (int row = 0; row < newMatrix.getRows(); ++row)
	{
		for (int col = 0; col < newMatrix.getCols(); ++col)
		{
			for (int i = 0; i < this->getCols(); ++i)
			{
				newMatrix(row, col) += ((*this)(row, i) * otherMatrix(i, col));
			}
		}
	}
	return newMatrix;
}

/**
 * Scalar multiplication on the right
 * @param scalar	scalar
 * @return			Matrix
 */
Matrix Matrix::operator*(const float scalar) const
{
	Matrix newMatrix(*this);
	for (int i = 0; i < (newMatrix.getRows() * newMatrix.getCols()); ++i)
	{
		newMatrix[i] *= scalar;
	}
	return newMatrix;
}

/**
 * Scalar multiplication on the left
 * @param scalar			scalar
 * @param otherMatrix		Matrix
 * @return					Matrix
 */
Matrix operator*(float scalar, const Matrix& otherMatrix)
{
	const Matrix& newMatrix(otherMatrix);
	return newMatrix * scalar;
}

/**
 * Matrix addition
 * @param otherMatrix	Matrix
 * @return				Matrix
 */
Matrix Matrix::operator+(const Matrix& otherMatrix) const
{
	if (this->_dims->cols != otherMatrix.getCols() ||
		this->_dims->rows != otherMatrix.getRows())
	{
		std::cerr << SIZE_ERROR << std::endl;
		exit(EXIT_FAILURE);
	}
	Matrix newMatrix(this->_dims->rows, this->_dims->cols);
	for (int i = 0; i < this->getRows() * this->getCols(); ++i)
	{
		newMatrix[i] = this->_mat[i] + otherMatrix._mat[i];
	}
	return newMatrix;
}

/**
 * Matrix addition accumulation
 * @param otherMatrix	Matrix
 * @return				Matrix
 */
Matrix& Matrix::operator+=(const Matrix& otherMatrix)
{
	*this = *this + otherMatrix;
	return *this;
}

/**
 * Parenthesis indexing
 * @param row	row
 * @param col	column
 * @return		this(row, col)
 */
float& Matrix::operator()(int row, int col)
{
	if (row < 0 || row >= this->_dims->rows ||
		col < 0 || col >= this->_dims->cols)
	{
		std::cerr << INVALID_INPUT_ERROR << std::endl;
		exit(EXIT_FAILURE);
	}
	return this->_mat[row * _dims->cols + col];

}

/**
 * Parenthesis indexing, const
 * @param row	row
 * @param col	column
 * @return		this(row, col)
 */
const float& Matrix::operator()(int row, int col) const
{
	if (row < 0 || row >= this->_dims->rows ||
		col < 0 || col >= this->_dims->cols)
	{
		std::cerr << INVALID_INPUT_ERROR << std::endl;
		exit(EXIT_FAILURE);
	}
	return this->_mat[row * this->getCols() + col];
}

/**
 * Brackets indexing
 * @param index		Index
 * @return		this[i]
 */
float& Matrix::operator[](int index)
{
	if ((index >= this->_dims->rows * this->_dims->cols) || (index < 0))
	{
		std::cerr << INVALID_INPUT_ERROR << std::endl;
		exit(EXIT_FAILURE);
	}
	return this->_mat[index];
}

/**
 * Brackets indexing, const
 * @param index 	Index
 * @return 		this[i]
 */
const float& Matrix::operator[](int index) const
{
	if ((index >= this->_dims->rows * this->_dims->cols) || (index < 0))
	{
		std::cerr << INVALID_INPUT_ERROR << std::endl;
		exit(EXIT_FAILURE);
	}
	return this->_mat[index];
}

/**
	 * Input stream
	 * Fills matrix elements
	 * @param in		Istream
	 * @param matrix	Matrix
	 * @return			Istream
	 */
std::istream& operator>>(std::istream& in, Matrix& matrix)
{
	for (int i = 0; i < matrix._dims->rows; ++i)
	{
		for (int j = 0; j < matrix._dims->cols; ++j)
		{
			if (!in.good())
			{
				std::cerr << INVALID_READ_ERROR << std::endl;
				exit(EXIT_FAILURE);
			}
			in.read((char*)(&(matrix._mat[i * matrix._dims->cols + j])), 4);
		}
	}
	return in;
}

/**
	 * Output stream
	 * Pretty export of matrix
	 * @param os		Ostream
	 * @param matrix	Matrix
	 * @return			Matrix
	 */
std::ostream& operator<<(std::ostream& os, const Matrix& matrix)
{
	for (int row = 0; row < matrix._dims->rows; ++row)
	{
		for (int col = 0; col < matrix._dims->cols; ++col)
		{
			if (matrix[row * matrix._dims->cols + col] <= 0.1f)
			{
				os << "  ";
			}
			else
			{
				os << "**";
			}
		}
		os << std::endl;
	}
	return os;
}
#ifndef MATRIX_H
#define MATRIX_H

#include <iostream>

/**
 * @struct MatrixDims
 * @brief Matrix dimensions container
 */
typedef struct MatrixDims
{
	int rows, cols;
} MatrixDims;

/**
 * Class matrix
 */
class Matrix
{
 private:
	/**
	 * Matrix dimensions
	 */
	MatrixDims _dims{};

	/**
	 * Matrix array
	 */
	float* _mat{};
 public:
	/**
	 * Constructs 1*1 Matrix
	 * Inits the single element to 0
	 */
	Matrix();

	/**
	 * Constructs Matrix rows * cols
	 * Inits all elements to 0
	 */
	Matrix(int rows, int cols);

	/**
	 * Copy constructor
	 * @param otherMatrix	Matrix
	 */
	Matrix(const Matrix& otherMatrix);

	/**
	 * Matrix destructor
	 */
	~Matrix();

	/**
	 * returns the amount of rows as int
	 * @return	amount of rows as int
	 */
	int getRows() const;

	/**
	 * returns the amount of cols as int
	 * @return	amount of cols as int
	 */
	int getCols() const;

	/**
	 * Transforms a matrix into a column vector
	 * @return	Matrix
	 */
	Matrix& vectorize();

	/**
	 * Prints matrix elements, no return value.
	 */
	void plainPrint() const;

	/**
	 * Assignment
	 * @param otherMatrix	Matrix
	 * @return				this
	 */
	Matrix& operator=(const Matrix& otherMatrix);

	/**
	 * Matrix multiplication
	 * @param otherMatrix	Matrix
	 * @return				Matrix
	 */
	Matrix operator*(const Matrix& otherMatrix) const;

	/**
	 * Scalar multiplication on the right
	 * @param scalar	scalar
	 * @return			Matrix
	 */
	Matrix operator*(float scalar) const;

	/**
	 * Scalar multiplication on the left
	 * @param scalar			scalar
	 * @param otherMatrix		Matrix
	 * @return					Matrix
	 */
	friend Matrix operator*(float scalar, const Matrix& otherMatrix);

	/**
	 * Matrix addition
	 * @param otherMatrix	Matrix
	 * @return				Matrix
	 */
	Matrix operator+(const Matrix& otherMatrix) const;

	/**
	 * Matrix addition accumulation
	 * @param otherMatrix	Matrix
	 * @return				Matrix
	 */
	Matrix& operator+=(const Matrix& otherMatrix);

	/**
	 * Parenthesis indexing
	 * @param row	row
	 * @param col	column
	 * @return		this(row, col)
	 */
	float& operator()(int row, int col);

	/**
	 * Parenthesis indexing, const
	 * @param row	row
	 * @param col	column
	 * @return		this(row, col)
	 */
	const float& operator()(int row, int col) const;

	/**
	 * Brackets indexing
	 * @param i		Index
	 * @return		this[i]
	 */
	float& operator[](int i);

	/**
	 * Brackets indexing, const
	 * @param i 	Index
	 * @return 		this[i]
	 */
	const float& operator[](int i) const;

	/**
	 * Input stream
	 * Fills matrix elements
	 * @param in		Istream
	 * @param matrix	Matrix
	 * @return			Istream
	 */
	friend std::istream& operator>>(std::istream& in, Matrix& matrix);

	/**
	 * Output stream
	 * Pretty export of matrix
	 * @param os		Ostream
	 * @param matrix	Matrix
	 * @return			Matrix
	 */
	friend std::ostream& operator<<(std::ostream& os, const Matrix& matrix);
};
#endif
#include "MlpNetwork.h"

#define DEFAULT_VALUE 0
#define RESULT_VECTOR_SIZE 10

/**
 * Constructor
 * Accepts 2 arrays, size 4 each
 * @param weights	Weights array
 * @param biases	Biases array
 */
MlpNetwork::MlpNetwork(const Matrix* weights, const Matrix* biases) :
	_l1(Dense(weights[0], biases[0], Relu)),
	_l2(Dense(weights[1], biases[1], Relu)),
	_l3(Dense(weights[2], biases[2], Relu)),
	_l4(Dense(weights[3], biases[3], Softmax))
{
}

/**
 * Parenthesis operator override,
 * Applies the entire network on input
 * @param img	Image matrix
 * @return		Digit
 */
Digit MlpNetwork::operator()(const Matrix& img) const
{
	Digit digit;
	digit.probability = DEFAULT_VALUE;
	digit.value = DEFAULT_VALUE;

	Matrix matrix = Matrix(img);
	matrix = this->_l1(matrix);
	matrix = this->_l2(matrix);
	matrix = this->_l3(matrix);
	matrix = this->_l4(matrix);

	for (int i = 0; i < RESULT_VECTOR_SIZE; ++i)
	{
		if (matrix[i] > digit.probability)
		{
			digit.probability = matrix[i];
			digit.value = i;
		}
	}
	return digit;
}

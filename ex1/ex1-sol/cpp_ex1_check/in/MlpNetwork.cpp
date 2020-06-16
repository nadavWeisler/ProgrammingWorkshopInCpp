#include "MlpNetwork.h"
#include "Dense.h"

/**
 * Constructor
 * Accepts 2 arrays, size 4 each
 * @param weights	Weights array
 * @param biases	Biases array
 */
MlpNetwork::MlpNetwork(Matrix* weights, Matrix* biases)
{
	this->_weights = weights;
	this->_biases = biases;
}

/**
 * Parenthesis operator override,
 * Applies the entire network on input
 * @param img	Image matrix
 * @return		Digit
 */
Digit MlpNetwork::operator()(const Matrix& img)
{
	Dense d1(this->_weights[0], this->_biases[0], Relu);
	Dense d2(this->_weights[1], this->_biases[1], Relu);
	Dense d3(this->_weights[2], this->_biases[2], Relu);
	Dense d4(this->_weights[3], this->_biases[3], Softmax);

	Matrix matrix = d4(d3(d2(d1(img))));

	float maxValue = 0;
	unsigned int maxIndex = 0;

	for(int i = 0; i < matrix.getRows() * matrix.getCols(); ++i)
	{
		if(matrix[i] > maxValue)
		{
			maxValue = matrix[i];
			maxIndex = i;
		}
	}
	return Digit{maxIndex, maxValue};
}

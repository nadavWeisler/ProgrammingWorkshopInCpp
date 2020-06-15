#include <complex>
#include "Activation.h"

/**
 *	Constructor
 *	Accepts activation type
 * @param actType ActivationType
 */
Activation::Activation(ActivationType actType)
{
	this->_activationType = actType;
}

/**
 *	Returns this activation’s type
 * @return	ActivationType
 */
ActivationType Activation::getActivationType()
{
	return this->_activationType;
}

/**
 *	Parenthesis operator override,
 *	Applies activation function on input.
 * @param inputMatrix	Matrix
 * @return	Matrix
 */
Matrix Activation::operator()(const Matrix& inputMatrix)
{
	Matrix newMatrix(inputMatrix);
	if (this->_activationType == Relu)
	{
		for (int i = 0; i < inputMatrix.getRows() * inputMatrix.getCols(); ++i)
		{
			if (inputMatrix[i] < 0)
			{
				newMatrix[i] = 0;
			}
		}
	}
	else if (this->_activationType == Softmax)
	{
		float sum = 0;
		for (int i = 0; i < inputMatrix.getCols() * inputMatrix.getRows(); ++i)
		{
			sum += std::exp(inputMatrix[i]);
		}
		for (int i = 0; i < inputMatrix.getRows() * inputMatrix.getCols(); ++i)
		{
			newMatrix[i] = ((1 / sum) * std::exp(inputMatrix[i]));
		}
	}
	return newMatrix;
}

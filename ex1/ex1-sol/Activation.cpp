#include <cmath>
#include "Activation.h"

/**
 *	Constructor
 *	Accepts activation type
 * @param actType ActivationType
 */
Activation::Activation(ActivationType actType): _activationType(actType)
{
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
 * Relu activation
 * @param matrix 	Matrix
 * @return 			Matrix
 */
Matrix Activation::_relu(const Matrix& matrix)
{
	Matrix newMatrix = Matrix(matrix);
    for (int i = 0; i < newMatrix.getRows() * newMatrix.getCols(); ++i)
    {
        if (newMatrix[i] < 0)
        {
			newMatrix[i] = 0;
        }
    }
    return newMatrix;
}

/**
 * Softmax activation
 * @param matrix 	Matrix
 * @return 			Matrix
 */
Matrix Activation::_softmax(const Matrix& matrix)
{
	Matrix newMatrix = Matrix(matrix);
    float count = 0;
    for (int i = 0; i < matrix.getRows(); ++i)
    {
        newMatrix[i] = std::exp(newMatrix[i]);
		count += newMatrix[i];
    }
    newMatrix = (1 / count) * newMatrix;

    return newMatrix;
}

/**
 *	Parenthesis operator override,
 *	Applies activation function on input.
 * @param inputMatrix	Matrix
 * @return	Matrix
 */
Matrix Activation::operator()(const Matrix& inputMatrix) const
{
	if (this->_activationType == Relu)
	{
		return Activation::_relu(inputMatrix);
	}
	else
	{
		return Activation::_softmax(inputMatrix);
	}
}

#include "Dense.h"

/**
 * Inits a new layer with given parameters
 * @param weightMat			Matrix
 * @param biasMat			Matrix
 * @param activationType	ActivationType
 */
Dense::Dense(const Matrix &weightMat, const Matrix &biasMat, ActivationType activationType):
	_weightMatrix(weightMat), _biasMatrix(biasMat), _activation(Activation(activationType))
{
}

/**
 * Returns the weights of this layer
 * @return Weights matrix
 */
const Matrix &Dense::getWeights() const
{
	return this->_weightMatrix;
}

/**
 * Returns the bias of this layer
 * @return 	Bias matrix
 */
const Matrix &Dense::getBias() const
{
	return this->_biasMatrix;
}

/**
 * Returns the activation function of this layer
 * @return	Activation
 */
const Activation &Dense::getActivation() const
{
	return this->_activation;
}

/**
 * Parenthesis operator override,
 * Applies the layer on inputMatrix and returns output matrix
 * @param inputMatrix		Matrix
 * @return					Matrix
 */
Matrix Dense::operator()(const Matrix& inputMatrix) const
{
	Matrix result = Matrix(inputMatrix);
    result = (this->_weightMatrix * result) + this->_biasMatrix;
    result = this->_activation(result);
    return result;
}



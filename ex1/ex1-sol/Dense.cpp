#include "Dense.h"

/**
 * Inits a new layer with given parameters
 * @param _weightMat		Matrix
 * @param _biasMat			Matrix
 * @param _activationType	ActivationType
 */
Dense::Dense(const Matrix& _weightMat, const Matrix& _biasMat, ActivationType _activationType)
{
	this->weightMatrix = _weightMat;
	this->bias = _biasMat;
	this->activationType = _activationType;
}

/**
 * Returns the weights of this layer
 * @return Weights matrix
 */
Matrix Dense::getWeights() const
{
	return this->weightMatrix;
}

/**
 * Returns the bias of this layer
 * @return 	Bias matrix
 */
Matrix Dense::getBias() const
{
	return this->bias;
}

/**
 * Returns the activation function of this layer
 * @return	Activation
 */
Activation Dense::getActivation() const
{
	Activation currentActivation(this->activationType);
	return currentActivation;
}

/**
 * Parenthesis operator override,
 * Applies the layer on inputMatrix and returns output matrix
 * @param inputMatrix		Matrix
 * @return					Matrix
 */
Matrix Dense::operator()(const Matrix& inputMatrix) const
{
	return (getWeights() * inputMatrix) + getBias();
}



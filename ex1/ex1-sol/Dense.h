#ifndef DENSE_H
#define DENSE_H

#include "Matrix.h"
#include "Activation.h"
class Dense
{
 private:
	/**
	 * Weights matrix
	 */
	Matrix weightMatrix;
	/**
	 * Bias matrix
	 */
	Matrix bias;
	/**
	 * Activation type
	 */
	ActivationType activationType;
 public:
	/**
	 * Inits a new layer with given parameters
	 * @param _weightMat		Matrix
	 * @param _biasMat			Matrix
	 * @param _activationType	ActivationType
	 */
	Dense(const Matrix &_weightMat, const Matrix &_biasMat, ActivationType _activationType);

	/**
	 * Returns the weights of this layer
	 * @return Weights matrix
	 */
	Matrix getWeights() const;

	/**
	 * Returns the bias of this layer
	 * @return 	Bias matrix
	 */
	Matrix getBias() const;

	/**
	 * Returns the activation function of this layer
	 * @return	Activation
	 */
	Activation getActivation() const;

	/**
	 * Parenthesis operator override,
	 * Applies the layer on inputMatrix and returns output matrix
	 * @param inputMatrix		Matrix
	 * @return					Matrix
	 */
	Matrix operator()(const Matrix &inputMatrix) const;
};

#endif

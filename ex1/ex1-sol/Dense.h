#ifndef DENSE_H
#define DENSE_H

#include "Matrix.h"
#include "Activation.h"

/**
 * Class dense
 */
class Dense
{
 private:
	/**
	 * Weights matrix
	 */
	Matrix _weightMatrix;
	/**
	 * Bias matrix
	 */
	Matrix _biasMatrix;
	/**
	 * Activation type
	 */
	Activation _activation;
 public:
	/**
	 * Inits a new layer with given parameters
	 * @param weightMat		Matrix
	 * @param biasMat			Matrix
	 * @param activationType	ActivationType
	 */
	Dense(const Matrix &weightMat, const Matrix &biasMat, ActivationType activationType);

	/**
	 * Returns the weights of this layer
	 * @return Weights matrix
	 */
	const Matrix &getWeights() const;

	/**
	 * Returns the bias of this layer
	 * @return 	Bias matrix
	 */
	const Matrix &getBias() const;

	/**
	 * Returns the activation function of this layer
	 * @return	Activation
	 */
	const Activation &getActivation() const;

	/**
	 * Parenthesis operator override,
	 * Applies the layer on inputMatrix and returns output matrix
	 * @param inputMatrix		Matrix
	 * @return					Matrix
	 */
	Matrix operator()(const Matrix &inputMatrix) const;
};

#endif

#ifndef ACTIVATION_H
#define ACTIVATION_H

#include "Matrix.h"

/**
 * Activation types enum
 */
enum ActivationType
{
	Relu,
	Softmax
};

/**
 * Class activation
 */
class Activation
{
 private:
	/**
	 * Activation type
	 */
	ActivationType _activationType;
 public:
	/**
	 * Constructor
	 * Accepts activation type
	 * @param actType	ActivationType
	 */
	explicit Activation(ActivationType actType);
	/**
	 * Returns this activation’s type
	 * @return	ActivationType
	 */
	ActivationType getActivationType();

	/**
	 * Parenthesis operator override,
	 * Applies activation function on input.
	 * @param inputMatrix	Matrix
	 * @return	Matrix
	 */
	Matrix operator()(const Matrix& inputMatrix);

};

#endif

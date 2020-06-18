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

	/**
	 * Relu activation
	 * @param matrix 	Matrix
	 * @return 			Matrix
	 */
	static Matrix _relu(const Matrix& matrix);

	/**
	 * Softmax activation
	 * @param matrix 	Matrix
	 * @return 			Matrix
	 */
	static Matrix _softmax(const Matrix& matrix);
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
	Matrix operator()(const Matrix& inputMatrix) const;

};

#endif

#ifndef MLPNETWORK_H
#define MLPNETWORK_H

#include "Matrix.h"
#include "Digit.h"

#define MLP_SIZE 4

const MatrixDims imgDims = { 28, 28 };
const MatrixDims weightsDims[] = {{ 128, 784 }, { 64, 128 }, { 20, 64 }, { 10, 20 }};
const MatrixDims biasDims[] = {{ 128, 1 }, { 64, 1 }, { 20, 1 }, { 10, 1 }};

/**
 * MlpNetwork class
 */
class MlpNetwork
{
 private:
	/**
	 * Weights array
	 */
	Matrix* _weights{};
	/**
	 * Biases array
	 */
	Matrix* _biases{};
 public:
	/**
	 * Constructor
	 * Accepts 2 arrays, size 4 each
	 * @param weights	Weights array
	 * @param biases	Biases array
	 */
	MlpNetwork(Matrix weights[], Matrix biases[]);
	/**
	 * Parenthesis operator override,
	 * Applies the entire network on input
	 * @param img	Image matrix
	 * @return		Digit
	 */
	Digit operator()(const Matrix &img);
};

#endif

#ifndef MLPNETWORK_H
#define MLPNETWORK_H

#include "Matrix.h"
#include "Digit.h"
#include "Dense.h"

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
	 * First layer
	 */
	Dense _l1;
	/**
	 * Second layer
	 */
	Dense _l2;
	/**
	 * Third layer
	 */
	Dense _l3;
	/**
	 * Forth layer
	 */
	Dense _l4;

 public:
	/**
	 * Constructor
	 * Accepts 2 arrays, size 4 each
	 * @param weights	Weights array
	 * @param biases	Biases array
	 */
	MlpNetwork(const Matrix weights[MLP_SIZE], const Matrix biases[MLP_SIZE]);
	/**
	 * Parenthesis operator override,
	 * Applies the entire network on input
	 * @param img	Image matrix
	 * @return		Digit
	 */
	Digit operator()(const Matrix& img) const;
};

#endif

#include <iostream>
#include <random>

#include "Dataset.h"
#include "../Matrix.h"
#include "../Activation.h"
#include "../Dense.h"
#include "../MlpNetwork.h"

#define PRINT false
#define PERCENTAGE 1.0

#define WEIGHTS_START_IDX 0
#define BIAS_START_IDX 4
#define ERROR_INVALID_PARAMETER "Error: invalid Parameters file for layer: "
#define ERROR_INVALID_IMG "Error: invalid image path or size: "

#define IMAGES_TRAIN_FILENAME "data/train-images-idx3-ubyte"
#define LABELS_TRAIN_FILENAME "data/train-labels-idx1-ubyte"
#define IMAGES_TEST_FILENAME "data/t10k-images-idx3-ubyte"
#define LABELS_TEST_FILENAME "data/t10k-labels-idx1-ubyte"

#define IMAGES_FILE IMAGES_TEST_FILENAME
#define LABELS_FILE LABELS_TEST_FILENAME

#define PARAMS "./parameters"
#define W1 PARAMS"/w1"
#define W2 PARAMS"/w2"
#define W3 PARAMS"/w3"
#define W4 PARAMS"/w4"
#define B1 PARAMS"/b1"
#define B2 PARAMS"/b2"
#define B3 PARAMS"/b3"
#define B4 PARAMS"/b4"
const std::string args[8] = {W1, W2, W3, W4, B1, B2, B3, B4};

/**
 * Given a binary file path and a matrix,
 * reads the content of the file into the matrix.
 * file must match matrix in size in order to read successfully.
 * @param filePath - path of the binary file to read
 * @param mat -  matrix to read the file into.
 * @return boolean status
 *          true - success
 *          false - failure
 */
bool readFileToMatrix(const std::string &filePath, Matrix &mat)
{
	std::ifstream is;
	is.open(filePath, std::ios::in | std::ios::binary | std::ios::ate);
	if(!is.is_open())
	{
		return false;
	}

	long int matByteSize = (long int) mat.getCols() * mat.getRows() * sizeof(float);
	if(is.tellg() != matByteSize)
	{
		is.close();
		return false;
	}

	is.seekg(0, std::ios_base::beg);
	is >> mat;
	is.close();
	return true;
}

/**
 * Loads MLP parameters from weights & biases paths
 * to Weights[] and Biases[].
 * Exits (code == 1) upon failures.
 * @param paths array of programs arguments, expected to be mlp parameters
 *        path.
 * @param weights array of matrix, weigths[i] is the i'th layer weights matrix
 * @param biases array of matrix, biases[i] is the i'th layer bias matrix
 *          (which is actually a vector)
 */
void loadParameters(const std::string *paths, Matrix weights[MLP_SIZE], Matrix biases[MLP_SIZE])
{
	for(int i = 0; i < MLP_SIZE; i++)
	{
		weights[i] = Matrix(weightsDims[i].rows, weightsDims[i].cols);
		biases[i] = Matrix(biasDims[i].rows, biasDims[i].cols);

		std::string weightsPath(paths[WEIGHTS_START_IDX + i]);
		std::string biasPath(paths[BIAS_START_IDX + i]);

		if(!(readFileToMatrix(weightsPath, weights[i]) &&
			 readFileToMatrix(biasPath, biases[i])))
		{
			std::cerr << ERROR_INVALID_PARAMETER << (i + 1) << std::endl;
			exit(EXIT_FAILURE);
		}

	}
}

/**
 * This programs Command line interface for the mlp network.
 * Looping on: {
 *                  Retrieve user input
 *                  Feed input to mlpNetwork
 *                  print image & netowrk prediction
 *             }
 * Exits (code == 1) on fatal errors: unable to read user input path.
 * @param mlp MlpNetwork to use in order to predict img.
 */
Digit mlpRun(MlpNetwork &mlp, std::string imgPath)
{
	Matrix img(imgDims.rows, imgDims.cols);

	if(readFileToMatrix(imgPath, img))
	{
		if (PRINT) {
			std::cout << img << std::endl;
		}
		return mlp(img.vectorize());
	}
	throw std::runtime_error(ERROR_INVALID_IMG + imgPath);
}


int main()
{
	Dataset dataset = Dataset(IMAGES_FILE, LABELS_FILE);
	Matrix weights[MLP_SIZE];
	Matrix biases[MLP_SIZE];
	loadParameters(args, weights, biases);

	MlpNetwork mlp(weights, biases);
	std::string input = "img.in";

	int success = 0;
	int loopSize = dataset.len() * PERCENTAGE;
	for (int i = 0; i < loopSize; i++)
	{
		unsigned int label = dataset.genImageTest(i, input);
		Digit res = mlpRun(mlp, input);
		if (PRINT) {
			std::cout << "num: " << res.value;
			std::cout << " prob: " << res.probability << std::endl << std::endl;
		}
		if (label == res.value) {
			success++;
		}
	}
	std::cout << "done " << std::endl;
	std::cout << "guessed correctly " << success  << " out of " << loopSize;
	std::cout << " (" << (float)success/loopSize << ")" << std::endl;

	return 0;
}
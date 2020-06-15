/******************************************************************************

                   Written by Ariel Terkeltoub, June 2020.
             Song recommendation of the day: "The Wall" by Kansas
                    So Long, and Thanks for All the Fish.

*******************************************************************************/
#include <fstream>
#include <sstream>
#include <cstring>
#include <limits>
#include <vector>
#include <streambuf>
#include "MlpNetwork.h"

std::string const USAGE(char *const argv[])
{
  return "Usage: " + std::string(argv[0]) + " <test-name> [<test-params>...]\n\n"
  "Available tests:\n"
  "\t* matmul <mat1-rows> <mat1-cols> <mat2-rows> <mat2-cols>";
}

char constexpr MATLOAD_ERR[]{"When testing \"matload\", 2 integer magnitudes must be passed."};
char constexpr MATASSIGN_ERR[]{"When testing \"matassign\", 4 integer magnitudes must be passed."};
char constexpr MATCTOR1_ERR[]{"When testing \"matctor1\", 2 integer magnitude must be passed."};
char constexpr MATCTOR2_ERR[]{"When testing \"matctor2\", 2 integer magnitudes must be passed."};
char constexpr MATMUL_ERR[]{"When testing \"matmul\", 4 integer magnitudes must be passed."};
char constexpr MATADD_ERR[]{"When testing \"matadd\", 4 integer magnitudes must be passed."};
char constexpr MATADD_INPLACE_ERR[]{"When testing \"matadd_inplace\", 4 integer magnitudes must be passed."};
char constexpr SCALAR_MAT_LMUL_ERR[]{"When testing \"scalar_mat_lmul\", 2 integer magnitudes must be passed."};
char constexpr SCALAR_MAT_RMUL_ERR[]{"When testing \"scalar_mat_rmul\", 2 integer magnitudes must be passed."};
char constexpr FLAT_GETITEM_ERR[]{"When testing \"flat_getitem\", 3 integer magnitudes must be passed."};
char constexpr GETITEM_ERR[]{"When testing \"getitem\", 3 integer magnitudes must be passed."};
char constexpr FLAT_SETITEM_ERR[]{"When testing \"flat_setitem\", 3 integer magnitudes must be passed."};
char constexpr SETITEM_ERR[]{"When testing \"setitem\", 3 integer magnitudes must be passed."};
char constexpr ATEXIT_FAIL[]{"Failed to register heap destruction to atexit."};

char constexpr MODEL_WEIGHT_FILENAMES[MLP_SIZE][9]{"model/w1", "model/w2", "model/w3", "model/w4"};
char constexpr MODEL_BIAS_FILENAMES[MLP_SIZE][9]{"model/b1", "model/b2", "model/b3", "model/b4"};

size_t constexpr IMG_DIMS[]{28, 28};

char constexpr INSERT_IMAGE_PATH[]{"Please insert image path:"};

struct membuf : std::streambuf
{
    membuf(char *begin, char *end) {
        this->setg(begin, begin, end);
    }
};

std::vector<size_t*> g_destructionCache1;
std::vector<float*> g_destructionCache2;

void destroy()
{
  for (size_t *__restrict ptr : g_destructionCache1)
  {
    delete[] ptr;
  }
  for (float *__restrict ptr : g_destructionCache2)
  {
    delete[] ptr;
  }
}

inline void matctor0()
{
  std::cout.precision(std::numeric_limits<float>::max_digits10);
  Matrix().plainPrint();
}

inline void matctor1(size_t const rowsA, size_t const colsA)
{
  std::cout.precision(std::numeric_limits<float>::max_digits10);
  Matrix a(rowsA, colsA);
  std::cin >> a;
  Matrix(a).plainPrint();
}

inline void matctor2(size_t const rowsA, size_t const colsA)
{
  std::cout.precision(std::numeric_limits<float>::max_digits10);
  Matrix(rowsA, colsA).plainPrint();
}

inline void matload(size_t const rowsA, size_t const colsA)
{
  Matrix a(rowsA, colsA);
  std::cin >> a;
}

void matassign(size_t const rowsA, size_t const colsA, size_t const rowsB, size_t const colsB)
{
  std::cout.precision(std::numeric_limits<float>::max_digits10);
  Matrix a(rowsA, colsA), b(rowsB, colsB);
  float *a_arr = new float[rowsA * colsA];
  g_destructionCache2.push_back(a_arr);
  std::cin.read(reinterpret_cast<char*>(a_arr), rowsA * colsA * sizeof(float));
  std::string const a_string(reinterpret_cast<char*>(a_arr), rowsA * colsA * sizeof(float));
  std::istringstream a_stream(a_string);

  a_stream >> a;
  std::cin >> b;
  a = b;
  a.plainPrint();
  delete[] a_arr;
  g_destructionCache2.pop_back();
}

void matmul(size_t const rowsA, size_t const colsA, size_t const rowsB, size_t const colsB)
{
  std::cout.precision(std::numeric_limits<float>::max_digits10);
  Matrix a(rowsA, colsA), b(rowsB, colsB);
  float *a_arr = new float[rowsA * colsA];
  g_destructionCache2.push_back(a_arr);
  std::cin.read(reinterpret_cast<char*>(a_arr), rowsA * colsA * sizeof(float));
  std::string const a_string(reinterpret_cast<char*>(a_arr), rowsA * colsA * sizeof(float));
  std::istringstream a_stream(a_string);

  a_stream >> a;
  std::cin >> b;
  (a * b).plainPrint();
  delete[] a_arr;
  g_destructionCache2.pop_back();
}

void scalar_mat_lmul(size_t const rowsA, size_t const colsA)
{
  std::cout.precision(std::numeric_limits<float>::max_digits10);
  float c;
  std::cin.read(reinterpret_cast<char*>(&c), sizeof(float));
  Matrix a(rowsA, colsA);
  std::cin >> a;
  (c * a).plainPrint();
}

void scalar_mat_rmul(size_t const rowsA, size_t const colsA)
{
  std::cout.precision(std::numeric_limits<float>::max_digits10);
  float c;
  std::cin.read(reinterpret_cast<char*>(&c), sizeof(float));
  Matrix a(rowsA, colsA);
  std::cin >> a;
  (a * c).plainPrint();
}

void matadd(size_t const rowsA, size_t const colsA, size_t const rowsB, size_t const colsB)
{
  std::cout.precision(std::numeric_limits<float>::max_digits10);
  Matrix a(rowsA, colsA), b(rowsB, colsB);
  float *a_arr = new float[rowsA * colsA];
  g_destructionCache2.push_back(a_arr);
  std::cin.read(reinterpret_cast<char*>(a_arr), rowsA * colsA * sizeof(float));
  std::string const a_string(reinterpret_cast<char*>(a_arr), rowsA * colsA * sizeof(float));
  std::istringstream a_stream(a_string);

  a_stream >> a;
  std::cin >> b;
  (a + b).plainPrint();
  delete[] a_arr;
  g_destructionCache2.pop_back();
}

void matadd_inplace(size_t const rowsA, size_t const colsA, size_t const rowsB, size_t const colsB)
{
  std::cout.precision(std::numeric_limits<float>::max_digits10);
  Matrix a(rowsA, colsA), b(rowsB, colsB);
  float *a_arr = new float[rowsA * colsA];
  g_destructionCache2.push_back(a_arr);
  std::cin.read(reinterpret_cast<char*>(a_arr), rowsA * colsA * sizeof(float));
  std::string const a_string(reinterpret_cast<char*>(a_arr), rowsA * colsA * sizeof(float));
  std::istringstream a_stream(a_string);

  a_stream >> a;
  std::cin >> b;
  a += b;
  a.plainPrint();
  delete[] a_arr;
  g_destructionCache2.pop_back();
}

void flat_getitem(size_t const rowsA, size_t const colsA, size_t const nIndices)
{
  std::cout.precision(std::numeric_limits<float>::max_digits10);
  size_t *indices = new size_t[nIndices];
  g_destructionCache1.push_back(indices);
  std::cin.read(reinterpret_cast<char*>(indices), nIndices * sizeof(size_t));
  Matrix a(rowsA, colsA);
  std::cin >> a;
  Matrix const &a_ref = a; // Force the use of the const operator[], if one exists
  for (size_t i = 0; i < nIndices; ++i)
  {
    std::cout << a_ref[indices[i]] << " ";
  }
  delete[] indices;
  (void)g_destructionCache1.pop_back();
}

void getitem(size_t const rowsA, size_t const colsA, size_t const nIndices)
{
  std::cout.precision(std::numeric_limits<float>::max_digits10);
  size_t *indices = new size_t[2 * nIndices];
  g_destructionCache1.push_back(indices);
  std::cin.read(reinterpret_cast<char*>(indices), 2 * nIndices * sizeof(size_t));
  Matrix a(rowsA, colsA);
  std::cin >> a;
  Matrix const &a_ref = a; // Force the use of the const operator[], if one exists
  for (size_t i = 0; i < 2 * nIndices; i += 2)
  {
    std::cout << a_ref(indices[i], indices[i + 1]) << " ";
  }
  delete[] indices;
  (void)g_destructionCache1.pop_back();
}

void flat_setitem(size_t const rowsA, size_t const colsA, size_t const nIndices)
{
  std::cout.precision(std::numeric_limits<float>::max_digits10);
  size_t *indices = new size_t[nIndices];
  g_destructionCache1.push_back(indices);
  float *newValues = new float[nIndices];
  g_destructionCache2.push_back(newValues);
  std::cin.read(reinterpret_cast<char*>(indices), nIndices * sizeof(size_t));
  std::cin.read(reinterpret_cast<char*>(newValues), nIndices * sizeof(float));
  Matrix a(rowsA, colsA);
  std::cin >> a;
  for (size_t i = 0; i < nIndices; ++i)
  {
    a[indices[i]] = newValues[i];
  }
  delete[] newValues;
  (void)g_destructionCache2.pop_back();
  delete[] indices;
  (void)g_destructionCache1.pop_back();
  a.plainPrint();
}

void setitem(size_t const rowsA, size_t const colsA, size_t const nIndices)
{
  std::cout.precision(std::numeric_limits<float>::max_digits10);
  size_t *indices = new size_t[2 * nIndices];
  g_destructionCache1.push_back(indices);
  float *newValues = new float[nIndices];
  g_destructionCache2.push_back(newValues);
  std::cin.read(reinterpret_cast<char*>(indices), 2 * nIndices * sizeof(size_t));
  std::cin.read(reinterpret_cast<char*>(newValues), nIndices * sizeof(float));
  Matrix a(rowsA, colsA);
  std::cin >> a;
  for (size_t i = 0; i < 2 * nIndices; i += 2)
  {
    a(indices[i], indices[i + 1]) = newValues[i / 2];
  }
  delete[] newValues;
  (void)g_destructionCache2.pop_back();
  delete[] indices;
  (void)g_destructionCache1.pop_back();
  a.plainPrint();
}

bool readFileToMatrix(std::string const &filePath, Matrix &mat)
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

void loadParameters(Matrix (&weights)[MLP_SIZE], Matrix (&biases)[MLP_SIZE])
{
  for (size_t i = 0; i < MLP_SIZE; ++i)
  {
    weights[i] = Matrix(weightsDims[i].rows, weightsDims[i].cols);
    biases[i] = Matrix(biasDims[i].rows, biasDims[i].cols);

    std::string const weightsPath(MODEL_WEIGHT_FILENAMES[i]);
    std::string const biasPath(MODEL_BIAS_FILENAMES[i]);

    if(!(readFileToMatrix(weightsPath, weights[i]) && readFileToMatrix(biasPath, biases[i])))
    {
      std::cerr << "Couldn't read model files." << std::endl;
      std::exit(EXIT_FAILURE);
    }
  }
}

void digits(char const imageFilename[])
{
  Matrix weights[MLP_SIZE], biases[MLP_SIZE];
  Matrix image(IMG_DIMS[0], IMG_DIMS[1]);
  loadParameters(weights, biases);
  MlpNetwork mlp(weights, biases);

  if (!readFileToMatrix(std::string(imageFilename), image))
  {
    std::cerr << "Error reading image " << imageFilename << "." << std::endl;
    std::exit(2);
  }

  Digit const output = mlp(Matrix(image).vectorize());
  std::cout << INSERT_IMAGE_PATH << std::endl
            << "Image processed:" << std::endl << image << std::endl << "Mlp result: " << output.value << " at probability: " << output.probability << std::endl
            << INSERT_IMAGE_PATH << std::endl;
}

int main(int argc, char *argv[])
{
  if (std::atexit(destroy))
  {
    std::cerr << ATEXIT_FAIL << std::endl;
    std::exit(EXIT_FAILURE);
  }

  if (argc == 1)
  {
    std::cerr << USAGE(argv) << std::endl;
    std::exit(EXIT_FAILURE);
  }

  if (!strcmp(argv[1], "matmul") && argc == 6)
  {
    size_t rowsA, colsA, rowsB, colsB;
        if (!((std::istringstream(argv[2]) >> rowsA) && (std::istringstream(argv[3]) >> colsA) && (std::istringstream(argv[4]) >> rowsB) && (std::istringstream(argv[5]) >> colsB)))
    {
      std::cerr << MATMUL_ERR << std::endl;
      std::exit(EXIT_FAILURE);
    }
    matmul(rowsA, colsA, rowsB, colsB);
  }
  else if (!strcmp(argv[1], "matadd") && argc == 6)
  {
    size_t rowsA, colsA, rowsB, colsB;
    if (!((std::istringstream(argv[2]) >> rowsA) && (std::istringstream(argv[3]) >> colsA) && (std::istringstream(argv[4]) >> rowsB) && (std::istringstream(argv[5]) >> colsB)))
    {
      std::cerr << MATADD_ERR << std::endl;
      std::exit(EXIT_FAILURE);
    }
    matadd(rowsA, colsA, rowsB, colsB);
  }
  else if (!strcmp(argv[1], "matadd_inplace") && argc == 6)
  {
    size_t rowsA, colsA, rowsB, colsB;
        if (!((std::istringstream(argv[2]) >> rowsA) && (std::istringstream(argv[3]) >> colsA) && (std::istringstream(argv[4]) >> rowsB) && (std::istringstream(argv[5]) >> colsB)))
    {
      std::cerr << MATADD_INPLACE_ERR << std::endl;
      std::exit(EXIT_FAILURE);
    }
    matadd_inplace(rowsA, colsA, rowsB, colsB);
  }
  else if (!strcmp(argv[1], "matassign") && argc == 6)
  {
    size_t rowsA, colsA, rowsB, colsB;
        if (!((std::istringstream(argv[2]) >> rowsA) && (std::istringstream(argv[3]) >> colsA) && (std::istringstream(argv[4]) >> rowsB) && (std::istringstream(argv[5]) >> colsB)))
    {
      std::cerr << MATASSIGN_ERR << std::endl;
      std::exit(EXIT_FAILURE);
    }
    matassign(rowsA, colsA, rowsB, colsB);
  }
  else if (!strcmp(argv[1], "scalar_mat_lmul") && argc == 4)
  {
    size_t rowsA, colsA;
    if (!((std::istringstream(argv[2]) >> rowsA) && (std::istringstream(argv[3]) >> colsA)))
    {
      std::cerr << SCALAR_MAT_LMUL_ERR << std::endl;
      std::exit(EXIT_FAILURE);
    }
    scalar_mat_lmul(rowsA, colsA);
  }
  else if (!strcmp(argv[1], "scalar_mat_rmul") && argc == 4)
  {
    size_t rowsA, colsA;
        if (!((std::istringstream(argv[2]) >> rowsA) && (std::istringstream(argv[3]) >> colsA)))
    {
      std::cerr << SCALAR_MAT_RMUL_ERR << std::endl;
      std::exit(EXIT_FAILURE);
    }
    scalar_mat_rmul(rowsA, colsA);
  }
  else if (!strcmp(argv[1], "flat_getitem") && argc == 5)
  {
    size_t rowsA, colsA, nIndices;
    if (!((std::istringstream(argv[2]) >> rowsA) && (std::istringstream(argv[3]) >> colsA) && (std::istringstream(argv[4]) >> nIndices)))
    {
      std::cerr << FLAT_GETITEM_ERR << std::endl;
      std::exit(EXIT_FAILURE);
    }
    flat_getitem(rowsA, colsA, nIndices);
  }
  else if (!strcmp(argv[1], "getitem") && argc == 5)
  {
    size_t rowsA, colsA, nIndices;
        if (!((std::istringstream(argv[2]) >> rowsA) && (std::istringstream(argv[3]) >> colsA) && (std::istringstream(argv[4]) >> nIndices)))
    {
      std::cerr << GETITEM_ERR << std::endl;
      std::exit(EXIT_FAILURE);
    }
    getitem(rowsA, colsA, nIndices);
  }
  else if (!strcmp(argv[1], "flat_setitem") && argc == 5)
  {
    size_t rowsA, colsA, nIndices;
        if (!((std::istringstream(argv[2]) >> rowsA) && (std::istringstream(argv[3]) >> colsA) && (std::istringstream(argv[4]) >> nIndices)))
    {
      std::cerr << FLAT_SETITEM_ERR << std::endl;
      std::exit(EXIT_FAILURE);
    }
    flat_setitem(rowsA, colsA, nIndices);
  }
  else if (!strcmp(argv[1], "setitem") && argc == 5)
  {
    size_t rowsA, colsA, nIndices;
        if (!((std::istringstream(argv[2]) >> rowsA) && (std::istringstream(argv[3]) >> colsA) && (std::istringstream(argv[4]) >> nIndices)))
    {
      std::cerr << SETITEM_ERR << std::endl;
      std::exit(EXIT_FAILURE);
    }
    setitem(rowsA, colsA, nIndices);
  }
  else if (!strcmp(argv[1], "digit") && argc == 3)
  {
    digits(argv[2]);
  }
  else if (!strcmp(argv[1], "matctor0") && argc == 2)
  {
    matctor0();
  }
  else if (!strcmp(argv[1], "matctor1") && argc == 4)
  {
    size_t rowsA, colsA;
    if (!((std::istringstream(argv[2]) >> rowsA) && (std::istringstream(argv[3]) >> colsA)))
    {
      std::cerr << MATCTOR1_ERR << std::endl;
      std::exit(EXIT_FAILURE);
    }
    matctor1(rowsA, colsA);
  }
  else if (!strcmp(argv[1], "matload") && argc == 4)
  {
    size_t rowsA, colsA;
    if (!((std::istringstream(argv[2]) >> rowsA) && (std::istringstream(argv[3]) >> colsA)))
    {
      std::cerr << MATLOAD_ERR << std::endl;
      std::exit(EXIT_FAILURE);
    }
    matload(rowsA, colsA);
  }
  else if (!strcmp(argv[1], "matctor2") && argc == 4)
  {
    size_t rowsA, colsA;
    if (!((std::istringstream(argv[2]) >> rowsA) && (std::istringstream(argv[3]) >> colsA)))
    {
      std::cerr << MATCTOR2_ERR << std::endl;
      std::exit(EXIT_FAILURE);
    }
    matctor2(rowsA, colsA);
  }
  else
  {
    std::cerr << USAGE(argv) << std::endl;
  }
}

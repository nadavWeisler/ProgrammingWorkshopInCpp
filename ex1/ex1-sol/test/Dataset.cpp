#include "Dataset.h"

float Dataset::maxVal = 255.f;
float Dataset::offset = 4;

Dataset::Dataset(std::string imagesFile, std::string labelsFile)
{
	std::ifstream imagesSet, labelsSet;
	imagesSet.open(imagesFile, std::ios::binary);
	labelsSet.open(labelsFile, std::ios::binary);
	int len = _validateFiles(imagesSet, labelsSet);

	_items = new Item[len];
	_len = len;

	for(size_t i = 0; i < _len; i++)
	{
		_items[i].data = new float[IMG_SIZE];
		_items[i].dataLen = IMG_SIZE;
		uchar pixel, label;

		for (int j = 0; j < IMG_SIZE; j++)
		{
			imagesSet.read((char *)&pixel, 1);
			_items[i].data[j] = normalize(pixel);
		}
		labelsSet.read((char *)&label, 1);
		_items[i].label = label;
	}

	imagesSet.close();
	labelsSet.close();
}

Dataset::~Dataset()
{
	delete[] _items;
}

int Dataset::_reverseInt(int i)
{
	unsigned char c1, c2, c3, c4;

	c1 = i & 255;
	c2 = (i >> 8) & 255;
	c3 = (i >> 16) & 255;
	c4 = (i >> 24) & 255;

	return ((int)c1 << 24) + ((int)c2 << 16) + ((int)c3 << 8) + c4;
}

int Dataset::genImageTest(int i, std::string filename) const
{
	auto file = std::fstream(filename, std::ios::out | std::ios::binary);
	Item item = _items[i];
	file.write((char*)item.data, item.dataLen*sizeof(float));
	file.close();
	return item.label;
}


int Dataset::_validateFiles(std::ifstream &imagesSet, std::ifstream &labelsSet)
{
	if (!imagesSet.good()) throw std::runtime_error("File missing");
	if (!labelsSet.good()) throw std::runtime_error("File missing");

	int magicNumber, itemsNum, rows, cols;
	if (!imagesSet.read((char*)&magicNumber, Dataset::offset)) throw std::runtime_error("Failed reading.");
	if (!imagesSet.read((char*)&itemsNum, Dataset::offset)) throw std::runtime_error("Failed reading.");
	if (!imagesSet.read((char*)&rows, Dataset::offset)) throw std::runtime_error("Failed reading.");
	if (!imagesSet.read((char*)&cols, Dataset::offset)) throw std::runtime_error("Failed reading.");

	magicNumber = _reverseInt(magicNumber);
	itemsNum = _reverseInt(itemsNum);
	rows = _reverseInt(rows);
	cols = _reverseInt(cols);
	if (magicNumber != MAGIC_NUMBER_IMG ||
		rows != IMG_DIM ||
		cols != IMG_DIM)
	{
		throw std::runtime_error("Invalid images file");
	}

	if (!labelsSet.read((char*)&magicNumber, Dataset::offset)) throw std::runtime_error("Failed reading.");
	if (!labelsSet.read((char*)&itemsNum, Dataset::offset)) throw std::runtime_error("Failed reading.");

	magicNumber = _reverseInt(magicNumber);
	itemsNum = _reverseInt(itemsNum);
	if (magicNumber != MAGIC_NUMBER_LABEL)
	{
		throw std::runtime_error("Invalid labels file");
	}

	return itemsNum;
}


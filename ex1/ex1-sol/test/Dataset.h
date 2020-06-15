//
// Created by dorro on 11/06/2020.
//

#ifndef EX4_DATASET_H
#define EX4_DATASET_H

#include <fstream>
#include <iostream>
#include <string>
#include <cstring>

#define OFFSET 4

#define MAGIC_NUMBER_IMG 2051
#define MAGIC_NUMBER_LABEL 2049
#define IMG_DIM 28
#define IMG_SIZE 784


typedef unsigned char uchar;
typedef struct Item
{
	float *data;
	size_t dataLen;
	uchar label;
	Item(): label()
	{
		dataLen = 0;
		data = nullptr;
	}
	Item(const Item &item)
	{
		dataLen = item.dataLen;
		label = item.label;
		data = new float[dataLen];
		std::memcpy(data, item.data, dataLen*sizeof(float));
	}
	Item& operator=(const Item &item)
	{
		dataLen = item.dataLen;
		label = item.label;
		delete[] data;
		data = new float[dataLen];
		std::memcpy(data, item.data, dataLen*sizeof(float));
		return *this;
	}
	~Item() { delete []data; }
} Item;

class Dataset
{
	public:
		static float maxVal;
		static float offset;

		Dataset(std::string images, std::string labels);
		~Dataset();
		Item &operator[](int i){ return _items[i]; }
		int genImageTest(int i, std::string filename) const;
		inline static float normalize(float x) { return x / Dataset::maxVal; };
		inline size_t len() const { return _len; };
	private:
		Item *_items;
		size_t _len;

		static int _validateFiles(std::ifstream &imagesSet, std::ifstream &labelsSet);
		static int _reverseInt (int i);
};


#endif //EX4_DATASET_H

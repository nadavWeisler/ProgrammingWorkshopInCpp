// WARNING
// This test don't compare results with school solution, since I can't unit test their program
// So take failing this test with grain of salt
// If you think there is a mistake, you can always contact me here: amit.david@mail.huji.ac.il

// operator>> and operator<< not tested here :(

#include <iostream>
#include <cassert>

#include "Matrix.h"

int main()
{
	std::cout << "Build matrix" << std::endl;
	Matrix m1;

	std::cout << "Build const matrix" << std::endl;
	const Matrix m2;
	std::cout << "Build matrix 10*20" << std::endl;
	Matrix m3(10, 20);

	std::cout << "Build const matrix 20*5" << std::endl;
	const Matrix m4(20, 5);

	std::cout << "Build matrix using copy constructor" << std::endl;
	Matrix m5(m3);
	
	std::cout << "Build const matrix using copy constructor" << std::endl;
	const Matrix m6(m4);

	std::cout << std::endl;
	std::cout << "Test getRows()" << std::endl;
	assert(m5.getRows() == 10);
	assert(m6.getRows() == 20);

	std::cout << "Test getCols()" << std::endl;
	assert(m5.getCols() == 20);
	assert(m6.getCols() == 5);


	std::cout << std::endl;
	std::cout << "Test operator=" << std::endl;
	Matrix m8;
	m8 = m1;
	m8 = m2;
	m8 = m3;
	m8 = m4;

	std::cout << std::endl;
	std::cout << "Test operator[], set value to 4" << std::endl;
	m1[0] = 4;

	std::cout << "value in index is " << m1[0] << std::endl;
	std::cout << "value in const matrix index is " << m2[0] << std::endl;
	std::cout << "assert " << m2[0] << " == " << 0 << std::endl;
	assert(m2[0] == 0);


	std::cout << std::endl;
	std::cout << "Test operator(,) set value to -1" << std::endl;
	m3(2, 1) = -1;

	std::cout << "value in index is " << m3(2, 1) << std::endl;
	std::cout << "value in const matrix index is " << m4(3,3) << std::endl;
	std::cout << "assert " << m4(3,3) << " == " << 0 << std::endl;
	assert(m4(3,3) == 0);


	std::cout << std::endl;
	std::cout << "Test operator matrix*matrix" << std::endl;
	m1 * m1;
	m1 * m2;
	m2 * m1;
	m2 * m2;

	std::cout << "Test operator matrix*matrix concatenating" << std::endl;
	Matrix m9(m3 * m4);
	assert(m9.getRows() == 10);
	assert(m9.getCols() == 5);


	std::cout << std::endl;
	std::cout << "Test operator matrix*float" << std::endl;
	float num = 2;
	m1[0] = 4;
	m1 = m1 * num;
	std::cout << "assert " << m1[0] << " == " << 8 << std::endl;
	assert(m1[0] == 8);


	std::cout << std::endl;
	std::cout << "Test operator float*matrix" << std::endl;
	num = 5;
	m3(2, 1) = -3;
	m3 = num * m3;
	std::cout << "assert " << m3(2,1) << " == " << -15 << std::endl;
	assert(m3(2,1) == -15);


	std::cout << std::endl;
	std::cout << "Test operator matrix+matrix" << std::endl;
	m1 + m1;
	m1 + m2;
	m2 + m1;
	m2 + m2;

	std::cout << "Test operator matrix+matrix concatenating" << std::endl;
	Matrix m10(m1 + m2);
	assert(m10.getRows() == 1);
	assert(m10.getCols() == 1);


	std::cout << std::endl;
	std::cout << "Test operator matrix+=matrix" << std::endl;
	m1[0] = 3;
	m1 += m1;
	m1 += m2;
	std::cout << "assert " << m1[0] << " == " << 6 << std::endl;
	assert(m1[0] == 6);

	std::cout << "Test operator matrix+=matrix concatenating" << std::endl;
	Matrix m11(m1 + m2);
	assert(m11.getRows() == 1);
	assert(m11.getCols() == 1);
	std::cout << "assert " << m11[0] << " == " << 6 << std::endl;
	assert(m11[0] == 6);


	std::cout << std::endl;
	std::cout << "Test m.vectorize()" << std::endl;
	m5[70] = 99;
	Matrix m12(m5.vectorize());
	m12[44] = 333;

	assert(m5[70] == 99);
	assert(m12[70] == 99);
	assert(m5[44] == 0);
	assert(m12[44] == 333);

	std::cout << "Check dimensions" << std::endl;
	assert(m5.getRows() == 200);
	assert(m12.getRows() == 200);

	assert(m5.getCols() == 1);
	assert(m12.getCols() == 1);


	std::cout << std::endl;
	std::cout << "Test m.plainPrint()" << std::endl;
	std::cout << "m1" << std::endl;
	m1.plainPrint();
	std::cout << "m2" << std::endl;
	m2.plainPrint();
	std::cout << "m3" << std::endl;
	m3.plainPrint();
	std::cout << "m5" << std::endl;
	m5.plainPrint();
	std::cout << "m6" << std::endl;
	m6.plainPrint();
	std::cout << "m10" << std::endl;
	m10.plainPrint();
	std::cout << "m11" << std::endl;
	m11.plainPrint();

	std::cout << std::endl;
	std::cout << "Test operator<<" << std::endl;
	Matrix m13(5, 6);
	m13(0,0) = -1;
	m13(0,1) = 0.2f;
	m13(0,2) = 0.10f;
	m13(1,1) = 0.4f;
	m13(0,4) = 1;
	m13(1,3) = 0.09f;
	m13(1,4) = 3;
	m13(3,0) = 5.11f;
	m13(4,1) = 0.99f;
	m13(4,2) = 0.89f;
	m13(4,3) = 0.5f;
	m13(4,4) = 0.12f;
	m13(4,5) = -0.02f;
	m13(3,5) = 0.77f;
	m13.plainPrint();
	std::cout << std::endl << m13;

	std::cout << std::endl << "Done." << std::endl;
	return EXIT_SUCCESS;
}

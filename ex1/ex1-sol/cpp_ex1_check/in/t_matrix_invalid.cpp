// WARNING
// This test don't compare results with school solution, since I can't unit test their program
// So take failing this test with grain of salt
// If you think there is a mistake, you can always contact me here: amit.david@mail.huji.ac.il

// operator>> and operator<< not tested here :(

#include <iostream>
#include <cassert>

#include "Matrix.h"

// Don't do this
extern "C" void exit(int status) {
	throw status;
}


int main()
{
	std::cout << "Pass means you exited from the program with code 1 (as you should have)" << std::endl
			  << "If 'Pass x' is absent it means you accepted invalid parameter instead of exiting from the program"
			  << std::endl << std::endl;
	std::cout << "Try build invalid matrix" << std::endl;
	try
	{
		Matrix m100(-111, 20);
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 1" << std::endl;
	}

	try
	{
		Matrix m100(2, -20);
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 2" << std::endl;
	}

	try
	{
		Matrix m100(10, 0);
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 3" << std::endl;
	}

	try
	{
		Matrix m100(0, 4);
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 4" << std::endl;
	}


	Matrix m3(2, 5);
	const Matrix m4(3, 6);

	try
	{
		m3[-1];
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 5" << std::endl;
	}
	try
	{
		m3[10];
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 6" << std::endl;
	}

	try
	{
		m4[-1];
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 7" << std::endl;
	}
	try
	{
		m4[18];
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 8" << std::endl;
	}


	try
	{
		m3(-1, 1);
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 9" << std::endl;
	}
	try
	{
		m3(1, -1);
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 10" << std::endl;
	}
	try
	{
		m3(0, 5);
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 11" << std::endl;
	}
	try
	{
		m3(3, 0);
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 12" << std::endl;
	}

	try
	{
		m4(-1, 1);
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 13" << std::endl;
	}
	try
	{
		m4(1, -1);
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 14" << std::endl;
	}
	try
	{
		m3(0, 6);
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 15" << std::endl;
	}
	try
	{
		m3(3, 0);
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 16" << std::endl;
	}

	try
	{
		m3 * m4;
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 17" << std::endl;
	}
	try
	{
		m4 * m4;
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 18" << std::endl;
	}

	try
	{
		m3 + m4;
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 19" << std::endl;
	}
	try
	{
		m4 + m3;
	}
	catch (int e)
	{
		if (e != 1)
		{
			return e;
		}
		std::cout << "Pass 20" << std::endl;
	}

	std::cout << std::endl << "Done." << std::endl;
	return EXIT_SUCCESS;
}

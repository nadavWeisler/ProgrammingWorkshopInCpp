#include <iostream>
#include <vector>
#include "VLVector.hpp"

#define NUMBER_TO_CHECK 1e4

#include <cassert>

int main()
{
    VLVector<int, 16> v1;
    std::vector<int> std_vec;
    for (int i = 0; i < NUMBER_TO_CHECK; ++i)
    {
        v1.insert(v1.begin(), i);
        std_vec.insert(std_vec.begin(), i);
    }
    for (int i = 0; i < NUMBER_TO_CHECK; ++i)
    {
        if (v1[i] != std_vec[i])
        {
            printf("%d %d %d\n", i, v1[i], std_vec[i]);
        }
        assert(v1[i] == std_vec[i]);
    }
    v1.insert(++v1.begin(), 0);
    std_vec.insert(++std_vec.begin(), 0);
    assert(v1[1] == std_vec[1]);

    return 0;
}


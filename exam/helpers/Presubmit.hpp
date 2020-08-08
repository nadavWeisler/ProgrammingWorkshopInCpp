#ifndef PRESUBMIT_H
#define PRESUBMIT_H

#include "../VLVector.hpp"
#include "Helpers.h"
#include <iostream>
#include <vector>
#include <algorithm>

#ifndef __DISABLE_PRESUBMISSION_TESTS
#define PRESUBMISSION_ASSERT(testCase) __ASSERT_TEST("Presubmission", testCase)
#else
#define PRESUBMISSION_ASSERT(testCase)
#endif

//-------------------------------------------------------
// Tests
//-------------------------------------------------------

int __presubmit_testCreateVLAs()
{
    VLVector<int, STATIC_CAP> intVec{};
    VLVector<std::string, STATIC_CAP> stringVec{};
    VLVector<double, 4> doubleVec{};

    ASSERT_VLA_PROPERTIES(intVec, false, STATIC_CAP, 0)
    ASSERT_VLA_PROPERTIES(stringVec, false, STATIC_CAP, 0)
    ASSERT_VLA_PROPERTIES(doubleVec, false, 4, 0)

    auto dynamicallyAllocated = new VLVector<int, STATIC_CAP>;
    delete dynamicallyAllocated;

    return 1;
}

int __presubmit_testPushBack()
{
    VLVector<int, STATIC_CAP> vec;
    vec.push_back(1);

    return 1;
}

int __presubmit_testSize()
{
    VLVector<int, STATIC_CAP> vec;
    RETURN_ASSERT_TRUE(vec.size() == 0)
}

int __presubmit_testCapacity()
{
    VLVector<int, STATIC_CAP> vec;
    RETURN_ASSERT_TRUE(vec.capacity() == STATIC_CAP)
}

int __presubmit_testEmpty()
{
    VLVector<int, STATIC_CAP> vec;
    RETURN_ASSERT_TRUE(vec.empty())
}

int __presubmit_testClear()
{
    VLVector<int, STATIC_CAP> vec;
    if (!vec.empty())
    {
        return 0;
    }

    vec.push_back(1);
    vec.clear();

    RETURN_ASSERT_TRUE(vec.empty())
}

int __presubmit_testPopBack()
{
    VLVector<int, STATIC_CAP> vec;
    if (!vec.empty())
    {
        return 0;
    }

    vec.push_back(1);
    vec.pop_back();

    RETURN_ASSERT_TRUE(vec.empty())
}

int __presubmit_testGetElement()
{
    VLVector<int, STATIC_CAP> vec;
    vec.push_back(1);

    ASSERT_TRUE(vec.at(0) == 1)  // using VLVector::at
    RETURN_ASSERT_TRUE(vec[0] == 1) // using VLVector::operator[]
}

int __presubmit_testData()
{
    VLVector<int, STATIC_CAP> vec;
    vec.data();
    return 1;
}

int __presubmit_testComparison()
{
    VLVector<int, STATIC_CAP> vec1{};
    VLVector<int, STATIC_CAP> vec2{};

    RETURN_ASSERT_TRUE(vec1 == vec2)
}

int __presubmit_testAssignment()
{
    VLVector<int, STATIC_CAP> vec1{};
    vec1.push_back(1);

    VLVector<int, STATIC_CAP> vec2 = vec1;
    return 1;
}

int __presubmit_testIterator()
{
    VLVector<int, STATIC_CAP> vec;

    vec.begin();
    vec.end();
    vec.cbegin();
    vec.cend();

    return 1;
}

int __presubmit_testInsert1()
{
    VLVector<int, STATIC_CAP> vec;
    vec.push_back(0);
    vec.push_back(2);
    auto it = vec.begin();
    ++it;
    vec.insert(it, 1);

    RETURN_ASSERT_TRUE(vec[1] == 1)
}

int __presubmit_testInsert2()
{
    VLVector<int, STATIC_CAP> vec;
    vec.push_back(0);

    std::vector<int> values{1, 2, 3, 4};
    auto it = vec.begin();
    ++it;
    vec.insert(it, values.begin(), values.end());
    RETURN_ASSERT_TRUE(vec.size() == 5)
}

int __presubmit_testErase1()
{
    VLVector<int, STATIC_CAP> vec;
    for (int i = 0; i < 5; ++i)
    {
        vec.push_back(i);
    }
    vec.erase(vec.begin());
    RETURN_ASSERT_TRUE(vec.size() == 4)
}

int __presubmit_testIteratorsCtor()
{
    /* Create the values */
    std::vector<int> values{1, 2};

    /* Create the vec */
    VLVector<int, STATIC_CAP> vec(values.begin(), values.end());
    RETURN_ASSERT_TRUE(vec.size() == 2 && vec[0] == 1)
}

int __presubmit_testCopyCtor()
{
    VLVector<int, STATIC_CAP> vec1{};
    vec1.push_back(5);

    VLVector<int, STATIC_CAP> vec2(vec1);
    RETURN_ASSERT_TRUE(vec2[0] == 5)
}

//-------------------------------------------------------
//  The main entry point
//-------------------------------------------------------
int runPreSubmissionChecks()
{
    PRESUBMISSION_ASSERT(__presubmit_testCreateVLAs)
    PRESUBMISSION_ASSERT(__presubmit_testPushBack)
    PRESUBMISSION_ASSERT(__presubmit_testSize)
    PRESUBMISSION_ASSERT(__presubmit_testCapacity)
    PRESUBMISSION_ASSERT(__presubmit_testEmpty)
    PRESUBMISSION_ASSERT(__presubmit_testClear)
    PRESUBMISSION_ASSERT(__presubmit_testPopBack)
    PRESUBMISSION_ASSERT(__presubmit_testGetElement)
    PRESUBMISSION_ASSERT(__presubmit_testData)
    PRESUBMISSION_ASSERT(__presubmit_testComparison)
    PRESUBMISSION_ASSERT(__presubmit_testAssignment)
    PRESUBMISSION_ASSERT(__presubmit_testIterator)
    PRESUBMISSION_ASSERT(__presubmit_testInsert1)
    PRESUBMISSION_ASSERT(__presubmit_testInsert2)
    PRESUBMISSION_ASSERT(__presubmit_testErase1)
    PRESUBMISSION_ASSERT(__presubmit_testIteratorsCtor)
    PRESUBMISSION_ASSERT(__presubmit_testCopyCtor)

    return 1;
}

#endif
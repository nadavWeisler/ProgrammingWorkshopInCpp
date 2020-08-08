#include <cstdlib>
#include <stdexcept>

#ifndef EXAM_VLVECTOR_H
#define EXAM_VLVECTOR_H

#define OUT_OF_BOUND_ERROR "ERROR: out of bound"
#define DEFAULT_CAPACITY_VALUE 16

/**
 * @brief           Class represent
 * @tparam TYPE     Generic type
 * @tparam CAP      Max stack capacity
 */
template<typename TYPE, size_t CAP = DEFAULT_CAPACITY_VALUE>
class VLVector
{
private:
    size_t _size;
    size_t _capacity;
    size_t _stackCapacity;
    TYPE _stackValues[CAP];
    TYPE *_heapValues;

    /**
     * @brief           Resize array
     * @param newSize   New size
     */
    void _resize(size_t newSize)
    {
        bool needToDelete = this->_capacity != this->_stackCapacity;
        this->_capacity = this->_growingSize();
        TYPE *tmp = new TYPE[newSize];
        if (needToDelete)
        {
            for (size_t i = 0; i < this->_size; ++i)
            {
                tmp[i] = this->_heapValues[i];
            }
            delete[] this->_heapValues;
        }
        else
        {
            for (size_t i = 0; i < this->_size; ++i)
            {
                tmp[i] = this->_stackValues[i];
            }
        }
        this->_heapValues = new TYPE[this->_capacity];
        for (size_t i = 0; i < this->_size; ++i)
        {
            this->_heapValues[i] = tmp[i];
        }
        delete[]tmp;

    }

    /**
     * @brief           Add new item
     * @param newItem   New item
     * @param index     Index
     */
    void _addNewItem(const TYPE newItem, size_t index)
    {
        if (this->_size == this->_capacity)
        {
            this->_resize(this->_size + 1);
            this->_heapValues[index] = newItem;
        }
        else if (this->_capacity > this->_stackCapacity)
        {
            this->_heapValues[index] = newItem;
        }
        else
        {
            this->_stackValues[index] = newItem;
        }
        this->_size++;
    }

    /**
     * @brief   Calculate growing size
     * @return  Growing size
     */
    size_t _growingSize() const
    {
        return (3 * (this->_size + 1)) / 2;
    }

public:
    /**
     * @brief   Iterator class
     */
    class Iterator
    {
    private:
        TYPE *cur;
    public:
        typedef TYPE &ref;
        typedef TYPE *pointer;
        typedef Iterator self;

        /**
         * @brief Default constructor
         */
        Iterator() : cur(nullptr)
        {

        }

        /**
         * @brief           Copy constructor
         * @param other     Other constructor
         */
        Iterator(const Iterator &other) : cur(other.cur)
        {

        }

        /**
         * @brief           Another constructor
         * @param p         TYPE pointer
         */
        explicit Iterator(TYPE *p)
        {
            this->cur = p;
        }

        /**
         * @brief           = operator
         * @param other     Other iterator
         * @return          Iterator reference
         */
        Iterator &operator=(Iterator other)
        {
            this->cur = other.cur;
        }

        /**
         * @brief       ++ operator
         * @return      Iterator
         */
        self operator++()
        {
            this->cur++;
            return *this;
        }

        /**
         * @brief       += operator
         * @param num   number
         * @return      Iterator
         */
        self operator+=(size_t num)
        {
            this->cur += num;
            return *this;
        }

        /**
         * @brief       -- operator
         * @return      Iterator
         */
        self operator--()
        {
            Iterator res = *this;
            this->cur--;
            return res;
        }

        /**
         * @brief       -= operator
         * @param num   number
         * @return      Iterator
         */
        self operator-=(size_t num)
        {
            this->cur -= num;
            return *this;
        }

        /**
         * @brief   -> operator
         * @return  pointer to TYPE
         */
        pointer operator->()
        {
            return this->cur;
        }

        /**
         * @brief   * const operator
         * @return  TYPE reference
         */
        ref operator*() const
        {
            return *cur;
        }

        /**
         * @brief   * operator
         * @return  TYPE reference
         */
        ref operator*()
        {
            return *this->cur;
        }

        /**
         * @brief           == operator
         * @param other     Other iterator const reference
         * @return          true if equal, false otherwise
         */
        bool operator==(const Iterator &other)
        {
            return this->cur == other.cur;
        }

        /**
         * @brief           != operator
         * @param other     Other iterator const reference
         * @return          false if equal, true otherwise
         */
        bool operator!=(const Iterator &other)
        {
            return this->cur != other.cur;
        }

        /**
         * @brief           > operator
         * @param other     Other operator const reference
         * @return          true if cur > other's cur, false otherwise
         */
        bool operator>(const Iterator &other)
        {
            return this->cur > other.cur;
        }

        /**
         * @brief           >= operator
         * @param other     Other operator const reference
         * @return          true if cur >= other's cur, false otherwise
         */
        bool operator>=(const Iterator &other)
        {
            return this->cur >= other.cur;
        }

        /**
         * @brief           < operator
         * @param other     Other operator const reference
         * @return          true if cur < other's cur, false otherwise
         */
        bool operator<(const Iterator &other)
        {
            return this->cur < other.cur;
        }

        /**
         * @brief           < operator
         * @param other     Other operator const reference
         * @return          true if cur < other's cur, false otherwise
         */
        bool operator<=(const Iterator &other)
        {
            return this->cur <= other.cur;
        }

    };

    /**
     * @brief Const Iterator class
     */
    class ConstIterator
    {
    private:
        TYPE *cur;
    public:
        typedef TYPE value_type;
        typedef TYPE &ref;
        typedef ConstIterator self;

        /**
         * @brief Default constructor
         */
        ConstIterator() : cur(nullptr)
        {

        }

        /**
         * @brief           Copy constructor
         * @param other     ConstIterator
         */
        ConstIterator(const ConstIterator &other) : cur(other.cur)
        {

        }

        /**
         * @brief           Constructor
         * @param other     TYPE pointer
         */
        explicit ConstIterator(TYPE *other) : cur(other)
        {

        }

        /**
         * @brief           = operator
         * @param other     ConstIterator
         * @return          ConstIterator reference
         */
        ConstIterator &operator=(ConstIterator other)
        {
            this->cur = other.cur;
        }

        /**
         * @brief   * operator
         * @return  TYPE reference
         */
        ref operator*()
        {
            return *this->cur;
        }

        /**
         * @brief   -> operator
         * @return  Const TYPE value
         */
        value_type operator->() const
        {
            return *this->cur;
        }

        /**
         * @brief   ++ operator
         * @return  ConstIterator
         */
        self operator++()
        {
            this->cur++;
            return *this;
        }

        /**
         * @brief       += operator
         * @param num   Number
         * @return      ConstIterator
         */
        self operator+=(size_t num)
        {
            this->cur += num;
            return *this;
        }

        /**
         * @brief   -- operator
         * @return  ConstIterator
         */
        self operator--()
        {
            Iterator res = *this;
            this->cur--;
            return res;
        }

        /**
         * @brief       -= operator
         * @param num   Number
         * @return      ConstIterator
         */
        self operator-=(size_t num)
        {
            this->cur -= num;
            return *this;
        }

        /**
         * @brief           == operator
         * @param other     ConstIterator const reference
         * @return          true if equal, false otherwise
         */
        bool operator==(const ConstIterator &other)
        {
            return this->cur == other.cur;
        }

        /**
         * @brief           != operator
         * @param other     ConstIterator const reference
         * @return          false if equal, true otherwise
         */
        bool operator!=(const ConstIterator &other)
        {
            return this->cur != other.cur;
        }

        /**
         * @brief           > operator
         * @param other     ConstIterator const reference
         * @return          true if this > other, false otherwise
         */
        bool operator>(const ConstIterator &other)
        {
            return this->cur > other.cur;
        }

        /**
         * @brief           >= operator
         * @param other     ConstIterator const reference
         * @return          true if this >= other, false otherwise
         */
        bool operator>=(const ConstIterator &other)
        {
            return this->cur >= other.cur;
        }

        /**
         * @brief           < operator
         * @param other     ConstIterator const reference
         * @return          true if this < other, false otherwise
         */
        bool operator<(const ConstIterator &other)
        {
            return this->cur < other.cur;
        }

        /**
         * @brief           <= operator
         * @param other     ConstIterator const reference
         * @return          true if this <= other, false otherwise
         */
        bool operator<=(const ConstIterator &other)
        {
            return this->cur <= other.cur;
        }
    };

    /**
     * @brief   Const begin function
     * @return  ConstIterator
     */
    ConstIterator begin() const
    {
        if (this->_capacity > this->_stackCapacity)
        {
            return Iterator(this->_heapValues[0]);
        }
        else
        {
            return Iterator(this->_stackValues[0]);
        }
    }

    /**
     * @brief   Const end function
     * @return  ConstIterator
     */
    ConstIterator end() const
    {
        if (this->_capacity > this->_stackCapacity)
        {
            return Iterator(&this->_heapValues[0] + this->_size);
        }
        else
        {
            return Iterator(&this->_stackValues[0] + this->_size);
        }
    }

    /**
     * @brief   begin function
     * @return  Iterator
     */
    Iterator begin()
    {
        if (this->_capacity > this->_stackCapacity)
        {
            return Iterator(&this->_heapValues[0]);
        }
        else
        {
            return Iterator(&this->_stackValues[0]);
        }
    }

    /**
     * @brief   end function
     * @return  Iterator
     */
    Iterator end()
    {
        if (this->_capacity > this->_stackCapacity)
        {
            return Iterator(&this->_heapValues[this->_size]);
        }
        else
        {
            return Iterator(&this->_stackValues[this->_size]);
        }
    }

    /**
     * @brief   cbegin function
     * @return  ConstIterator
     */
    ConstIterator cbegin()
    {
        if (this->_capacity > this->_stackCapacity)
        {
            return ConstIterator(&this->_heapValues[0]);
        }
        else
        {
            return ConstIterator(&this->_stackValues[0]);
        }
    }

    /**
     * @brief   cend function
     * @return  ConstIterator
     */
    ConstIterator cend()
    {
        if (this->_capacity > this->_stackCapacity)
        {
            return ConstIterator(&this->_heapValues[0] + this->_size);
        }
        else
        {
            return ConstIterator(&this->_stackValues[0] + this->_size);
        }
    }

    /**
     * @brief Default constructor
     */
    VLVector<TYPE, CAP>() : _size(0),
                            _capacity(CAP),
                            _stackCapacity(CAP)
    {

    }

    /**
     * @brief       Copy constructor
     * @param v     VLVector
     */
    VLVector<TYPE, CAP>(VLVector const &v) : _size(v._size),
                                             _capacity(v._capacity),
                                             _stackCapacity(v._stackCapacity)
    {
        if (this->_capacity > this->_stackCapacity)
        {
            this->_heapValues = new TYPE[this->_capacity];
            for (size_t i = 0; i < this->_size; i++)
            {
                this->_heapValues[i] = v._heapValues[i];
            }
        }
        else
        {
            for (size_t i = 0; i < this->_size; i++)
            {
                this->_stackValues[i] = v._stackValues[i];
            }
        }
    }

    /**
     * @brief                   Constructor 1
     * @tparam InputIterator    Input iterator
     * @param first             First iterator
     * @param last              Last iterator
     */
    template<class InputIterator>
    VLVector<TYPE, CAP>(InputIterator first, InputIterator last) :_size(0),
                                                                  _capacity(0),
                                                                  _stackCapacity(0)
    {
        while (first != last)
        {
            this->push_back(*first);
            ++first;
        }
    }

    /**
     * @brief Destructor
     */
    ~VLVector<TYPE, CAP>()
    {
        if (this->_capacity > this->_stackCapacity)
        {
            delete[] this->_heapValues;
        }
        this->_size = 0;
        this->_capacity = 0;
    }

    /**
     * @brief   Size of VLVector
     * @return  Return size_t
     */
    size_t size() const
    {
        return this->_size;
    }

    /**
     * @brief   Capacity of VLVector
     * @return  size_t
     */
    size_t capacity() const
    {
        return this->_capacity;
    }

    /**
     * @brief   Boolean if vector is empty
     * @return  true if empty, false otherwise
     */
    bool empty() const
    {
        return this->_size == 0;
    }

    /**
     * @brief           Get the value on the given index
     * @param index     Index
     * @return          Value on the given index
     */
    TYPE &at(size_t index)
    {
        if (index < 0 || index > this->_size)
        {
            throw std::out_of_range(OUT_OF_BOUND_ERROR);
        }
        else
        {
            if (this->_capacity > this->_stackCapacity)
            {
                return this->_heapValues[index];
            }
            else
            {
                return this->_stackValues[index];
            }
        }
    }

    /**
     * @brief               Push back
     * @param newValue
     */
    void push_back(const TYPE &newValue)
    {
        this->_addNewItem(newValue, this->_size);
    }

    /**
     * @brief               Insert 1
     * @param iterator      Iterator
     * @param newValue      New value
     * @return              Iterator
     */
    Iterator insert(Iterator iterator, const TYPE &newValue)
    {
        size_t itrLoc = this->_itLocation(iterator);
        if (this->_size == this->_capacity)
        {
            _resize(this->_size + 1);
        }
        bool found = false;
        for (size_t i = this->_size; i > 0; i--)
        {
            if (i == itrLoc)
            {
                if (this->_capacity > this->_stackCapacity)
                {
                    this->_heapValues[i] = newValue;
                }
                else
                {
                    this->_stackValues[i] = newValue;
                }
                found = true;
                break;
            }
            else
            {
                if (this->_capacity > this->_stackCapacity)
                {
                    this->_heapValues[i] = this->_heapValues[i - 1];
                }
                else
                {
                    this->_stackValues[i] = this->_stackValues[i - 1];
                }
            }
        }
        this->_size++;
        if (!found)
        {
            if (this->_capacity > this->_stackCapacity)
            {
                this->_heapValues[0] = newValue;
            }
            else
            {
                this->_stackValues[0] = newValue;
            }
        }
        return this->_getIterator(itrLoc);
    }

    template<class InputIterator>
    Iterator insert(Iterator iterator, InputIterator first, InputIterator last)
    {
        size_t itrLoc = this->_itLocation(iterator);
        InputIterator current = first;
        size_t count = 0;
        while (current != last)
        {
            count++;
            ++current;
        }
        if (this->_size + count > this->_capacity)
        {
            this->_resize(this->_size + count);
        }
        size_t prevCount = this->_size - 1;
        size_t addCount = count;
        TYPE *tmp = new TYPE[this->_size + count];
        TYPE toAdd;
        current = last;
        for (size_t i = this->_size + count; i > 0; i--)
        {
            if (i == itrLoc + addCount && addCount != 0)
            {
                toAdd = *current;
                --current;
                addCount--;
            }
            else
            {
                toAdd = this->_getValue(prevCount);
                prevCount--;
            }
            tmp[i] = toAdd;
        }
        for (size_t i = 0; i < this->_size + count; i++)
        {
            if (this->_capacity > this->_stackCapacity)
            {
                this->_heapValues[i] = tmp[i];
            }
            else
            {
                this->_stackValues[i] = tmp[i];
            }
        }
        delete[] tmp;
        this->_size += count;
        return this->_getIterator(itrLoc);
    }

    /**
     * @brief Pop up last vector value
     */
    void pop_back()
    {
        if (this->_size > 0)
        {
            this->_size--;
            if (this->_size == this->_stackCapacity)
            {
                for (size_t i = 0; i < this->_stackCapacity; i++)
                {
                    this->_stackValues[i] = this->_heapValues[i];
                }
                delete[] this->_heapValues;
                this->_capacity = this->_stackCapacity;
            }
        }
    }

    /**
     * @brief           Erase 1
     * @param iterator  Iterator
     * @return          Iterator
     */
    Iterator erase(Iterator iterator)
    {
        TYPE *tmp = new TYPE[this->_size];
        for (size_t i = 0; i < this->_size; i++)
        {
            tmp[i] = this->_getValue(i);
        }
        this->_size--;
        bool found = false;
        size_t i = 0;
        auto it = this->begin();
        if (this->_size == this->_stackCapacity)
        {
            this->_capacity = this->_stackCapacity;
        }
        size_t iterLoc = this->_itLocation(iterator);
        while (i < this->_size - 1)
        {
            if (it == iterator)
            {
                found = true;
            }
            if (found)
            {
                if (this->_capacity > this->_stackCapacity)
                {
                    this->_heapValues[i] = tmp[i + 1];
                }
                else
                {
                    this->_stackValues[i] = tmp[i + 1];
                }
            }
            ++it;
            i++;
        }
        delete[] tmp;
        if (this->_size == this->_stackCapacity)
        {
            delete[] this->_heapValues;
        }
        return _getIterator(iterLoc);
    }


    /**
     * @brief           Erase 2
     * @param first     First index
     * @param last      Last index
     * @return          Iterator
     */
    Iterator erase(Iterator first, Iterator last)
    {
        size_t firstIndex = 0;
        size_t secondIndex = 0;
        size_t itrLoc = this->_itLocation(first);
        Iterator current = first;
        bool firstFound = false;
        while (current != last)
        {
            if (current == first)
            {
                firstFound = true;
            }
            if (!firstFound)
            {
                firstIndex++;
            }
            secondIndex++;
        }
        size_t gap = secondIndex - firstIndex;
        for (size_t i = secondIndex; i < this->_size; i++)
        {
            if (this->_capacity > this->_stackCapacity)
            {
                this->_heapValues[i - gap] = this->_heapValues[i];
            }
            else
            {
                this->_stackValues[i - gap] = this->_stackValues[i];
            }
            this->_size--;
        }
        if (this->_size <= this->_stackCapacity)
        {
            for (size_t i = 0; i < this->_size; i++)
            {
                this->_stackValues[i] = this->_heapValues[i];
            }
            delete[] this->_heapValues;
        }
        return this->_getIterator(itrLoc);
    }

    /**
     * @brief Clear function
     */
    void clear()
    {
        this->_capacity = 0;
        this->_size = 0;
        if (this->_capacity > this->_stackCapacity)
        {
            delete[] this->_heapValues;
        }
    }

    /**
     * @brief   Get data pointer
     * @return  Values pointer
     */
    TYPE *data()
    {
        if (this->_capacity == this->_stackCapacity)
        {
            return this->_stackValues;
        }
        else
        {
            return this->_heapValues;
        }
    }

    /**
     * @brief        = Operator
     * @param other  Other VLVector
     * @return       VLVector
     */
    VLVector<TYPE, CAP> &operator=(VLVector<TYPE, CAP> other)
    {
        if (this == other)
        {
            return *this;
        }
        this->_size = other._size;
        this->_stackCapacity = other._stackCapacity;
        if (this->_capacity > this->_stackCapacity)
        {
            delete[] this->_heapValues;
        }
        this->_capacity = other._capacity;
        this->_heapValues = other._heapValues;
        this->_stackValues = other._stackValues;
        return *this;
    }

    /**
     * @brief           [] operator
     * @param index     Index
     * @return          TYPE reference
     */
    TYPE &operator[](size_t index)
    {
        if (index > this->_size)
        {
            throw std::out_of_range(OUT_OF_BOUND_ERROR);
        }
        else
        {
            if (this->_capacity > this->_stackCapacity)
            {
                return this->_heapValues[index];
            }
            else
            {
                return this->_stackValues[index];
            }
        }
    }

    /**
     * @brief           const [] operator
     * @param index     Index
     * @return          TYPE reference
     */
    TYPE operator[](size_t index) const
    {
        if (index > this->_size)
        {
            throw std::out_of_range(OUT_OF_BOUND_ERROR);
        }
        else
        {
            if (this->_capacity > this->_stackCapacity)
            {
                return this->_heapValues[index];
            }
            else
            {
                return this->_stackValues[index];
            }
        }
    }

    /**
     * @brief           == operator
     * @param other     Other VLVector
     * @return          true if equal, false otherwise
     */
    bool operator==(VLVector other)
    {
        if (this->_size != other._size)
        {
            return false;
        }
        else
        {
            for (size_t i = 0; i < this->_size; i++)
            {
                if (this->_capacity > this->_stackCapacity)
                {
                    if (this->_heapValues[i] != other._heapValues[i])
                    {
                        return false;
                    }
                }
                else
                {
                    if (this->_stackValues[i] != other._stackValues[i])
                    {
                        return false;
                    }
                }
            }
        }
        return true;
    }

    /**
     * @brief           != operator
     * @param other     Other VLVector
     * @return          false if equal, true otherwise
     */
    bool operator!=(VLVector other)
    {
        if (this->_size != other._size)
        {
            return true;
        }
        else
        {
            for (size_t i = 0; i < this->_size; i++)
            {
                if (this->_capacity > this->_stackCapacity)
                {
                    if (this->_heapValues[i] != other._heapValues[i])
                    {
                        return true;
                    }
                }
                else
                {
                    if (this->_stackValues[i] != other._stackValues[i])
                    {
                        return true;
                    }
                }
            }
        }
        return false;
    }

private:
    /**
     * @brief       Get iterator pointer location
     * @param it    Iterator
     * @return      size_t
     */
    size_t _itLocation(Iterator it)
    {
        auto tmp = this->begin();
        size_t index = 0;
        while (tmp != it)
        {
            index++;
            ++tmp;
        }
        return index;
    }

    Iterator _getIterator(size_t iterLoc)
    {
        if (_capacity > _stackCapacity)
        {
            return Iterator(&this->_heapValues[iterLoc]);
        }
        else
        {
            return Iterator(&this->_stackValues[iterLoc]);
        }
    }

    TYPE _getValue(size_t n)
    {
        if (this->_capacity > this->_stackCapacity)
        {
            return this->_heapValues[n];
        }
        else
        {
            return this->_stackValues[n];
        }
    }
};

#endif

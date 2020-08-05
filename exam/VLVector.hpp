#include <cstdlib>

#ifndef EXAM_VLVECTOR_H
#define EXAM_VLVECTOR_H
#define DEFAULT_CAPACITY 16
#define GROWS 2

template<class TYPE>
class VLVector
{
private:
    TYPE *_values;
    size_t _capacity = 0;
    size_t _size = 0;

    void _resize()
    {
        TYPE tmp[] = _deepCopyValues();
        this->_values = new TYPE[this->_capacity * 2];
        for (int i = 0; i < this->_capacity; i++)
        {
            this->_values[i] = tmp[i];
        }
        this->_capacity *= 2;
    }

    void _addNewItem(TYPE *newItem, int index)
    {
        if (this->_values == nullptr)
        {
            this->_values = new TYPE[DEFAULT_CAPACITY];
        }
        if (this->_size == this->_capacity)
        {
            this->_resize();
            this->_addNewItem(newItem, index);
        }
        this->_values[index] = newItem;
    }

    TYPE *_deepCopyValues()
    {
        TYPE result[] = new TYPE[this->_capacity];
        for (int i = 0; i < this->_capacity; i++)
        {
            result[i] = this->_values[i];
        }
        return result;
    }

public:
    //Iterator
    class InputIterator
    {
    private:
        TYPE *arr;
    public:
        InputIterator(TYPE *p) : arr(p)
        {
        }

        InputIterator &operator++()
        {
            this->arr++;
            return *this;
        }

        InputIterator &operator--()
        {
            this->arr--;
            return *this;
        }

        TYPE *operator*()
        {
            return *arr;
        }

        bool operator==(const InputIterator &other) const
        {
            return *arr == *other.arr;
        }

        bool operator!=(const InputIterator &other) const
        {
            return *arr != *other.arr;
        }
    };

    InputIterator _iterator;

    InputIterator begin() const
    {
        return this->_iterator[0];
    }

    InputIterator end() const
    {
        return this->_iterator[this->_size];
    }

    //Constructors \ Destructors
    /**
     * @brief   Default constructor
     */
    VLVector() : _size(0), _capacity(DEFAULT_CAPACITY), _values(nullptr)
    {
    }

    /**
     * @brief       Copy constructor
     * @param v     VLVector
     */
    VLVector(VLVector const &v) : _size(v._size), _capacity(v._capacity)
    {
        this->_values = (TYPE *) malloc(v._capacity * sizeof(TYPE));
        for (int i = 0; i < this->_size; i++)
        {
            this[i] = v.at(i);
        }
    }

    /**
     * @brief                   Constructor
     * @tparam InputIterator
     * @param first
     * @param last
     */
    template<class InputIterator>
    VLVector(InputIterator &first, InputIterator &last)
    {
        this->_capacity = DEFAULT_CAPACITY;
        this->_size = 0;
    }

    /**
     * @brief Class destructor
     */
    ~VLVector()
    {
        if (_capacity > 0)
        {
            delete[] this->_values;
        }
        this->_size = 0;
        this->_capacity = 0;
        this->_values = nullptr;
    }

    //Size \ capacity

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
    TYPE &at(const int index)
    {
        if (index < 0 or index > this->_size)
        {
            throw "OUT OF RANGE";
        }
        return this->_values[index];
    }

    const TYPE &at(const int index) const
    {
        if (index < 0 or index > this->_size)
        {
            throw "OUT OF RANGE";
        }
        return this->_values[index];
    }

    /**
     * @brief               Push back
     * @param newValue
     */
    void push_back(const TYPE &newValue)
    {
        this->_addNewItem(newValue, this->_size);
        this->_size++;
    }

    InputIterator insert(InputIterator iterator)
    {
        return NULL;
    }

    InputIterator insert(InputIterator iterator, int first, int last)
    {
        return NULL;
    }

    void pop_back()
    {
        
    }

    InputIterator erase(InputIterator iterator)
    {
        return NULL;
    }

    InputIterator erase(InputIterator, int first, int last)
    {
        return NULL;
    }

    void clear()
    {
        this->_capacity = 0;
        this->_size = 0;
        this->_values = nullptr;
    }

    TYPE *data()
    {
        return this->_values;
    }

    TYPE &operator[](int index)
    {
        return this->_values[index];
    }

    bool operator==(const InputIterator &rhs) const
    {
        return _values == rhs.ptr;
    }

    bool operator!=(const InputIterator &rhs) const
    {
        return *this != rhs;
    }
};

#endif //EXAM_VLVECTOR_H

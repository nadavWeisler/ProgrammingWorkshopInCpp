#include <iostream>
#include "RecommenderSystem.h"
#include <cmath>
using namespace std;

#define SQUARE 2

void printMap(const unordered_map<string, vector<double>>& map)
{
    for (pair<string, vector<double>> couple : map )
    {
        cout << couple.first << ": " << endl;
        for (double num : couple.second)
        {
            cout << num << " ";
        }
        cout << endl;
    }
}

void printMap(const unordered_map<string, unordered_map<string, double>> & map)
{
    for (pair<string, unordered_map<string, double>> couple : map )
    {
        cout << couple.first << ": " << endl;
        for (pair<string, double> rank : couple.second)
        {
            cout << rank.first << ": " << rank.second << endl;
        }
    }
}

void printMapToVector(const unordered_map<string, double> & map)
{

    cout << "{";
    for (pair<string, double> couple : map )
    {
        cout << couple.second << ", ";
    }
    cout << "}" << endl;
}

void printVector( const vector<double> & vec)
{
    cout << "{";
    for (double num : vec)
    {
        cout << num << ", ";
    }
    cout << "}" << endl;
}

int main()
{
    vector<double> vector1 = {1, 1, 1, 1};
    vector<double> vector2 = {2, 2, 2, 2};
    RecommenderSystem rec;
    rec.loadData("movies_big.txt", "ranks_big.txt");
    string res = rec.recommendByCF("Michaela", 2);
    cout << "Michaela CF:" << res << endl;
    return 0;
}

#include <fstream>
#include <iostream>
#include <sstream>
#include <algorithm>
#include <cmath>
#include "RecommenderSystem.h"

#define USER_NOT_FOUND "USER NOT FOUND"
#define UNABLE_TO_OPEN_FILE "Unable to open file <file_path>"
#define SPACE ' '
#define FAIL -1
#define SUCCESS 0
#define NONE "NA"

/**
 * Basic constructor
 */
RecommenderSystem::RecommenderSystem()
{
	this->movieRating = unordered_map<string, vector<double>>();
	this->userRating = unordered_map<string, unordered_map<string, double>>();
}

/**
 *	Get movie split
 * @param str	String
 * @return		string and double vector pair
 */
pair<string, vector<double>> RecommenderSystem::_getMovieSplit(string& str)
{
	size_t pos = 0;
	string subStr;
	string name;
	pair<string, vector<double>> result;

	name = str.substr(0, pos);
	result.first = name;
	result.second = vector<double>();
	str.erase(0, pos + 1);

	while ((pos = str.find(SPACE)) != string::npos)
	{
		subStr = str.substr(0, pos);
		result.second.push_back(stoi(subStr));
		str.erase(0, pos + 1);
	}
	return result;
}

/**
 *	Get average
 * @param unorderedMap Calculate average
 * @return	Average
 */
double RecommenderSystem::_getAvg(const unordered_map<string, double>& unorderedMap)
{
	double sum = 0;
	double count = 0;
	for (auto& item: unorderedMap)
	{
		if (item.second != 0)
		{
			count++;
			sum += item.second;
		}
	}
	return (sum / count);
}

/**
 *	Normalize user rank
 * @param userName	User name
 * @param avg		Average
 */
void RecommenderSystem::_normalizeUserRank(const string& userName, double avg)
{
	for (auto& p : this->userRating[userName])
	{
		if (p.second != 0)
		{
			this->userRating[userName][p.first] -= avg;
		}
	}
}

/**
 *	Multiply vector with scalar
 * @param vec		Vector
 * @param scalar	Scalar
 * @return			double vector
 */
vector<double> RecommenderSystem::_multiplyVectorInScalar(const vector<double>& vec, double scalar)
{
	vector<double> result = vector<double>();
	for (double item: vec)
	{
		result.push_back(item * scalar);
	}
	return result;
}

/**
 *	Return sum of two vectors
 * @param vec1		Vector
 * @param vec2		Vector
 * @return			Vector sum
 */
vector<double> RecommenderSystem::_addVectorToAnother(vector<double> vec1, const vector<double>& vec2)
{
	vector<double> result = vector<double>();
	for (int i = 0; i < max(int(vec1.size()), int(vec2.size())); i++)
	{
		double current = 0;
		if (int(vec1.size()) < i)
		{
			current += vec1.at(i);
		}

		if (int(vec2.size()) < i)
		{
			current += vec2.at(i);
		}

		result.push_back(current);
	}
	return result;
}

/**
 * Get preference vector of user ranks
 * @param userRanks
 * @return
 */
vector<double> RecommenderSystem::_getPreferenceVector(const unordered_map<string, double>& userRanks)
{
	vector<int> result = vector<int>();
	vector<double> resultVector = vector<double>();
	for (auto& p: userRanks)
	{
		vector<double> movieVector = _multiplyVectorInScalar(this->movieRating[p.first], p.second);
		resultVector = _addVectorToAnother(resultVector, movieVector);
	}
	return resultVector;
}

/**
 * Get norm of vector
 * @param vec	Vector
 * @return		Vector norm
 */
double RecommenderSystem::_getNorm(const vector<double>& vec)
{
	double sum = 0;
	for (double item: vec)
	{
		sum += (item * item);
	}
	return sqrt(sum);
}

/**
 * Get scalar multiplications between two vectors
 * @param vector1 		Vector1
 * @param vector2 		Vector2
 * @return				Scalar multiplication
 */
double RecommenderSystem::_getScalarMultiplication(vector<double> vector1, vector<double> vector2)
{
	double result = 0;
	for (int i = 0; i < int(vector1.size()); i++)
	{
		result += (vector1[i] * vector2[i]);
	}
	return result;
}

/**
 * Get angle between 2 vectors
 * @param vector1 			vector1
 * @param vector2			Movie vector
 * @return					Angle between 2 vectors
 */
double RecommenderSystem::_getAngleBetweenVectors(const vector<double>& vector1, const vector<double>& vector2)
{
	return _getScalarMultiplication(vector1, vector2) /
		(_getNorm(vector1) * _getNorm(vector2));
}

/**
 * Get suggested movie from preference vector user rank
 * @param preferenceVector
 * @param userMap
 * @return
 */
string RecommenderSystem::_getSuggestedMovie(const vector<double>& preferenceVector, const unordered_map<string, double>& userMap)
{
	string result;
	double minValue = 2;
	double currentValue;
	for (pair<string, int> p: userMap)
	{
		if (p.second == 0)
		{
			currentValue = _getAngleBetweenVectors(preferenceVector, this->movieRating[p.first]);
			if (currentValue < minValue)
			{
				minValue = currentValue;
				result = p.first;
			}
		}
	}
	return result;
}

/**
 * Load movies
 * @param moviePath		Movie file path
 * @return				FAIL if fail, SUCCESS otherwise
 */
int RecommenderSystem::_loadMovies(const string& moviePath)
{
	ifstream infile;
	infile.open(moviePath);
	if (!infile.is_open())
	{
		cerr << UNABLE_TO_OPEN_FILE << endl;
		return FAIL;
	}

	string line;
	this->movieRating = unordered_map<string, vector<double>>();
	while (getline(infile, line))
	{
		istringstream str(line);
		{
			this->movieRating.insert(this->_getMovieSplit(line));
		}
	}
	return SUCCESS;
}

/**
 * Add line to unordered map
 * @param movie				Movie
 * @param input				string
 * @param movieIndex		Movie index
 * @param moviesNames		Movie names
 */
unordered_map<string, double> RecommenderSystem::_addLineToMap(unordered_map<string, double> movie, const string& input, int movieIndex, vector<string>& moviesNames)
{
	if (input != NONE)
	{
		movie[moviesNames[movieIndex]] = stod(input);
	}
	else
	{
		movie[moviesNames[movieIndex]] = 0;
	}
	return movie;
}

/**
 * Load user ranking
 * @param moviePath		Movie path
 * @return				FAIL if fail, SUCCESS otherwise
 */
int RecommenderSystem::_loadUserRanking(const string& moviePath)
{
	ifstream infile;
	infile.open(moviePath);
	if (!infile.is_open())
	{
		return FAIL;
	}

	this->_updateUserRanking(infile);
	return SUCCESS;
}

/**
 * Update user ranking by file
 * @param infile ifstream
 */
void RecommenderSystem::_updateUserRanking(ifstream& infile)
{
	int lineCount = 0;
	string line;
	vector<string> names;
	userRating = unordered_map<string, unordered_map<string, double>>();
	while (getline(infile, line))
	{
		_updateRankLine(lineCount, line, names);
	}
}

/**
 * Update rank line
 * @param lineCount		Line count
 * @param line			string
 * @param names			movie names
 */
void RecommenderSystem::_updateRankLine(int lineCount, const string& line, vector<string>& names)
{
	istringstream str(line);
	{
		if (lineCount == 0)
		{
			string movieName;
			while (str)
			{
				str >> movieName;
				names.push_back(movieName);
			}
		}
		else
		{
			string userName;
			str >> userName;
			unordered_map<string, double> movieRate;
			int index = 0;
			while (str)
			{
				string input;
				str >> input;
				if (!input.empty())
				{
					movieRate = _addLineToMap(movieRate, input, index, names);
				}
				index++;
			}
			userRating[userName] = movieRate;
		}
		lineCount++;
	}
}

/**
 *	Load data from files
 * @param moviePath		Movie file path
 * @param userPath		User file path
 * @return
 */
int RecommenderSystem::loadData(const string& moviePath, const string& userPath)
{
	if (_loadMovies(moviePath) == FAIL || _loadUserRanking(userPath) == FAIL)
	{
		return FAIL;
	}
	return SUCCESS;
}

/**
 *	Recommend to user by content
 * @param userName		User name
 * @return				Recommended movie
 */
string RecommenderSystem::recommendByContent(const string& userName)
{
	unordered_map<string, double> userMap = this->userRating[userName];
	if (userMap.empty())
	{
		return USER_NOT_FOUND;
	}
	_normalizeUserRank(userName, _getAvg(userMap));
	vector<double> prefVector = _getPreferenceVector(userMap);
	return _getSuggestedMovie(prefVector, userMap);
}

/**
 *	Predict movie score for user
 * @param movieName		Movie name
 * @param userName		User name
 * @param k				int
 * @return				Movie score
 */
double RecommenderSystem::predictMovieScoreForUser(const string& movieName, const string& userName, int k)
{
	unordered_map<double, string> similarMovies;
	vector<double> newMovieVec = this->movieRating[movieName];
	unordered_map<string, double> usersMap = this->userRating[userName];
	if (newMovieVec.empty() || usersMap.empty())
	{
		return FAIL;
	}

	for (pair<string, double> p: usersMap)
	{
		if (p.second != 0)
		{
			vector<double> attrVec = this->movieRating[p.first];
			double normValue = _getAngleBetweenVectors(newMovieVec, attrVec);
			similarMovies[normValue] = p.first;
		}
	}

	return _predictScore(similarMovies, userName, k);
}

/**
 * Predict score
 * @param similarMovies		Similar movies map
 * @param userName			String user map
 * @param k					int
 * @return					Score
 */
double RecommenderSystem::_predictScore(unordered_map<double, string>& similarMovies, const string& userName, int k)
{
	double userRank = 0;
	double similarRank = 0;
	for (auto i = std::next(similarMovies.begin(), similarMovies.size() - k);
		 i != similarMovies.end(); i++)
	{
		userRank += i->first * this->userRating[userName][i->second];
		similarRank += i->first;
	}

	return userRank / similarRank;
}

/**
 *	Recommend by CF
 * @param userName		User name
 * @param k				K
 * @return				Recommended movie
 */
string RecommenderSystem::recommendByCF(const string& userName, int k)
{
	unordered_map<double, vector<string>> moviesRate;
	unordered_map<string, double> usersMap = this->userRating[userName];
	if (usersMap.empty())
	{
		return USER_NOT_FOUND;
	}
	for (auto& p : this->userRating[userName])
	{
		if (p.second == 0)
		{
			double predictRate = predictMovieScoreForUser(p.first, userName, k);
			moviesRate[predictRate].push_back(p.first);
		}
	}
	string suggestedMovie = _getMovie(moviesRate);
	return suggestedMovie;
}

/**
 * Get movie
 * @param moviesRate	Movie rate
 * @return				Movie name
 */
string RecommenderSystem::_getMovie(unordered_map<double, vector<string>> moviesRate)
{
	string suggestedMovie;
	if (moviesRate.begin()->second.size() > 1)
	{
		suggestedMovie = _getFirstMovie(moviesRate.begin()->second);
	}
	else
	{
		suggestedMovie = moviesRate.begin()->second[0];
	}
	return suggestedMovie;
}

/**
 * Get first best movie
 * @param bestMovies	Best movies vector
 * @return				Best movie string
 */
string RecommenderSystem::_getFirstMovie(vector<string>& bestMovies)
{
	for (auto& p: this->movieRating)
	{
		for (auto& bestMovie : bestMovies)
		{
			if (p.first == bestMovie)
			{
				return p.first;
			}
		}
	}
	return "";
}

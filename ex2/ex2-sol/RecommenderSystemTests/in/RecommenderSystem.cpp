#include <fstream>
#include <iostream>
#include <sstream>
#include <algorithm>
#include <cmath>
#include <forward_list>
#include "RecommenderSystem.h"
#include <unordered_map>

#define USER_NOT_FOUND "USER NOT FOUND"
#define UNABLE_TO_OPEN_FILE "Unable to open file "
#define FAIL -1
#define SUCCESS 0
#define NONE "NA"
#define SQUARE 2

/**
 * Basic constructor
 */
RecommenderSystem::RecommenderSystem()
{
    this->movieRating = std::unordered_map<std::string, std::vector<double>>();
    this->userRating = std::unordered_map<std::string,
            std::unordered_map<std::string, double>>();
    this->movies = std::vector<std::string>();
}

/**
 *	Get movie split
 * @param line	String
 * @return		string and double vector pair
 */
bool RecommenderSystem::_getMovieSplit(std::string &line)
{
    std::pair<std::string, std::vector<double>> result =
            std::pair<std::string, std::vector<double>>();
    result.second = std::vector<double>();
    int count = 0;
    std::istringstream stringStream(line);
    while (!stringStream.eof())
    {
        std::string str = std::string();
        stringStream >> str;
        if (!str.empty())
        {
            if (count == 0)
            {
                result.first = str;
            }
            else
            {
                try
                {
                    result.second.resize(count + 1);
                    result.second.at(count) = stod(str);
                }
                catch (const std::invalid_argument &)
                {
                    return false;
                }
            }
        }
        ++count;
    }

    this->movieRating.insert(result);
    return true;
}

/**
 *	Get average
 * @param map Calculate average
 * @return	Average
 */
double RecommenderSystem::_getAvg(const std::unordered_map<std::string, double> &mapHash)
{
    double sum = 0;
    double count = 0;
    for (const auto &p: mapHash)
    {
        if (p.second != 0)
        {
            count++;
            sum += p.second;
        }
    }
    return (sum / count);
}

/**
 *	Normalize user rank
 * @param userName	User name
 * @param avg		Average
 */
std::unordered_map<std::string, double> RecommenderSystem::_getNormalizeUserRank(
        const std::string &userName, double avg)
{
    std::unordered_map<std::string, double> result =
            std::unordered_map<std::string, double>();
    double insertValue;
    for (const auto &p : this->userRating[userName])
    {
        insertValue = 0;
        if (p.second != 0)
        {
            insertValue = p.second - avg;
        }
        result.insert({p.first, insertValue});
    }
    return result;
}

/**
 *	Multiply vector with scalar
 * @param vec		Vector
 * @param scalar	Scalar
 * @return			double vector
 */
std::vector<double>
RecommenderSystem::_multiplyVectorInScalar(const std::vector<double> &vec, double scalar)
{
    std::vector<double> result = std::vector<double>();
    int count = 0;
    for (size_t i = 0, size = vec.size(); i != size; ++i)
    {
        result.resize(count + 1);
        result.at(count) = vec[i] * scalar;
        count++;
    }
    return result;
}

/**
 *	Return sum of two vectors
 * @param vec1		Vector
 * @param vec2		Vector
 * @return			Vector sum
 */
std::vector<double> RecommenderSystem::_addVectorToAnother(
        std::vector<double> &vec1,
        std::vector<double> &&vec2)
{
    std::vector<double> result = std::vector<double>();
    for (size_t i = 0, size = vec2.size(); i != size; ++i)
    {
        result.resize(i + 1);
        double addValue = vec2[i];
        if (vec1.size() == vec2.size())
        {
            addValue += vec1[i];
        }
        result.at(i) = addValue;
    }
    return result;
}

/**
 * Get preference vector of user ranks
 * @param userRanks
 * @return
 */
std::vector<double> RecommenderSystem::_getPreferenceVector(
        std::unordered_map<std::string, double> &&normelizeUserRanks)
{
    std::vector<double> resultVector = std::vector<double>();
    for (const auto &p: normelizeUserRanks)
    {
        if (p.second != 0)
        {
            resultVector = _addVectorToAnother(
                    resultVector,
                    std::move(_multiplyVectorInScalar(
                            this->movieRating[p.first], p.second)));
        }
    }
    return resultVector;
}

/**
 * Get norm of vector
 * @param vec	Vector
 * @return		Vector norm
 */
double RecommenderSystem::_getNorm(const std::vector<double> &vec)
{
    double sum = 0;
    for (size_t i = 0, size = vec.size(); i != size; ++i)
    {
        sum += pow(vec[i], SQUARE);
    }
    return sqrt(sum);
}

/**
 * Get scalar multiplications between two vectors
 * @param vector1 		Vector1
 * @param vector2 		Vector2
 * @return				Scalar multiplication
 */
double RecommenderSystem::_getScalarMultiplication(const std::vector<double> &vector1,
                                                   const std::vector<double> &vector2)
{
    double result = 0;
    for (size_t i = 0, size = vector1.size(); i != size; ++i)
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
double RecommenderSystem::_getAngleBetweenVectors(const std::vector<double> &vector1,
                                                  const std::vector<double> &vector2)
{
    return (_getScalarMultiplication(vector1, vector2)) /
           (_getNorm(vector1) * _getNorm(vector2));
}

/**
 * Get suggested movie from preference vector user rank
 * @param preferenceVector
 * @param userMap
 * @return
 */
std::string RecommenderSystem::_getSuggestedMovie(
        std::vector<double> &&preferenceVector,
        std::unordered_map<std::string, double> &&userMap)
{
    std::string result = std::string();
    double bestScore = -1;
    double currentValue;
    for (const auto &p: userMap)
    {
        if (p.second == 0)
        {
            currentValue = _getAngleBetweenVectors(preferenceVector,
                                                   this->movieRating[p.first]);
            if (currentValue > bestScore)
            {
                bestScore = currentValue;
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
bool RecommenderSystem::_loadMovies(const std::string &fileName)
{
    bool retValue = true;
    std::ifstream movieFile;
    try
    {
        movieFile.open(fileName);
    }
    catch (const std::exception &)
    {
        std::cerr << UNABLE_TO_OPEN_FILE << fileName << std::endl;
        return false;
    }

    return _uploadMovieRanks(retValue, movieFile);

}

/**
 * Upload movie ranks
 * @param retValue	return value
 * @param movieFile	Movie file
 * @return	true if succeeded, false otherwise
 */
bool RecommenderSystem::_uploadMovieRanks(bool retValue, std::ifstream &movieFile)
{
    std::string line = std::string();
    while (std::getline(movieFile, line))
    {
        std::istringstream str(line);
        {
            if (!_getMovieSplit(line))
            {
                retValue = false;
                break;
            }
        }
    }

    if (movieFile.peek() != EOF)
    {
        retValue = false;
    }
    movieFile.close();
    return retValue;
}

/**
 * Load user ranking
 * @param userRankPath		Movie path
 * @return				FAIL if fail, SUCCESS otherwise
 */
bool RecommenderSystem::_loadUserRanking(const std::string &fileName)
{
    bool retValue = true;
    std::ifstream rankFile;
    try
    {
        rankFile.open(fileName);
    }
    catch (const std::exception &)
    {
        std::cerr << UNABLE_TO_OPEN_FILE << fileName << std::endl;
        return false;
    }

    if (!(this->_updateUserRanking(rankFile) && rankFile.peek() != EOF))
    {
        retValue = false;
    }
    rankFile.close();
    return retValue;
}

/**
 * Update user ranking by file
 * @param infile ifstream
 */
bool RecommenderSystem::_updateUserRanking(std::ifstream &infile)
{
    int lineCount = 0;
    std::string line = std::string();
    std::vector<std::string> movieNames = std::vector<std::string>();
    while (std::getline(infile, line))
    {
        std::istringstream stringStream(line);
        if (lineCount == 0)
        {
            int count = 0;
            while (!stringStream.eof())
            {
                std::string str;
                stringStream >> str;
                if (str.empty())
                {
                    break;
                }
                if (this->movieRating.count(str) == 0)
                {
                    return false;
                }
                movieNames.resize(count + 1);
                movieNames.at(count) = str;
                ++count;
            }
        }
        else
        {
            if (!_updateRankLine(stringStream, movieNames))
            {
                return false;
            }
        }
        ++lineCount;
    }
    this->movies = movieNames;
    return true;
}

/**
 * Update rank line
 * @param lineCount		Line count
 * @param line			string
 * @param names			movie names
 */
bool RecommenderSystem::_updateRankLine(std::istringstream &stringStream,
                                        std::vector<std::string> const &movieNames)
{
    std::pair<std::string, double> movieRate;
    std::pair<std::string, std::unordered_map<std::string, double>> oneUserRank;
    int count = 0;
    while (!stringStream.eof())
    {
        if (count == 0)
        {
            stringStream >> oneUserRank.first;
        }
        else
        {
            std::string str;
            stringStream >> str;
            if (str.empty())
            {
                break;
            }
            movieRate.first = movieNames.at(count - 1);
            if (str != NONE)
            {
                try
                {
                    movieRate.second = stod(str);
                }
                catch (const std::invalid_argument &)
                {
                    return false;
                }
            }
            else
            {
                movieRate.second = 0;
            }
            oneUserRank.second.insert(movieRate);
        }
        count++;
    }
    this->userRating.insert(oneUserRank);
    return true;
}

/**
 * @brief predict movie score for user with result double
 * @param movieName     movie name
 * @param userName      user name
 * @param k             number
 * @return              Movie score for user
 */
double RecommenderSystem::_predictUserScoreDouble(const std::string &movieName,
                                                  const std::string &userName, int k)
{
    std::map<double, std::string, std::greater<>> similarMovies =
            std::map<double, std::string, std::greater<>>();
    std::vector<double> &newMovieVec = this->movieRating[movieName];
    std::unordered_map<std::string, double> &usersMap = this->userRating[userName];
    if (newMovieVec.empty() || usersMap.empty())
    {
        return FAIL;
    }
    for (const auto &p: usersMap)
    {
        if (p.second != 0)
        {
            double angle = _getAngleBetweenVectors(newMovieVec,
                                                   this->movieRating[p.first]);
            similarMovies.insert({angle, p.first});
        }
    }
    return _predictScore(std::move(similarMovies), userName, k);
}

/**
 *	Load data from files
 * @param moviePath		Movie file path
 * @param userPath		User file path
 * @return
 */
int RecommenderSystem::loadData(const std::string &moviePath, const std::string &userPath)
{
    if (!(_loadMovies(moviePath) && _loadUserRanking(userPath)))
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
std::string RecommenderSystem::recommendByContent(const std::string &userName)
{
    std::unordered_map<std::string, double> &userMap = this->userRating[userName];
    if (userMap.empty())
    {
        return USER_NOT_FOUND;
    }
    std::vector<double> prefVector = _getPreferenceVector(
            std::move(_getNormalizeUserRank(userName, _getAvg(userMap))));
    return _getSuggestedMovie(std::move(prefVector), std::move(userMap));
}

/**
 *	Predict movie score for user
 * @param movieName		Movie name
 * @param userName		User name
 * @param k				int
 * @return				Movie score
 */
float RecommenderSystem::predictMovieScoreForUser(const std::string &movieName,
                                                  const std::string &userName, int k)
{
    return (float) _predictUserScoreDouble(movieName, userName, k);
}

/**
 * Predict score
 * @param similarMovies		Similar movies map
 * @param userName			String user map
 * @param k					int
 * @return					Score
 */
double RecommenderSystem::_predictScore(std::map<double, std::string, std::greater<>>
                                        &&similarMovies,
                                        const std::string &userName, int k)
{
    double up = 0;
    double down = 0;
    int count = 0;

    for (const auto &p :similarMovies)
    {
        if (count == k)
        {
            break;
        }
        count++;
        up += (p.first * this->userRating[userName][p.second]);
        down += p.first;
    }

    return (up / down);
}

/**
 *	Recommend by CF
 * @param userName		User name
 * @param k				K
 * @return				Recommended movie
 */
std::string RecommenderSystem::recommendByCF(const std::string &userName, int k)
{
    if (this->userRating[userName].empty())
    {
        return USER_NOT_FOUND;
    }

    return _getBestRecommendedMovie(userName, k);
}

/**
 * @brief Recommend best movie
 * @param userName      User name
 * @param k             number k
 * @return              string of best movie
 */
std::string RecommenderSystem::_getBestRecommendedMovie(const std::string &userName, int k)
{
    std::string result = std::string();
    double score = -1;
    for (size_t i = 0, size = this->movies.size(); i != size; ++i)
    {
        if (this->userRating[userName][this->movies[i]] == 0)
        {
            double predictRate = _predictUserScoreDouble(this->movies[i],
                                                         userName, k);
            if (predictRate > score)
            {
                score = predictRate;
                result = this->movies[i];
            }
        }
    }
    return result;
}

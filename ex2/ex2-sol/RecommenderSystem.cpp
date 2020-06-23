#include <fstream>
#include <iostream>
#include <sstream>
#include "RecommenderSystem.h"

#define USER_NOT_FOUND "USER NOT FOUND"
#define UNABLE_TO_OPEN_FILE "Unable to open file %s"
#define SPACE ' '

std::vector<std::string> splitString(std::string& str)
{
	size_t pos = 0;
	std::string subStr;
	std::string name;
	std::vector<std::string> result;

	name = str.substr(0, pos);
	result.push_back(subStr);
	str.erase(0, pos + 1);

	while ((pos = str.find(SPACE)) != std::string::npos)
	{
		subStr = str.substr(0, pos);
		result.push_back(subStr);
		str.erase(0, pos + 1);
	}
	return result;
}

int RecommenderSystem::loadData(const std::string& moviesAttributesFilePath,
	const std::string& userRanksFilePath)
{
	std::ifstream moviesFile(moviesAttributesFilePath);
	std::string line;
	while (std::getline(moviesFile, line))
	{
		std::vector<std::string> splitLine = splitString(line);
		std::string name = splitLine.at(0);
		splitLine.erase(splitLine.begin());
		this->movieRating[name] = splitLine;
	}

	std::ifstream rankFile(userRanksFilePath);

	return 0;
}
std::string RecommenderSystem::recommendByContent(std::string userName)
{
	return std::string();
}
int RecommenderSystem::predictMovieScoreForUser(std::string movieName, std::string userName, int k)
{
	return 0;
}
std::string RecommenderSystem::recommendByCF(std::string userName, int k)
{
	return std::string();
}

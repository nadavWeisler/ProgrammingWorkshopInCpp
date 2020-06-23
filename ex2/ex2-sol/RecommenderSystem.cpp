#include <fstream>
#include <iostream>
#include <sstream>
#include "RecommenderSystem.h"

#define USER_NOT_FOUND "USER NOT FOUND"
#define UNABLE_TO_OPEN_FILE "Unable to open file %s"
#define SPACE ' '
#define NONE "NA"

RecommenderSystem::RecommenderSystem()
{
	this->movieRating = std::unordered_map<std::string, std::unordered_map<std::string, int>>();
	this->userRating = std::multimap<std::string, std::pair<std::string, int>>();
}

std::pair<std::string, std::unordered_map<std::string, int>> getMovieSplit(std::string& str)
{
	size_t pos = 0;
	std::string subStr;
	std::string name;
	std::pair<std::string, std::unordered_map<std::string, int>> result;

	name = str.substr(0, pos);
	result.first = name;
	result.second = std::unordered_map<std::string, int>();
	str.erase(0, pos + 1);

	while ((pos = str.find(SPACE)) != std::string::npos)
	{
		subStr = str.substr(0, pos);
		result.second.insert({name, std::stoi(subStr)});
		str.erase(0, pos + 1);
	}

	return result;
}

std::pair<std::string, std::pair<std::string, int>> getRankSplit(std::string& str,
	std::vector<std::string> movies)
{
	size_t pos = 0;
	std::string subStr;
	std::string name;

	std::pair<std::string, std::pair<std::string, int>> result =
		std::pair<std::string, std::pair<std::string, int>>();
	int count = 0;
	while ((pos = str.find(SPACE)) != std::string::npos)
	{
		subStr = str.substr(0, pos);
		result.second.insert({name, std::stoi(subStr)});
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
		this->movieRating.insert(getMovieSplit(line));
	}

	std::ifstream rankFile(userRanksFilePath);
	while (std::getline(moviesFile, line))
	{
		this->userRating.insert(getRankSplit(line));
		this->movieRating.insert(getMovieSplit(line));
	}

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

#include "RecommenderSystem.h"

#define USER_NOT_FOUND "USER NOT FOUND"
#define UNABLE_TO_OPEN_FILE "Unable to open file %s"


int RecommenderSystem::loadData(std::string moviesAttributesFilePath, std::string userRanksFilePath)
{
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

#ifndef EX2_SOL__RECOMMENDERSYSTEM_H_
#define EX2_SOL__RECOMMENDERSYSTEM_H_

#include <string>
class RecommenderSystem
{
 private:
	int x;

 public:
	int loadData(std::string moviesAttributesFilePath, std::string userRanksFilePath);

	std::string recommendByContent(std::string userName);

	int predictMovieScoreForUser(std::string movieName, std::string userName, int k);

	std::string recommendByCF(std::string userName, int k);
};

#endif //EX2_SOL__RECOMMENDERSYSTEM_H_

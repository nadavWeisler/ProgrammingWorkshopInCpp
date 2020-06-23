#ifndef EX2_SOL__RECOMMENDERSYSTEM_H_
#define EX2_SOL__RECOMMENDERSYSTEM_H_

#include <string>
#include <map>
#include <unordered_map>
#include <vector>
#include <list>
class RecommenderSystem
{
 private:
	/**
	 *
	 */
	std::multimap<std::string, std::pair<std::string, int>> userRating;

	/**
	 *
	 */
	std::unordered_map<std::string, std::map<std::string, int>> movieRating;

 public:
	/**
	 *
	 * @param moviesAttributesFilePath
	 * @param userRanksFilePath
	 * @return
	 */
	int loadData(const std::string& moviesAttributesFilePath, const std::string& userRanksFilePath);

	/**
	 *
	 * @param userName
	 * @return
	 */
	std::string recommendByContent(std::string userName);

	/**
	 *
	 * @param movieName
	 * @param userName
	 * @param k
	 * @return
	 */
	int predictMovieScoreForUser(std::string movieName, std::string userName, int k);

	/**
	 *
	 * @param userName
	 * @param k
	 * @return
	 */
	std::string recommendByCF(std::string userName, int k);
};

#endif //EX2_SOL__RECOMMENDERSYSTEM_H_

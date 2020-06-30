#ifndef EX2_SOL__RECOMMENDERSYSTEM_H_
#define EX2_SOL__RECOMMENDERSYSTEM_H_

#include <string>
#include <map>
#include <unordered_map>
#include <vector>
#include <list>

/**
 * Recommender system class
 */
class RecommenderSystem
{
private:
    /**
     *	User rating unordered map
     */
    std::map<std::string, std::map<std::string, double>> userRating;

    /**
     *	Movie rating unordered m
     */
    std::map<std::string, std::vector<double>> movieRating;

    /**
     * @brief Movie names
     */
    std::vector<std::string> movies;

    /**
     *	Get average
     * @param mapHash Calculate average
     * @return	Average
     */
    static double _getAvg(const std::map<std::string, double> &mapHash);

    /**
     *	Normalize user rank
     * @param userName	User name
     * @param avg		Average
     */
    std::map<std::string, double> _getNormalizeUserRank(const std::string &userName, double avg);

    /**
     * Get preference vector of user ranks
     * @param userRanks
     * @return
     */
    std::vector<double> _getPreferenceVector(const std::map<std::string, double> &userRanks);

    /**
     *	Get movie split
     * @param line	String
     * @return		string and double vector pair
     */
    bool _getMovieSplit(std::string &line);

    /**
     *	Multiply vector with scalar
     * @param vec		Vector
     * @param scalar	Scalar
     * @return			double vector
     */
    static std::vector<double>
    _multiplyVectorInScalar(const std::vector<double> &vec, double scalar);

    /**
     *	Return sum of two vectors
     * @param vec1		Vector
     * @param vec2		Vector
     * @return			Vector sum
     */
    static std::vector<double>
    _addVectorToAnother(std::vector<double> &vec1, const std::vector<double> &vec2);

    /**
     * Get suggested movie from preference vector user rank
     * @param preferenceVector
     * @param userMap
     * @return
     */
    std::string _getSuggestedMovie(const std::vector<double> &preferenceVector,
                                   const std::map<std::string, double> &userMap);

    /**
     * Predict score
     * @param similarMovies		Similar movies map
     * @param userName			String user map
     * @param k					int
     * @return					Score
     */
    double _predictScore(std::map<double, std::string, std::greater<>> &similarMovies,
                         const std::string &userName, int k);

    /**
     * Get angle between 2 vectors
     * @param vector1 			vector1
     * @param vector2			Movie vector
     * @return					Angle between 2 vectors
     */
    static double _getAngleBetweenVectors(const std::vector<double> &vector1,
                                          const std::vector<double> &vector2);

    /**
     * Get scalar multiplications between two vectors
     * @param vector1 		Vector1
     * @param vector2 		Vector2
     * @return				Scalar multiplication
     */
    static double
    _getScalarMultiplication(std::vector<double> vector1, std::vector<double> vector2);

    /**
     * Get norm of vector
     * @param vec	Vector
     * @return		Vector norm
     */
    static double _getNorm(const std::vector<double> &vec);

    /**
     * Load movies
     * @param moviePath		Movie file path
     * @return				FAIL if fail, SUCCESS otherwise
     */
    bool _loadMovies(const std::string &fileName);

    /**
     * Load user ranking
     * @param userRankPath		Movie path
     * @return				FAIL if fail, SUCCESS otherwise
     */
    bool _loadUserRanking(const std::string &fileName);

    /**
    * Update rank line
    * @param lineCount		Line count
    * @param line			string
    * @param names			movie names
    */
    bool
    _updateRankLine(std::istringstream &stringStream, std::vector<std::string> const &movieNames);

    /**
     * Update user ranking by file
     * @param infile ifstream
     */
    bool _updateUserRanking(std::ifstream &infile);

    /**
     * Upload movie ranks
     * @param retValue	return value
     * @param movieFile	Movie file
     * @return	true if succeeded, false otherwise
     */
    bool _uploadMovieRanks(bool retValue, std::ifstream &movieFile);

    /**
     * @brief predict movie score for user with result double
     * @param movieName     movie name
     * @param userName      user name
     * @param k             number
     * @return              Movie score for user
     */
    double _predictUserScoreDouble(const std::string &movieName, const std::string &userName,
                                  int k);

public:
    /**
     * Basic constructor
     */
    RecommenderSystem();

    /**
     *	Load data from files
     * @param moviePath		Movie file path
     * @param userPath		User file path
     * @return
     */
    int loadData(const std::string &moviePath, const std::string &userPath);

    /**
     *	Recommend to user by content
     * @param userName		User name
     * @return				Recommended movie
     */
    std::string recommendByContent(const std::string &userName);

    /**
     *	Predict movie score for user
     * @param movieName		Movie name
     * @param userName		User name
     * @param k				int
     * @return				Movie score
     */
    float predictMovieScoreForUser(const std::string &movieName,
                                   const std::string &userName, int k);

    /**
     *	Recommend by CF
     * @param userName		User name
     * @param k				K
     * @return				Recommended movie
     */
    std::string recommendByCF(const std::string &userName, int k);
};

#endif

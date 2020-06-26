#ifndef EX2_SOL__RECOMMENDERSYSTEM_H_
#define EX2_SOL__RECOMMENDERSYSTEM_H_

#include <string>
#include <map>
#include <unordered_map>
#include <vector>
#include <list>
using namespace std;

/**
 * Recommender system class
 */
class RecommenderSystem
{
 private:
	/**
	 *	User rating unordered map
	 */
	unordered_map<string, unordered_map<string, double>> userRating;

	/**
	 *	Movie rating unordered m
	 */
	unordered_map<string, vector<double>> movieRating;

	/**
	 *	Get average
	 * @param unorderedMap Calculate average
	 * @return	Average
	 */
	static double _getAvg(const unordered_map<string, double>& unorderedMap);

	/**
	 *	Normalize user rank
	 * @param userName	User name
	 * @param avg		Average
	 */
	void _normalizeUserRank(const string& userName, double avg);

	/**
	 * Get preference vector of user ranks
	 * @param userRanks
	 * @return
	 */
	vector<double> _getPreferenceVector(const unordered_map<string, double>& userRanks);

	/**
	 *	Get movie split
	 * @param str	String
	 * @return		string and double vector pair
	 */
	static pair<string, vector<double>> _getMovieSplit(string& str);

	/**
	 *	Multiply vector with scalar
	 * @param vec		Vector
	 * @param scalar	Scalar
	 * @return			double vector
	 */
	static vector<double> _multiplyVectorInScalar(const vector<double>& vec, double scalar);

	/**
	 *	Return sum of two vectors
	 * @param vec1		Vector
	 * @param vec2		Vector
	 * @return			Vector sum
	 */
	static vector<double> _addVectorToAnother(vector<double> vec1, const vector<double>& vec2);

	/**
	 * Get suggested movie from preference vector user rank
	 * @param preferenceVector
	 * @param userMap
	 * @return
	 */
	string _getSuggestedMovie(const vector<double>& preferenceVector, const unordered_map<string, double>& userMap);

	/**
	 * Predict score
	 * @param similarMovies		Similar movies map
	 * @param userName			String user map
	 * @param k					int
	 * @return					Score
	 */
	double _predictScore(unordered_map<double, string>& similarMovies, const string& userName, int k);

	/**
	 * Get first best movie
	 * @param bestMovies	Best movies vector
	 * @return				Best movie string
	 */
	string _getFirstMovie(vector<string>& bestMovies);

	/**
	 * Get movie
	 * @param moviesRate	Movie rate
	 * @return				Movie name
	 */
	string _getMovie(unordered_map<double, vector<string>> moviesRate);

	/**
	 * Get angle between 2 vectors
	 * @param vector1 			vector1
	 * @param vector2			Movie vector
	 * @return					Angle between 2 vectors
	 */
	static double _getAngleBetweenVectors(const vector<double>& vector1, const vector<double>& vector2);

	/**
	 * Get scalar multiplications between two vectors
	 * @param vector1 		Vector1
	 * @param vector2 		Vector2
	 * @return				Scalar multiplication
	 */
	static double _getScalarMultiplication(vector<double> vector1, vector<double> vector2);

	/**
	 * Get norm of vector
	 * @param vec	Vector
	 * @return		Vector norm
	 */
	static double _getNorm(const vector<double>& vec);

	/**
	 * Load movies
	 * @param moviePath		Movie file path
	 * @return				FAIL if fail, SUCCESS otherwise
	 */
	int _loadMovies(const string& moviePath);

	/**
	 * Load user ranking
	 * @param moviePath		Movie path
	 * @return				FAIL if fail, SUCCESS otherwise
	 */
	int _loadUserRanking(const string& moviePath);

	/**
	 * Add line to unordered map
	 * @param movie				Movie
	 * @param input				string
	 * @param movieIndex		Movie index
	 * @param moviesNames		Movie names
	 */
	static unordered_map<string, double> _addLineToMap(unordered_map<string, double> movie,	const string& input, int movieIndex, vector<string>& moviesNames);

	/**
	* Update rank line
	* @param lineCount		Line count
	* @param line			string
	* @param names			movie names
	*/
	void _updateRankLine(int lineCount, const string& line, vector<string>& names);

	/**
	 * Update user ranking by file
	 * @param infile ifstream
	 */
	void _updateUserRanking(ifstream& infile);

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
	int loadData(const string& moviePath, const string& userPath);

	/**
	 *	Recommend to user by content
	 * @param userName		User name
	 * @return				Recommended movie
	 */
	string recommendByContent(const string& userName);

	/**
	 *	Predict movie score for user
	 * @param movieName		Movie name
	 * @param userName		User name
	 * @param k				int
	 * @return				Movie score
	 */
	double predictMovieScoreForUser(const string& movieName, const string& userName, int k);

	/**
	 *	Recommend by CF
	 * @param userName		User name
	 * @param k				K
	 * @return				Recommended movie
	 */
	string recommendByCF(const string& userName, int k);
};

#endif

#include <iostream>
#include <stack>
#include <algorithm>
#include <sstream>

class RPN {
	private:
	    std::stack<std::string> operations;

		// RPN();
	public:
		RPN(char** av);
		// RPN(const RPN& other);
		// ~RPN();
		const RPN&		operator=(const RPN& other);
		void			parseAndValidate(char** av);
		long long int	calculate(long long int a, long long int b, char op);
		void			RPNcalculator();
};
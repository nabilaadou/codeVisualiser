#include "RPN.hpp"

RPN::RPN(char** av) {
	parseAndValidate(av);
	RPNcalculator();
}

void	RPN::parseAndValidate(char** av) {
    std::stack<std::string> operationStack;
	std::stack<std::string>	tempStack;
    std::string				expression(av[1]);
    std::stringstream		ss(expression);
    std::string				token;
    
    while (ss >> token) {
        tempStack.push(token);
    }
	
	while (!tempStack.empty()) {
        std::string arg = tempStack.top();
        tempStack.pop();
        
        if (arg == "+" || arg == "-" || arg == "*" || arg == "/") {
            operationStack.push(arg);
        } 
        else {
			std::stringstream numCheck(arg);
            double value;
            
            if (numCheck >> value && numCheck.eof()) {
                operationStack.push(arg);
            } else {
                throw std::invalid_argument("Error: Invalid token '" + arg + "'. Must be a number or one of '+', '-', '*', '/'.");
            }
        }
    }
	this->operations = operationStack;
}	

long long int	RPN::calculate(long long int a, long long int b, char op) {
	switch (static_cast<int>(op))
	{
	case 43:
		return a + b;
	case 45:
		return a - b;
	case 42:
		return a * b;
	default:
		return a / b;
	}
}

void	RPN::RPNcalculator() {
    std::stack<long long int> numberHolder;
    int a, b;

    while (!operations.empty()) {
		std::string	token = operations.top(); operations.pop();

        if (token == "+" || token == "-" || token == "*" || token == "/") {
            if (numberHolder.size() < 2)
                throw std::invalid_argument("Error: insufficient operands for operation");       

            b = numberHolder.top();
            numberHolder.pop();
            a = numberHolder.top();
            numberHolder.pop();
            
            long long int result = calculate(a, b, token[0]);
            numberHolder.push(result);
        } else {
			std::stringstream	ss(token);
			int					value;

			ss >> value;
            numberHolder.push(value);
		}
    }
	if (numberHolder.size() != 1)
		throw std::invalid_argument("Error: syntax error");
	std::cout << numberHolder.top() << std::endl;
}
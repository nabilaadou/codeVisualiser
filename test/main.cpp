#include <iostream>
#include<iostream>
// void grah();

class Animal {
	std::string	name;
	Animal() {}
	public:
		Animal(std::string name) : name(name) {}
		std::string	getName();
};

std::string	Animal::getName() {
	return name;
}

void greet() {
	std::cout << "Hello" << std::endl;
}

void another() {
	greet();
}

int main() {
	greet();
	another();
	// grah();
	Animal a("lion");
	a.getName();
	return 0;
}
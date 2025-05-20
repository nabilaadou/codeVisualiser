CC = c++
CFLAGS =  -fsanitize=address -g3 -Wall -Wextra -Werror -std=c++98 

SRC_CPP = *.cpp
SRC_H = *.hpp

NAME = RPN

all: $(NAME)

$(NAME): $(SRC_CPP) $(SRC_H)
	$(CC) $(CFLAGS) $(SRC_CPP) -o $(NAME)

clean:
	rm -f

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
all:
	sudo docker compose up -d --build

re: clean all

clean:
	sudo docker compose down -v
	sudo docker kill $$(sudo docker ps -q) || true
	sudo docker rmi -f $$(sudo docker images -q) || true
	sudo docker volume prune -f
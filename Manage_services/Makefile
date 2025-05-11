
COMPOSE_FILE := docker-compose.yaml

DETACHED_SERVICES := echo_server

.DEFAULT_GOAL := up

# colors
NORMAL		=	\e[0m
PURPLE		= 	\e[1;35m

up:
	@printf "$(PURPLE) 	- Build and start the services $(NORMAL)\n"
	@ docker-compose -f $(COMPOSE_FILE) up -d

list:
	@printf "$(PURPLE) 	- List all services $(NORMAL)\n"
	@ docker-compose ps

%:
	@printf "$(PURPLE) 	- Build and start the service $(NORMAL)\n"
	@ docker-compose -f $(COMPOSE_FILE) up $@

$(DETACHED_SERVICES):
	@printf "$(PURPLE) 	- Build and start the container in detached mode $(NORMAL)\n"
	@ docker-compose -f $(COMPOSE_FILE) up $@

down:
	@printf "$(PURPLE) 	- Stop and Remove all services $(NORMAL)\n"
	@ docker-compose -f $(COMPOSE_FILE) down

clean:
	@printf "$(PURPLE) 	- Stop and Remove all services && Clean everything else :: Network, volumes, images ... $(NORMAL)\n"
	@ docker-compose -f $(COMPOSE_FILE) down -v
	@ if [ -n "$$(docker ps -q)" ]; then docker stop $$(docker ps -q); fi
	@ docker volume prune -f
	@ docker system prune -af

re: clean up

.PHONY: up ls down clean $(DETACHED_SERVICES)


d = docker
dc = docker compose
dctest = $(dc) -f compose-test.yaml

up:
	$(dc) up -d --build

test:
	$(dctest) up -d --build

test-result:

	$(d) logs twitter-test

down:
	$(dc) down

downv:
	$(dc) down -v

down-test:
	$(dctest) down

data-load:
	$(d) exec -it twitter-db pg_restore -U admin -d twitter --data-only dump/my_database.dump
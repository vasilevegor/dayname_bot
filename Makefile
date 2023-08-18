generate:
	alembic revision --m="{$(NAME)}" --autogenerate


migrate:
	alembic upgrade head


install:
	sudo apt install docker-compose \
	&& sudo usermod -aG docker $$USER \
	&& sudo service docker restart


rm:
	docker-compose stop \
	&& docker-compose rm \
	&& sudo rm -rf pgdata/

up:
	docker-compose -f docker-compose.yml up --force-recreate
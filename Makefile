build:
	docker-compose build
	docker-compose up --no-start

rebuild:
	docker-compose stop
	build
start:
	docker-compose start

stop:
	docker-compose stop

restart:
	docker-compose restart
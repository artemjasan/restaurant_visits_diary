# Run full process for the first start
first-launch: build create migrate up

# Just build the application image
build:
	docker-compose build

# Create the containers without starting them.
# Can be run before migration on the first application start.
create:
	docker-compose up --no-start

# Start the containers
up:
	docker-compose up

# Shorthand to build and run the application without migration
build-up: build up

# Migrate the database
migrate:
	docker-compose run --rm web python restaurant_visits_diary/manage.py migrate
	docker-compose stop

# Create migrations
makemigrations:
	docker-compose run --rm web python restaurant_visits_diary/manage.py makemigrations
	docker-compose stop

# Run the testing
.PHONY: test
test:
	docker-compose run --rm web pytest
	docker-compose stop

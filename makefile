FRONTEND_DIR=frontend
BACKEND_DIR=backend

FRONTEND_RUN_CMD=cd $(FRONTEND_DIR) && npm start
BACKEND_RUN_CMD=cd $(BACKEND_DIR) && python manage.py runserver

.PHONY: frontend backend local

# run frontend locally
frontend:
	$(FRONTEND_RUN_CMD)

# run backend locally
backend:
	$(BACKEND_RUN_CMD)

# make migrations
migrations:
	cd $(BACKEND_DIR) && python manage.py makemigrations

# migrate
migrate:
	cd $(BACKEND_DIR) && python manage.py migrate

# run frontend and backend locally
local:
	$(FRONTEND_RUN_CMD) & $(BACKEND_RUN_CMD)

static:
	cd $(BACKEND_DIR) && python manage.py collectstatic

build:
	cd $(FRONTEND_DIR) && npm run build

test:
	cd $(BACKEND_DIR) && python manage.py test

dependencies:
	cd $(FRONTEND_DIR) && npm i && cd .. && \
	pip install -r requirements.txt

test:
	cd $(BACKEND_DIR) && python manage.py test

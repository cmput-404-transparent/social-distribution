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

# run frontend and backend locally
local:
	$(FRONTEND_RUN_CMD) & $(BACKEND_RUN_CMD)

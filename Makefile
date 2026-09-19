up:
	docker compose up --build
down:
	docker compose down -v
python-test:
	cd python-evals && pytest -q
java-test:
	cd java-evaluator && mvn test

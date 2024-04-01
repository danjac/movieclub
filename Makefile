install: pyinstall npminstall precommitinstall

dbinstall: migrate fixtures

update: pyupdate npmupdate precommitupdate

pyinstall:
	uv venv && source .venv/bin/activate
	uv pip install -r requirements-ci.txt

pydeps:
	uv pip compile pyproject.toml --upgrade -o requirements.txt
	uv pip compile pyproject.toml --upgrade --extra dev -o requirements-ci.txt

pysync:
	uv pip sync requirements-ci.txt

pyupdate: pydeps pysync


npminstall:
	npm ci

npmupdate:
	npm run check-updates && npm install

precommitinstall:
	pre-commit install

precommitupdate:
	pre-commit autoupdate

nltkdownload:
	xargs -I{} python -c "import nltk; nltk.download('{}')" < nltk.txt

migrate:
	python ./manage.py migrate

fixtures:
	python ./manage.py loaddata ./movieclub/users/fixtures/users.json.gz

serve:
	python ./manage.py runserver

rq:
	python ./manage.py rqworker default

shell:
	python ./manage.py shell_plus

build:
	npm run build

watch:
	npm run watch

test:
	python -m pytest

clean:
	git clean -Xdf

podbuild:
	podman play kube podman-kube.yml

podstart:
	podman pod start movieclub-pod

podstop:
	podman pod stop movieclub-pod

podclean:
	podman pod rm movieclub-pod
	podman volume rm movieclub_pg_data

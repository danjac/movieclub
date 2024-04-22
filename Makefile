install: pyinstall npminstall precommitinstall

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
	npm run check-updates && npm install npm-update-all

precommitinstall:
	pre-commit install

precommitupdate:
	pre-commit autoupdate

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

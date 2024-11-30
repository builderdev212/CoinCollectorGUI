CONTAINER_IMG := localhost/ccgui:latest
CONTAINER_DEV_IMG := localhost/ccgui-dev:latest
CONTAINER_FILE := Containerfile
CONTAINER_DEV_FILE := Containerfile-dev

build::
	@podman build -f ${CONTAINER_FILE} -t ${CONTAINER_IMG} "${PWD}"

build-dev::
	@podman build -f ${CONTAINER_DEV_FILE} -t ${CONTAINER_DEV_IMG} "${PWD}"

run::
	@podman run -it --rm \
	    -e DISPLAY \
	    -v "/tmp/.X11-unix":"/tmp/.X11-unix" \
	    -v "${XAUTHORITY}":"/root/.Xauthority" \
	    -v "${PWD}/src":"/usr/src/ccgui/" \
	    --ipc host \
	    ${CONTAINER_IMG}

run-dev::
	@podman run -it --rm \
	    -e DISPLAY \
	    -v "/tmp/.X11-unix":"/tmp/.X11-unix" \
	    -v "${XAUTHORITY}":"/root/.Xauthority" \
	    -v "${PWD}":"/usr/src/ccgui/" \
	    --ipc host \
	    ${CONTAINER_DEV_IMG}

clean::
	@find . -type d -name "*.venv" -exec echo {} + -exec rm -rf {} +
	@find . -type d -name "*__pycache__" -exec echo {} + -exec rm -rf {} +
	@find . -name "*.db" -exec echo {} + -exec rm -rf {} +
	@find . -name "*.db-journal" -exec echo {} + -exec rm -rf {} +
	@find . -name "*.log" -exec echo {} + -exec rm -rf {} +

format::
	@python -m black src/

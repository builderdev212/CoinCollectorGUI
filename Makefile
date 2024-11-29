CONTAINER_IMG := localhost/ccgui:latest
CONTAINER_FILE := Containerfile

build::
	@podman build -f ${CONTAINER_FILE} -t ${CONTAINER_IMG} "${PWD}"

# publish::
# 	@podman login
# 	@podman push ${CONTAINER_IMG}:latest

run::
	@podman run -it --rm \
	    -e DISPLAY \
	    -v "/tmp/.X11-unix":"/tmp/.X11-unix" \
	    -v "${XAUTHORITY}":"/root/.Xauthority" \
	    -v "${PWD}":"/usr/src/ccgui/" \
	    --ipc host \
	    ${CONTAINER_IMG}

clean::
	@find . -type d -name "*.venv" -exec echo {} + -exec rm -rf {} +
	@find . -type d -name "*__pycache__" -exec echo {} + -exec rm -rf {} +
	@find . -name "*.db" -exec echo {} + -exec rm -rf {} +

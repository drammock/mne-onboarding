SHELL = bash
PORT = 8888

default:
	echo No default recipe. Current recipes are: clean

start:
	@trap ctrl_c INT
	@ctrl_c () { kill %1 }  # stop the Jupyter server when done
	@export JUPYTER_BASE_URL="http://localhost:$(PORT)" ;\
	export JUPYTER_TOKEN="foo" ;\
	jupyter server --IdentityProvider.token="$(JUPYTER_TOKEN)" --ServerApp.port="$(PORT)" & \
	sleep 1 ;\
	myst start --execute

clean:
	rm -rf .ipynb_checkpoints
	rm -rf _build
	rm -rf __pycache__
	rm -f optimization/profile_output.lprof
	rm -f optimization/profile_output*.txt
	rm -f optimization/mprofile_*.dat
	killall -q jupyter-server || true

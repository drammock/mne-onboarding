PORT=8888
export JUPYTER_BASE_URL="http://localhost:${PORT}"
export JUPYTER_TOKEN="foo"
jupyter server --IdentityProvider.token="${JUPYTER_TOKEN}" --ServerApp.port="${PORT}" &
myst start --execute && echo "killing Jupyter server"
# kill %1  # run manually, to stop the Jupyter server when done

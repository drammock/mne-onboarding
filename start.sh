trap ctrl_c INT

ctrl_c () {
    kill %1  # stop the Jupyter server when done
}

PORT=8888
export JUPYTER_BASE_URL="http://localhost:${PORT}"
export JUPYTER_TOKEN="foo"
jupyter server --IdentityProvider.token="${JUPYTER_TOKEN}" --ServerApp.port="${PORT}" &
myst start --execute

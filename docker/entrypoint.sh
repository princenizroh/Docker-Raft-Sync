#!/usr/bin/env sh
#
# Entrypoint for distributed node container.
# Chooses which Python module to run based on $NODE_ROLE and forwards common env args.
#
# Usage:
#   NODE_ROLE=lock NODE_ID=node-1 NODE_HOST=0.0.0.0 NODE_PORT=5000 CLUSTER_NODES="node-1:host:5000,..." ENABLE_HTTP_API=true \
#     /app/entrypoint.sh
#
# This script is intentionally small and POSIX-compatible so it works in minimal images.

set -eu

# Helper: print to stderr
log() {
    printf '%s\n' "$*" >&2
}

# Normalize boolean-ish env
is_true() {
    case "${1:-}" in
        1|true|True|TRUE|yes|YES) return 0 ;;
        *) return 1 ;;
    esac
}

# Defaults (if not provided)
: "${NODE_ROLE:=base}"
: "${NODE_ID:=node-1}"
: "${NODE_HOST:=0.0.0.0}"
: "${NODE_PORT:=5000}"
: "${CLUSTER_NODES:=}"
: "${ENABLE_HTTP_API:=false}"
: "${API_HOST:=0.0.0.0}"
: "${API_PORT:=6000}"

# Allow a user-provided PYTHON to override, otherwise use 'python' on PATH
: "${PYTHON:=python}"

log "[entrypoint] role=${NODE_ROLE} id=${NODE_ID} host=${NODE_HOST} port=${NODE_PORT}"
if [ -n "${CLUSTER_NODES}" ]; then
    log "[entrypoint] cluster_nodes=${CLUSTER_NODES}"
else
    log "[entrypoint] CLUSTER_NODES is empty; node will start in standalone/cluster-less mode"
fi

# Choose module to run based on NODE_ROLE
case "${NODE_ROLE}" in
    lock|lock_manager|lock-node)
        MODULE="src.nodes.lock_manager"
        ;;
    queue|queue_node|queue-node)
        MODULE="src.nodes.queue_node"
        ;;
    cache|cache_node|cache-node)
        MODULE="src.nodes.cache_node"
        ;;
    base|base_node|default)
        MODULE="src.nodes.base_node"
        ;;
    *)
        log "[entrypoint] WARNING: Unrecognized NODE_ROLE='${NODE_ROLE}', falling back to base node"
        MODULE="src.nodes.base_node"
        ;;
esac

# Build command arguments
set -- "${PYTHON}" "-m" "${MODULE}" \
    "--node-id" "${NODE_ID}" \
    "--host" "${NODE_HOST}" \
    "--port" "${NODE_PORT}"

# Some modules expect a single comma-separated --cluster-nodes argument
if [ -n "${CLUSTER_NODES}" ]; then
    set -- "$@" "--cluster-nodes" "${CLUSTER_NODES}"
fi

# If user requested HTTP API, pass the flag and export API env vars so the server can pick them up
if is_true "${ENABLE_HTTP_API}"; then
    log "[entrypoint] Enabling HTTP API (API_HOST=${API_HOST} API_PORT=${API_PORT})"
    export API_HOST API_PORT
    set -- "$@" "--enable-http-api"
fi

# Append any extra user-specified args passed to the container (docker run ... CMD/ARGS)
# If the container CMD includes arguments they will be appended to the python invocation.
# Note: "$@" currently contains the python command - we will exec it directly below.
log "[entrypoint] Exec: $*"

# Replace shell with the python process
exec "$@"

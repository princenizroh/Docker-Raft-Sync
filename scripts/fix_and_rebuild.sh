#!/usr/bin/env bash
# Helper script to convert CRLF -> LF for Docker entrypoint(s) and rebuild docker-compose.
# Usage: ./scripts/fix_and_rebuild.sh
set -euo pipefail

log() {
    printf '%s\n' "$*" >&2
}

die() {
    log "ERROR: $*"
    exit 1
}

# Resolve repo root (script lives in Tugas-individu/scripts)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Files/dirs to sanitize (relative to repo root)
DOCKER_DIR="$REPO_ROOT/docker"
ENTRYPOINT="$DOCKER_DIR/entrypoint.sh"

# Detect compose command (prefer `docker compose` over legacy `docker-compose`)
if command -v docker >/dev/null 2>&1; then
    if docker compose version >/dev/null 2>&1; then
        COMPOSE_CMD="docker compose"
    elif command -v docker-compose >/dev/null 2>&1; then
        COMPOSE_CMD="docker-compose"
    else
        COMPOSE_CMD="docker compose" # let the call fail later with informative message
    fi
elif command -v docker-compose >/dev/null 2>&1; then
    COMPOSE_CMD="docker-compose"
else
    die "Neither 'docker' nor 'docker-compose' found in PATH. Install Docker and Docker Compose."
fi

log "Repository root: $REPO_ROOT"
log "Docker dir: $DOCKER_DIR"
log "Using compose command: $COMPOSE_CMD"

# Ensure docker dir exists
if [ ! -d "$DOCKER_DIR" ]; then
    die "Docker directory not found at: $DOCKER_DIR"
fi

# Convert a file from CRLF -> LF using available tool (dos2unix or perl)
convert_file_if_crlf() {
    local file="$1"
    if [ ! -f "$file" ]; then
        log "Skipping non-existent file: $file"
        return 0
    fi

    # Detect CRLF (search for CR characters)
    if grep -q $'\r' "$file"; then
        log "CRLF line endings detected in: $file"
        if command -v dos2unix >/dev/null 2>&1; then
            log "Converting with dos2unix..."
            dos2unix "$file"
        else
            log "dos2unix not found, falling back to perl conversion..."
            perl -pi -e 's/\r\n/\n/g' "$file"
        fi
        log "Converted to LF: $file"
    else
        log "No CRLF found in: $file"
    fi

    # Ensure executable permission for shell scripts
    if [ "${file##*.}" = "sh" ] || head -c 2 "$file" | grep -q "^#\!"; then
        chmod +x "$file" || true
    fi
}

# Sanitize entrypoint specifically (most important)
convert_file_if_crlf "$ENTRYPOINT"

# Sanitize all .sh files and common Docker scripts under docker/
find "$DOCKER_DIR" -type f \( -name "*.sh" -o -name "entrypoint.*" \) -print0 |
    while IFS= read -r -d '' f; do
        convert_file_if_crlf "$f"
    done

# Also sanitize any other obvious script files in repo/docker (optional)
# (keeps script robust if other files had CRLF)
find "$DOCKER_DIR" -type f -maxdepth 2 -print0 |
    while IFS= read -r -d '' f; do
        # Only run quick check on files under docker (not binary files)
        case "$f" in
            *.sh|*entrypoint*|*.env|Dockerfile*|*.yml|*.yaml)
                convert_file_if_crlf "$f" || true
                ;;
            *) ;;
        esac
    done

# Rebuild images and bring up compose stack (no-cache to ensure fresh copy)
cd "$DOCKER_DIR"

log "Building images (no cache)..."
# Use eval so COMPOSE_CMD with space works (e.g. "docker compose")
if ! eval "$COMPOSE_CMD build --no-cache"; then
    die "Compose build failed. See output above."
fi

log "Bringing up services (force recreate, detached)..."
if ! eval "$COMPOSE_CMD up -d --force-recreate"; then
    die "Compose up failed. See output above."
fi

log "Waiting a few seconds for services to initialize..."
sleep 3

log "Done. Recommended next checks:"
log "  $COMPOSE_CMD ps"
log "  $COMPOSE_CMD logs --no-color --tail=200"
log "Verify HTTP APIs:"
log "  curl -sS http://127.0.0.1:6000/status | jq . || true"
log "  curl -sS http://127.0.0.1:6010/status | jq . || true"
log "  curl -sS http://127.0.0.1:6020/status | jq . || true"

exit 0

#!/bin/bash

set -e

MIN_PY_V=3.9
MAX_PY_V=3.11
VENV_PATH="venv"

# Icons
ICON_START="▶"
ICON_STOP="■"
ICON_SETUP="◆"
ICON_RUN="●"
ICON_AUTH="◉"
ICON_DOWNLOAD="↓"
ICON_CLEAN="▽"
ICON_OK="✓"
ICON_ERR="✗"

# Colors
RED="\033[31m"
GREEN="\033[32m"
BLUE="\033[34m"
CYAN="\033[36m"
MAGENTA="\033[35m"
YELLOW="\033[33m"

# -------------------------

start() {
    printer -start "Starting the project..."

    # Docker
    docker compose start
    handler
}

stop() {
    printer -stop "Stopping the project..."

    # Docker
    docker compose stop
    handler
}

debug() {
    printer -setup "Starting debug..."

    # Docker
    docker builder prune -f
    docker compose down --volumes
    docker compose up -d --build
    handler
}

resolve_python() {
    for minor in $(seq $(echo $MAX_PY_V | cut -d. -f2) -1 $(echo $MIN_PY_V | cut -d. -f2)); do
        py="python3.$minor"
        if command -v "$py" &> /dev/null; then
            version=$($py -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
            if "$py" - <<EOF &>/dev/null
import sys
v = tuple(map(int, "$version".split(".")))
min_v = tuple(map(int, "$MIN_PY_V".split(".")))
max_v = tuple(map(int, "$MAX_PY_V".split(".")))
exit(not (min_v <= v <= max_v))
EOF
            then
                if "$py" -m venv /tmp/test_venv_$$ &>/dev/null; then
                    rm -rf /tmp/test_venv_$$
                    echo "$py"
                    return 0
                fi
            fi
        fi
    done

    printer -error "[Environment] No working Python found (${MIN_PY_V}–${MAX_PY_V})"
    exit 1
}

setup() {

    # Options
    TARGET="${2:--all}"

    # Environment
    if [[ "$TARGET" == "--env" || "$TARGET" == "--all" ]]; then
        printer -setup "Setting up the environment..."

        PYTHON_BIN=$(resolve_python)
        printer -setup "[Environment] Python: $PYTHON_BIN"

        if [ -d "${VENV_PATH}" ]; then
            rm -rf ${VENV_PATH}
        fi

        $PYTHON_BIN -m venv ${VENV_PATH}
        if [ ! -d "${VENV_PATH}" ]; then
            printer -error "[Environment] Failed to create virtual environment"
            exit 1
        fi

        source ${VENV_PATH}/bin/activate
        python -m pip install --upgrade pip
        python -m pip install -r notebook/requirements.txt
        deactivate
    fi

    # Docker
    if [[ "$TARGET" == "--docker" || "$TARGET" == "--all" ]]; then
        printer -setup "Setting up Docker resources..."
        docker compose down --volumes --rmi all
        docker builder prune -f
        docker compose up -d --build
    fi
    handler
}

install() {
    printer -install "Installing dependencies..."

    if [[ "$#" -lt 3 ]]; then
        usage
        exit 1
    fi

    local SERVICE="$1"
    local MANAGER="$2"
    shift 2
    local PACKAGE="$@"
    local CONTAINER_ID

    CONTAINER_ID=$(docker compose ps -q "$SERVICE")
    if [[ -z "$CONTAINER_ID" ]]; then
        printer -error "[Docker] Container $SERVICE is not running"
        exit 1
    fi

    # Docker
    case "$MANAGER" in
        pip)
            docker compose exec "$SERVICE" pip install $PACKAGE
            ;;
        npm)
            docker compose exec "$SERVICE" npm install $PACKAGE
            ;;
        yarn)
            docker compose exec "$SERVICE" yarn add $PACKAGE
            ;;
        apt)
            docker compose exec "$SERVICE" apt update && apt install -y $PACKAGE
            ;;
        *)
            usage
            ;;
    esac
    handler
}

clean() {

    # Options
    TARGET="${2:--all}"

    # Environment
    if [[ "$TARGET" == "--env" || "$TARGET" == "--all" ]]; then
        printer -clean "Cleaning the environment..."
        rm -rf ${VENV_PATH}
    fi

    # Docker
    if [[ "$TARGET" == "--docker" || "$TARGET" == "--all" ]]; then
        printer -clean "Cleaning Docker resources..."
        docker compose down --volumes --rmi all
    fi
    handler
}

usage() {
    cat <<EOF

1. Usage:
    - bash $0 <command> [options]

2. Commands:
    - [${ICON_START}] start
    - [${ICON_STOP}] stop
    - [${ICON_SETUP}] debug
    - [${ICON_SETUP}] setup --[env|docker]
    - [${ICON_SETUP}] install <container_name> <pip|npm|yarn|apt> <package>
    - [${ICON_CLEAN}] clean --[env|docker]

EOF
    exit 1
}

printer() {
    local STATUS="$1"
    local MESSAGE="$2"
    local ICON=""
    local COLOR=""
    case "$STATUS" in
        -start)
            ICON="$ICON_START"
            COLOR="$BLUE"
            ;;
        -stop)
            ICON="$ICON_STOP"
            COLOR="$RED"
            ;;
        -debug)
            ICON="$ICON_RUN"
            COLOR="$CYAN"
            ;;
        -setup)
            ICON="$ICON_SETUP"
            COLOR="$MAGENTA"
            ;;
        -install)
            ICON="$ICON_SETUP"
            COLOR="$MAGENTA"
            ;;
        -clean)
            ICON="$ICON_CLEAN"
            COLOR="$YELLOW"
            ;;
        -success)
            ICON="$ICON_OK"
            COLOR="$GREEN"
            ;;
        -error)
            ICON="$ICON_ERR"
            COLOR="$RED"
            ;;
        *)
            ICON=""
            COLOR="$RESET"
            ;;
    esac
    echo ""
    printf "%b%s %s%b\n" "$COLOR" ["$ICON"] "$MESSAGE" "$RESET"
    echo ""
}

handler() {
    if [ $? -eq 0 ]; then
        printer -success "Process completed successfully"
    else
        printer -error "An unexpected error occurred"
        exit 1
    fi
}

case $1 in
    start)
        start
        ;;
    stop)
        stop
        ;;
    debug)
        debug
        ;;
    setup)
        setup "$@"
        ;;
    install)
        shift
        install "$@"
        ;;
    clean)
        shift
        clean "$@"
        ;;
    *)
        usage
        ;;
esac

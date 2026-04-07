#!/bin/bash

PYTHON_VERSION="3.12"
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

    # Docker Ops
    docker compose start
    handler
}

stop() {
    printer -stop "Stopping the project..."

    # Docker Ops
    docker compose stop
    handler
}

debug() {
    printer -setup "Starting debug..."

    # Docker Ops
    docker builder prune -f
    docker compose down --volumes
    docker compose up -d --build
    handler
}

setup() {
    printer -setup "Setting up the project..."

    # Environment
    if [ -d "${VENV_PATH}" ]; then
        rm -rf ${VENV_PATH}
    fi

    python${PYTHON_VERSION} -m venv ${VENV_PATH}
    source ${VENV_PATH}/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    deactivate

    # Docker Ops
    docker compose down --volumes --rmi all
    docker builder prune -f
    docker compose up -d --build
    handler
}

install() {
    printer -install "Installing dependencies..."

    # Validation
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
        printer -error "Container for is not running"
        exit 1
    fi

    # Docker Ops
    case "$MANAGER" in
        pip)
            docker compose exec "$CONTAINER" pip install $PACKAGE
            ;;
        npm)
            docker compose exec "$CONTAINER" npm install $PACKAGE
            ;;
        yarn)
            docker compose exec "$CONTAINER" yarn add $PACKAGE
            ;;
        apt)
            docker compose exec "$CONTAINER" apt update && apt install -y $PACKAGE
            ;;
        *)
            usage
            ;;
    esac
    handler
}

clean() {
    printer -clean "Cleaning all..."

    # Docker Ops
    docker compose down --volumes --rmi all
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
    - [${ICON_SETUP}] setup
    - [${ICON_SETUP}] install <container_name> <pip|npm|yarn|apt> <package>
    - [${ICON_CLEAN}] clean

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

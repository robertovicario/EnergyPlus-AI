#!/bin/bash

# Variables
VENV_PATH="venv/"

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
    printer -start "Starting the app..."

    # Docker Ops
    docker-compose start
    handler
}

stop() {
    printer -stop "Stopping the app..."

    # Docker Ops
    docker-compose stop
    handler
}

debug() {
    printer -setup "Starting debug..."

    # Docker Ops
    docker-compose down --volumes
    docker-compose up -d
    handler
}

setup() {
    printer -setup "Setting up the app..."

    # Environment
    cd app
    python3 -m venv $VENV_PATH
    source $VENV_PATH/bin/activate

    # Dependencies
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    cd ..

    # Docker Ops
    docker-compose down --volumes
    docker-compose up -d --build
    handler
}

clean() {

    # Option
    OPTION=$1
    if [[ "$OPTION" != --* ]]; then
        printer -error "Invalid option: $OPTION"
        usage
    fi

    # Type
    TYPE="${OPTION#--}"
    case "$TYPE" in
        env)

            # Environment
            printer -clean "Cleaning environment..."
            if [ -d "app/$VENV_PATH" ]; then
                rm -rf "app/$VENV_PATH"
            fi
            ;;
        docker)
            printer -clean "Cleaning Docker containers, volumes and images..."
            docker-compose down --volumes --rmi all
            ;;
        all)
            printer -clean "Cleaning all..."

            # Environment
            printer -clean "Cleaning environment..."
            if [ -d "app/$VENV_PATH" ]; then
                rm -rf "app/$VENV_PATH"
            fi

            # Docker Ops
            docker-compose down --volumes --rmi all
            ;;
        *)
            usage
            ;;
    esac
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
    - [${ICON_CLEAN}] clean

3. Options:
    - [${ICON_CLEAN}] clean --env
    - [${ICON_CLEAN}] clean --docker
    - [${ICON_CLEAN}] clean --all

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
        -setup)
            ICON="$ICON_SETUP"
            COLOR="$MAGENTA"
            ;;
        -run)
            ICON="$ICON_RUN"
            COLOR="$CYAN"
            ;;
        -auth)
            ICON="$ICON_AUTH"
            COLOR="$CYAN"
            ;;
        -download)
            ICON="$ICON_DOWNLOAD"
            COLOR="$BLUE"
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
        setup
        ;;
    clean)
        shift
        clean "$@"
        ;;
    *)
        usage
        ;;
esac

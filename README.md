| <img src="docs/logo.svg" width="128"> |
| - |

# EnergyPlus AI

## Overview

This project is an application that leverages predictive _Machine Learning_ to estimate building energy consumption (EUI). It integrates a _Retrieval-Augmented Generation (RAG)_ framework to tackle complex inferential challenges and incorporates _Explainable AI (XAI)_ techniques to provide clear, interpretable insights into the model's predictions.

## Prerequisites

> [!IMPORTANT]
>
> - Docker
> - Docker Compose

## User Interface (UI)

| <a href="#"><img src="docs/cover.png" alt="UI" width="512"></a> |
| :-: |
| **Home - EnergyPlus AI** |

## Instructions

Usage:

```sh
bash cmd.sh <command> [options]
```

### `setup`

If you haven't built the project yet, you can do so by running:

```sh
bash cmd.sh setup
```

Once the setup process is complete, the project will be accessible at `localhost:8000`.

> [!WARNING]
>
> If this port is already in use, search for all occurrences of `8000` within the project and replace them with your preferred port number. After making these changes, you'll need to rebuild the project for the modifications to take effect.

### `start`

The program will run in debug mode, meaning frontend changes will be rendered upon reload. However, if you make changes to the backend, you will need to restart the program by running:

```sh
bash cmd.sh start
```

### `debug`

For development, use debug mode to enable faster and more accurate rebuilds:

```sh
bash cmd.sh debug
```

### `stop`

To stop the program, simply run:

```sh
bash cmd.sh stop
```

> [!TIP]  
> For a quicker way to stop, use `ctrl + C` to force stop the program.

### `clean`

If you want to clean the project, you can run this command using few options:

```sh
# Cleaning the environment
bash cmd.sh clean --env
```

```sh
# Cleaning the Docker resources
bash cmd.sh clean --docker
```

```sh
# Cleaning all the resources
bash cmd.sh clean --all
```

## License

This project is distributed under [GNU General Public License version 3](https://opensource.org/license/gpl-3-0). You can find the complete text of the license in the project repository.

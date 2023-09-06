# Birdie Booker <!-- omit in toc -->
This terminal-based application is a clone of [TeeTime Alerts](https://teetimealerts.io/) built using Selenium for web scraping and PushOver for sending mobile device notifications.

### Table of Contents <!-- omit in toc -->
- [Setup](#setup)
  - [Device](#device)
  - [Server](#server)
  - [Installing Dependencies](#installing-dependencies)
- [Available Commands](#available-commands)
  - [`./main.py`](#mainpy)
  - [`./main.py [-l | --list]`](#mainpy--l----list)
  - [`./main.py [-s | --scrape]`](#mainpy--s----scrape)


## Setup

### Device
1. Install [PushOver](https://pushover.net/) on your mobile device and create an account.
2. Create `.env` inside `birdie-booker` and add the following credentials associated:
    ```env
    PUSHOVER_API_KEY='secr3t'   # Birdie Booker application key
    PUSHOVER_USER_KEY='secr3t'  # User account key
    ```
    
### Server

1. Install python3 and [Chrome](https://www.google.com/chrome/) for web scraping on your machine
1. Clone the repository and cd into it.
    ```sh
    git clone https://github.com/ajtadeo/birdie-booker.git
    cd birdie-booker
    ```
3. Set up the virtual environment.
    * Create the virutal environment.
        ```sh
        conda env create -f base.yml
        ```
    * Verify that the virtual environment was created correctly.
        ```sh
        conda info --envs
        ```
    * Activate the virtual environment.
        ```sh
        conda activate bb_base
        ```
4. Add executable permissions to `main.py`.
  ```
  chmod +x main.py
  ```
5. Set up the CRON job to be run every 5 minutes.
    * It's recommended to use a dedicated machine for running CRON's. I personally use a Raspberry Pi to host this application.
    * Add `main.py -s` to the list of CRON jobs using `crontab -e`
  
        ```
        5 * * * * python3 /path/to/main.py -s > /path/to/birdie-booker/cron.log 2>&1
        ```

### Installing Dependencies
1. Update dependencies under `pip` in `base.yml`.
2. Deactivate the virtual environment if it is currently running.
    ```sh
    conda deactivate
    ```
3. Update the virtual environment. 
    * If you are removing a dependency, removing and recreating the virtual environment is necessary since `--prune` does not work as of August 9 2023. 
        ```sh
        conda remove --name bb_base --all
        conda env create -f base.yml
        ```
    * Otherwise, update the virtual environment as normal.
        ```sh
        conda env update -f base.yml
        ```
4. Verify that the virtual environment was updated correctly.
    ```sh
    conda info --envs
    ```
5. Activate the virtual environment.
    ```sh
    conda activate bb_base
    ```
6. Verify that the new dependency was added to the virtual environment.
    ```sh
    pip list --local

## Available Commands

### `./main.py`
Creates an Alert and stores it in the database.

### `./main.py [-l | --list]`
Lists the Alerts currently in the database.

### `./main.py [-s | --scrape]`
Runs the web scrapers fro all Alerts currently in the database.
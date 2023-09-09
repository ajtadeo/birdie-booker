# Birdie Booker <!-- omit in toc -->
This terminal-based application is a clone of [TeeTime Alerts](https://teetimealerts.io/) built using Selenium for web scraping and Pushover for sending mobile device notifications.

### Table of Contents <!-- omit in toc -->
- [Setup](#setup)
  - [Pushover](#pushover)
  - [Docker](#docker)
  - [Helpful Docker Commands](#helpful-docker-commands)
    - [`docker logs [container name]`](#docker-logs-container-name)
    - [`docker ps -a`](#docker-ps--a)
    - [`docker image list`](#docker-image-list)

## Setup

### Pushover
1. Go to [Pushover](https://pushover.net/) and create an account. Note the user key displayed on your account dashboard.
2. Create an application "Birdie Booker". Note the application key displayed on the application dashboard.
3. Install Pushover on your mobile device and login.
4. (Optional) In the application dashboard, create a subscription to allow multiple people to join the app. In later steps, use the group key instead of the user key.
    
### Docker
To run in the production environment, replace `compose.dev.yml` with `compose.prod.yml`

1. Clone the repository and cd into it.
    ```sh
    git clone https://github.com/ajtadeo/birdie-booker.git
    cd birdie-booker
    ```
3. Create `.env.dev` and `.env.prod`
   
   `.env.dev`
   ```env
   FLASK_APP=app/__init__.py
   FLASK_DEBUG=1
   PORT=5000
   ```

   `.env.prod`
   ```env
   FLASK_APP=app/__init__.py
   FLASK_DEBUG=0
   PORT=4000
   ```
4. Start the server.
    ```
    docker compose -f compose.dev.yml up -d
    ```
5. Open Birdie Booker in your browser
    * Dev: `[raspberry pi IP]:5000`
    * Production: `[raspberry pi IP]:4000`
6. Stop the server.
    ```
    docker compose -f compose.dev.yml down -v
    ```

### Helpful Docker Commands

#### `docker logs [container name]`
View a container's logs.

#### `docker ps -a`
List all containers, including inactive ones.

#### `docker image list`
List all images

<!-- ### Terminal (deprecated)
2. Install the latest Chrome for Testing and Chromedriver versions for your OS.
    * Download Chrome for Testing and Chromedriver from [this site](https://googlechromelabs.github.io/chrome-for-testing/) to your home directory.
    * Move `Chrome for Testing` into the same directory as `chromedriver`, should be something like `chromedriver-os`
    * Append `export PATH=/path/to/chromedriver-os` to `.bashrc`
3. Clone the repository and cd into it.
    ```sh
    git clone https://github.com/ajtadeo/birdie-booker.git
    cd birdie-booker
    ```
4. Create `.env` inside `birdie-booker` and add the following credentials:
    ```env
    PUSHOVER_API_KEY='secr3t'   # Birdie Booker application key
    PUSHOVER_USER_KEY='secr3t'  # User key or Group key if using a subscription
    CHROME_BINARY_PATH="/path/to/Google Chrome for Testing"
    CHROMEDRIVER_PATH="/path/to/chromedriver"
    ```
5. Set up the virtual environment using venv.
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     pip3 install -r requirements.txt
     ```
6. Set up the CRON job to be run every 5 minutes.
    * Create a CRON job by entering the following code in the file opened by `crontab -e`
        ```
        SHELL=/bin/bash
        BASH_ENV=~/.bashrc
        */5 * * * * cd /path/to/birdie-booker; source venv/bin/activate; python3 /path/to/birdie-booker/main.py -s > /path/to/birdie-booker/cron.log 2>&1; deactivate
        ```
    * Make sure the `*/5 * * * * ...` command is all on one line, otherwise `crontab` will complain.
    * Check that the CRON job was created using `crontab -l`

## Available Commands

### `./main.py`
Creates an Alert and stores it in the database.

### `./main.py [-l | --list]`
Lists the Alerts currently in the database.

### `./main.py [-s | --scrape]`
Runs the web scrapers fro all Alerts currently in the database. -->
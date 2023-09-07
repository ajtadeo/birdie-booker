# Birdie Booker <!-- omit in toc -->
This terminal-based application is a clone of [TeeTime Alerts](https://teetimealerts.io/) built using Selenium for web scraping and Pushover for sending mobile device notifications.

### Table of Contents <!-- omit in toc -->
- [Setup](#setup)
  - [Pushover](#pushover)
  - [Server](#server)
- [Available Commands](#available-commands)
  - [`python3 main.py`](#python3-mainpy)
  - [`python3 main.py [-l | --list]`](#python3-mainpy--l----list)
  - [`python3 main.py [-s | --scrape]`](#python3-mainpy--s----scrape)

## Setup

### Pushover
1. Go to [Pushover](https://pushover.net/) and create an account. Note the user key displayed on your account dashboard.
2. Create an application "Birdie Booker". Note the application key displayed on the application dashboard.
3. Install Pushover on your mobile device and login.
4. (Optional) In the application dashboard, create a subscription to allow multiple people to join the app. In later steps, use the group key instead of the user key.
    
### Server
1. Install Python 3.7 on your machine.
1. Clone the repository and cd into it.
    ```sh
    git clone https://github.com/ajtadeo/birdie-booker.git
    cd birdie-booker
    ```
2. Create `.env` inside `birdie-booker` and add the following credentials:
    ```env
    PUSHOVER_API_KEY='secr3t'   # Birdie Booker application key
    PUSHOVER_USER_KEY='secr3t'  # User key or Group key if using a subscription
    ```
3. Set up the virtual environment using venv.
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     pip3 install -r requirements.txt
     ```
4. Add executable permissions to `main.py`: `chmod +x main.py`
5. Set up the CRON job to be run every 5 minutes.
    * Create a CRON job by entering the following code in the file opened by `crontab -e`
        ```
        SHELL=/bin/bash
        BASH_ENV=~/.bashrc
        */5 * * * * cd /path/to/birdie-booker; source venv/bin/activate; python3 /path/to/birdie-booker/main.py -s > /path/to/birdie-booker/cron.log 2>&1; deactivate
        ```
    * Make sure the `*/5 * * * * ...` command is all on one line, otherwise `crontab` will complain.
    * Check that the CRON job was created using `crontab -l`

## Available Commands

### `python3 main.py`
Creates an Alert and stores it in the database.

### `python3 main.py [-l | --list]`
Lists the Alerts currently in the database.

### `python3 main.py [-s | --scrape]`
Runs the web scrapers fro all Alerts currently in the database.
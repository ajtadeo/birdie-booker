# Birdie Booker <!-- omit in toc -->
This terminal-based application is a clone of [TeeTime Alerts](https://teetimealerts.io/) built using Selenium for web scraping and Pushover for sending mobile device notifications.

### Table of Contents <!-- omit in toc -->
- [Setup](#setup)
  - [Pushover](#pushover)
  - [Server](#server)
  - [Installing Dependencies](#installing-dependencies)
- [Available Commands](#available-commands)
  - [`./main.py`](#mainpy)
  - [`./main.py [-l | --list]`](#mainpy--l----list)
  - [`./main.py [-s | --scrape]`](#mainpy--s----scrape)


## Setup

### Pushover
1. Go to [Pushover](https://pushover.net/) and create an account. Note the user key displayed on your account dashboard.
2. Create an application "Birdie Booker". Note the application key displayed on the application dashboard.
3. Install Pushover on your mobile device and login.
4. (Optional) In the application dashboard, create a subscription to allow multiple people to join the app. In later steps, use the group key instead of the user key.
    
### Server
1. Install python3 and [Chrome](https://www.google.com/chrome/) for web scraping on your machine
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
4. Add executable permissions to `main.py`: `chmod +x main.py`
5. Set up the CRON job to be run every 5 minutes.
    * Open `~/.bashrc`. If there is no conda initialization, copy the following code and fill in the paths to Anaconda/Miniconda on your machine

        ```sh
        # >>> conda initialize >>>
        # !! Contents within this block are managed by 'conda init' !!
        __conda_setup="$('"/path/to/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
        if [ $? -eq 0 ]; then
            eval "$__conda_setup"
        else
            if [ -f "/path/to/miniconda3/etc/profile.d/conda.sh" ]; then
                . "/path/to/miniconda3/etc/profile.d/conda.sh"
            else
                export PATH="/path/to/miniconda3/bin:$PATH"
            fi
        fi
        unset __conda_setup
        # <<< conda initialize <<<
        ```

    * Create a CRON job by entering the following code in the file opened by `crontab -e`
        ```
        SHELL=/bin/bash
        BASH_ENV=~/.bashrc
        */5 * * * * conda activate bb_base; python3 /path/to/birdie-booker/main.py -s > /path/to/birdie-booker/cron.log 2>&1; conda deactivate
        ```
    * Make sure the `*/5 * * * * ...` command is all on one line, otherwise `crontab` will complain.
    * Check that the CRON job was created using `crontab -l`

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
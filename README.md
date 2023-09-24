# Yugi Books <!-- omit in toc -->
This website is a hub for web scraping applications making automatic reservation bookings. Yugi Books is built using the Python Flask web framework, Selenium fro web scraping, Pushover for sending mobile device notifications, and Docker, NGINX, and a Raspberry Pi for deployment over a local network. 

*Current Yugi Books applications:*
* Birdie Blitz: golf tee time alerts for select Southern California courses

### Table of Contents <!-- omit in toc -->
- [Setup](#setup)
  - [Pushover](#pushover)
  - [Raspberry Pi](#raspberry-pi)
  - [Docker](#docker)
  - [Flask](#flask)

<!-- ## Application Organization

### Dev

### Prod -->

## Setup

### Pushover
1. Go to [Pushover](https://pushover.net/) and create an account. Note the user key displayed on your account dashboard.
2. Create an application "Birdie Booker". Note the application key displayed on the application dashboard.
3. Install Pushover on your mobile device and login.
4. (Optional) In the application dashboard, create a subscription to allow multiple people to join the app. In later steps, use the group key instead of the user key.
    
### Raspberry Pi
For production, this Yugi Books is deployed over a local network by a Raspberry Pi using NGINX. All Docker setup is done on the Raspberry Pi via an SSH connection. 
1. Install Rasberry Pi OS version 11 (Bullseye) or higher.
2. Install Docker using this tutorial: [https://docs.docker.com/engine/install/raspberry-pi-os/](https://docs.docker.com/engine/install/raspberry-pi-os/)
3. Set a static IP for the Raspberry Pi by following this tutorial: [https://www.tomshardware.com/how-to/static-ip-raspberry-pi](https://www.tomshardware.com/how-to/static-ip-raspberry-pi)
4. Note the static IP for Docker setup.

### Docker
To run in the production environment, replace `compose.dev.yml` with `compose.prod.yml`. 

1. Open Docker on your machine.
2. Clone the repository and cd into `yugi-books`.
    ```sh
    git clone https://github.com/ajtadeo/yugi-books.git
    cd yugi-books
    ```
3. Create `.env.dev` and `.env.prod`
   
   `.env.dev`
   ```env
   FLASK_APP=app/__init__.py
   FLASK_DEBUG=1
   PORT=5000
   PYTHONDONTWRITEBYTECODE=1
   PYTHONUNBUFFERED=1
   SECRET_KEY=s3cret
   CSRF_SECRET=s3cret

   PUSHOVER_API_KEY=s3cret
   PUSHOVER_USER_KEY=s3cret

   CHROME_BINARY_PATH=/path/to/Google Chrome for Testing
   CHROMEDRIVER_PATH=/path/to/chromedriver
   ```

   `.env.prod`
   ```env
   FLASK_APP=app/__init__.py
   FLASK_DEBUG=0
   PORT=4000
   PYTHONDONTWRITEBYTECODE=1
   PYTHONUNBUFFERED=1
   SECRET_KEY=s3cret
   CSRF_SECRET=s3cret

   PUSHOVER_API_KEY=s3cret
   PUSHOVER_USER_KEY=s3cret

   CHROME_BINARY_PATH=/path/to/Google Chrome for Testing
   CHROMEDRIVER_PATH=/path/to/chromedriver
   ```
4. Start the server.
    ```
    docker compose -f compose.dev.yml up -d --build
    ```
5. Open Yugi Books in your browser
    * Dev: `[raspberry pi IP]:5001`
    * Production: `[raspberry pi IP]:1337`
6. Stop the server.
    ```
    docker compose -f compose.dev.yml down -v
    ```

*Helpful Docker Commands*
* `docker logs [container name]`
  * View a container's logs.
* `docker ps -a`
  * List all containers, including inactive ones.
* `docker image list`
  * List all images

### Flask
Sometimes it's easier to host Yugi Books as a normal Flask app without Docker, especially if the developer's changes cause frequent application crashes. These crashes cause the docker container to immediately shut down, so re-composing the container can get tiring. These hosting steps are an alternate option for situations with frequent crashing.

1. Install the latest Chrome for Testing and Chromedriver versions for your OS.
    * Download Chrome for Testing and Chromedriver from [this site](https://googlechromelabs.github.io/chrome-for-testing/).
    * Move `Chrome for Testing` into the same directory as `chromedriver`
    * Append `export PATH=/path/to/chromedriver` to your run command file, usually `.bashrc` for MacOS.
2. Clone the repository and cd into `web`. Stay in this directory for the remainder of setup.
    ```sh
    git clone https://github.com/ajtadeo/yugi-books.git
    cd yugi-books/web
    ```
3. Create `.flaskenv` and add the following credentials:
    ```env
    FLASK_APP=app/__init__.py
    FLASK_DEBUG=1
    HOST='127.0.0.1'
    PORT=5000

    PYTHONDONTWRITEBYTECODE=1
    PYTHONUNBUFFERED=1
    SECRET_KEY=s3cret
    CSRF_SECRET=s3cret

    PUSHOVER_API_KEY=s3cret
    PUSHOVER_USER_KEY=s3cret

    CHROME_BINARY_PATH=/path/to/Google Chrome for Testing
    CHROMEDRIVER_PATH=/path/to/chromedriver
    ```
4. Set up the virtual environment using venv.
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     pip3 install -r requirements.txt
     ```
5. Start the server.
    ```sh
    run flask
    ```
6. Open Yugi Books in your browser at `127.0.0.1:5001`

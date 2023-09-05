# birdie-booker
## Device Setup
1. Install [PushSafer](https://www.pushsafer.com/) on your mobile device and create an account.
2. Create `.env` inside `birdie-booker` and add a `PRIVATE_KEY` variable associated with your PushSafer account.
    ```
    PRIVATE_KEY='secret'
    ```
    
## Server Setup

1. Install python3 and the [Chrome driver](https://chromedriver.storage.googleapis.com/index.html?path=111.0.5563.41/) for web scraping on your machine
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
4. Add executable permissions to `main.py` and run it.
  ```
  chmod +x main.py
  ./main.py
  ```

## Installing Dependencies
1. Update dependencies under `pip` in `base.yml`.
2. Deactivate the virtual environment if it is currently running.
    ```sh
    conda deactivate
    ```
3. Update the virtual environment. 
    * If you are removing a dependency, removing and recreating the virtual environment is necessary since `--prune` does not work as of August 9 2023. 
        ```sh
        conda remove --name cm_base --all
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
    conda activate cm_base
    ```
6. Verify that the new dependency was added to the virtual environment.
    ```sh
    pip list --local
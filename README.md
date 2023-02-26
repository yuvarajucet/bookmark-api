# bookmark-api

## Do below steps to start bookmarker-API server.

`git clone https://github.com/yuvarajucet/bookmark-api.git`

`cd bookmark-api`

## pre-requirements :
    - python3
    - pip

## source config :
 - ### Credential config:
    - use `.env` file to enter your credential like JWT encryption key, email and password for email related operations.
 - ### Linux:
    - open your `terminal`, navigate to bookmark-api folder and run below commends
    - `chmod +x build.sh`
    - `./build.sh`
    - the server will run now you can continue with shown URL.
 - ### Windows:
    - open your `cmd`, navigate to bookmark-api folder and run below file.
    - double click `build.bat` file.
    - if server not run please run server manually by doing this.
    - `python3 -m uvicorn app:app` or `uvicorn app:app`

## For API reference please check this documentation
    https://documenter.getpostman.com/view/21418798/2s8YzTU2QX

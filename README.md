# README

## Description

This is a small bot for matrix which brings a little [chatgpt]-like assistant into any matrix room.

This is written in python. Currently the code base is messy. Here is a list of things to be done or improved upon:

- [ ] Restructure codebase, maybe check out other python projects for hints on how to best structure the project.
- [ ] Containerize the application.
- [ ] Replace/stop using [simplematrixbotlib] and just use [nio] directly.
- [ ] Support encrypted rooms.
- [ ] Handle things like connectivity loss to matrix server better.
- [ ] More configuration options.
- [ ] Introduce a usage quota per room.
- [ ] Save users in database and introduce a usage quota per user.
- [ ] Better control over the openai API.
    - [ ] Better control regarding token limit.
    - [ ] Better error handling (currently hard to do with the openai package?).
- [ ] Better control over the context and how much history is sent to the API.
- [ ] More modularized way to interact with API in order to support more/different APIs.
- [ ] Maybe rewrite this in a more suitable language than python.
- [ ] Different database schema where active session is not based on timestamp.

## Install

```sh
poetry install
```

## Run

Provide environment variables or a `.env` file with these variables:

```sh
# GENERAL
PRODUCTION=false
DB_PATH="./mydb.db" # Path to an sqlite db. It will be automatically created!

# CREDENTIALS
MATRIX_HOMESERVER="https://my.matrix.home.server" # Matrix homeserver
MATRIX_BOT_USERNAME="ai-assistant" # User name of the user used for the bot
MATRIX_ACCESS_TOKEN="syt_MY_SECRET_TOKEN" # An access token fot the user
OPENAI_API_KEY="my-secret-openai-api-key" # An OpenAI API access key
```

Run the script:

```sh
poetry run matrix-ai-assistant
```

# Reddit Deleter
This is a simple command-line app that batch-deletes all chosen Reddit comments in the last `[specified number of days]` (last 7 days by default). It uses the Reddit API to fetch all your comments and allows the user to toggle the ones they want to select for batch-deletion.

In order to use this app, you need to create a Reddit app at https://www.reddit.com/prefs/apps in order to fill in the required fields in the `.env` file.

## Installation
1. Clone the repository
```bash
git clone https://github.com/oddtiming/reddit-deleter
```
2. Go in the directory, and copy the `.env.example` file to `.env`
```bash
cd reddit-deleter && cp .env.example .env
```
3. Fill in the required fields in the `.env` file.
    a. You can get the `client_id` and `client_secret` of the app created at https://www.reddit.com/prefs/apps

    b. The `username` and `password` are the credentials for the Reddit account from which you want to delete comments.

    c. The `user_agent` is a string that identifies your app to Reddit. It can be anything you want.

    d. Here is an example of a filled `.env` file:
    ```bash
        REDDIT_CLIENT_ID=abc123
        REDDIT_CLIENT_SECRET=def456
        REDDIT_USERNAME=myusername
        REDDIT_PASSWORD=mypassword
        REDDIT_USER_AGENT=comment deleter
    ```
4. Build the Docker image
```bash
docker build -t reddit-deleter .
```

## Usage
1. Run the app
```bash
docker run -it --env-file .env reddit-deleter
```
2. If you want to delete comments older than 7 days, you can specify the number of days as an argument. Here is an example for the last 30 days:
```bash
docker run -it --env-file .env reddit-deleter --days 30
```
3. Follow the instructions in the app to toggle the comments to be deleted, and then confirm the deletion.

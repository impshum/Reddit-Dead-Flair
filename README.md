## Reddit Dead Flairing Thing

A bot that adds flair to posts that have been reported N times with a chosen keyword.

![](ss.jpg)

### Install & Run Instructions

1.  Install Python https://www.python.org/ (make sure to add to PATH during install).
2.  Open up a command prompt and `cd` (change directory) to where you unzipped the bot files.
3.  Install requirements `pip install -r requirements.txt`.
4.  Create Reddit (script) app at https://www.reddit.com/prefs/apps/ and get client_id and client_secret.
5.  Edit `conf.ini` with your details and settings.
6.  Run it `python run.py`.

### Conf.ini Instructions

    [REDDIT]
    reddit_user = YOUR REDDIT USERNAME
    reddit_pass = YOUR REDDIT PASSWORD
    reddit_client_id = YOUR REDDIT CLIENT ID
    reddit_client_secret = YOUR REDDIT CLIENT SECRET

    [SETTINGS]
    max_reports = MAX NUMBER OF REPORTS BEFORE ADDING FLAIR
    flair_text = FLAIR TEXT


### Notes

-   I will not be held responsible for any bad things that might happen to you or your Reddit accounts whilst using this bot. Follow Reddiquette and stay safe.

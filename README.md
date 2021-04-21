# Ilias Schedule Bot

## Description
My retraining provider is using the ilias learning platform and since I felt very annoying, to check a few times a week if there is a new schedule available, I just wrote this bot. It checks if there is a new schedule and distribute it to all subscribers. This way, you simply get a telegram message with a pdf-file, each time there is a new schedule available.

## Sample
![Demo PNG Image](https://github.com/faraway030/IliasScheduleBot/raw/master/demo.png) ![Demo PNG Image](https://github.com/faraway030/IliasScheduleBot/raw/master/demo2.png)

## Installation & Usage
### Linux
- Clone the repository (`git clone https://github.com/faraway030/IliasScheduleBot.git`)
- Install firefox (`apt update && apt install firefox`) or similar command for your packet manager
- Install python requirements (`python3 -m pip install -r requirements.txt`)
- Create a folder `data/` containing the `config.txt` and `sticker.csv` as described below. 

Now you can start the bot just by exectuting `python3 main.py` or create a cronjob/service for running it automatically.

###  [Docker](https://hub.docker.com/r/faraway030/iliasschedulebot)
- Pull the image (`docker pull faraway030/iliasschedulebot:latest`)
- Create a local folder for storing persistent data.
- Create the `config.txt` and `sticker.csv` as described below in your persistent data folder.
- Create the container (`docker container create -v PATH_TO_YOUR_PERSISTENT_DATA_FOLDER:/bot/data/ --name NAME faraway030/iliasschedulebot:latest`) with your path and container name
- Run the container (`docker container start NAME`)

### Configuration
Create `config.txt` with the following content in `data/` and add your values.

```python
[General]
# name of the schedule file
filename =
# update interval in seconds
update = 3600

[Telegram]
# token of your telegram bot
token = 

[Ilias]
username = 
password = 
# timeout for webbrowser
timeout = 20
# url to login page of your ilias instance
url = 
# name of the link to the schedule page
step1 = 
# name of the download link at the schedule page
step2 = 
```
<br>

Create `sticker.csv` with your sticker id's in `data/`.

```
welcome=CAACAgIAAxkBAAEBnihfvXVCnmdMczzTFo3rcbpi9ij1xQACvgADJQNSDwrA0aYECcLxHgQ
attention=CAACAgIAAxkBAAEBnjZfvXbDq7NPEhfTe4bgOfP5YaK5GAACyQADJQNSD-zuumaYUqrHHgQ
```

## To do

- Fix crosslink error when setting tmp-dir outside of /bot/data (Docker related)
- ~~Change docker base to alpine~~
- Web-Interface / Admin-Panel
- Change from csv to database

## Contributions
Contributions of any kind are welcome.

## Donate :coffee: :hearts:

This is a project I develop in my free time. If you use `Ilias Schedule Bot` or simply like the project and want to help please consider [donating a coffee](https://www.buymeacoffee.com/teyifigoda).
FFmpeg is required on your system:
````
sudo apt update
sudo apt install ffmpeg
````

Due to the fact that Telegram imposes a 20 MB limit on files sent by bots, it makes sense to deploy your own custom Telegram API Server and work with the bot through it.
https://tdlib.github.io/telegram-bot-api/build.html


The configuration file <b>.env</b> is located in the project root and must contain the following:
````
BOT_TOKEN=your_telegram_bot_token
````

![5](https://github.com/user-attachments/assets/a7d54e97-6c2c-489c-8bb7-ec498bea2915)
_________________


![123](https://github.com/user-attachments/assets/f5e40f23-699c-421d-9430-ebc55a2e2aaf)


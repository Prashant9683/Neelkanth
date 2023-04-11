# Neelkanth


A discord bot that allows us to track record of the status updates.

## Usage

Type `!help` in a Discord server where this bot exists to get a list of commands you can use.

## Installation

You can install it by following - [install directly on your computer](#install-directly-on-your-computer).

### Creating a Discord bot token

- Create a [New Application](https://discord.com/developers/applications).
- Create a bot by going to Bot -> Add Bot -> Yes, do it!
- You can change Icon and Username here.
- Copy the bot token and paste it into the `TOKEN` environment variable.
- Go to the OAuth2 page -> URL Generator
  - Select the `bot` and `applications.commands` scope.
  - Select the bot permissions that you want the bot to have. Select `Administrator`. (TODO: Add a list of permissions
      that are needed)
  - Copy the generated URL and open it in your browser. You can now invite the bot to your server.

### Install directly on your computer

- Install the latest version of needed software:
  - [Python](https://www.python.org/)
    - You should use the latest version.
    - You need to add Python to your PATH in environment variables.
- Start the bot:
  - Go to the directory where the main.py file is located.
    - First install all the python dependencies needed by running below command in terminal -
    ```sh
    python3 pip install -r requirements.txt
    ```
    or simply
    ```sh
    pip install -r requirements.txt
    ```
    - Type -
    ```sh  
    python3 main.py
    ```
  into the PowerShell window.
      
  - You can stop the bot with <kbd>Ctrl</kbd> + <kbd>c</kbd>.

Note: It can take up to one hour for the slash commands to be visible in the Discord server.

## Help

- Email: [gehlotprashant968@gmail.com](mailto:gehlotprashant968@gmail.com)
- Discord: [Prashant Gehlot](https://discordapp.com/users/735113243286306836)

## Author
**Prashant Gehlot**
<br/>
**Instagram** - [Prashant Gehlot](https://www.instagram.com/prashant.gehlot)
<br/>
**Twitter** - [Prashant Gehlot](https://twitter.com/Prashan43360281)
<br/>
**LinkedIn** - [Prashant Gehlot](https://www.linkedin.com/in/prashant-gehlot/)
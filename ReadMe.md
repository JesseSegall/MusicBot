# Discord Music Bot

A simple bot that searches YouTube for a song and plays the first result. 

## Features

- Join voice channels
- Play music from YouTube
- Basic playback controls (play, pause, resume, stop)
- Display current song information
- Command list

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- pip (Python package manager)
- FFmpeg (You must have FFmpeg on your system for this to work)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/JesseSegall/discord-music-bot.git
   cd discord-music-bot
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Install FFmpeg:

   - Windows (using Chocolatey):
     ```
     choco install ffmpeg
     ```
   
   - Windows (manual installation):
     1. Go to the FFmpeg official website: https://ffmpeg.org/download.html
     2. Click on the Windows icon under "Get packages & executable files"
     3. Download the "essentials" build
     4. Extract the zip file to a location on your computer (e.g., C:\ffmpeg)
     5. Add the FFmpeg bin folder to your system PATH:
        - Right-click on 'This PC' or 'My Computer' and select 'Properties'
        - Click on 'Advanced system settings'
        - Click on 'Environment Variables'
        - Under 'System variables', find and select 'Path', then click 'Edit'
        - Click 'New' and add the path to the bin folder (e.g., C:\ffmpeg\bin)
        - Click 'OK' on all windows to save the changes
   
   - macOS (using Homebrew):
     ```
     brew install ffmpeg
     ```
   
   - Ubuntu/Debian:
     ```
     sudo apt update
     sudo apt install ffmpeg
     ```

4. Create a `.env` file in the project root and add your Discord bot token and the FFmpeg path:
   ```
   DISCORD_BOT_TOKEN=your_bot_token_here
   FFMPEG_PATH=your_path_here
   ```

## Usage

1. Start the bot:
   ```
   python main.py
   ```

2. In Discord, use the following commands:
   - `$commands`: Display all available commands
   - `$join`: Bot joins your current voice channel
   - `$play <song name>`: Plays the specified song
   - `$pause`: Pause the current song
   - `$resume`: Resume the paused song
   - `$stop`: Stop playing the current song
   - `$song`: Display information about the current song
   - `$quit`: Remove the bot from the current voice channel

## Adding the Bot to Your Server

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click on your application, then navigate to the "Bot" tab
3. Under "Token", click "Copy" to copy your bot token (use this in your .env file)
4. Go to the "OAuth2" tab, then "URL Generator"
5. In "Scopes", select "bot"
6. In "Bot Permissions", select:
   - Send Messages
   - Connect
   - Speak
7. Copy the generated URL and open it in a new tab
8. Select the server you want to add the bot to and click "Authorize"

## Troubleshooting

- If you encounter a "FFmpeg not found" error, ensure FFmpeg is correctly installed and added to your system's PATH.
- Make sure you have the correct path for the FFmpeg location, and it is added to the .env file
- Make sure your Discord bot token in the .env file is correct and the bot has the necessary permissions in your server.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
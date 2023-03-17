# Truquen

Truquen is a Discord bot that allows users to play the popular Argentinian card game, Truco. With Truquen, you can create private games with your friends and enjoy playing Truco in the comfort of your own Discord server.

## Installation

To install Truquen, please follow the instructions below:

1. Clone the repository using the following command:
```
git clone https://github.com/nahuel-borda/truquen.git
```
2. Navigate to the cloned directory using the following command:
```
cd truquen
```
3. Install the required packages using the following command:
```
pip install -r requirements.txt
```
4. Create a Discord bot account and obtain its token. You can follow the instructions [here](https://discordjs.guide/preparations/setting-up-a-bot-application.html#creating-your-bot) to create a bot account and obtain its token.

5. Create a `.env` file in the root directory of the project and add the following line to it:
```
DISCORD_TOKEN=<your-bot-token-here>
```
6. Start the bot using the following command:
```
python main.py
```

That's it! You should now have Truquen up and running on your Discord server.

## Usage

To start a game of Truco with Truquen, simply type `!truco play` in a channel where Truquen is present. This will create a private game that only you and your friends can join. 

You can use the `!truco help` command to see a list of available commands and their usage.

## Contributing

If you'd like to contribute to Truquen, please follow the instructions below:

1. Fork the repository and clone it to your local machine.
2. Create a new branch for your changes.
3. Make your changes and test them locally.
4. Commit your changes with a clear and concise commit message.
5. Push your changes to your forked repository.
6. Create a pull request and describe your changes.

# Summary Lecture Writer

This project is designed to help students work with lectures


## Using process description
1. Record a lecture on audio;
2. Send this audio to telegram bot;
3. Wait processing;
4. Get `.md`/`.txt` file with summary;


## Tecnology stack
- [Python](https://www.python.org/) (as P.L.)
- [Vosk](https://github.com/alphacep/vosk/) (for voice recognising)
- [Aiogram](https://github.com/aiogram/aiogram/) (for work with telegram api)
- [Langchain](https://github.com/langchain-ai/langchain/) (for work with LLM)


## Usage

I you want to use vosk server, then run this server, after it run the bot:
```sh
docker run --rm -d -p 2700:2700 alphacep/kaldi-ru:latest
```
```sh
uv run src/main.py
```

---

I you want to use vosk python api, then simply edit the setup.py and run the bot:
```sh
uv run src/main.py
```

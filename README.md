# DaibaNana

English ｜[繁體中文](README.zh-TW.md)

A python based discord bot designed for private server management

## Development details

### Directory structure

```plain
.
├── requirements.txt
├── .env
└── src/
    ├── cogs/
    │   └── generative.py
    ├── history.json
    └── main.py
```

### Secrets

Token are accessed with `dotenv.load_dotenv()` and `os.getenv()`.

```env
BOT_TOKEN=
GEMINI_TOKEN=
```

## Build

### Dependencies

Install packages via `pip install -r requirements.txt`.

### Release

There are two options for hosting bot:

1. Hosting locally

   ```shell
   python3 -B main.py
   ```

2. Hosting with pm2

   ```shell
   pm2 start src/main.py --name "nana" --interpreter "python3" --interpreter-args "-B"
   ```

## License

Licensed under [MIT](LICENSE).

# DaibaNana

[English](README.md) ｜繁體中文

以 Python 為基礎的 Discord 伺服器管理機器人

## 開發細節

### 目錄結構

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

### 機密

權杖皆使用 `dotenv.load_dotenv()` 和 `os.getenv()` 存取。

```env
BOT_TOKEN=
GEMINI_TOKEN=
```

## 建構

### 依賴項

透過 `pip install -r requirements.txt` 安裝依賴項。

### 發行

你可以透過以下方式發行機器人：

1. 本地發行

   ```shell
   python3 -B main.py
   ```

2. pm2 托管發行

   ```shell
   pm2 start src/main.py --name "nana" --interpreter "python3" --interpreter-args "-B"
   ```

## 授權條款

本軟體遵守 [MIT](LICENSE) 授權條款。

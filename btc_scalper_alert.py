name: BTC Scalper Alerts

on:
  workflow_dispatch:
  schedule:
    - cron: "*/5 * * * *"

jobs:
  btc-alert:
    runs-on: ubuntu-latest
    steps:
      - name: Get repository code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run BTC alert check
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: python btc_scalper_alert.py --once

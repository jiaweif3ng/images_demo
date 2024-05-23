import os

jiucai_config = dict(
    firefox_binary_location = "/home/csmn/firefox/firefox",  # https://ftp.mozilla.org/pub/firefox/releases/115.10.0esr/linux-x86_64/en-US/
    # firefox_binary_location = "/Applications/Firefox.app/Contents/MacOS/firefox",
    # firefox_binary_location = "/root/firefox/firefox",  # https://ftp.mozilla.org/pub/firefox/releases/115.10.0esr/linux-x86_64/en-US/
    geckodriver_path = "/usr/local/bin/geckodriver",   # https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz
    # geckodriver_path = "/opt/homebrew/bin/geckodriver",
    items_num = 10,    # 取前 n 篇文章
    recent_day = 20,  # 限定 n 天之内
    max_len = 8000,
)
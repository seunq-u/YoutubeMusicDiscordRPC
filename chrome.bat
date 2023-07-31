title CHROME
chcp 65001

set CHRMDIR=%cd%/chrome

cd "C:\Program Files\Google\Chrome\Application"

chrome.exe --remote-debugging-port=9222 --user-data-dir="%CHRMDIR%" https://music.youtube.com

EXIT
# MusicEventLineBot
This is a linebot where users can search live music events based on given time and location.

## 官方文件
https://docs.render.com/deploy-flask

## 檔案說明
- requirements.txt > 此app會需要安裝的套件
- app.py > 跑的主程式(flask, linebot)

## 自己嘗試
- Fork this repo to your github
- Go to render
- Deploy Web Services
- Connect to your repo
- Deploy 設定都留預設即可
- 複製左上角網址到Line Developer Webhook URL 更改（最後面要加上/callback)
- e.g. https://xxxx.onrender.com/callback
- 只要你的repo有commit change, render會自動 re-deploy

## Render Env Variable
- 建議把較機密的資訊如API Key, DB URL存到Render env varialbe而不是放在code裡
- https://docs.render.com/configure-environment-variables

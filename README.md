# 改造したscratch用のapi サーバー
blobサーバーとgptとlinebot関連のapi.

Usage:
`bash setup.sh`により`.env`ファイルの作成 \
作成した`.env`に適宜必要な項目の入力

- サーバ―の起動

```
uvicorn main:app --reload
```

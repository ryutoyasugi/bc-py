# ブロックチェーンを作ることで学ぶ
> ブロックチェーンがどのように動いているのか学ぶ最速の方法は作ってみることだ

https://qiita.com/hidehiro98/items/841ece65d896aeaa8a2a

## ブロックチェーンとは
* 不変の連続したブロックと呼ばれる記録のチェーン
* ブロックは取引・ファイルやあらゆるデータを格納することが出来る
* ブロックはハッシュを使って繋がっている

## プルーフ・オブ・ワークアルゴリズム (PoW) とは
* ブロックチェーン上でどのように新しいブロックが作られるか、または採掘されるかということ
* PoWのゴールは、問題を解く番号を発見すること
* その番号はネットワーク上の誰からも見つけるのは難しく、確認するのは簡単

## 設定
```
$ python -V
3.6.4

$ pip install -r requirements.txt
```

## 実行
```
$ python app.py
$ curl http://localhost:5000/mine | jq
$ curl -X POST -H "Content-Type: application/json" -d '{
 "sender": "3e158673353f4c0290064ecf537e70c5",
 "recipient": "someone-other-address",
 "amount": 1
}' "http://localhost:5000/transactions/new" | jq
$ curl http://localhost:5000/chain | jq
```

# 開発環境構築

## リポジトリのインストール
```bash
git clone https://github.com/shogogoto/conoha-client.git
```

## パッケージのインストール
プロジェクトルートで以下を実行
```bash
poetry install
```

## vimで編集準備
jediのpython補完が効くようにjedi-language-server packageがあるvenv環境に入ってからvi編集を始める
```bash
poetry shell
vi ???
```

## pre-commit設定
git commit前にlinterを動かす準備
```bash
poetry run task pre-commit
```

# テスト実行
プロジェクトルートで以下を実行
```bash
poetry run task test
```
ファイルを追加・更新することを検知して、自動でユニットテストを実行したい場合は以下
```bash
poetry run task test-watch
```

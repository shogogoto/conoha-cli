# conoha-client

conoha-client は [ConoHa API](https://www.conoha.jp/docs/?btn_id=docs-image-get_quota--sidebar_docs)
をいい感じに組み合わせて叩く「ConoHa VPS」用 Command Line Interface (CLI) です。
Linux サーバー(=VM)の作成・保存・削除・経過時間の確認などが簡単に実行できます。  
開発環境に VPS を利用する場合、睡眠時間分の費用も請求される月額課金は無駄が多い一方、
利用時間分のみ請求される[時間課金](https://www.conoha.jp/vps/pricing/?btn_id=vps-hourly--vpsHeader_vps-pricing)
は効率的です。  
時間課金での利用には頻繁な VM 操作が必要であり、そのために conoha-client を作成しました。

## 主な機能

<details>
<summary>←詳細を開く/閉じる

- VM の不本意な追加課金が発生しないように待ってから VM を保存・削除する Graceful Remove
- 見やすく強化された VM 一覧 e.g. 作成からの経過時間が確認できる
- VM(=サーバー)のライフサイクルの操作 e.g. 作成・削除・停止・再起動 etc
- スナップショット(VM 由来の docker image)の保存
- スナップショットから VM を復元
- リスト系コマンドの表示形式指定 e.g. json or table
</summary>

---

詳細

- VM の不本意な追加課金が発生しないように待ってから VM を保存・削除する Graceful Remove

  ログイン中の全ユーザーにブロードキャストメッセージを通知しつつ VM の停止・スナップショット・削除する

  ```bash
  $ ccli lsvm
      ipv4           status    elapsed            image_name                                           memoryMB    n_cpu    storageGB  sshkey                          vm_id
  --  -------------  --------  -----------------  -------------------------------------------------  ----------  -------  -----------  ------------------------------  ------------------------------------
   0  xxx.x.xxx.xxx  ACTIVE    80 days, 15:54:24  vmi-kusanagimanager8-0.4.0-centos-7.9-amd64-100gb        1024        2          100  key-2023-08-24-23-09            27c3379a-6510-4757-8b1c-069981be3b35
   1  yyy.y.yyy.yy   ACTIVE    0:02:53            vmi-ubuntu-20.04-amd64-30gb                               512        1           30  conoha-client-2023-11-07-15-45  ead20a7d-db9d-493c-8297-8581ba8b56b4

  # 本来は1時間後に削除する設定を6分後に変更して実行している例
  $ ccli vm rm-gracefully ea debug-snapshot -h 0.1
  elapsed from created VM(ead20a7d-db9d-493c-8297-8581ba8b56b4): 0:03:56

  Broadcast message from user@hostname (pts/10) (Mon Nov 13 14:17:41 2023

  VM(ead20a7d-db9d-493c-8297-8581ba8b56b4) makes additional charge when it takes 6 minutes. So it will save and remove this VM right now.

  It took 0:00:02 to stop VM(ead20a7d-db9d-493c-8297-8581ba8b56b4)
  save progress is 25%
  save progress is 50%
  save progress is 50%
  save progress is 50%
  save progress is 50%
  save progress is 100%
  It took 0:00:55 to save VM(ead20a7d-db9d-493c-8297-8581ba8b56b4)
  VM(ead20a7d-db9d-493c-8297-8581ba8b56b4) was removed
  Duration time of VM(ead20a7d-db9d-493c-8297-8581ba8b56b4) was 0:04:55
  ```

- 見やすく強化された VM 一覧 e.g. 作成からの経過時間が確認できる

  ```bash
  $ ccli lsvm
      ipv4           status    elapsed              memoryMB    n_cpu    storageGB  sshkey                vm_id
  --  -------------  --------  -----------------  ----------  -------  -----------  --------------------  ------------------------------------
   0  xxx.x.xxx.xxx  ACTIVE    75 days, 19:07:47        1024        2          100  key-2023-08-24-23-09  27c3379a-6510-4757-8b1c-069981be3b35
  ```

- VM(=サーバー)のライフサイクルの操作 e.g. 作成・削除・停止・再起動 etc

  - vm_id や image_id を前方一致で検索・補完するため、値全てを入力しなくてもよい
  - conoha-client では`ccli vm add -m 0.5 -d ubuntu -v 20.04`のように分かりやすく簡単で指定できる。
    他の CLI ツール では VM 作成に使用するイメージやスペックを指定するために image_id や flavor_id を調査・入力する必要があり面倒

  ```bash
  # 512MB = 0.5GBのメモリ、ubuntuのバージョン20.04でVMを新規追加
  $ ccli vm add -m 0.5 -d ubuntu -v 20.04
  VM(uuid=5f11867c-d01f-4dde-a8cb-00ffb8e1eacb) was added newly
  $ ccli lsvm # 追加されたことを確認
     ipv4           status    elapsed              memoryMB    n_cpu    storageGB  sshkey                          vm_id
  -- -------------  --------  -----------------  ----------  -------  -----------  ------------------------------  ------------------------------------
  0  xxx.x.xxx.xxx  ACTIVE    75 days, 19:17:47        1024        2          100  key-2023-08-24-23-09            27c3379a-6510-4757-8b1c-069981be3b35
  1  yyy.y.yy.yy    BUILD     -1 day, 23:59:48          512        1           30  conoha-client-2023-11-07-15-45  5f11867c-d01f-4dde-a8cb-00ffb8e1eacb

  # VMを停止
  $ ccli vm stop 5f
  5f11867c-d01f-4dde-a8cb-00ffb8e1eacb was shutdowned.
  $ ccli lsvm
      ipv4           status    elapsed              memoryMB    n_cpu    storageGB  sshkey                          vm_id
  --  -------------  --------  -----------------  ----------  -------  -----------  ------------------------------  ------------------------------------
   0  xxx.x.xxx.xxx  ACTIVE    75 days, 19:22:47        1024        2          100  key-2023-08-24-23-09            27c3379a-6510-4757-8b1c-069981be3b35
   1  yyy.y.yy.yy    SHUTOFF   0:04:48                   512        1           30  conoha-client-2023-11-07-15-45  5f11867c-d01f-4dde-a8cb-00ffb8e1eacb

  # VMを起動
  $ ccli vm boot 5f
  5f11867c-d01f-4dde-a8cb-00ffb8e1eacb was booted.
  $ ccli lsvm
      ipv4           status    elapsed              memoryMB    n_cpu    storageGB  sshkey                          vm_id
  --  -------------  --------  -----------------  ----------  -------  -----------  ------------------------------  ------------------------------------
   0  xxx.x.xxx.xxx  ACTIVE    75 days, 19:22:47        1024        2          100  key-2023-08-24-23-09            27c3379a-6510-4757-8b1c-069981be3b35
   1  yyy.y.yy.yy    ACTIVE    0:04:48                   512        1           30  conoha-client-2023-11-07-15-45  5f11867c-d01f-4dde-a8cb-00ffb8e1eacb
  ```

- スナップショット(VM 由来の docker image)の保存

  ```bash
  # VMを停止しておかないとスナップショットを保存できない
  $ ccli vm stop 5f
  5f11867c-d01f-4dde-a8cb-00ffb8e1eacb was shutdowned.
  $ ccli lsvm
      ipv4           status    elapsed              memoryMB    n_cpu    storageGB  sshkey                          vm_id
  --  -------------  --------  -----------------  ----------  -------  -----------  ------------------------------  ------------------------------------
   0  xxx.x.xxx.xxx  ACTIVE    75 days, 19:22:47        1024        2          100  key-2023-08-24-23-09            27c3379a-6510-4757-8b1c-069981be3b35
   1  yyy.y.yy.yy    SHUTOFF   0:04:48                   512        1           30  conoha-client-2023-11-07-15-45  5f11867c-d01f-4dde-a8cb-00ffb8e1eacb

  # スナップショット名「test」としてimage_id=5f...を保存
  $ ccli snapshot save 5f test
  5f11867c-d01f-4dde-a8cb-00ffb8e1eacb was snapshot as test.
  $ ccli snapshot ls
      image_id                              name    dist                app      min_disk    progress  created                      sizeGB
  --  ------------------------------------  ------  ------------------  -----  ----------  ----------  -------------------------  --------
   0  7abc6c4c-935d-4a4a-a4e9-a02cd80c74f5  test    Ubuntu-20.04-64bit                 30          25  2023-11-08T17:56:00+09:00         0

  # しばらくすると、progress:100となり、スナップショットの保存が完了する
  $ ccli snapshot ls
      image_id                              name    dist                app      min_disk    progress  created                      sizeGB
  --  ------------------------------------  ------  ------------------  -----  ----------  ----------  -------------------------  --------
   0  7abc6c4c-935d-4a4a-a4e9-a02cd80c74f5  test    Ubuntu-20.04-64bit                 30         100  2023-11-08T17:56:00+09:00    7.9245
  ```

- スナップショットから VM を復元

  ```bash
  # スナップショットを保存したのでVMを削除
  $ ccli vm rm 5f
  5f11867c-d01f-4dde-a8cb-00ffb8e1eacb was removed.
  $ ccli lsvm
      ipv4           status    elapsed              memoryMB    n_cpu    storageGB  sshkey                vm_id
  --  -------------  --------  -----------------  ----------  -------  -----------  --------------------  ------------------------------------
   0  xxx.x.xxx.xxx  ACTIVE    75 days, 19:39:47        1024        2          100  key-2023-08-24-23-09  27c3379a-6510-4757-8b1c-069981be3b35

  # image_id=7a...のスナップショット、メモリ0.5GBでVMを作成
  $ ccli snapshot restore 7a 0.5
  VM(uuid=f73538f7-cc42-427b-aae8-e9222f7b76e7) was restored from test snapshot
  $ ccli lsvm
      ipv4           status    elapsed              memoryMB    n_cpu    storageGB  sshkey                          vm_id
  --  -------------  --------  -----------------  ----------  -------  -----------  ------------------------------  ------------------------------------
   0  xxx.x.xxx.xxx  ACTIVE    75 days, 19:40:47        1024        2          100  key-2023-08-24-23-09            27c3379a-6510-4757-8b1c-069981be3b35
   1  yyy.y.yyy.yy   BUILD     -1 day, 23:59:44          512        1           30  conoha-client-2023-11-07-15-45  f73538f7-cc42-427b-aae8-e9222f7b76e7

  # しばらくするとステータスがACTIVEになる
  $ ccli lsvm
      ipv4           status    elapsed              memoryMB    n_cpu    storageGB  sshkey                          vm_id
  --  -------------  --------  -----------------  ----------  -------  -----------  ------------------------------  ------------------------------------
   0  xxx.x.xxx.xxx  ACTIVE    75 days, 19:41:47        1024        2          100  key-2023-08-24-23-09            27c3379a-6510-4757-8b1c-069981be3b35
   1  yyy.y.yyy.yy   ACTIVE    0:00:44                   512        1           30  conoha-client-2023-11-07-15-45  f73538f7-cc42-427b-aae8-e9222f7b76e7
  ```

- リスト系コマンドの表示形式指定 e.g. json or table  
   grep や jq コマンドなどのパイプ処理に便利

  ```bash
  # json形式
  $ ccli lsvm --json
  [
    {
      "ipv4": "xxx.x.xxx.xxx",
      "status": "ACTIVE",
      "elapsed": "75 days, 19:53:47",
      "memoryMB": 1024,
      "n_cpu": 2,
      "storageGB": 100,
      "sshkey": "key-2023-08-24-23-09",
      "vm_id": "27c3379a-6510-4757-8b1c-069981be3b35"
    },
    {
      "ipv4": "yyy.y.yyy.yy",
      "status": "ACTIVE",
      "elapsed": "0:12:44",
      "memoryMB": 512,
      "n_cpu": 1,
      "storageGB": 30,
      "sshkey": "conoha-client-2023-11-07-15-45",
      "vm_id": "f73538f7-cc42-427b-aae8-e9222f7b76e7"
    }
  ]

  # tableのカラム名などを削除
  $ ccli lsvm -p
  xxx.x.xxx.xxx  ACTIVE  75 days, 19:53:47  1024  2  100  key-2023-08-24-23-09            27c3379a-6510-4757-8b1c-069981be3b35
  yyy.y.yyy.yy   ACTIVE  0:12:44             512  1   30  conoha-client-2023-11-07-15-45  f73538f7-cc42-427b-aae8-e9222f7b76e7

  # 表示カラムを絞る
  $ ccli lsvm -k ipv4 -k elapsed
      ipv4           elapsed
  --  -------------  -----------------
   0  xxx.x.xxx.xxx  75 days, 19:54:47
   1  yyy.y.yyy.yy   0:13:44

  # where句みたいにstorageGB = 30 の行を表示
  $ ccli lsvm -w storageGB 30
      ipv4          status    elapsed      memoryMB    n_cpu    storageGB  sshkey                          vm_id
  --  ------------  --------  ---------  ----------  -------  -----------  ------------------------------  ------------------------------------
   0  yyy.y.yyy.yy  ACTIVE    0:13:44           512        1           30  conoha-client-2023-11-07-15-45  f73538f7-cc42-427b-aae8-e9222f7b76e7
  ```

  </details>

## 使い方

### インストール

[PyPI](https://pypi.org/project/conoha-client/) からインストール

```bash
pip3 intall conoha-client
```

すると、python3 のエンドポイントに ccli が追加され、実行可能になります。

### help オプション

本ツールは python の CLI 用ライブラリ[click](https://click.palletsprojects.com/en/8.1.x/)を利用しています。
使用可能なコマンドやオプションは help オプションで随時確認できます。
サブコマンドに対しても help オプションは使用可能です。

```bash
// 例
$ ccli --help
Usage: ccli [OPTIONS] COMMAND [ARGS]...

  root.

Options:
  --help  Show this message and exit.

Commands:
  lsimg      list image
  lsinvoice  課金一覧.
  lsorder    契約一覧.
  lspaid     入金履歴.
  lsplan     List vm plan.
  lsvm       list VM as human friendly
  snapshot   スナップショット=ユーザーがVMから作成したイメージ.
  sshkey     キーペアCRUD.
  vm         VM追加・削除など
```

### 環境変数の設定

[API を使用するためのトークンを取得する](https://support.conoha.jp/v/apitokens/)
を参考に ConoHa のダッシュボードを参照して環境変数を設定する

```bash
# ConoHa VPSのダッシュボード由来の情報 must
export OS_USERNAME=***       # APIユーザー > ユーザー名
export OS_PASSWORD=***       # APIユーザー > パスワード
export OS_TENANT_ID=***      # テナント情報 > テナントID
export OS_CONOHA_REGION_NO=? # エンドポイントのtyo?の数字 e.g. https://account.tyo3.conoha.io/v1/... => 3

# VM作成に関わる環境変数 optional
export OS_ADMIN_PASSWORD=***        # VMのrootユーザーのパスワード
export OS_SSHKEY_NAME=***           # VMに登録するsshのキーペア名
export OS_TEMPLATE_READ=~/.ssh/...  # 新規作成したVMの情報を適用するテンプレート
export OS_TEMPLATE_WRITE=~/.ssh/... # 適用したテンプレートの出力先
```

### テンプレートの例

```
# ~/.ssh/conf.d/dev/template

Host dev
  HostName ${ipv4}
  Port 22
  User gotoh
  IdentityFile ~/.ssh/conf.d/dev/id_rsa
  ServerAliveInterval 60 #sshの自動切断を防ぐために記述
  ForwardX11 yes
  ForwardAgent yes
```

`${ipv4}`の部分が作成した VM の値で置き換わった内容が
`OS_TEMPLATE_WRITE`で指定したパスに出力される  
${key}の key には`ccli lsvm`のカラム名が使用できる

### シェル補完機能

conoha-client は CLI 用ライブラリ[click](https://click.palletsprojects.com/en/8.1.x/)
を使用しています。  
click は[シェル補完機能](https://click.palletsprojects.com/en/8.1.x/shell-completion/)
が利用できます。`~/.bashrc`に以下を追記してください。

```bashrc
# ~/.bashrc
. <(curl -s https://raw.githubusercontent.com/shogogoto/conoha-client/main/conoha-client.bash)
```

ただし、ネットワーク経由で取得したコードを直接実行するこの方法は重大なセキュリティリスクのようです。  
不安な方は本リポジトリのルートディレクトリの`conoha-client.bash`
の内容をコピペして`~/.bashrc`に追記してください。以下に転記しておきます.

```bash
# conoha-client.bash

_ccli_completion() {
    local IFS=$'\n'
    local response

    response=$(env COMP_WORDS="${COMP_WORDS[*]}" COMP_CWORD=$COMP_CWORD _CCLI_COMPLETE=bash_complete $1)

    for completion in $response; do
        IFS=',' read type value <<< "$completion"

        if [[ $type == 'dir' ]]; then
            COMPREPLY=()
            compopt -o dirnames
        elif [[ $type == 'file' ]]; then
            COMPREPLY=()
            compopt -o default
        elif [[ $type == 'plain' ]]; then
            COMPREPLY+=($value)
        fi
    done

    return 0
}

_ccli_completion_setup() {
    complete -o nosort -F _ccli_completion ccli
}

_ccli_completion_setup;
```

## 開発動機

### PC はシンクライアントに限る

低スペック PC で個人開発するのに限界を感じた私は VPS を開発環境として利用することを考えました。  
PC くらい買えって？時代はシェアリングエコノミー。
自分が専有する資源は、自分が使用していない間には場所を奪うだけの置物と化します。
クラウド時代において、PC は低スペックなシンクライアントに徹するべきです。  
そうすれば、スペースと費用が節約できるはずです。

### なぜ「ConoHa VPS」なのか

いろんな VPS がある中で ConoHa VPS を選んだ理由は以下です。

- １時間毎の時間課金で VPS が利用可能  
  多くの VPS は月額課金であり、寝ている間にも課金されるのはいただけない  
  ※ [WebArena Indigo](https://web.arena.ne.jp/indigo/price/)も時間課金プランを提供しているようだ
- スナップショットを 50GB まで無料で使用できる  
  時間課金では、削除する VM の状態を無料で保存できることは重要
- GMO(9449)の株主優待が使える(年間 1 万円分)

### なぜ既存ツールを使わなかったのか

時間課金を意識した既存ツールが見当たらなかったためです。  
[ConoHa API](https://www.conoha.jp/docs/?btn_id=docs-image-get_quota--sidebar_docs)
と１対１対応しただけの単純な CLI では不満がありました。
サーバーを起動・停止・削除＋ α だけではなく、

- サーバー作成からの時間経過を知りたい
- 次の 1 時間に突入して追加で課金される前にサーバー削除を予約したい
- サーバーの状態を保存・復元を簡単したい

などの機能は頻繁にサーバーを削除する時間課金では重要です。

## 開発環境構築

### パッケージのインストール

プロジェクトルートで以下を実行

```bash
poetry install
```

### pre-commit 設定

git commit 前に linter を動かす準備

```bash
poetry run task pre-commit
```

### テスト実行

プロジェクトルートで以下を実行

```bash
poetry run task test
```

ファイルを追加・更新することを検知して、自動でユニットテストを実行したい場合は以下

```bash
poetry run task test-watch
```

### リリース方法

poetry 経由で PyPI にリリースする
poetry 拡張の poetry-dynamic-versioning によって、
git tag を PyPI のバージョンとして動的に設定・リリースする

```bash
git tag vx.x.x

poetry publish --build
```

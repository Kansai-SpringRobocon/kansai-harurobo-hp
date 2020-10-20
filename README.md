# kansai-harurobo-hp

[![Build Status](https://travis-ci.org/Kansai-SpringRobocon/kansai-harurobo-hp.svg?branch=master)](https://travis-ci.org/Kansai-SpringRobocon/kansai-harurobo-hp)

春ロボコン(関西大会)のホームページ

## 利用しているもの
- [Hugo](https://gohugo.io/)
- [Hugo Themes Universal](https://themes.gohugo.io/hugo-universal-theme/)

## 環境構築

### Hugoのインストール

#### Ubuntu >= 18
```shell
snap install hugo
```

#### Ubuntu < 18 or Debian

<https://github.com/gohugoio/hugo/releases>からdebファイルをダウンロードしてインストールする。

#### ソースから
事前にgoコマンドのインストールが必要
````shell
go get github.com/gohugoio/hugo
````

#### 他の方法

<https://gohugo.io/getting-started/installing>を参照。

### このリポジトリのクローン

submoduleを使用しているため、クローン時に`--recursive`オプションが必要。

任意のディレクトリで

```shell
git clone https://github.com/Kansai-SpringRobocon/kansai-harurobo-hp.git --recursive
```

sshでも可

### ワークツリーの設定 (手動ビルド時のみ必須)

`public/`以下に`gh-pages`ブランチを割り当てる。

```shell
git worktree add -B gh-pages public origin/gh-pages
```

## サイト編集手順

### 編集

まず、編集内容をコミットするためのブランチを切る。そのブランチ上でページを編集する。

hugo server (プレビュー用のローカルWebサーバー) を使って編集すると楽。サイトを編集するとリアルタイムで反映されるので重宝する。以下のコマンドで起動できる。

```shell
hugo server -D
```
プレビュー用URLは`Web Server is available at {URL} (bind address 127.0.0.1)`の形式でコマンドから出力されるので、そのURLにアクセスする。URLは通常<http://localhost:1313/>

編集し終わったら次の手順でデプロイする。

### デプロイ

#### 現在 (自動ビルドあり)

編集内容をコミットし、Pushしてmasterブランチへのプルリクエストを発行する。自動ビルドに成功してマージすると自動的に本番環境にデプロイされる。

#### 古い手順 (手動ビルド)

**注意:** 現在、この手順は不要。

```shell
hugo
```

を実行すると`public/`にビルド結果が出力される。`public/`に移動するとワークツリーの機能で勝手にgh-pagesブランチに切り替わる。全ての変更をコミットし、pushして反映する。

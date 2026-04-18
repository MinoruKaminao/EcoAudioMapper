# EcoAudio Mapper 操作説明書

## 目的
この文書は、現在実装済みの最初のスライスを起動し、確認し、利用するための操作手順をまとめたものです。

現在の実装対象は以下です。
- 最小バックエンド起動 API
- 最小 DB 接続済み観測一覧 API
- 最初のデスクトップ向け UI シェル

この文書では、未実装機能は扱いません。

## 公開リポジトリ安全運用メモ
- 実際の秘密情報をコミットしないでください。
- 実際の私有フィールド録音はこのリポジトリで扱わないでください。
- 保護種の正確な座標や精密な時刻を公開資料に含めないでください。
- 検証にはマスク済み、合成、または公開承認済みのサンプルだけを使用してください。

## 現在操作可能な実装範囲

### バックエンド
- アプリケーションエントリポイント
- ヘルスチェック API
- 観測一覧 API
- 環境変数による設定読込
- SQLAlchemy セッション配線
- Alembic 初期設定

### フロントエンド
- デスクトップ優先ワークスペースシェル
- 上部ツールバー
- 左ナビゲーションサイドバー
- 中央観測ワークスペース
- 右インスペクタペイン
- normal、loading、empty、error、offline、success、permission 相当の状態表示

## バックエンド操作手順

### 1. バックエンド環境を準備する
リポジトリルートから実行します。

```bash
cd backend
python3 -m venv .venv
./.venv/bin/python -m pip install -e '.[dev]'
```

### 2. 環境変数を設定する
設定の基準は [`backend/app/core/config.py`](../../backend/app/core/config.py) と [`.env.example`](../../.env.example) です。

主要な変数:
- `APP_NAME`
- `ENVIRONMENT`
- `DEBUG`
- `API_V1_PREFIX`
- `ENABLE_DOCS`
- `DATABASE_URL`
- `ALEMBIC_DATABASE_URL`

ローカル確認では、検証目的に応じて SQLite または PostgreSQL の URL を指定できます。

### 3. バックエンドを起動する
[`backend`](../../backend) で実行します。

```bash
./.venv/bin/python -m uvicorn app.main:app --reload
```

### 4. バックエンドの稼働確認を行う
ヘルスチェック API を開きます。

- `GET /health`

期待されるレスポンス構造:

```json
{
  "status": "ok",
  "environment": "development"
}
```

### 5. 観測一覧 API を利用する
利用可能な API:

- `GET /api/v1/observations?limit=20&offset=0`

現在の挙動:
- `deleted_at` が設定されていない観測だけを返します
- 新しい作成日時順で返します
- `id`、`status`、`visibility_level`、`recorded_at_utc` を含む最小形式で返します

## データベース操作手順

### 1. マイグレーション準備状態
Alembic の初期ファイルは以下です。
- [`alembic.ini`](../../alembic.ini)
- [`alembic/env.py`](../../alembic/env.py)
- [`alembic/versions/0001_initial_schema.py`](../../alembic/versions/0001_initial_schema.py)

### 2. マイグレーション時の注意
初期マイグレーションは PostgreSQL / PostGIS 前提のスキーマ意図を含みます。

実 DB に適用する前に、以下を確認してください。
- PostgreSQL が利用可能であること
- PostGIS が利用可能であること
- 非本番の安全な認証情報を使っていること
- サンプルデータが機微な座標や時刻を含まないこと

### 3. ロールバックに関するメモ
現在の最小 DB スライスでは、新規マイグレーション改訂は追加していません。
そのため、直近変更のロールバックは主にアプリケーションコードを戻すことで対応できます。

## フロントエンド操作手順

### 1. フロントエンド環境を準備する
リポジトリルートから実行します。

```bash
cd frontend
npm install
```

### 2. フロントエンドを起動する
[`frontend`](../../frontend) で実行します。

```bash
npm run dev
```

現在のフロントエンド開発サーバーは [`frontend/package.json`](../../frontend/package.json) でポート `3102` を使う設定です。

### 3. UI スライスを確認する
最初の UI スライスは、静的なワークステーション型シェルを表示します。

確認ポイント:
- 上部ツールバーに主要操作があること
- 左にナビゲーションサイドバーがあること
- 中央に状態表示と観測テーブルがあること
- 右にインスペクタパネルがあること
- キーボードフォーカス表示が見えること
- メイン領域へ移動するスキップリンクがあること

### 4. フロントエンド型チェックを行う

```bash
npm run typecheck
```

## 現在の利用フロー

### バックエンド利用フロー
1. バックエンドを起動します。
2. [`/health`](../../backend/app/main.py) で稼働確認を行います。
3. [`/api/v1/observations`](../../backend/app/api/v1/observations.py) を呼び出します。
4. レスポンス形式と並び順を確認します。

### フロントエンド利用フロー
1. フロントエンドを起動します。
2. ルートページを開きます。
3. 三分割ワークスペース構成を確認します。
4. 状態表示が明示されていることを確認します。
5. 選択観測の詳細がインスペクタに表示されることを確認します。

## トラブルシューティング

### バックエンドテストコマンド
[`backend`](../../backend) で実行します。

```bash
./.venv/bin/python -m pytest
```

### よくある問題
- Python 依存関係不足: 仮想環境を作り直して再インストールしてください。
- Node 依存関係不足: [`frontend`](../../frontend) で `npm install` を再実行してください。
- DB 接続エラー: `DATABASE_URL` と DB の起動状態を確認してください。
- マイグレーションエラー: 初期スキーマ適用前に PostgreSQL / PostGIS 互換性を確認してください。

## 現在の制限
- 観測の完全 CRUD は未実装
- 分析機能は未実装
- ML 推論機能は未実装
- フロントエンドと API のライブ接続は未実装
- 本番向け認証・認可は未実装

## 関連する実装済みファイル
- [`backend/app/main.py`](../../backend/app/main.py)
- [`backend/app/api/v1/observations.py`](../../backend/app/api/v1/observations.py)
- [`backend/app/db/models/observation.py`](../../backend/app/db/models/observation.py)
- [`backend/app/db/session.py`](../../backend/app/db/session.py)
- [`frontend/src/app/page.tsx`](../../frontend/src/app/page.tsx)
- [`frontend/src/components/workspace-shell.tsx`](../../frontend/src/components/workspace-shell.tsx)
- [`frontend/src/app/globals.css`](../../frontend/src/app/globals.css)

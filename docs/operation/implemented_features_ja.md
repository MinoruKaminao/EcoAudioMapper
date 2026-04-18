# EcoAudio Mapper 実装済み機能説明書

## この文書の対象範囲
この文書は、現時点でリポジトリに実装されている機能だけを整理したものです。

将来計画を含む全製品仕様の説明ではありません。

## 1. バックエンド起動機能

### 1.1 アプリケーション起動
バックエンドアプリケーションは [`backend/app/main.py`](../../backend/app/main.py) から生成・起動できます。

実装済み内容:
- アプリファクトリ設定
- FastAPI 初期化
- 設定によるドキュメント公開制御
- 観測 API ルーター登録

### 1.2 ヘルスチェック API
[`backend/app/main.py`](../../backend/app/main.py) にヘルスチェック API を実装しています。

実装済み内容:
- `GET /health`
- サービス状態と現在環境名を返却

## 2. 設定機能

設定は [`backend/app/core/config.py`](../../backend/app/core/config.py) に実装されています。

実装済み内容:
- 環境変数ベースの設定読込
- ローカル開発向けデフォルト値
- Alembic 用 DB URL の分離対応
- ドキュメント有効・無効切替

関連サンプルファイル:
- [`.env.example`](../../.env.example)

## 3. データベース配線機能

### 3.1 SQLAlchemy 基盤とエンジン設定
実装ファイル:
- [`backend/app/db/base.py`](../../backend/app/db/base.py)
- [`backend/app/db/session.py`](../../backend/app/db/session.py)

実装済み内容:
- 共通宣言的ベース
- 設定済み DB URL からのエンジン生成
- セッションファクトリ生成
- リクエスト単位の DB セッション依存性

### 3.2 Alembic 初期化準備
実装ファイル:
- [`alembic.ini`](../../alembic.ini)
- [`alembic/env.py`](../../alembic/env.py)
- [`alembic/versions/0001_initial_schema.py`](../../alembic/versions/0001_initial_schema.py)

実装済み内容:
- Alembic 環境設定
- アプリ設定を用いたマイグレーション設定
- 初期スキーマ改訂ファイルをリポジトリに保持

## 4. 観測データ機能

### 4.1 最小観測 ORM モデル
[`backend/app/db/models/observation.py`](../../backend/app/db/models/observation.py) に実装しています。

実装済み内容:
- `observations` テーブルの最小マッピング
- 最初の read-only スライス向けに、文書化された初期スキーマ意図に整合するフィールドを定義

### 4.2 観測一覧 API
[`backend/app/api/v1/observations.py`](../../backend/app/api/v1/observations.py) に実装しています。

実装済み内容:
- `GET /api/v1/observations`
- `limit` と `offset` に対応
- 論理削除行を除外
- 新しい作成順で返却
- 最小レスポンス構造を返却

### 4.3 観測レスポンススキーマ
[`backend/app/schemas/observation.py`](../../backend/app/schemas/observation.py) に実装しています。

実装済み内容:
- サマリー項目形式
- ページング情報付き一覧レスポンス形式

## 5. バックエンドテスト実装

実装ファイル:
- [`backend/tests/conftest.py`](../../backend/tests/conftest.py)
- [`backend/tests/api/test_bootstrap.py`](../../backend/tests/api/test_bootstrap.py)

実装済み内容:
- 一時 SQLite DB を使ったテスト環境
- ヘルスチェック API 検証
- 空の観測一覧検証
- データ投入後の観測一覧検証

## 6. フロントエンド最初の UI スライス

### 6.1 フロントエンド基盤
実装ファイル:
- [`frontend/package.json`](../../frontend/package.json)
- [`frontend/tsconfig.json`](../../frontend/tsconfig.json)
- [`frontend/next-env.d.ts`](../../frontend/next-env.d.ts)
- [`frontend/src/app/layout.tsx`](../../frontend/src/app/layout.tsx)
- [`frontend/src/app/page.tsx`](../../frontend/src/app/page.tsx)

実装済み内容:
- 最小 Next.js アプリ設定
- ルートレイアウトとページ入口
- 型チェック可能なフロントエンド基盤

### 6.2 デスクトップワークスペースシェル
[`frontend/src/components/workspace-shell.tsx`](../../frontend/src/components/workspace-shell.tsx) に実装しています。

実装済み内容:
- 主要操作を持つ上部ツールバー
- 左ナビゲーションサイドバー
- 概要、状態表示、観測テーブルを持つ中央ワークスペース
- 右インスペクタペイン
- 必須状態を明示する UI 表示

### 6.3 UI スタイルとアクセシビリティ基盤
[`frontend/src/app/globals.css`](../../frontend/src/app/globals.css) に実装しています。

実装済み内容:
- 抑制的で中立的なデスクトップ向けスタイル
- ペインベース構成
- 明確なキーボードフォーカス表示
- スキップリンク対応
- 幅が狭い場合の段組み切替

## 7. まだ未実装のもの
- 観測の完全 CRUD
- バックエンド API とフロントエンドのライブ連携
- 分析画面と分析サービス
- ML 推論ワークフロー
- 本番利用向け認証・認可
- UI 上での保護種マスキング運用制御
- 完全なレビュー業務フロー

## 8. 公開安全性メモ
- 実装済みスライスで秘密情報は追加していません
- 生の私有フィールド録音は含んでいません
- 実装済み文書や UI サンプルデータに保護種の正確座標は含んでいません
- 現在の UI サンプルデータは静的なデモ用表示です


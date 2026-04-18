# EcoAudio Mapper Alembic初期マイグレーション案

このパッケージは、EcoAudio Mapper 向けの **Alembic 初期マイグレーション案** です。

## 含まれるもの
- `versions/0001_initial_schema.py`
- `alembic_README.md`

## 前提
- PostgreSQL 16+
- 拡張: `pgcrypto`, `postgis`
- Python パッケージ:
  - `alembic`
  - `sqlalchemy`
  - `psycopg`
  - `geoalchemy2`

## 想定インストール例

```bash
pip install alembic sqlalchemy psycopg[binary] geoalchemy2
```

## 配置例

```text
your_project/
  alembic.ini
  alembic/
    env.py
    script.py.mako
    versions/
      0001_initial_schema.py
```

## 注意
- この案は「初期マイグレーションのたたき台」です。
- 実プロジェクトでは、命名規則、スキーマ名、RLS、ロール権限、パーティション戦略に応じて調整してください。
- `downgrade()` は開発用の簡易版として用意しています。運用ではデータ損失に注意してください。
- `geoalchemy2` を使っているため、`env.py` 側で metadata の import を適切に行ってください。

## 実行例

```bash
alembic upgrade head
```

## 次に作るとよいもの
- SQLAlchemy ORM モデル雛形
- `alembic/env.py` の推奨設定例
- 2本目以降の migration 分割案
- seed データの専用 migration

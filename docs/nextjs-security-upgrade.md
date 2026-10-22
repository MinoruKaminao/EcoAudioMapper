# Next.js セキュリティ更新（未対応・判断待ち）

> **状態: 未対応・判断待ち。** 2026-10 の Node.js 26.12.1 移行では Next.js に手を入れていない（オーナー判断「開発実装時に検討できるようにドキュメントで残し、今回は触れない」）。この文書は、開発中に更新を行う担当者向けのメモ。

## 現状（2026-10-23 時点）

- `frontend/package.json`: `"next": "15.3.1"`（完全固定）。`react` / `react-dom` は `19.1.0`
- `frontend/` で `npm audit` を実行すると 5 パッケージで計 5 件（critical 1 / high 4）が報告される
  - `next`: critical。15.3.1 に該当する Next.js の advisory は 37 件（critical 4 / high 13 / moderate 17 / low 3）
  - `postcss` / `sharp`: high（どちらも Next.js の依存）
  - `nanoid` / `source-map-js`: high（間接依存）
- 個々の advisory は `cd frontend && npm audit` で確認できる（GitHub Advisory の ID と影響範囲が表示される）

## 選択肢

各案は、ロックファイルだけ更新した作業用コピーで `npm audit` を実行して確かめた（2026-10-23）。

| 案 | npm の dist-tag | 種類 | Next.js 自身の advisory | `npm audit` の残り |
|---|---|---|---|---|
| `15.3.9` | `next-15-3` | パッチ更新 | 32 件残る（critical 3 を含む） | 5 件（critical 1 / high 4）。15.3 系だけの修正分しか入らない |
| `15.5.28` | `backport` | マイナー更新 | 0 件 | 5 件（moderate 1 / high 4）。続けて `npm audit fix` を実行すると 2 件（`postcss` high と、それを理由にした `next` moderate）。Next.js が依存として固定している `postcss` 8.4.31 が残るため |
| `16.4.2` | `latest` | メジャー更新 | 0 件 | 0 件 |

- **推奨: 少なくとも `15.5.28`。** Next.js 自身の advisory をすべて解消できる、もっとも小さい更新。`15.3.9` だけでは不十分
- `16.4.2` なら `npm audit` の報告もなくなる。ただしメジャー更新なので、Next.js 16 の移行ガイド（破壊的変更）を確認し、ビルド・型チェック・画面の動作確認を行うこと
- どの案でも peerDependencies は現行の `react` 19.1.0 を受け入れ、engines も Node 26.12.1 を受け入れる

## 更新するときの手順（目安）

1. `cd frontend && npm install next@<版> --save-exact`
2. `npm audit` で残りを確認し、必要なら `npm audit fix`（`--force` は使わない）
3. `npm run build` と `npm run typecheck` が通ることを確認
4. `docker/frontend.Dockerfile` でイメージをビルドして起動を確認

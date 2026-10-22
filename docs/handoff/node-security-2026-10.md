# Handoff: Node.js 2026年10月セキュリティリリース対応（EcoAudioMapper）

- 優先度: **P4（ローカル開発環境）**
- 期限: 2026-10-30
- 作成日: 2026-10-23

Claude Code への作業依頼。上から順に読み、「作業」を実施して「完了条件」を満たしたら「完了報告」を埋める。

## 背景

2026-10-21 に Node.js のセキュリティリリースが公開された（[告知](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases)）。

- **修正版**: `22.23.4` / `24.22.1` / `26.12.1`
- **主な脆弱性（High）**: Brotli デコーダの範囲外書き込みによる RCE（CVE-2026-111497）、TLS 証明書のホスト名検証回避 2 件（CVE-2026-105483 / CVE-2026-106069）、`dns.resolve` の NUL 文字切り詰め（CVE-2026-105482）
- **その他**: keep-alive ソケットの応答取り違え、非正規 IPv4 による証明書検証の誤り、SEA/スナップショットでの乱数キャッシュ再利用、権限モデルのバイパスなど（Medium / Low）
- **同梱依存の更新**: c-ares・Undici・ca-cert（eMudhra 中間 CA 失効）は全系列、OpenSSL は 22/24、SQLite は 22
- **Node 20 以前は 2026-04-30 で EOL**。影響を受けるが修正版は出ない
- npm 依存として `undici` を別途同梱しているかはロックファイルで確認済みで、該当なし。Node 本体の更新だけで対処できる

全体計画: [Node.js 2026年10月セキュリティリリース 対応計画](https://claude.ai/artifact/BHcg2TN4NNmuxc7V9mTad4)

## このリポジトリの現状

`frontend/` が Next.js 15.3.1（`next dev` / `next start`）。`docker/frontend.Dockerfile` と `docker-compose.yml` は空。**公開リポジトリ**。
リポジトリ内で Node のバージョンを指定しておらず、手元のマシンの Node がそのまま使われる。

## 作業

- [x] 手元の Node を `24.22.1`（または `22.23.4` / `26.12.1`）以上に更新し、`node -v` で確認する
- [x] リポジトリ直下に `.nvmrc`（内容: `24`）を追加する（ユーザー判断により内容は `26.12.1`）
- [ ] Node を使う `package.json` に `"engines": { "node": ">=22.23.4 <23 || >=24.22.1 <25 || >=26.12.1" }` を追加する（ユーザー判断により `">=26.12.1"`）
- [x] `frontend` で `npm ci` と `npm run build` が通ることを確認する
- [x] README に推奨 Node バージョンを追記する

## 完了条件

- `.nvmrc` と `engines` が追加されている
- 更新後の Node で依存のインストールとビルド（または起動）が通る

## 守ること

- この PR のブランチ `chore/node-security-2026-10` 上で作業し、作業内容をこのブランチに追加コミットする。
- Node.js のバージョン変更と、それに必要な最小限の修正だけを行う。関係のないリファクタリングや依存の一括更新はしない。
- 作業前に `AGENTS.md` を読み、このリポジトリの規約に従う。
- `node -v` などの実測結果で確認する。バージョンを推測で書かない。
- 動作確認で問題が出て判断が要る場合（メジャーバージョンを上げる必要がある、テストが落ちる等）は、作業を止めて状況を報告する。
- 作業が終わったら、このファイルの「完了報告」欄を埋めてコミットする（ファイル自体は記録として残す）。
- Next.js 15.3.1 には今回とは別に Next.js 自体のセキュリティ修正が出ている可能性がある。15.3 系の最新パッチを確認し、更新が必要なら報告する（メジャー・マイナーの更新は行わない）。

## 完了報告

- 実施日: 2026-10-23
- 対象バージョンについて: ハンドオフ記載の `24`（engines は 22/24/26 の範囲指定）ではなく、**ユーザー判断で 26.12.1 に統一**した。
- 変更したファイル:
  - `.nvmrc`（新規、内容 `26.12.1`）
  - `frontend/package.json`: `"engines": { "node": ">=26.12.1" }` を追加。`@types/node` を `24.6.0` → `^26` に変更（Node 26 の型に合わせるため。ロック上は `26.6.5`）
  - `frontend/package-lock.json`: 上記に合わせて同期
  - `README.md`: `## Requirements` に推奨 Node バージョン（26.12.1 以上、`.nvmrc`）を追記
  - `AGENTS.md` を確認し、規約（公開リポジトリ・秘匿情報を含めない等）に従った
- 確認した Node バージョン（`node -v` の出力）: `v26.12.1`（npm `11.20.0`）
- テスト・動作確認の結果:
  - `frontend`: コミット済みロックファイルで `npm ci` 成功
  - `frontend`: `npm run build`（`next build`）成功。`npm run typecheck`（`tsc --noEmit`）成功
  - テストスクリプトは定義されていない
- Next.js のセキュリティ修正（報告のみ、変更はしていない）:
  - 15.3 系の最新パッチは `15.3.9`（現在は `15.3.1`）。`npm audit --omit=dev` は `next` に critical を含む多数の advisory を報告
  - `15.3.9` へ上げると 15.3 系向けの修正（critical の RCE GHSA-9qr9-h5gf-34mp、GHSA-mwv6-3258-q52c、GHSA-h25m-26qc-wcjf など）は取り込めるが、15.5 系でのみ修正された advisory（critical の GHSA-p293-qw3h-jr36 / GHSA-2xp9-vwfh-vxw4 / GHSA-2464-fhr4-w9xw など）は残る。npm audit が示す修正版は `15.5.28`（マイナー更新）
  - **更新が必要**と判断する。少なくとも `15.3.9` へのパッチ更新、できれば `15.5.28` 以降へのマイナー更新を別途判断・実施してほしい
- 残課題:
  - 上記 Next.js の更新（今回のスコープ外のため未実施）
  - `npm audit` は `nanoid` / `postcss` / `sharp` / `source-map-js`（Next.js 経由を含む）にも high を報告。Next.js の更新で大半が解消する見込み
- 追補 2026-10-23: Next.js の更新は未対応・判断待ち（オーナー判断で今回は触れない）。現状・`npm audit` の結果・選択肢（15.3.9 / 15.5.28 / 16.4.2）を [`docs/nextjs-security-upgrade.md`](../nextjs-security-upgrade.md) にまとめた。engine-strict もこのリポジトリには入れていない

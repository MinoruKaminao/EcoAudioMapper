# 位置情報・日時情報付き動画音声による生物分布可視化システム
## DB設計詳細版

- 文書名: 位置情報・日時情報付き動画音声による生物分布可視化システム DB設計詳細版
- 版数: v1.3
- 作成日: 2026-04-18
- 想定プロジェクト名称: EcoAudio Mapper

---

## 1. 目的

本書は、EcoAudio Mapper におけるデータベース設計の詳細仕様を定義する。  
対象は、観測データ、動画・音声メディア、位置情報、日時情報、音声区間、推論結果、レビュー結果、時系列集計、公開制御、管理マスタを保持する永続化層である。

本設計は、以下を重視する。

- 観測データの再現性
- 位置情報と日時情報の厳密管理
- AI 推論結果と人手レビュー結果の分離
- 地図表示と時系列分析に適した検索性
- 保護対象種とプライバシーに配慮した公開制御
- 将来的な再学習・再処理に耐える履歴管理

---

## 2. DB設計方針

### 2.1 採用方針
- 主データストアは **PostgreSQL** を前提とする
- 地理検索のため **PostGIS** 拡張を利用する
- JSON 的な柔軟属性には `jsonb` を必要最小限で使用する
- 主キーは原則 `uuid` を採用する
- 日時は原則として `timestamp with time zone` を利用し、必要に応じて原本文字列も保持する
- 集計高速化のため、一部サマリテーブルを持つ
- 削除は論理削除を基本とし、必要に応じて物理削除を行う
- 監査性の高い項目は更新履歴を別テーブルで保持する

### 2.2 命名規則
- テーブル名: 複数形の snake_case  
  例: `observations`, `audio_segments`
- カラム名: snake_case
- 主キー: `<table>_id` ではなく `id`
- 外部キー: `<related_table_singular>_id`
- 作成日時: `created_at`
- 更新日時: `updated_at`
- 論理削除日時: `deleted_at`

### 2.3 スキーマ分割方針
以下の論理分割を推奨する。

- `core`: 観測主体データ
- `ml`: 推論・モデル・学習関連
- `analytics`: 集計関連
- `admin`: ユーザー・権限・監査関連
- `master`: マスタ関連

本書では、可読性のため単一記法で示す。

---

## 3. 採用想定DB機能

- PostgreSQL 16 以降
- PostGIS
- pgcrypto または uuid-ossp
- GIN / B-Tree / BRIN / GiST / SP-GiST インデックス
- Materialized View または集計テーブル
- Row Level Security は必要に応じて検討

---

## 4. エンティティ一覧

### 4.1 主テーブル
- users
- roles
- user_roles
- observations
- media_files
- locations
- observation_datetimes
- observation_conditions
- audio_segments
- detections
- detection_candidates
- reviewer_decisions
- processing_jobs
- model_versions
- seasonal_rules
- access_control_rules
- protected_species_rules
- audit_logs
- export_jobs

### 4.2 集計・補助テーブル
- species_master
- taxa_groups
- region_master
- habitat_types
- weather_types
- time_series_aggregates
- observation_tags
- tag_master
- observation_datetime_history
- location_history
- model_inference_runs

---

## 5. ER上の主要関係

- 1 User は複数 Observation を作成できる
- 1 Observation は 1 MediaFile を持つ
- 1 Observation は 1 Location を持つ
- 1 Observation は 1 ObservationDateTime を持つ
- 1 Observation は 0..1 ObservationCondition を持つ
- 1 Observation は複数 AudioSegment を持つ
- 1 AudioSegment は複数 Detection を持つ
- 1 Detection は複数 DetectionCandidate を持つ
- 1 Detection は複数 ReviewerDecision を持ち得る
- 1 Detection は 1 ModelVersion により生成される
- 1 Observation は複数 AccessControlRule を持ち得る
- 1 Observation は複数 ProcessingJob に関係する

---

## 6. テーブル定義詳細

## 6.1 users

### 用途
利用者情報を保持する。

### カラム定義

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | ユーザーID |
| email | varchar(320) | NO | UK | メールアドレス |
| display_name | varchar(200) | NO |  | 表示名 |
| organization | varchar(200) | YES |  | 所属 |
| status | varchar(30) | NO |  | active / inactive / suspended |
| password_hash | text | YES |  | 外部認証時はNULL可 |
| last_login_at | timestamptz | YES |  | 最終ログイン |
| created_at | timestamptz | NO |  | 作成日時 |
| updated_at | timestamptz | NO |  | 更新日時 |
| deleted_at | timestamptz | YES |  | 論理削除 |

### インデックス
- unique index on `email`
- index on `status`

---

## 6.2 roles

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | ロールID |
| role_code | varchar(50) | NO | UK | observer / reviewer / admin |
| role_name | varchar(100) | NO |  | ロール名 |
| created_at | timestamptz | NO |  | 作成日時 |

---

## 6.3 user_roles

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | ID |
| user_id | uuid | NO | FK users(id) | ユーザー |
| role_id | uuid | NO | FK roles(id) | ロール |
| granted_at | timestamptz | NO |  | 付与日時 |
| granted_by_user_id | uuid | YES | FK users(id) | 付与者 |

### 制約
- unique (`user_id`, `role_id`)

---

## 6.4 species_master

### 用途
種マスタを保持する。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | 種ID |
| species_code | varchar(100) | NO | UK | システム内種コード |
| scientific_name | varchar(255) | NO |  | 学名 |
| common_name_ja | varchar(255) | YES |  | 和名 |
| common_name_en | varchar(255) | YES |  | 英名 |
| taxa_group_id | uuid | YES | FK taxa_groups(id) | 分類群 |
| is_protected | boolean | NO | default false | 保護対象種 |
| protection_level | varchar(50) | YES |  | 保護レベル |
| region_scope | varchar(100) | YES |  | 地域適用範囲 |
| active_flag | boolean | NO | default true | 有効フラグ |
| created_at | timestamptz | NO |  | 作成日時 |
| updated_at | timestamptz | NO |  | 更新日時 |

### インデックス
- unique index on `species_code`
- index on `is_protected`
- index on `taxa_group_id`

---

## 6.5 taxa_groups

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | ID |
| group_code | varchar(50) | NO | UK | bird / amphibian / insect |
| group_name | varchar(100) | NO |  | 分類群名 |

---

## 6.6 region_master

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | ID |
| region_code | varchar(50) | NO | UK | 地域コード |
| region_name | varchar(200) | NO |  | 地域名 |
| country_code | varchar(10) | YES |  | 国コード |
| timezone_name | varchar(100) | YES |  | IANA timezone |
| geom | geometry(MultiPolygon, 4326) | YES |  | 地域ポリゴン |

### インデックス
- unique index on `region_code`
- GiST index on `geom`

---

## 6.7 observations

### 用途
観測の親レコード。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | 観測ID |
| user_id | uuid | NO | FK users(id) | 登録者 |
| media_file_id | uuid | NO | FK media_files(id) | メディア |
| location_id | uuid | NO | FK locations(id) | 位置 |
| observation_datetime_id | uuid | NO | FK observation_datetimes(id) | 日時 |
| observation_condition_id | uuid | YES | FK observation_conditions(id) | 観測条件 |
| source_type | varchar(50) | NO |  | mobile_video / imported / batch |
| quality_score | numeric(5,4) | YES |  | 観測品質 |
| visibility_level | varchar(30) | NO |  | public / masked / restricted / private |
| status | varchar(30) | NO |  | uploaded / processing / analyzed / reviewed / failed |
| note | text | YES |  | 備考 |
| place_name | varchar(255) | YES |  | 地点名 |
| current_top_detection_id | uuid | YES | FK detections(id) | 代表検出 |
| created_at | timestamptz | NO |  | 作成日時 |
| updated_at | timestamptz | NO |  | 更新日時 |
| deleted_at | timestamptz | YES |  | 論理削除 |

### インデックス
- index on `user_id`
- index on `status`
- index on `visibility_level`
- index on `created_at`
- partial index on `deleted_at IS NULL`

---

## 6.8 media_files

### 用途
元動画および派生メディアファイル情報。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | メディアID |
| original_filename | varchar(500) | NO |  | 元ファイル名 |
| storage_bucket | varchar(200) | NO |  | ストレージバケット |
| storage_path | text | NO |  | 保存先パス |
| media_type | varchar(30) | NO |  | video / audio / image |
| mime_type | varchar(100) | NO |  | MIME |
| file_size_bytes | bigint | NO |  | サイズ |
| duration_seconds | numeric(10,3) | YES |  | 再生時間 |
| video_width | integer | YES |  | 幅 |
| video_height | integer | YES |  | 高さ |
| audio_sample_rate | integer | YES |  | サンプルレート |
| audio_channels | integer | YES |  | チャネル数 |
| codec | varchar(100) | YES |  | コーデック |
| checksum_sha256 | char(64) | YES | UK | 重複検出 |
| uploaded_at | timestamptz | NO |  | アップロード日時 |
| created_at | timestamptz | NO |  | 作成日時 |

### インデックス
- unique index on `checksum_sha256` where checksum_sha256 is not null
- index on `media_type`
- index on `uploaded_at`

---

## 6.9 locations

### 用途
観測位置情報。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | 位置ID |
| latitude | numeric(9,6) | NO |  | 緯度 |
| longitude | numeric(9,6) | NO |  | 経度 |
| altitude | numeric(8,2) | YES |  | 標高 |
| gps_accuracy_m | numeric(8,2) | YES |  | GPS精度 |
| location_precision | varchar(30) | NO |  | gps / manual / estimated / masked |
| manually_corrected | boolean | NO | default false | 手動補正有無 |
| region_id | uuid | YES | FK region_master(id) | 地域 |
| geom | geometry(Point, 4326) | NO |  | 地理点 |
| masking_policy | varchar(30) | NO |  | none / rounded / hidden |
| created_at | timestamptz | NO |  | 作成日時 |
| updated_at | timestamptz | NO |  | 更新日時 |

### 制約
- check latitude between -90 and 90
- check longitude between -180 and 180
- check gps_accuracy_m >= 0

### インデックス
- GiST index on `geom`
- index on `region_id`
- index on `location_precision`

---

## 6.10 location_history

### 用途
位置補正履歴。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | 履歴ID |
| location_id | uuid | NO | FK locations(id) | 対象位置 |
| changed_by_user_id | uuid | YES | FK users(id) | 変更者 |
| old_latitude | numeric(9,6) | YES |  | 旧値 |
| old_longitude | numeric(9,6) | YES |  | 旧値 |
| new_latitude | numeric(9,6) | YES |  | 新値 |
| new_longitude | numeric(9,6) | YES |  | 新値 |
| change_reason | text | YES |  | 変更理由 |
| changed_at | timestamptz | NO |  | 変更日時 |

---

## 6.11 observation_datetimes

### 用途
観測日時とタイムゾーンを保持する中核テーブル。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | ID |
| recorded_at_original | timestamptz | YES |  | 原本日時 |
| recorded_at_local | timestamptz | YES |  | 採用ローカル日時 |
| recorded_at_utc | timestamptz | YES |  | UTC |
| original_datetime_text | varchar(100) | YES |  | 元文字列 |
| timezone_original | varchar(100) | YES |  | 元TZ |
| timezone_resolved | varchar(100) | YES |  | 確定TZ |
| timezone_status | varchar(30) | NO |  | resolved / inferred / unknown |
| datetime_source_type | varchar(30) | NO |  | metadata / device / manual / estimated |
| datetime_precision | varchar(30) | NO |  | accurate / corrected / estimated / unknown |
| corrected_by_user_id | uuid | YES | FK users(id) | 補正者 |
| corrected_reason | text | YES |  | 補正理由 |
| created_at | timestamptz | NO |  | 作成日時 |
| updated_at | timestamptz | NO |  | 更新日時 |

### インデックス
- index on `recorded_at_utc`
- index on `recorded_at_local`
- index on `timezone_resolved`
- index on `datetime_precision`

---

## 6.12 observation_datetime_history

### 用途
日時補正履歴。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | 履歴ID |
| observation_datetime_id | uuid | NO | FK observation_datetimes(id) | 対象 |
| changed_by_user_id | uuid | YES | FK users(id) | 変更者 |
| old_recorded_at_local | timestamptz | YES |  | 旧値 |
| new_recorded_at_local | timestamptz | YES |  | 新値 |
| old_timezone_resolved | varchar(100) | YES |  | 旧TZ |
| new_timezone_resolved | varchar(100) | YES |  | 新TZ |
| change_reason | text | YES |  | 理由 |
| changed_at | timestamptz | NO |  | 変更日時 |

---

## 6.13 observation_conditions

### 用途
観測時環境条件。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | ID |
| weather_code | varchar(50) | YES | FK weather_types(weather_code) | 天候 |
| temperature_c | numeric(5,2) | YES |  | 気温 |
| humidity_pct | numeric(5,2) | YES |  | 湿度 |
| wind_level | varchar(30) | YES |  | none / low / medium / high |
| ambient_noise_db | numeric(6,2) | YES |  | 周辺騒音 |
| habitat_type_code | varchar(50) | YES | FK habitat_types(habitat_type_code) | 生息環境 |
| land_use_type | varchar(100) | YES |  | 土地利用区分 |
| extra_attributes | jsonb | YES |  | 拡張属性 |
| created_at | timestamptz | NO |  | 作成日時 |

### 制約
- check humidity_pct between 0 and 100

### インデックス
- index on `weather_code`
- index on `habitat_type_code`
- GIN index on `extra_attributes`

---

## 6.14 habitat_types

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| habitat_type_code | varchar(50) | NO | PK | habitat code |
| habitat_name | varchar(100) | NO |  | 名称 |

---

## 6.15 weather_types

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| weather_code | varchar(50) | NO | PK | weather code |
| weather_name | varchar(100) | NO |  | 名称 |

---

## 6.16 audio_segments

### 用途
音声前処理後の分析区間。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | 区間ID |
| observation_id | uuid | NO | FK observations(id) | 観測 |
| start_sec | numeric(10,3) | NO |  | 開始秒 |
| end_sec | numeric(10,3) | NO |  | 終了秒 |
| duration_sec | numeric(10,3) | NO |  | 長さ |
| preprocessing_version | varchar(100) | NO |  | 前処理版 |
| quality_score | numeric(5,4) | YES |  | 品質 |
| human_voice_flag | boolean | NO | default false | 人声混入 |
| wind_noise_flag | boolean | NO | default false | 風雑音 |
| traffic_noise_flag | boolean | NO | default false | 交通音 |
| audio_storage_path | text | YES |  | 派生音声パス |
| spectrogram_storage_path | text | YES |  | スペクトログラムパス |
| created_at | timestamptz | NO |  | 作成日時 |

### 制約
- check start_sec >= 0
- check end_sec > start_sec
- check duration_sec = round(end_sec - start_sec, 3) OR duration_sec > 0

### インデックス
- index on `observation_id`
- index on (`observation_id`, `start_sec`)
- index on `quality_score`

---

## 6.17 model_versions

### 用途
利用モデルの版管理。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | モデルID |
| model_name | varchar(200) | NO |  | モデル名 |
| model_family | varchar(100) | NO |  | foundation / regional / custom |
| version_label | varchar(100) | NO |  | 版 |
| supported_taxa | varchar(255) | YES |  | 対象分類群 |
| training_region | varchar(100) | YES |  | 学習地域 |
| pipeline_version | varchar(100) | NO |  | パイプライン版 |
| artifact_uri | text | YES |  | モデル配置先 |
| released_at | timestamptz | YES |  | リリース日時 |
| active_flag | boolean | NO | default true | 有効フラグ |
| created_at | timestamptz | NO |  | 作成日時 |

### 制約
- unique (`model_name`, `version_label`)

### インデックス
- index on `model_family`
- index on `active_flag`

---

## 6.18 detections

### 用途
音声区間単位の推論結果ヘッダ。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | 検出ID |
| audio_segment_id | uuid | NO | FK audio_segments(id) | 音声区間 |
| model_version_id | uuid | NO | FK model_versions(id) | モデル |
| detection_confidence | numeric(5,4) | NO |  | 代表信頼度 |
| detection_rank | integer | NO |  | 区間内順位 |
| review_status | varchar(30) | NO |  | pending / confirmed / rejected / needs_second_review |
| review_required_flag | boolean | NO | default true | レビュー要否 |
| false_positive_risk | numeric(5,4) | YES |  | 誤検知リスク |
| detection_status | varchar(30) | NO |  | active / superseded / invalidated |
| inferred_at | timestamptz | NO |  | 推論日時 |
| created_at | timestamptz | NO |  | 作成日時 |

### 制約
- check detection_confidence between 0 and 1
- check false_positive_risk is null or false_positive_risk between 0 and 1

### インデックス
- index on `audio_segment_id`
- index on `model_version_id`
- index on `review_status`
- index on `detection_confidence desc`

---

## 6.19 detection_candidates

### 用途
推論候補詳細。1 detection に複数候補。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | 候補ID |
| detection_id | uuid | NO | FK detections(id) | 検出 |
| species_id | uuid | YES | FK species_master(id) | 種 |
| common_name_snapshot | varchar(255) | YES |  | 表示用スナップショット |
| scientific_name_snapshot | varchar(255) | YES |  | 表示用スナップショット |
| rank_order | integer | NO |  | 順位 |
| confidence_score | numeric(5,4) | NO |  | 信頼度 |
| is_unknown | boolean | NO | default false | 不明候補 |
| is_protected_snapshot | boolean | NO | default false | 作成時点保護フラグ |
| created_at | timestamptz | NO |  | 作成日時 |

### 制約
- unique (`detection_id`, `rank_order`)
- check confidence_score between 0 and 1

### インデックス
- index on `detection_id`
- index on `species_id`
- index on (`species_id`, `confidence_score desc`)

---

## 6.20 reviewer_decisions

### 用途
専門家レビュー結果。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | レビューID |
| detection_id | uuid | NO | FK detections(id) | 検出 |
| reviewer_user_id | uuid | NO | FK users(id) | レビュアー |
| decision_type | varchar(30) | NO |  | confirmed / rejected / corrected / hold |
| final_species_id | uuid | YES | FK species_master(id) | 最終種 |
| comment | text | YES |  | コメント |
| mark_as_training_candidate | boolean | NO | default false | 学習候補 |
| decision_version | integer | NO | default 1 | レビュー版 |
| reviewed_at | timestamptz | NO |  | 実施日時 |
| created_at | timestamptz | NO |  | 作成日時 |

### インデックス
- index on `detection_id`
- index on `reviewer_user_id`
- index on `final_species_id`
- index on `reviewed_at`

---

## 6.21 processing_jobs

### 用途
非同期処理ジョブ。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | ジョブID |
| observation_id | uuid | YES | FK observations(id) | 観測 |
| job_type | varchar(50) | NO |  | observation_pipeline / export / reprocess |
| status | varchar(30) | NO |  | queued / running / completed / failed / cancelled |
| progress_pct | integer | YES |  | 進捗 |
| current_step | varchar(100) | YES |  | 現在処理 |
| requested_by_user_id | uuid | YES | FK users(id) | 起票者 |
| model_version_id | uuid | YES | FK model_versions(id) | 使用モデル |
| pipeline_version | varchar(100) | YES |  | 処理パイプライン版 |
| started_at | timestamptz | YES |  | 開始 |
| finished_at | timestamptz | YES |  | 終了 |
| error_code | varchar(100) | YES |  | エラー |
| error_message | text | YES |  | 詳細 |
| created_at | timestamptz | NO |  | 作成日時 |

### 制約
- check progress_pct is null or progress_pct between 0 and 100

### インデックス
- index on `observation_id`
- index on `status`
- index on `job_type`
- index on `created_at`

---

## 6.22 model_inference_runs

### 用途
再現性向上のための推論実行ログ。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | 実行ID |
| job_id | uuid | NO | FK processing_jobs(id) | ジョブ |
| model_version_id | uuid | NO | FK model_versions(id) | モデル |
| preprocessing_version | varchar(100) | NO |  | 前処理版 |
| inference_parameters | jsonb | YES |  | 推論パラメータ |
| started_at | timestamptz | YES |  | 開始 |
| finished_at | timestamptz | YES |  | 終了 |
| created_at | timestamptz | NO |  | 作成日時 |

### インデックス
- index on `job_id`
- index on `model_version_id`
- GIN index on `inference_parameters`

---

## 6.23 seasonal_rules

### 用途
地域・分類群別の季節区分ルール。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | ルールID |
| region_id | uuid | YES | FK region_master(id) | 地域 |
| taxa_group_id | uuid | YES | FK taxa_groups(id) | 分類群 |
| rule_version | varchar(50) | NO |  | 版 |
| season_name | varchar(100) | NO |  | season 名 |
| start_month | integer | NO |  | 開始月 |
| end_month | integer | NO |  | 終了月 |
| description | text | YES |  | 説明 |
| active_flag | boolean | NO | default true | 有効 |
| created_at | timestamptz | NO |  | 作成日時 |

### 制約
- check start_month between 1 and 12
- check end_month between 1 and 12

### インデックス
- index on `region_id`
- index on `taxa_group_id`
- index on `rule_version`
- index on `active_flag`

---

## 6.24 access_control_rules

### 用途
観測データの公開制御。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | ルールID |
| observation_id | uuid | NO | FK observations(id) | 対象観測 |
| target_scope | varchar(50) | NO |  | public / researcher / admin |
| visibility_rule | varchar(30) | NO |  | public / masked / restricted / private |
| coordinates_masked | boolean | NO | default false | 座標マスク |
| datetime_masked | boolean | NO | default false | 日時マスク |
| applied_reason | text | YES |  | 適用理由 |
| active_flag | boolean | NO | default true | 有効 |
| created_by_user_id | uuid | YES | FK users(id) | 作成者 |
| created_at | timestamptz | NO |  | 作成日時 |

### インデックス
- index on `observation_id`
- index on `visibility_rule`
- index on `active_flag`

---

## 6.25 protected_species_rules

### 用途
保護対象種に対する表示制御ルール。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | ルールID |
| species_id | uuid | NO | FK species_master(id) | 種 |
| visibility_rule | varchar(30) | NO |  | masked / restricted / private |
| coordinate_rounding_digits | integer | YES |  | 丸め桁数 |
| datetime_mask_policy | varchar(30) | YES |  | none / day_only / month_only |
| active_flag | boolean | NO | default true | 有効 |
| created_at | timestamptz | NO |  | 作成日時 |

### インデックス
- unique index on (`species_id`) where active_flag = true

---

## 6.26 tag_master

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | タグID |
| tag_name | varchar(100) | NO | UK | タグ名 |
| created_at | timestamptz | NO |  | 作成日時 |

---

## 6.27 observation_tags

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | ID |
| observation_id | uuid | NO | FK observations(id) | 観測 |
| tag_id | uuid | NO | FK tag_master(id) | タグ |

### 制約
- unique (`observation_id`, `tag_id`)

### インデックス
- index on `tag_id`

---

## 6.28 time_series_aggregates

### 用途
分析高速化用集計テーブル。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | 集計ID |
| aggregation_level | varchar(20) | NO |  | hour / day / week / month / season / year |
| aggregation_timezone | varchar(100) | NO |  | 集計TZ |
| bucket_start_at | timestamptz | NO |  | バケット開始 |
| bucket_label | varchar(50) | NO |  | 2026-04, 2026-W12 等 |
| region_id | uuid | YES | FK region_master(id) | 地域 |
| species_id | uuid | YES | FK species_master(id) | 種 |
| taxa_group_id | uuid | YES | FK taxa_groups(id) | 分類群 |
| occurrence_count | bigint | NO |  | 件数 |
| reviewed_count | bigint | NO |  | レビュー済み件数 |
| avg_confidence | numeric(5,4) | YES |  | 平均信頼度 |
| recomputed_at | timestamptz | NO |  | 再計算日時 |

### 制約
- unique (`aggregation_level`, `aggregation_timezone`, `bucket_start_at`, `region_id`, `species_id`, `taxa_group_id`)

### インデックス
- index on (`aggregation_level`, `bucket_start_at`)
- index on `species_id`
- index on `region_id`
- index on `aggregation_timezone`

---

## 6.29 export_jobs

### 用途
CSV / GeoJSON 等のエクスポートジョブ。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | エクスポートID |
| requested_by_user_id | uuid | NO | FK users(id) | 起票者 |
| report_type | varchar(50) | NO |  | species_occurrence 等 |
| output_format | varchar(20) | NO |  | csv / json / geojson |
| filter_json | jsonb | YES |  | 条件 |
| status | varchar(30) | NO |  | queued / running / completed / failed |
| result_storage_path | text | YES |  | 出力先 |
| expires_at | timestamptz | YES |  | 期限 |
| created_at | timestamptz | NO |  | 作成日時 |
| finished_at | timestamptz | YES |  | 完了日時 |

### インデックス
- index on `requested_by_user_id`
- index on `status`
- GIN index on `filter_json`

---

## 6.30 audit_logs

### 用途
重要操作の監査ログ。

| カラム名 | 型 | NULL | 制約 | 説明 |
|---|---|---:|---|---|
| id | uuid | NO | PK | 監査ID |
| actor_user_id | uuid | YES | FK users(id) | 操作者 |
| action_type | varchar(100) | NO |  | action code |
| target_table | varchar(100) | YES |  | 対象テーブル |
| target_id | uuid | YES |  | 対象ID |
| request_id | varchar(100) | YES |  | リクエスト識別 |
| before_json | jsonb | YES |  | 変更前 |
| after_json | jsonb | YES |  | 変更後 |
| ip_address | inet | YES |  | IP |
| user_agent | text | YES |  | UA |
| created_at | timestamptz | NO |  | 作成日時 |

### インデックス
- index on `actor_user_id`
- index on `action_type`
- index on (`target_table`, `target_id`)
- index on `created_at`
- GIN index on `before_json`
- GIN index on `after_json`

---

## 7. 推奨DDL断片

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE users (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    email varchar(320) NOT NULL UNIQUE,
    display_name varchar(200) NOT NULL,
    organization varchar(200),
    status varchar(30) NOT NULL DEFAULT 'active',
    password_hash text,
    last_login_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz
);

CREATE TABLE locations (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    latitude numeric(9,6) NOT NULL CHECK (latitude BETWEEN -90 AND 90),
    longitude numeric(9,6) NOT NULL CHECK (longitude BETWEEN -180 AND 180),
    altitude numeric(8,2),
    gps_accuracy_m numeric(8,2) CHECK (gps_accuracy_m >= 0),
    location_precision varchar(30) NOT NULL,
    manually_corrected boolean NOT NULL DEFAULT false,
    region_id uuid,
    geom geometry(Point, 4326) NOT NULL,
    masking_policy varchar(30) NOT NULL DEFAULT 'none',
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_locations_geom ON locations USING GIST (geom);

CREATE TABLE observation_datetimes (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    recorded_at_original timestamptz,
    recorded_at_local timestamptz,
    recorded_at_utc timestamptz,
    original_datetime_text varchar(100),
    timezone_original varchar(100),
    timezone_resolved varchar(100),
    timezone_status varchar(30) NOT NULL,
    datetime_source_type varchar(30) NOT NULL,
    datetime_precision varchar(30) NOT NULL,
    corrected_by_user_id uuid,
    corrected_reason text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_observation_datetimes_utc ON observation_datetimes (recorded_at_utc);
CREATE INDEX idx_observation_datetimes_local ON observation_datetimes (recorded_at_local);
```

---

## 8. リレーション設計上の要点

### 8.1 Observation を中心にした正規化
- 観測本体を `observations` に集約
- 位置は `locations`
- 日時は `observation_datetimes`
- 観測条件は `observation_conditions`
- 音声区間は `audio_segments`
- 推論は `detections`
- 候補種は `detection_candidates`
- レビューは `reviewer_decisions`

この分離により、再処理時に日時や位置を不必要に複製しない構造とする。

### 8.2 原本と補正後の両保持
- 位置も日時も、原本と補正履歴を保持する
- 実務上の分析には補正後値を使う
- 監査や再現では原本値と履歴を参照する

### 8.3 推論結果と確定結果の分離
- `detections` / `detection_candidates` は機械判定
- `reviewer_decisions` は人手判定
- UI 上では混同しない

---

## 9. インデックス戦略

### 9.1 検索系
- `observations.status`
- `observation_datetimes.recorded_at_utc`
- `locations.geom`
- `detection_candidates.species_id`
- `detections.review_status`

### 9.2 分析系
- `time_series_aggregates` の複合 unique/index
- `observation_datetimes.timezone_resolved`
- `region_id`, `species_id` の複合検索

### 9.3 監査系
- `audit_logs.created_at`
- `audit_logs.actor_user_id`
- `audit_logs.target_table, target_id`

### 9.4 推奨複合インデックス例
```sql
CREATE INDEX idx_obs_status_created_at
    ON observations (status, created_at DESC);

CREATE INDEX idx_det_review_confidence
    ON detections (review_status, detection_confidence DESC);

CREATE INDEX idx_ts_species_bucket
    ON time_series_aggregates (species_id, bucket_start_at);
```

---

## 10. パーティショニング方針

データ量増加時は以下を検討する。

### 10.1 パーティション候補
- `observations`: 年月ベース
- `audio_segments`: observation created month ベース
- `detections`: inferred_at 月ベース
- `audit_logs`: created_at 月ベース
- `time_series_aggregates`: 年ベース

### 10.2 パーティショニング判断基準
- 観測件数が数千万を超える
- 音声区間・検出件数が急増する
- 監査ログ保持年数が長い
- 再計算対象が年単位になる

---

## 11. マスキング・公開制御設計

### 11.1 基本方針
- 原データは DB 内に完全保持する
- API 応答では権限に応じて加工した値を返す
- DB 上でも公開ルールを `access_control_rules` に明示記録する

### 11.2 位置マスキング例
- `none`: 精密座標
- `rounded`: 小数点以下丸め
- `hidden`: 非表示

### 11.3 日時マスキング例
- `none`: 秒まで
- `day_only`: 日付のみ
- `month_only`: 月単位のみ

---

## 12. 更新履歴管理

更新履歴が必要なテーブル:
- locations
- observation_datetimes
- access_control_rules
- reviewer_decisions
- species_master
- seasonal_rules

### 管理方法
- 単純項目変更: history テーブル
- 高頻度・汎用監査: audit_logs
- 重要な人手変更: changed_by / corrected_reason を必須化

---

## 13. データ品質チェック

### 13.1 位置
- 緯度経度範囲チェック
- GPS精度の負値禁止
- 異常に広域移動する連続観測の警告

### 13.2 日時
- UTC と local の整合確認
- IANA タイムゾーン妥当性
- 将来日時・極端な過去日時の警告
- 端末設定異常の検知

### 13.3 推論
- confidence の範囲チェック
- detection の重複順位禁止
- 候補順位の連続性検査

---

## 14. 推奨ビュー / マテリアライズドビュー

### 14.1 view_observation_full
観測、位置、日時、代表検出を結合した参照用ビュー。

### 14.2 mv_species_monthly_summary
月別・種別・地域別集計の高速参照用。

### 14.3 mv_review_quality_summary
レビュアー別件数、確定率、棄却率集計。

---

## 15. バックアップ・保持方針

### 15.1 バックアップ
- DB 日次フルバックアップ
- WAL アーカイブ
- Object Storage バージョニング有効化

### 15.2 保持期間
- 観測本体: 原則長期保持
- 監査ログ: 最低 1〜3 年
- 一時派生ファイル: ポリシーにより削除可
- エクスポート成果物: 有効期限付き保持

---

## 16. 将来拡張余地

- 画像解析結果テーブル追加
- eDNA データ連携テーブル追加
- 外部気象 API キャッシュテーブル追加
- 音源方向推定テーブル追加
- 個体識別補助テーブル追加
- 学習データセット管理テーブル追加

---

## 17. 実装時に続けて作るべきもの

次に作成すると良い成果物は以下。

1. PostgreSQL 用完全DDL  
2. Alembic 初期マイグレーション案  
3. SQLAlchemy ORM モデル雛形  
4. インデックス・パーティション運用ガイド  
5. サンプルクエリ集  
6. DBアクセス権限設計  

---

## 18. まとめ

本 DB 設計は、単なる観測記録保存ではなく、以下を中核にしている。

- **位置情報と日時情報の厳密管理**
- **AI 推論と専門家レビューの分離管理**
- **地図表示と時系列分析の両立**
- **再現性・監査性・保護制御の確保**
- **将来のモデル更新や学習資産化への対応**

この構成により、EcoAudio Mapper を PoC から実運用へ拡張しやすい土台とする。

---

以上

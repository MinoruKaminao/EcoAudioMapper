# 位置情報・日時情報付き動画音声による生物分布可視化システム
## API仕様書付き版

- 文書名: 位置情報・日時情報付き動画音声による生物分布可視化システム API仕様書付き版
- 版数: v1.2
- 作成日: 2026-04-18
- 想定プロジェクト名称: EcoAudio Mapper

---

## 1. 目的

本書は、位置情報・日時情報付き動画から音声を抽出し、生物候補を推定して地図上および時系列上で可視化するシステム **EcoAudio Mapper** の API 要件を定義する。  
本APIは、Webフロントエンド、モバイルクライアント、将来の外部連携システム、および管理者ツールから利用されることを想定する。

---

## 2. API基本方針

- API 形式は REST を基本とする
- データ形式は JSON を標準とする
- 動画アップロードは multipart/form-data を利用する
- 認証は Bearer Token 方式を基本とする
- 内部処理は非同期ジョブを前提とする
- 時刻は **ISO 8601** 形式で扱う
- 内部比較用として **UTC** を保持し、表示・分析にはローカル時刻も保持する
- 緯度経度は WGS84 を前提とする
- 稀少種や非公開観測地点は権限に応じてマスキングする

---

## 3. 共通仕様

### 3.1 ベースURL

```text
https://api.ecoaudio-mapper.example.com/v1
```

### 3.2 認証

```http
Authorization: Bearer <token>
```

### 3.3 共通ヘッダ

```http
Content-Type: application/json
Accept: application/json
X-Request-Id: <optional-client-request-id>
```

### 3.4 共通レスポンス構造

#### 正常系

```json
{
  "success": true,
  "data": {},
  "meta": {
    "request_id": "req_12345",
    "timestamp": "2026-04-18T08:30:00Z"
  }
}
```

#### 異常系

```json
{
  "success": false,
  "error": {
    "code": "OBSERVATION_NOT_FOUND",
    "message": "指定された観測データが見つかりません。",
    "details": {}
  },
  "meta": {
    "request_id": "req_12345",
    "timestamp": "2026-04-18T08:30:00Z"
  }
}
```

### 3.5 共通エラーコード

| コード | 意味 |
|---|---|
| UNAUTHORIZED | 認証失敗 |
| FORBIDDEN | 権限不足 |
| VALIDATION_ERROR | 入力不正 |
| NOT_FOUND | リソース不存在 |
| CONFLICT | 状態競合 |
| RATE_LIMITED | レート制限 |
| INTERNAL_ERROR | 内部エラー |
| OBSERVATION_NOT_FOUND | 観測データ不存在 |
| JOB_NOT_FOUND | ジョブ不存在 |
| MODEL_NOT_FOUND | モデル不存在 |
| REVIEW_NOT_ALLOWED | レビュー権限なし |
| PROTECTED_SPECIES_RESTRICTED | 保護対象種により制限 |

### 3.6 日時・タイムゾーン規約

#### APIで返す日時項目
- `recorded_at_original`
- `recorded_at_local`
- `recorded_at_utc`
- `timezone_original`
- `timezone_resolved`
- `timezone_status`
- `datetime_precision`

#### ルール
- 検索条件の `from` / `to` は ISO 8601 文字列で受け付ける
- タイムゾーン付き入力を優先する
- タイムゾーン無し入力は API で拒否するか、明示パラメータ `timezone` を必須とする
- 集計 API では `aggregation_timezone` を指定可能とする
- 季節判定は `aggregation_timezone` または観測地点の地域タイムゾーンを基準とする

---

## 4. リソース一覧

本APIは以下の主要リソースで構成する。

- Auth
- Users
- Observations
- Media Files
- Jobs
- Audio Segments
- Detections
- Species Candidates
- Reviews
- Maps
- Analytics
- Models
- Seasonal Rules
- Access Control
- Admin

---

## 5. 認証・ユーザーAPI

## 5.1 ログイン

### POST /auth/login

#### リクエスト

```json
{
  "email": "user@example.com",
  "password": "********"
}
```

#### レスポンス

```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOi...",
    "refresh_token": "rft_12345",
    "token_type": "Bearer",
    "expires_in": 3600,
    "user": {
      "user_id": "usr_001",
      "display_name": "Example User",
      "role": "observer"
    }
  }
}
```

## 5.2 自分のユーザー情報取得

### GET /users/me

#### レスポンス

```json
{
  "success": true,
  "data": {
    "user_id": "usr_001",
    "email": "user@example.com",
    "display_name": "Example User",
    "role": "observer",
    "organization": "Eco Lab"
  }
}
```

---

## 6. 観測登録API

## 6.1 動画アップロードと観測新規登録

### POST /observations

- Content-Type: `multipart/form-data`

#### フォーム項目

| 項目 | 必須 | 内容 |
|---|---:|---|
| file | ○ | 動画ファイル |
| observer_note | - | 観測メモ |
| place_name | - | 地点名 |
| latitude | - | 緯度 |
| longitude | - | 経度 |
| gps_accuracy | - | GPS精度 |
| recorded_at_original | - | 元撮影日時 |
| timezone_original | - | 元タイムゾーン |
| recorded_at_local | - | 補正後ローカル日時 |
| timezone_resolved | - | 確定タイムゾーン |
| datetime_precision | - | `accurate` / `corrected` / `estimated` / `unknown` |
| habitat_type | - | 生息環境 |
| weather | - | 天候 |
| temperature | - | 気温 |
| humidity | - | 湿度 |
| tags | - | カンマ区切りタグ |

#### レスポンス例

```json
{
  "success": true,
  "data": {
    "observation_id": "obs_1001",
    "job_id": "job_5001",
    "status": "uploaded",
    "media_file": {
      "original_filename": "field_20260418.mov",
      "duration_seconds": 94
    }
  }
}
```

## 6.2 観測一覧取得

### GET /observations

#### クエリパラメータ

| 項目 | 内容 |
|---|---|
| page | ページ番号 |
| per_page | 1ページ件数 |
| species_id | 種ID |
| review_status | review 状態 |
| confidence_gte | 信頼度下限 |
| recorded_from | 観測開始日時 |
| recorded_to | 観測終了日時 |
| timezone | フィルタ基準タイムゾーン |
| latitude | 中心緯度 |
| longitude | 中心经度 |
| radius_m | 半径メートル |
| habitat_type | 生息環境 |
| visibility_scope | 可視範囲 |

#### レスポンス例

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "observation_id": "obs_1001",
        "status": "analyzed",
        "recorded_at_local": "2026-04-18T06:15:21+09:00",
        "timezone_resolved": "Asia/Tokyo",
        "location": {
          "latitude": 35.1234,
          "longitude": 138.1234,
          "masked": false
        },
        "top_detection": {
          "species_id": "sp_001",
          "common_name": "ウグイス",
          "confidence": 0.93
        }
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 135
    }
  }
}
```

## 6.3 観測詳細取得

### GET /observations/{observation_id}

#### レスポンス例

```json
{
  "success": true,
  "data": {
    "observation_id": "obs_1001",
    "status": "analyzed",
    "note": "林縁部で撮影",
    "media_file": {
      "media_file_id": "med_9001",
      "original_filename": "field_20260418.mov",
      "duration_seconds": 94,
      "storage_url": "https://signed.example.com/media/med_9001"
    },
    "location": {
      "latitude": 35.1234,
      "longitude": 138.1234,
      "altitude": 112.4,
      "gps_accuracy": 8.5,
      "location_precision": "gps",
      "masking_policy": "none"
    },
    "datetime": {
      "recorded_at_original": "2026-04-18T06:15:18+09:00",
      "recorded_at_local": "2026-04-18T06:15:21+09:00",
      "recorded_at_utc": "2026-04-17T21:15:21Z",
      "timezone_original": "Asia/Tokyo",
      "timezone_resolved": "Asia/Tokyo",
      "timezone_status": "resolved",
      "datetime_precision": "accurate"
    },
    "condition": {
      "weather": "cloudy",
      "temperature": 15.2,
      "humidity": 78.0,
      "wind_level": "low",
      "ambient_noise_level": 28.5,
      "habitat_type": "forest_edge"
    },
    "detections_summary": [
      {
        "detection_id": "det_701",
        "segment_start_sec": 12.0,
        "segment_end_sec": 15.5,
        "top_species": "ウグイス",
        "confidence": 0.93,
        "review_status": "pending"
      }
    ]
  }
}
```

## 6.4 観測情報更新

### PATCH /observations/{observation_id}

#### リクエスト例

```json
{
  "note": "林道入口付近",
  "place_name": "北側観測点A",
  "location": {
    "latitude": 35.1235,
    "longitude": 138.1235,
    "gps_accuracy": 5.0
  },
  "datetime": {
    "recorded_at_local": "2026-04-18T06:15:21+09:00",
    "timezone_resolved": "Asia/Tokyo",
    "datetime_precision": "corrected",
    "corrected_reason": "端末時刻補正"
  }
}
```

## 6.5 観測削除

### DELETE /observations/{observation_id}

#### レスポンス例

```json
{
  "success": true,
  "data": {
    "observation_id": "obs_1001",
    "deleted": true
  }
}
```

---

## 7. ジョブAPI

## 7.1 解析ジョブ取得

### GET /jobs/{job_id}

#### レスポンス例

```json
{
  "success": true,
  "data": {
    "job_id": "job_5001",
    "job_type": "observation_pipeline",
    "status": "running",
    "progress": 65,
    "current_step": "bioacoustic_inference",
    "started_at": "2026-04-18T08:00:00Z",
    "updated_at": "2026-04-18T08:02:14Z",
    "observation_id": "obs_1001"
  }
}
```

## 7.2 ジョブ再実行

### POST /jobs/{job_id}/retry

#### レスポンス例

```json
{
  "success": true,
  "data": {
    "job_id": "job_5002",
    "previous_job_id": "job_5001",
    "status": "queued"
  }
}
```

---

## 8. 音声区間・推論結果API

## 8.1 音声区間一覧取得

### GET /observations/{observation_id}/segments

#### レスポンス例

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "audio_segment_id": "seg_301",
        "start_sec": 12.0,
        "end_sec": 15.5,
        "quality_score": 0.88,
        "human_voice_flag": false,
        "wind_noise_flag": false,
        "traffic_noise_flag": true
      }
    ]
  }
}
```

## 8.2 推論結果一覧取得

### GET /observations/{observation_id}/detections

#### クエリパラメータ
- `review_status`
- `confidence_gte`
- `species_id`
- `include_candidates=true|false`

#### レスポンス例

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "detection_id": "det_701",
        "audio_segment_id": "seg_301",
        "detection_confidence": 0.93,
        "review_status": "pending",
        "review_required_flag": true,
        "model": {
          "model_version_id": "mdl_201",
          "model_name": "Perch-like Regional Model",
          "version_label": "2026.04-ja-central-01"
        },
        "candidates": [
          {
            "species_id": "sp_001",
            "common_name": "ウグイス",
            "scientific_name": "Horornis diphone",
            "rank_order": 1,
            "confidence_score": 0.93,
            "is_protected": false
          },
          {
            "species_id": "sp_010",
            "common_name": "センダイムシクイ",
            "scientific_name": "Phylloscopus coronatus",
            "rank_order": 2,
            "confidence_score": 0.41,
            "is_protected": false
          }
        ]
      }
    ]
  }
}
```

## 8.3 単一推論結果取得

### GET /detections/{detection_id}

---

## 9. レビューAPI

## 9.1 レビュー登録

### POST /detections/{detection_id}/reviews

#### リクエスト例

```json
{
  "decision_type": "confirmed",
  "final_species_id": "sp_001",
  "comment": "鳴声パターンと時間帯から妥当",
  "mark_as_training_candidate": true
}
```

#### レスポンス例

```json
{
  "success": true,
  "data": {
    "reviewer_decision_id": "rev_801",
    "detection_id": "det_701",
    "decision_type": "confirmed",
    "final_species_id": "sp_001",
    "reviewed_at": "2026-04-18T08:15:10Z"
  }
}
```

## 9.2 レビュー履歴取得

### GET /detections/{detection_id}/reviews

---

## 10. 地図API

## 10.1 地図表示用観測点取得

### GET /map/observations

#### クエリパラメータ

| 項目 | 内容 |
|---|---|
| bbox | `minLng,minLat,maxLng,maxLat` |
| zoom | ズームレベル |
| species_id | 種ID |
| recorded_from | 開始日時 |
| recorded_to | 終了日時 |
| aggregation_timezone | 集計基準タイムゾーン |
| season | 季節区分 |
| year | 年 |
| confidence_gte | 信頼度下限 |
| cluster | `true/false` |
| heatmap | `true/false` |

#### レスポンス例

```json
{
  "success": true,
  "data": {
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "Point",
          "coordinates": [138.1234, 35.1234]
        },
        "properties": {
          "observation_id": "obs_1001",
          "recorded_at_local": "2026-04-18T06:15:21+09:00",
          "species_id": "sp_001",
          "common_name": "ウグイス",
          "confidence": 0.93,
          "masked": false
        }
      }
    ]
  }
}
```

## 10.2 ヒートマップ集計取得

### GET /map/heatmap

#### 主なパラメータ
- `species_id`
- `recorded_from`
- `recorded_to`
- `aggregation_timezone`
- `grid_size`
- `season`
- `year`

---

## 11. 分析API

## 11.1 種別出現集計

### GET /analytics/species-occurrence

#### クエリパラメータ

| 項目 | 内容 |
|---|---|
| species_id | 種ID |
| region_code | 地域コード |
| aggregation_level | `hour` / `day` / `week` / `month` / `season` / `year` |
| aggregation_timezone | 集計タイムゾーン |
| recorded_from | 開始日時 |
| recorded_to | 終了日時 |
| confidence_gte | 信頼度下限 |
| reviewed_only | `true/false` |

#### レスポンス例

```json
{
  "success": true,
  "data": {
    "aggregation_level": "month",
    "aggregation_timezone": "Asia/Tokyo",
    "items": [
      {
        "bucket": "2026-03",
        "species_id": "sp_001",
        "common_name": "ウグイス",
        "occurrence_count": 25,
        "avg_confidence": 0.87
      },
      {
        "bucket": "2026-04",
        "species_id": "sp_001",
        "common_name": "ウグイス",
        "occurrence_count": 41,
        "avg_confidence": 0.90
      }
    ]
  }
}
```

## 11.2 季節比較

### GET /analytics/seasonal-comparison

#### 主なパラメータ
- `species_id`
- `region_code`
- `year`
- `aggregation_timezone`

## 11.3 年次比較

### GET /analytics/yearly-comparison

#### 主なパラメータ
- `species_id`
- `region_code`
- `from_year`
- `to_year`
- `aggregation_timezone`

## 11.4 同一地点経年比較

### GET /analytics/location-trend

#### 主なパラメータ
- `latitude`
- `longitude`
- `radius_m`
- `species_id`
- `aggregation_level`
- `aggregation_timezone`

## 11.5 レポートエクスポート

### POST /analytics/exports

#### リクエスト例

```json
{
  "report_type": "species_occurrence",
  "format": "csv",
  "filters": {
    "species_id": "sp_001",
    "recorded_from": "2026-01-01T00:00:00+09:00",
    "recorded_to": "2026-04-30T23:59:59+09:00",
    "aggregation_timezone": "Asia/Tokyo"
  }
}
```

#### レスポンス例

```json
{
  "success": true,
  "data": {
    "export_job_id": "exp_100",
    "status": "queued"
  }
}
```

---

## 12. モデル・季節ルール・管理API

## 12.1 モデル一覧取得

### GET /models

## 12.2 モデル詳細取得

### GET /models/{model_version_id}

## 12.3 季節区分ルール一覧取得

### GET /seasonal-rules

#### クエリパラメータ
- `region_code`
- `taxa_group`
- `rule_version`

## 12.4 季節区分ルール登録

### POST /seasonal-rules

#### リクエスト例

```json
{
  "region_code": "JP-22",
  "taxa_group": "bird",
  "rule_version": "v1",
  "season_name": "breeding",
  "start_month": 4,
  "end_month": 7,
  "description": "中部地方鳥類繁殖期"
}
```

## 12.5 公開制御設定更新

### PATCH /observations/{observation_id}/access-control

#### リクエスト例

```json
{
  "visibility_rule": "restricted",
  "coordinates_masked": true,
  "datetime_masked": false,
  "applied_reason": "protected_species_policy"
}
```

---

## 13. 管理者API

## 13.1 ユーザー一覧取得

### GET /admin/users

## 13.2 ユーザーロール更新

### PATCH /admin/users/{user_id}

#### リクエスト例

```json
{
  "role": "reviewer"
}
```

## 13.3 再処理要求

### POST /admin/observations/{observation_id}/reprocess

#### リクエスト例

```json
{
  "pipeline_version": "pipeline_2026_04",
  "model_version_id": "mdl_201",
  "reason": "model_updated"
}
```

## 13.4 監査ログ取得

### GET /admin/audit-logs

---

## 14. OpenAPI向け主要スキーマ案

## 14.1 Observation

```json
{
  "observation_id": "obs_1001",
  "status": "analyzed",
  "note": "string",
  "location": {
    "latitude": 35.1234,
    "longitude": 138.1234,
    "altitude": 112.4,
    "gps_accuracy": 8.5,
    "location_precision": "gps",
    "masking_policy": "none"
  },
  "datetime": {
    "recorded_at_original": "2026-04-18T06:15:18+09:00",
    "recorded_at_local": "2026-04-18T06:15:21+09:00",
    "recorded_at_utc": "2026-04-17T21:15:21Z",
    "timezone_original": "Asia/Tokyo",
    "timezone_resolved": "Asia/Tokyo",
    "timezone_status": "resolved",
    "datetime_precision": "accurate"
  }
}
```

## 14.2 Detection

```json
{
  "detection_id": "det_701",
  "audio_segment_id": "seg_301",
  "detection_confidence": 0.93,
  "detection_rank": 1,
  "review_status": "pending",
  "review_required_flag": true,
  "false_positive_risk": 0.12,
  "candidates": []
}
```

## 14.3 ReviewerDecision

```json
{
  "reviewer_decision_id": "rev_801",
  "decision_type": "confirmed",
  "final_species_id": "sp_001",
  "comment": "string",
  "reviewed_at": "2026-04-18T08:15:10Z"
}
```

---

## 15. ステータス設計案

### 15.1 Observation.status
- `uploaded`
- `metadata_extracted`
- `processing`
- `analyzed`
- `review_pending`
- `reviewed`
- `failed`
- `deleted`

### 15.2 Job.status
- `queued`
- `running`
- `completed`
- `failed`
- `cancelled`

### 15.3 Detection.review_status
- `pending`
- `confirmed`
- `rejected`
- `needs_second_review`

### 15.4 AccessControl.visibility_rule
- `public`
- `masked`
- `restricted`
- `private`

---

## 16. バリデーション方針

- 緯度は `-90` 以上 `90` 以下
- 経度は `-180` 以上 `180` 以下
- `confidence` は `0.0` 以上 `1.0` 以下
- `gps_accuracy` は 0 以上
- `temperature` は現実的範囲で制限
- `humidity` は `0` 以上 `100` 以下
- `recorded_to >= recorded_from`
- `timezone_resolved` は IANA タイムゾーン名
- `aggregation_level` は定義済み enum のみ許容
- 保護対象種の詳細座標は管理者権限なしでは返却しない

---

## 17. API利用上の重要方針

- 地図系APIは、権限に応じて座標マスキング済みの値を返す
- 分析系APIは、**UTC ではなく指定タイムゾーン基準の集計**を返せるようにする
- 推論結果は「候補」であり、レビュー結果と区別して返す
- 再現性確保のため、モデルバージョンとパイプラインバージョンを常に保持する
- 日時精度が低い観測データは分析結果から除外または区別表示できるようにする

---

## 18. 将来拡張を考慮した追加API候補

- `POST /observations/bulk-import`
- `GET /analytics/environment-correlation`
- `GET /analytics/protected-species-summary`
- `POST /training-datasets`
- `GET /notifications`
- `POST /mobile/offline-sync`
- `GET /map/timeline-animation`

---

## 19. OpenAPIファイル分割案

```text
openapi/
  openapi.yaml
  paths/
    auth.yaml
    users.yaml
    observations.yaml
    jobs.yaml
    detections.yaml
    reviews.yaml
    map.yaml
    analytics.yaml
    models.yaml
    seasonal_rules.yaml
    admin.yaml
  components/
    schemas/
      common.yaml
      observation.yaml
      datetime.yaml
      location.yaml
      detection.yaml
      review.yaml
      analytics.yaml
    parameters/
      pagination.yaml
      datetime_filters.yaml
      geo_filters.yaml
    responses/
      common.yaml
      errors.yaml
```

---

## 20. 次段階で作成すべきもの

本API仕様書付き版の次段階として、以下を作成すると実装へ進みやすい。

1. OpenAPI YAML 完全版  
2. DB設計詳細版（テーブル定義、型、制約、インデックス）  
3. 権限マトリクス  
4. 非同期ジョブ状態遷移図  
5. FastAPI または Spring Boot 用の雛形構成  

---

以上

"""Initial schema for EcoAudio Mapper

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-04-18 09:10:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from geoalchemy2 import Geometry


# revision identifiers, used by Alembic.
revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.create_table(
        "roles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("role_code", sa.String(length=50), nullable=False),
        sa.Column("role_name", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("role_code", name="uq_roles_role_code"),
    )

    op.create_table(
        "taxa_groups",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("group_code", sa.String(length=50), nullable=False),
        sa.Column("group_name", sa.String(length=100), nullable=False),
        sa.UniqueConstraint("group_code", name="uq_taxa_groups_group_code"),
    )

    op.create_table(
        "region_master",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("region_code", sa.String(length=50), nullable=False),
        sa.Column("region_name", sa.String(length=200), nullable=False),
        sa.Column("country_code", sa.String(length=10)),
        sa.Column("timezone_name", sa.String(length=100)),
        sa.Column("geom", Geometry(geometry_type="MULTIPOLYGON", srid=4326)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("region_code", name="uq_region_master_region_code"),
    )
    op.create_index("idx_region_master_geom", "region_master", ["geom"], unique=False, postgresql_using="gist")

    op.create_table(
        "habitat_types",
        sa.Column("habitat_type_code", sa.String(length=50), primary_key=True),
        sa.Column("habitat_name", sa.String(length=100), nullable=False),
    )

    op.create_table(
        "weather_types",
        sa.Column("weather_code", sa.String(length=50), primary_key=True),
        sa.Column("weather_name", sa.String(length=100), nullable=False),
    )

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("display_name", sa.String(length=200), nullable=False),
        sa.Column("organization", sa.String(length=200)),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="active"),
        sa.Column("password_hash", sa.Text()),
        sa.Column("last_login_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
        sa.CheckConstraint("status IN ('active', 'inactive', 'suspended')", name="ck_users_status"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )

    op.create_table(
        "user_roles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("role_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("granted_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("granted_by_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.UniqueConstraint("user_id", "role_id", name="uq_user_roles_user_role"),
    )

    op.create_table(
        "species_master",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("species_code", sa.String(length=100), nullable=False),
        sa.Column("scientific_name", sa.String(length=255), nullable=False),
        sa.Column("common_name_ja", sa.String(length=255)),
        sa.Column("common_name_en", sa.String(length=255)),
        sa.Column("taxa_group_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("taxa_groups.id")),
        sa.Column("is_protected", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("protection_level", sa.String(length=50)),
        sa.Column("region_scope", sa.String(length=100)),
        sa.Column("active_flag", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("species_code", name="uq_species_master_species_code"),
    )
    op.create_index("idx_species_master_is_protected", "species_master", ["is_protected"], unique=False)

    op.create_table(
        "media_files",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("original_filename", sa.String(length=500), nullable=False),
        sa.Column("storage_bucket", sa.String(length=200), nullable=False),
        sa.Column("storage_path", sa.Text(), nullable=False),
        sa.Column("media_type", sa.String(length=30), nullable=False),
        sa.Column("mime_type", sa.String(length=100), nullable=False),
        sa.Column("file_size_bytes", sa.BigInteger(), nullable=False),
        sa.Column("duration_seconds", sa.Numeric(10, 3)),
        sa.Column("video_width", sa.Integer()),
        sa.Column("video_height", sa.Integer()),
        sa.Column("audio_sample_rate", sa.Integer()),
        sa.Column("audio_channels", sa.Integer()),
        sa.Column("codec", sa.String(length=100)),
        sa.Column("checksum_sha256", sa.String(length=64)),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint("media_type IN ('video', 'audio', 'image')", name="ck_media_files_media_type"),
        sa.CheckConstraint("file_size_bytes >= 0", name="ck_media_files_file_size"),
    )
    op.create_index(
        "uq_media_files_checksum_sha256",
        "media_files",
        ["checksum_sha256"],
        unique=True,
        postgresql_where=sa.text("checksum_sha256 IS NOT NULL"),
    )

    op.create_table(
        "locations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("latitude", sa.Numeric(9, 6), nullable=False),
        sa.Column("longitude", sa.Numeric(9, 6), nullable=False),
        sa.Column("altitude", sa.Numeric(8, 2)),
        sa.Column("gps_accuracy_m", sa.Numeric(8, 2)),
        sa.Column("location_precision", sa.String(length=30), nullable=False),
        sa.Column("manually_corrected", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("region_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("region_master.id")),
        sa.Column("geom", Geometry(geometry_type="POINT", srid=4326), nullable=False),
        sa.Column("masking_policy", sa.String(length=30), nullable=False, server_default="none"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint("latitude BETWEEN -90 AND 90", name="ck_locations_latitude"),
        sa.CheckConstraint("longitude BETWEEN -180 AND 180", name="ck_locations_longitude"),
        sa.CheckConstraint("gps_accuracy_m IS NULL OR gps_accuracy_m >= 0", name="ck_locations_gps_accuracy"),
        sa.CheckConstraint("location_precision IN ('gps', 'manual', 'estimated', 'masked')", name="ck_locations_location_precision"),
        sa.CheckConstraint("masking_policy IN ('none', 'rounded', 'hidden')", name="ck_locations_masking_policy"),
    )
    op.create_index("idx_locations_geom", "locations", ["geom"], unique=False, postgresql_using="gist")

    op.create_table(
        "location_history",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("location_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("locations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("changed_by_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("old_latitude", sa.Numeric(9, 6)),
        sa.Column("old_longitude", sa.Numeric(9, 6)),
        sa.Column("new_latitude", sa.Numeric(9, 6)),
        sa.Column("new_longitude", sa.Numeric(9, 6)),
        sa.Column("change_reason", sa.Text()),
        sa.Column("changed_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "observation_datetimes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("recorded_at_original", sa.DateTime(timezone=True)),
        sa.Column("recorded_at_local", sa.DateTime(timezone=True)),
        sa.Column("recorded_at_utc", sa.DateTime(timezone=True)),
        sa.Column("original_datetime_text", sa.String(length=100)),
        sa.Column("timezone_original", sa.String(length=100)),
        sa.Column("timezone_resolved", sa.String(length=100)),
        sa.Column("timezone_status", sa.String(length=30), nullable=False),
        sa.Column("datetime_source_type", sa.String(length=30), nullable=False),
        sa.Column("datetime_precision", sa.String(length=30), nullable=False),
        sa.Column("corrected_by_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("corrected_reason", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint("timezone_status IN ('resolved', 'inferred', 'unknown')", name="ck_observation_datetimes_timezone_status"),
        sa.CheckConstraint("datetime_source_type IN ('metadata', 'device', 'manual', 'estimated')", name="ck_observation_datetimes_source_type"),
        sa.CheckConstraint("datetime_precision IN ('accurate', 'corrected', 'estimated', 'unknown')", name="ck_observation_datetimes_precision"),
    )
    op.create_index("idx_observation_datetimes_utc", "observation_datetimes", ["recorded_at_utc"], unique=False)
    op.create_index("idx_observation_datetimes_local", "observation_datetimes", ["recorded_at_local"], unique=False)

    op.create_table(
        "observation_datetime_history",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("observation_datetime_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("observation_datetimes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("changed_by_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("old_recorded_at_local", sa.DateTime(timezone=True)),
        sa.Column("new_recorded_at_local", sa.DateTime(timezone=True)),
        sa.Column("old_timezone_resolved", sa.String(length=100)),
        sa.Column("new_timezone_resolved", sa.String(length=100)),
        sa.Column("change_reason", sa.Text()),
        sa.Column("changed_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "observation_conditions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("weather_code", sa.String(length=50), sa.ForeignKey("weather_types.weather_code")),
        sa.Column("temperature_c", sa.Numeric(5, 2)),
        sa.Column("humidity_pct", sa.Numeric(5, 2)),
        sa.Column("wind_level", sa.String(length=30)),
        sa.Column("ambient_noise_db", sa.Numeric(6, 2)),
        sa.Column("habitat_type_code", sa.String(length=50), sa.ForeignKey("habitat_types.habitat_type_code")),
        sa.Column("land_use_type", sa.String(length=100)),
        sa.Column("extra_attributes", postgresql.JSONB(astext_type=sa.Text())),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint("humidity_pct IS NULL OR humidity_pct BETWEEN 0 AND 100", name="ck_observation_conditions_humidity"),
        sa.CheckConstraint("temperature_c IS NULL OR temperature_c BETWEEN -100 AND 100", name="ck_observation_conditions_temperature"),
        sa.CheckConstraint("wind_level IS NULL OR wind_level IN ('none', 'low', 'medium', 'high')", name="ck_observation_conditions_wind"),
        sa.CheckConstraint("ambient_noise_db IS NULL OR ambient_noise_db >= 0", name="ck_observation_conditions_noise"),
    )

    op.create_table(
        "model_versions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("model_name", sa.String(length=200), nullable=False),
        sa.Column("model_family", sa.String(length=100), nullable=False),
        sa.Column("version_label", sa.String(length=100), nullable=False),
        sa.Column("supported_taxa", sa.String(length=255)),
        sa.Column("training_region", sa.String(length=100)),
        sa.Column("pipeline_version", sa.String(length=100), nullable=False),
        sa.Column("artifact_uri", sa.Text()),
        sa.Column("released_at", sa.DateTime(timezone=True)),
        sa.Column("active_flag", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint("model_family IN ('foundation', 'regional', 'custom')", name="ck_model_versions_family"),
        sa.UniqueConstraint("model_name", "version_label", name="uq_model_versions_name_version"),
    )

    op.create_table(
        "observations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("media_file_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("media_files.id"), nullable=False),
        sa.Column("location_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("locations.id"), nullable=False),
        sa.Column("observation_datetime_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("observation_datetimes.id"), nullable=False),
        sa.Column("observation_condition_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("observation_conditions.id")),
        sa.Column("source_type", sa.String(length=50), nullable=False),
        sa.Column("quality_score", sa.Numeric(5, 4)),
        sa.Column("visibility_level", sa.String(length=30), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("note", sa.Text()),
        sa.Column("place_name", sa.String(length=255)),
        sa.Column("current_top_detection_id", postgresql.UUID(as_uuid=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
        sa.CheckConstraint("source_type IN ('mobile_video', 'imported', 'batch')", name="ck_observations_source_type"),
        sa.CheckConstraint("quality_score IS NULL OR quality_score BETWEEN 0 AND 1", name="ck_observations_quality_score"),
        sa.CheckConstraint("visibility_level IN ('public', 'masked', 'restricted', 'private')", name="ck_observations_visibility_level"),
        sa.CheckConstraint(
            "status IN ('uploaded', 'metadata_extracted', 'processing', 'analyzed', 'review_pending', 'reviewed', 'failed', 'deleted')",
            name="ck_observations_status",
        ),
    )
    op.create_index("idx_observations_status", "observations", ["status"], unique=False)
    op.create_index("idx_observations_created_at", "observations", ["created_at"], unique=False)
    op.create_index("idx_observations_not_deleted", "observations", ["id"], unique=False, postgresql_where=sa.text("deleted_at IS NULL"))

    op.create_table(
        "audio_segments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("observation_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("observations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("start_sec", sa.Numeric(10, 3), nullable=False),
        sa.Column("end_sec", sa.Numeric(10, 3), nullable=False),
        sa.Column("duration_sec", sa.Numeric(10, 3), nullable=False),
        sa.Column("preprocessing_version", sa.String(length=100), nullable=False),
        sa.Column("quality_score", sa.Numeric(5, 4)),
        sa.Column("human_voice_flag", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("wind_noise_flag", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("traffic_noise_flag", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("audio_storage_path", sa.Text()),
        sa.Column("spectrogram_storage_path", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint("start_sec >= 0", name="ck_audio_segments_start_sec"),
        sa.CheckConstraint("end_sec > start_sec", name="ck_audio_segments_end_sec"),
        sa.CheckConstraint("duration_sec > 0", name="ck_audio_segments_duration_sec"),
    )
    op.create_index("idx_audio_segments_observation_start", "audio_segments", ["observation_id", "start_sec"], unique=False)

    op.create_table(
        "processing_jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("observation_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("observations.id", ondelete="CASCADE")),
        sa.Column("job_type", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("progress_pct", sa.Integer()),
        sa.Column("current_step", sa.String(length=100)),
        sa.Column("requested_by_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("model_version_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("model_versions.id")),
        sa.Column("pipeline_version", sa.String(length=100)),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.Column("error_code", sa.String(length=100)),
        sa.Column("error_message", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint("job_type IN ('observation_pipeline', 'export', 'reprocess')", name="ck_processing_jobs_job_type"),
        sa.CheckConstraint("status IN ('queued', 'running', 'completed', 'failed', 'cancelled')", name="ck_processing_jobs_status"),
        sa.CheckConstraint("progress_pct IS NULL OR progress_pct BETWEEN 0 AND 100", name="ck_processing_jobs_progress"),
    )

    op.create_table(
        "model_inference_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("job_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("processing_jobs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("model_version_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("model_versions.id"), nullable=False),
        sa.Column("preprocessing_version", sa.String(length=100), nullable=False),
        sa.Column("inference_parameters", postgresql.JSONB(astext_type=sa.Text())),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "detections",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("audio_segment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("audio_segments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("model_version_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("model_versions.id"), nullable=False),
        sa.Column("detection_confidence", sa.Numeric(5, 4), nullable=False),
        sa.Column("detection_rank", sa.Integer(), nullable=False),
        sa.Column("review_status", sa.String(length=30), nullable=False),
        sa.Column("review_required_flag", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("false_positive_risk", sa.Numeric(5, 4)),
        sa.Column("detection_status", sa.String(length=30), nullable=False),
        sa.Column("inferred_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint("detection_confidence BETWEEN 0 AND 1", name="ck_detections_confidence"),
        sa.CheckConstraint("detection_rank > 0", name="ck_detections_rank"),
        sa.CheckConstraint("review_status IN ('pending', 'confirmed', 'rejected', 'needs_second_review')", name="ck_detections_review_status"),
        sa.CheckConstraint("false_positive_risk IS NULL OR false_positive_risk BETWEEN 0 AND 1", name="ck_detections_false_positive_risk"),
        sa.CheckConstraint("detection_status IN ('active', 'superseded', 'invalidated')", name="ck_detections_status"),
    )

    op.create_table(
        "detection_candidates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("detection_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("detections.id", ondelete="CASCADE"), nullable=False),
        sa.Column("species_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("species_master.id")),
        sa.Column("common_name_snapshot", sa.String(length=255)),
        sa.Column("scientific_name_snapshot", sa.String(length=255)),
        sa.Column("rank_order", sa.Integer(), nullable=False),
        sa.Column("confidence_score", sa.Numeric(5, 4), nullable=False),
        sa.Column("is_unknown", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_protected_snapshot", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint("rank_order > 0", name="ck_detection_candidates_rank_order"),
        sa.CheckConstraint("confidence_score BETWEEN 0 AND 1", name="ck_detection_candidates_confidence"),
        sa.UniqueConstraint("detection_id", "rank_order", name="uq_detection_candidates_detection_rank"),
    )

    op.create_table(
        "reviewer_decisions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("detection_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("detections.id", ondelete="CASCADE"), nullable=False),
        sa.Column("reviewer_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("decision_type", sa.String(length=30), nullable=False),
        sa.Column("final_species_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("species_master.id")),
        sa.Column("comment", sa.Text()),
        sa.Column("mark_as_training_candidate", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("decision_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint("decision_type IN ('confirmed', 'rejected', 'corrected', 'hold')", name="ck_reviewer_decisions_type"),
        sa.CheckConstraint("decision_version > 0", name="ck_reviewer_decisions_version"),
    )

    op.create_table(
        "access_control_rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("observation_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("observations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("target_scope", sa.String(length=50), nullable=False),
        sa.Column("visibility_rule", sa.String(length=30), nullable=False),
        sa.Column("coordinates_masked", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("datetime_masked", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("applied_reason", sa.Text()),
        sa.Column("active_flag", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_by_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint("target_scope IN ('public', 'researcher', 'admin')", name="ck_access_control_rules_target_scope"),
        sa.CheckConstraint("visibility_rule IN ('public', 'masked', 'restricted', 'private')", name="ck_access_control_rules_visibility_rule"),
    )

    op.create_table(
        "observation_tags",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("observation_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("observations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("tag_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tag_master.id"), nullable=False),
        sa.UniqueConstraint("observation_id", "tag_id", name="uq_observation_tags_observation_tag"),
    )

    op.create_table(
        "export_jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("requested_by_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("report_type", sa.String(length=50), nullable=False),
        sa.Column("output_format", sa.String(length=20), nullable=False),
        sa.Column("filter_json", postgresql.JSONB(astext_type=sa.Text())),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("result_storage_path", sa.Text()),
        sa.Column("expires_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.CheckConstraint("output_format IN ('csv', 'json', 'geojson')", name="ck_export_jobs_output_format"),
        sa.CheckConstraint("status IN ('queued', 'running', 'completed', 'failed')", name="ck_export_jobs_status"),
    )

    op.create_table(
        "time_series_aggregates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("aggregation_level", sa.String(length=20), nullable=False),
        sa.Column("aggregation_timezone", sa.String(length=100), nullable=False),
        sa.Column("bucket_start_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("bucket_label", sa.String(length=50), nullable=False),
        sa.Column("region_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("region_master.id")),
        sa.Column("species_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("species_master.id")),
        sa.Column("taxa_group_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("taxa_groups.id")),
        sa.Column("occurrence_count", sa.BigInteger(), nullable=False),
        sa.Column("reviewed_count", sa.BigInteger(), nullable=False),
        sa.Column("avg_confidence", sa.Numeric(5, 4)),
        sa.Column("recomputed_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint("aggregation_level IN ('hour', 'day', 'week', 'month', 'season', 'year')", name="ck_time_series_aggregates_level"),
        sa.CheckConstraint("occurrence_count >= 0", name="ck_time_series_aggregates_occurrence_count"),
        sa.CheckConstraint("reviewed_count >= 0", name="ck_time_series_aggregates_reviewed_count"),
        sa.CheckConstraint("avg_confidence IS NULL OR avg_confidence BETWEEN 0 AND 1", name="ck_time_series_aggregates_avg_confidence"),
        sa.UniqueConstraint(
            "aggregation_level", "aggregation_timezone", "bucket_start_at", "region_id", "species_id", "taxa_group_id",
            name="uq_time_series_aggregates_bucket_scope",
        ),
    )

    op.create_foreign_key(
        "fk_observations_current_top_detection",
        "observations",
        "detections",
        ["current_top_detection_id"],
        ["id"],
    )

    op.execute("""
    CREATE OR REPLACE FUNCTION set_updated_at()
    RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        NEW.updated_at := now();
        RETURN NEW;
    END;
    $$;
    """)

    for table in [
        "region_master",
        "species_master",
        "users",
        "locations",
        "observation_datetimes",
        "observations",
        "model_versions",
        "seasonal_rules",
        "protected_species_rules",
    ]:
        op.execute(f"""
        CREATE TRIGGER trg_{table}_set_updated_at
        BEFORE UPDATE ON {table}
        FOR EACH ROW
        EXECUTE FUNCTION set_updated_at();
        """)

    op.execute("""
    INSERT INTO roles (role_code, role_name) VALUES
      ('observer', 'Observer'),
      ('reviewer', 'Reviewer'),
      ('admin', 'Administrator')
    ON CONFLICT (role_code) DO NOTHING;
    """)

    op.execute("""
    INSERT INTO taxa_groups (group_code, group_name) VALUES
      ('bird', 'Bird'),
      ('amphibian', 'Amphibian'),
      ('insect', 'Insect'),
      ('other', 'Other')
    ON CONFLICT (group_code) DO NOTHING;
    """)

    op.execute("""
    INSERT INTO habitat_types (habitat_type_code, habitat_name) VALUES
      ('forest', 'Forest'),
      ('forest_edge', 'Forest Edge'),
      ('river', 'River'),
      ('wetland', 'Wetland'),
      ('farmland', 'Farmland'),
      ('urban', 'Urban'),
      ('coast', 'Coast'),
      ('grassland', 'Grassland')
    ON CONFLICT (habitat_type_code) DO NOTHING;
    """)

    op.execute("""
    INSERT INTO weather_types (weather_code, weather_name) VALUES
      ('clear', 'Clear'),
      ('cloudy', 'Cloudy'),
      ('rain', 'Rain'),
      ('snow', 'Snow'),
      ('fog', 'Fog'),
      ('windy', 'Windy')
    ON CONFLICT (weather_code) DO NOTHING;
    """)


def downgrade() -> None:
    for table in [
        "protected_species_rules",
        "seasonal_rules",
        "model_versions",
        "observations",
        "observation_datetimes",
        "locations",
        "users",
        "species_master",
        "region_master",
    ]:
        op.execute(f"DROP TRIGGER IF EXISTS trg_{table}_set_updated_at ON {table};")

    op.execute("DROP FUNCTION IF EXISTS set_updated_at()")

    op.drop_table("time_series_aggregates")
    op.drop_table("export_jobs")
    op.drop_table("observation_tags")
    op.drop_table("access_control_rules")
    op.drop_table("reviewer_decisions")
    op.drop_table("detection_candidates")
    op.drop_table("detections")
    op.drop_table("model_inference_runs")
    op.drop_table("processing_jobs")
    op.drop_table("audio_segments")
    op.drop_constraint("fk_observations_current_top_detection", "observations", type_="foreignkey")
    op.drop_table("observations")
    op.drop_table("model_versions")
    op.drop_table("observation_conditions")
    op.drop_table("observation_datetime_history")
    op.drop_index("idx_observation_datetimes_local", table_name="observation_datetimes")
    op.drop_index("idx_observation_datetimes_utc", table_name="observation_datetimes")
    op.drop_table("observation_datetimes")
    op.drop_table("location_history")
    op.drop_index("idx_locations_geom", table_name="locations")
    op.drop_table("locations")
    op.drop_index("uq_media_files_checksum_sha256", table_name="media_files")
    op.drop_table("media_files")
    op.drop_index("idx_species_master_is_protected", table_name="species_master")
    op.drop_table("species_master")
    op.drop_table("weather_types")
    op.drop_table("habitat_types")
    op.drop_index("idx_region_master_geom", table_name="region_master")
    op.drop_table("region_master")
    op.drop_table("taxa_groups")
    op.drop_table("user_roles")
    op.drop_table("audit_logs")
    op.drop_table("users")
    op.drop_table("roles")
    op.drop_table("tag_master")
    op.drop_table("protected_species_rules")
    op.drop_table("seasonal_rules")

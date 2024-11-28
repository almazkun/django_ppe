from ninja import ModelSchema, Field, Schema
from typing import Optional

from ppe.models import Camera, Event, Report


class CameraSchemaOut(ModelSchema):
    class Meta:
        model = Camera
        fields = [
            "uuid",
            "name",
            "rtsp_url",
            "is_active",
            "created_at",
            "updated_at",
        ]


class CameraSchemaIn(ModelSchema):
    class Meta:
        model = Camera
        fields = [
            "name",
            "rtsp_url",
            "is_active",
        ]


class CameraSchemaUpdate(Schema):
    name: Optional[str] = None
    rtsp_url: Optional[str] = None
    is_active: Optional[bool] = None


class EventSchemaOut(ModelSchema):
    class Meta:
        model = Event
        fields = [
            "uuid",
            "camera",
            "timestamp",
            "image",
            "is_analyzed",
            "is_violation",
            "violation_type",
            "created_at",
            "updated_at",
        ]


class EventSchemaIn(ModelSchema):
    camera_id: str = Field(..., description="Camera UUID")

    class Meta:
        model = Event
        fields = [
            "image",
            "is_analyzed",
            "is_violation",
            "violation_type",
        ]


class EventSchemaUpdate(Schema):
    is_analyzed: Optional[bool] = None
    is_violation: Optional[bool] = None
    violation_type: Optional[str] = ""


class ReportSchemaOut(ModelSchema):
    class Meta:
        model = Report
        fields = [
            "report_data",
            "created_at",
            "updated_at",
        ]


class ReportSchemaIn(ModelSchema):
    class Meta:
        model = Report
        fields = [
            "report_data",
        ]


class ReportSchemaUpdate(Schema):
    report_data: Optional[dict] = None

from typing import List, Optional
from ninja import Router, Query
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from ninja.pagination import paginate
from django.db.models import Q

from ppe.schemas import (
    CameraSchemaOut,
    CameraSchemaIn,
    CameraSchemaUpdate,
    EventSchemaOut,
    EventSchemaIn,
    EventSchemaUpdate,
    ReportSchemaOut,
    ReportSchemaIn,
    ReportSchemaUpdate,
)
from ppe.models import Camera, Event, Report

router = Router()


class BaseAPI:
    """
    Base class for CRUD operations with common functionality
    """

    model = None
    schema_out = None
    schema_in = None
    schema_update = None

    @classmethod
    def get_queryset(cls, request, **kwargs):
        """
        Base method for retrieving queryset with optional filtering
        """
        return cls.model.objects.all()

    @classmethod
    def filter_queryset(cls, queryset: QuerySet, filters: dict):
        """
        Apply filters to queryset
        """
        return queryset


class CameraAPI(BaseAPI):
    model = Camera
    schema_out = CameraSchemaOut
    schema_in = CameraSchemaIn
    schema_update = CameraSchemaUpdate

    @router.get("/cameras", response=List[CameraSchemaOut])
    @paginate
    def get_cameras(
        request,
        active: Optional[bool] = Query(None),
        search: Optional[str] = Query(None),
    ):
        queryset = Camera.objects.all()

        if active is not None:
            queryset = queryset.filter(is_active=active)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(rtsp_url__icontains=search)
            )

        return queryset

    @router.get("/cameras/{uuid}", response=CameraSchemaOut)
    def get_camera(request, uuid: str):
        return get_object_or_404(Camera, uuid=uuid)

    @router.post("/cameras", response=CameraSchemaOut)
    def create_camera(request, payload: CameraSchemaIn):
        try:
            camera = Camera.objects.create(**payload.dict())
            return camera
        except Exception as e:
            return {"error": str(e)}

    @router.put("/cameras/{uuid}", response=CameraSchemaOut)
    def update_camera(request, uuid: str, payload: CameraSchemaUpdate):
        camera = get_object_or_404(Camera, uuid=uuid)

        update_data = payload.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(camera, key, value)

        try:
            camera.full_clean()
            camera.save()
            return camera
        except Exception as e:
            return {"error": str(e)}

    @router.delete("/cameras/{uuid}")
    def delete_camera(request, uuid: str):
        camera = get_object_or_404(Camera, uuid=uuid)
        try:
            camera.delete()
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}


class EventAPI(BaseAPI):
    model = Event
    schema_out = EventSchemaOut
    schema_in = EventSchemaIn
    schema_update = EventSchemaUpdate

    @router.get("/events", response=List[EventSchemaOut])
    @paginate
    def get_events(
        request,
        camera_uuid: Optional[str] = Query(None),
        is_violation: Optional[bool] = Query(None),
        start_date: Optional[str] = Query(None),
        end_date: Optional[str] = Query(None),
    ):
        queryset = Event.objects.all()

        if camera_uuid:
            queryset = queryset.filter(camera__uuid=camera_uuid)

        if is_violation is not None:
            queryset = queryset.filter(is_violation=is_violation)

        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)

        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)

        return queryset

    @router.get("/events/{uuid}", response=EventSchemaOut)
    def get_event(request, uuid: str):
        return get_object_or_404(Event, uuid=uuid)

    @router.post("/events", response=EventSchemaOut)
    def create_event(request, payload: EventSchemaIn):
        try:
            event = Event.objects.create(**payload.dict())
            return event
        except Exception as e:
            return {"error": str(e)}

    @router.put("/events/{uuid}", response=EventSchemaOut)
    def update_event(request, uuid: str, payload: EventSchemaUpdate):
        event = get_object_or_404(Event, uuid=uuid)

        update_data = payload.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(event, key, value)

        try:
            event.full_clean()
            event.save()
            return event
        except Exception as e:
            return {"error": str(e)}

    @router.delete("/events/{uuid}")
    def delete_event(request, uuid: str):
        event = get_object_or_404(Event, uuid=uuid)
        try:
            event.delete()
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}


class ReportAPI(BaseAPI):
    model = Report
    schema_out = ReportSchemaOut
    schema_in = ReportSchemaIn
    schema_update = ReportSchemaUpdate

    @router.get("/reports", response=List[ReportSchemaOut])
    @paginate
    def get_reports(
        request,
        start_date: Optional[str] = Query(None),
        end_date: Optional[str] = Query(None),
    ):
        queryset = Report.objects.all()

        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)

        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset

    @router.get("/reports/{uuid}", response=ReportSchemaOut)
    def get_report(request, uuid: str):
        return get_object_or_404(Report, uuid=uuid)

    @router.post("/reports", response=ReportSchemaOut)
    def create_report(request, payload: ReportSchemaIn):
        try:
            report = Report.objects.create(**payload.dict())
            return report
        except Exception as e:
            return {"error": str(e)}

    @router.put("/reports/{uuid}", response=ReportSchemaOut)
    def update_report(request, uuid: str, payload: ReportSchemaUpdate):
        report = get_object_or_404(Report, uuid=uuid)

        update_data = payload.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(report, key, value)

        try:
            report.full_clean()
            report.save()
            return report
        except Exception as e:
            return {"error": str(e)}

    @router.delete("/reports/{uuid}")
    def delete_report(request, uuid: str):
        report = get_object_or_404(Report, uuid=uuid)
        try:
            report.delete()
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}

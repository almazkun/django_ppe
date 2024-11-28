from django.db import models
import uuid


def generate_path(instance, filename):
    return f"{instance.camera.name}/{filename}"


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Camera(BaseModel):
    name = models.CharField(max_length=255)
    rtsp_url = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cameras"
        ordering = ["-created_at"]


class Event(BaseModel):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=generate_path)
    is_analyzed = models.BooleanField(default=False)
    is_violation = models.BooleanField(default=False)
    violation_type = models.CharField(max_length=255, default="")

    def __str__(self):
        return f"{self.camera.name} - {self.timestamp}"

    class Meta:
        verbose_name_plural = "Events"
        ordering = ["-timestamp"]


class Report(BaseModel):
    report_data = models.JSONField()

    def __str__(self):
        return f"Report for {self.created_at}"

    class Meta:
        verbose_name_plural = "Reports"
        ordering = ["-created_at"]

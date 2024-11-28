from django.test import TestCase
from ppe.models import Camera, Event, Report


class TestCameraAPI(TestCase):
    def test_camera_create(self):
        endpoint = "/api/v1/ppe/cameras"
        payload = {
            "name": "Test Camera",
            "rtsp_url": "rtsp://test.com",
            "is_active": True,
        }
        response = self.client.post(endpoint, payload, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], payload["name"])
        self.assertEqual(response.json()["rtsp_url"], payload["rtsp_url"])
        self.assertEqual(response.json()["is_active"], payload["is_active"])

        camera = Camera.objects.get(uuid=response.json()["uuid"])

        self.assertEqual(camera.name, payload["name"])
        self.assertEqual(camera.rtsp_url, payload["rtsp_url"])
        self.assertEqual(camera.is_active, payload["is_active"])

    def test_camera_list(self):
        endpoint = "/api/v1/ppe/cameras"
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), Camera.objects.count())

        cameras = Camera.objects.bulk_create(
            [
                Camera(name=f"Camera {i}", rtsp_url=f"rtsp://test.com/{i}")
                for i in range(10)
            ]
        )

        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), Camera.objects.count())

        cameras = Camera.objects.all()
        items = response.json().get("items")

        for i, camera in enumerate(cameras):
            self.assertEqual(items[i]["name"], camera.name)
            self.assertEqual(items[i]["rtsp_url"], camera.rtsp_url)
            self.assertEqual(items[i]["is_active"], camera.is_active)

    def test_camera_update(self):
        camera = Camera.objects.create(
            name="Test Camera", rtsp_url="rtsp://test.com", is_active=True
        )
        endpoint = f"/api/v1/ppe/cameras/{camera.uuid}"
        payload = {
            "name": "Updated Camera",
            "is_active": False,
        }
        response = self.client.put(endpoint, payload, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], payload["name"])
        self.assertEqual(response.json()["is_active"], payload["is_active"])

        self.assertNotEqual(response.json()["name"], camera.name)
        self.assertNotEqual(response.json()["is_active"], camera.is_active)
        self.assertEqual(response.json()["rtsp_url"], camera.rtsp_url)

        camera.refresh_from_db()

        self.assertEqual(camera.name, payload["name"])
        self.assertEqual(camera.is_active, payload["is_active"])

    def test_camera_retrieve(self):
        camera = Camera.objects.create(
            name="Test Camera", rtsp_url="rtsp://test.com", is_active=True
        )
        endpoint = f"/api/v1/ppe/cameras/{camera.uuid}"
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], camera.name)
        self.assertEqual(response.json()["rtsp_url"], camera.rtsp_url)
        self.assertEqual(response.json()["is_active"], camera.is_active)

    def test_camera_delete(self):
        camera = Camera.objects.create(
            name="Test Camera", rtsp_url="rtsp://test.com", is_active=True
        )
        endpoint = f"/api/v1/ppe/cameras/{camera.uuid}"
        response = self.client.delete(endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Camera.objects.count(), 0)


class TestEventAPI(TestCase):
    def test_event_create(self):
        camera = Camera.objects.create(
            name="Test Camera", rtsp_url="rtsp://test.com", is_active=True
        )
        endpoint = "/api/v1/ppe/events"
        payload = {
            "camera_id": str(camera.uuid),
            "image": "/test.jpg",
            "is_analyzed": False,
            "is_violation": False,
            "violation_type": "",
        }

        response = self.client.post(endpoint, payload, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["camera"], str(camera.uuid))
        self.assertEqual(response.json()["image"], payload["image"])
        self.assertEqual(response.json()["is_analyzed"], payload["is_analyzed"])
        self.assertEqual(response.json()["is_violation"], payload["is_violation"])
        self.assertEqual(response.json()["violation_type"], payload["violation_type"])

    def test_event_list(self):
        endpoint = "/api/v1/ppe/events"
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), Event.objects.count())

        camera = Camera.objects.create(
            name="Test Camera", rtsp_url="rtsp://test.com", is_active=True
        )
        events = Event.objects.bulk_create(
            [
                Event(
                    camera=camera,
                    image="test.jpg",
                    is_analyzed=False,
                    is_violation=False,
                    violation_type="",
                )
                for i in range(10)
            ]
        )

        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), Event.objects.count())

        events = Event.objects.all()
        items = response.json().get("items")

        for i, event in enumerate(events):
            self.assertEqual(items[i]["camera"], str(event.camera.uuid))
            self.assertEqual(items[i]["image"], event.image.url)
            self.assertEqual(items[i]["is_analyzed"], event.is_analyzed)
            self.assertEqual(items[i]["is_violation"], event.is_violation)
            self.assertEqual(items[i]["violation_type"], event.violation_type)

    def test_event_update(self):
        camera = Camera.objects.create(
            name="Test Camera", rtsp_url="rtsp://test.com", is_active=True
        )
        event = Event.objects.create(
            camera=camera,
            image="test.jpg",
            is_analyzed=False,
            is_violation=False,
            violation_type="Should not Change",
        )
        endpoint = f"/api/v1/ppe/events/{event.uuid}"
        payload = {
            "is_analyzed": True,
            "is_violation": True,
        }

        response = self.client.put(endpoint, payload, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["camera"], str(camera.uuid))
        self.assertEqual(response.json()["image"], event.image.url)
        self.assertEqual(response.json()["is_analyzed"], payload["is_analyzed"])
        self.assertEqual(response.json()["is_violation"], payload["is_violation"])
        self.assertEqual(response.json()["violation_type"], event.violation_type)

        self.assertNotEqual(response.json()["is_analyzed"], event.is_analyzed)
        self.assertNotEqual(response.json()["is_violation"], event.is_violation)

        event.refresh_from_db()

        self.assertEqual(event.is_analyzed, payload["is_analyzed"])
        self.assertEqual(event.is_violation, payload["is_violation"])

    def test_event_retrieve(self):
        camera = Camera.objects.create(
            name="Test Camera", rtsp_url="rtsp://test.com", is_active=True
        )
        event = Event.objects.create(
            camera=camera,
            image="test.jpg",
            is_analyzed=False,
            is_violation=False,
            violation_type="",
        )
        endpoint = f"/api/v1/ppe/events/{event.uuid}"
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["camera"], str(camera.uuid))
        self.assertEqual(response.json()["image"], event.image.url)
        self.assertEqual(response.json()["is_analyzed"], event.is_analyzed)
        self.assertEqual(response.json()["is_violation"], event.is_violation)
        self.assertEqual(response.json()["violation_type"], event.violation_type)

    def test_event_delete(self):
        camera = Camera.objects.create(
            name="Test Camera", rtsp_url="rtsp://test.com", is_active=True
        )
        event = Event.objects.create(
            camera=camera,
            image="test.jpg",
            is_analyzed=False,
            is_violation=False,
            violation_type="",
        )
        endpoint = f"/api/v1/ppe/events/{event.uuid}"
        response = self.client.delete(endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Event.objects.count(), 0)


class TestReportAPI(TestCase):
    def test_report_create(self):
        endpoint = "/api/v1/ppe/reports"
        payload = {
            "report_data": {"test": "data"},
        }
        response = self.client.post(endpoint, payload, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["report_data"], payload["report_data"])

    def test_report_list(self):
        endpoint = "/api/v1/ppe/reports"
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), Report.objects.count())

        reports = Report.objects.bulk_create(
            [Report(report_data={"test": "data"}) for i in range(10)]
        )

        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), Report.objects.count())

        reports = Report.objects.all()
        items = response.json().get("items")

        for i, report in enumerate(reports):
            self.assertEqual(items[i]["report_data"], report.report_data)

    def test_report_retrieve(self):
        report = Report.objects.create(report_data={"test": "data"})
        endpoint = f"/api/v1/ppe/reports/{report.uuid}"
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["report_data"], report.report_data)

    def test_report_delete(self):
        report = Report.objects.create(report_data={"test": "data"})
        endpoint = f"/api/v1/ppe/reports/{report.uuid}"
        response = self.client.delete(endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Report.objects.count(), 0)

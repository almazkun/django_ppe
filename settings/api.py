from ppe.api import router as ppe_router

from ninja import NinjaAPI

api = NinjaAPI()

api.add_router("/ppe/", ppe_router)

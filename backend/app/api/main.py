from fastapi import APIRouter

import platform
if platform.system() in ["Windows"]:
    from api.routes import items, login, users, utils, unions, conferences, churches, districts, tensions_arterielles
else:
    from app.api.routes import items, login, users, utils, unions, conferences, churches, districts, tensions_arterielles

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(unions.router, prefix="/unions", tags=["unions"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(conferences.router, prefix="/conferences", tags=["conferences"])
api_router.include_router(churches.router, prefix="/churches", tags=["churches"])
api_router.include_router(districts.router, prefix="/districts", tags=["districts"])
api_router.include_router(tensions_arterielles.router, prefix="/tensions_arterielles", tags=["tensions_arterielles"])

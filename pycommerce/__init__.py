import uvicorn
from pycommerce.config import get_settings
from pycommerce.infra.api.app import create_app

SETTINGS = get_settings()

app = create_app(SETTINGS)


def start_server() -> None:
    uvicorn.run(
        "pycommerce:app",
        host=SETTINGS.SERVER_HOST,
        port=SETTINGS.SERVER_PORT,
        reload=SETTINGS.SERVER_RELOAD,
        log_level=SETTINGS.LOG_LEVEL,
    )

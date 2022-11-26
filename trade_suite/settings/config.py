from pydantic import BaseModel

class DefaultSettings(BaseModel):
    fullscreen: bool
    main_window: dict
    last_chart: dict
    exchanges: dict
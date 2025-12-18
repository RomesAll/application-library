__all__ = ['BASE_DIR', 'settings', 'engine_sync',
           'engine_def', 'engine_async',
           'session_factory_sync', 'session_factory_async', 'Base']

from .config_project import *
from .database import *

'''Альтернатива
__all__ = (
    'BASE_DIR', 'settings', 'engine_sync',
    'engine_def', 'engine_async', 'session_factory_sync',
    'session_factory_async', 'Base',
)
from .config_project import BASE_DIR, settings
from .database import engine_sync, engine_def, engine_async, session_factory_sync, session_factory_async, Base
'''
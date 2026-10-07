from .blueprint import api_bp

# Import route modules to attach them to api_bp
from . import auth       # noqa: E402, F401
from . import doctors    # noqa: E402, F401
from . import reference  # noqa: E402, F401
from . import user       # noqa: E402, F401
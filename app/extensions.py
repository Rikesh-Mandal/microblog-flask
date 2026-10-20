from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
    storage_options={
        "socket_connect_timeout": 2,
        "socket_timeout": 2,
    },
    strategy="fixed-window",
    headers_enabled=True,
    key_prefix="microblog:ratelimit",
)
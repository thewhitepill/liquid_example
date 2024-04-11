from types import SimpleNamespace

import os


config = SimpleNamespace(
    redis=SimpleNamespace(
        url=os.environ["REDIS_URL"],
        namespace=os.environ.get("REDIS_NAMESPACE", "liquid_example_api")
    )
)

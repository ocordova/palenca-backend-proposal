import cuid


def create_cuid() -> str:
    return str(cuid.cuid())

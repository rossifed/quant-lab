from shared.app_container import get_container


def inject(cls):
    def dependency():
        container = get_container()
        return container.resolve(cls)
    return dependency
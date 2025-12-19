from main import DiContainer, create_app

container = DiContainer()
app = create_app(container.get_use_case)

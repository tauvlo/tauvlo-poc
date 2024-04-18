from tauvlo.server.controller import Controller


def test_controller_instantiation():
    controller = Controller()
    assert controller is not None

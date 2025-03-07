import platform
if platform.system() in ["Windows"]:
    import app.core
    import app.api
    import app.tests
else:
    import core
    import api
    import tests


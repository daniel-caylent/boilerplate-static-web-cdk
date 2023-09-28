from pathlib import PurePath, Path

THIS_DIRECTORY = Path(__file__).parent.absolute()
WEB_PATH = str(PurePath(THIS_DIRECTORY.parent.parent, "web"))
WEB_DIST_PATH = str(PurePath(WEB_PATH, "dist"))

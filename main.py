import sys

from asciimatics.exceptions import StopApplication
from asciimatics.scene import Scene
from asciimatics.screen import ManagedScreen, Screen
from effects import FlagFX, SurfaceFX
from runner import AnimationRunner
from tools import Drawer


@ManagedScreen
def tools_test(screen: Screen):
    drawer = Drawer(screen=screen)

    effects = [
        SurfaceFX(screen=screen, drawer=drawer),
        FlagFX(screen=screen, drawer=drawer)
    ]
    scene = Scene(effects=effects)
    screen.set_scenes([scene])

    runner = AnimationRunner(screen)
    try:
        runner.run()
    except StopApplication:
        sys.exit()


tools_test()

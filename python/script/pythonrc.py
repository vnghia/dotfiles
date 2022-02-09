# flake8: noqa

import importlib
import os
import platform
import sys
from pathlib import Path

# Constant paths
sys.path.append(os.environ["DOTFILES_PYTHON_SCRIPT"])
import constants

try:
    # Autocompletion
    import atexit
    import readline
    import rlcompleter

    readline.parse_and_bind("tab: complete")
    histfile = constants.HISTFILE_HOME / ".python_history"
    try:
        readline.read_history_file(histfile)
    except IOError:
        pass
    atexit.register(readline.write_history_file, histfile)
    del atexit, readline, rlcompleter
except ImportError:
    pass

# Formatting library
sys.path.append(str(next(constants.PYVENV_LOCAL.glob("lib/python*/site-packages"))))
import rich
from rich import inspect as insp
from rich import pretty, print
from rich import traceback as richtb
from rich.console import Console
from rich.panel import Panel
from rich.pretty import pprint
from rich.table import Table
from rich.text import Text

# Class to store all informations and formatting
class __PYTHONRC__:
    def __init__(self):
        self.virtual_env = Path(os.environ.get("VIRTUAL_ENV", "global"))
        self.cwd = Path.cwd()
        self.console = Console()

        pretty.install()
        richtb.install()

        runtime_info = Table.grid(expand=True)
        runtime_info.add_column()
        runtime_info.add_column()
        divider_style = "color(45)"
        key_style = "color(45)" + " bold"
        function_style = "color(136)"
        module_style = "color(70)"
        runtime_info.add_row(Text("cwd", style=key_style), Text(f"{self.cwd}"))
        runtime_info.add_row(
            *self.__construct_runtime_info_row(
                "builtin modules",
                sorted(["os", "platform", "sys", "Path"]),
                key_style,
                module_style,
                divider_style,
            ),
        )
        common_modules = self.__import_modules(
            {
                "numpy": "np",
                "numpy.linalg": "npl",
                "matplotlib.pyplot": "plt",
                "scipy": "sci",
                "pandas": "pd",
            }
        )
        if len(common_modules):
            runtime_info.add_row(
                *self.__construct_runtime_info_row(
                    "common modules",
                    sorted(common_modules),
                    key_style,
                    module_style,
                    divider_style,
                )
            )
        runtime_info.add_row(
            *self.__construct_runtime_info_row(
                "rich functions",
                sorted(["inspect as insp", "print", "pprint"]),
                key_style,
                function_style,
                divider_style,
            ),
        )
        runtime_info.add_row(
            *self.__construct_runtime_info_row(
                "custom functions",
                sorted(["cd", "import_path"]),
                key_style,
                function_style,
                divider_style,
            ),
        )

        self.console.print(
            Panel(
                runtime_info,
                title=Text.from_markup(
                    f"[color(81)]{platform.python_version()} ~ {self.virtual_env.name}[/color(81)]",
                    style="bold",
                ),
                style="color(81)",
            )
        )

        self.ps1 = self.__get_output_string(Text("--> ", style="color(81)"))
        self.ps2 = self.__get_output_string(Text("... ", style="color(24)"))
        if sys.platform != "win32":
            self.ps1 = self.ps1.replace("\x1b", "\x01\x1b").replace("m", "m\x02")
            self.ps2 = self.ps2.replace("\x1b", "\x01\x1b").replace("m", "m\x02")

    def __get_output_string(self, rendable):
        with self.console.capture() as capture:
            self.console.print(rendable, end="")
        return capture.get()

    def __import_modules(self, modules):
        imported = []
        for module, name in modules.items():
            import_str = f"import {module}"
            if name:
                import_str += f" as {name}"
            try:
                exec(import_str, globals())
            except ImportError:
                pass
            else:
                imported.append(name or module)
        return imported

    def __construct_runtime_info_row(
        _, key, values, key_style, value_style, divider_style
    ):
        kT = Text(key, style=key_style)
        vT = Text()
        for value in values[:-1]:
            vT.append(value, style=value_style).append(" | ", style=divider_style)
        vT.append(values[-1], style=value_style)
        return kT, vT

    def cd(self, path):
        path = os.path.expandvars(os.path.expanduser(path))
        new_path = self.cwd / path
        if new_path == self.cwd:
            return
        try:
            sys.path.remove(str(self.cwd))
        except ValueError:
            pass
        self.cwd = new_path.resolve()
        os.chdir(self.cwd)
        sys.path.append(str(self.cwd))
        assert Path.cwd() == self.cwd
        self.console.print(Text(f"cwd: {str(self.cwd)}", "color(45)"))

    def import_path(self, path, *nargs, name=None):
        module_path = (self.cwd / os.path.expandvars(path)).resolve()
        sys.path.append(str(module_path.parent))
        module_name = name or module_path.stem
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        for arg in nargs:
            globals()[arg] = getattr(module, arg)
        sys.path.pop()
        return module


__pythonrc__ = __PYTHONRC__()
sys.ps1 = __pythonrc__.ps1
sys.ps2 = __pythonrc__.ps2

# Shortcuts
cd = __pythonrc__.cd
import_path = __pythonrc__.import_path
q = exit


del __PYTHONRC__

sys.path.pop()
sys.path.pop()
del sys.modules["constants"]

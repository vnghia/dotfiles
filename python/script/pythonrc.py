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
from rich import pretty
from rich import traceback as richtb

# Class to store all informations and formatting
class __PYTHONRC__:
    def __init__(self):
        self.virtual_env = Path(os.environ.get("VIRTUAL_ENV", "global"))
        self.cwd = Path.cwd()

        self.__import_rich_classes()
        self.__construct_runtime_info()

        pretty.install()
        richtb.install()

        self.__init_sys_ps()

    def __import_modules(self, modules):
        imported = []
        for module, (name, root) in modules.items():
            import_str = f"import {module}"
            if name:
                import_str += f" as {name}"
            if root:
                import_str = f"from {root} " + import_str
            try:
                exec(import_str, globals())
            except ImportError:
                pass
            else:
                imported.append(name or module)
        return imported

    def __import_rich_classes(self):
        names = ["Console", "Panel", "Table", "Text"]
        modules = {name: (None, f"rich.{name.lower()}") for name in names}
        imported = self.__import_modules(modules)
        assert len(imported) == len(modules)

    def __construct_runtime_info(self):
        self.console = Console()

        runtime_info = Table.grid(expand=True)
        runtime_info.add_column()
        runtime_info.add_column()

        self.divider_style = "color(45)"
        self.key_style = "color(45)" + " bold"
        self.function_style = "color(136)"
        self.module_style = "color(70)"

        runtime_info.add_row(Text("cwd", style=self.key_style), Text(f"{self.cwd}"))
        self.__construct_runtime_imported_row(runtime_info)

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

    def __construct_runtime_info_row(
        _, key, values, key_style, value_style, divider_style
    ):
        kT = Text(key, style=key_style)
        vT = Text()
        for value in values[:-1]:
            vT.append(value, style=value_style).append(" | ", style=divider_style)
        vT.append(values[-1], style=value_style)
        return kT, vT

    def __construct_runtime_imported_row(self, table):
        for name in (
            "builtin_modules",
            "common_modules",
            "rich_functions",
            "custom_functions",
        ):
            imported = getattr(self, f"{self.__class__.__name__[1:]}__import_{name}")()
            if imported:
                style = self.module_style if "modules" in name else self.function_style
                table.add_row(
                    *self.__construct_runtime_info_row(
                        name.replace("_", " "),
                        sorted(imported),
                        self.key_style,
                        style,
                        self.divider_style,
                    ),
                )

    def __import_builtin_modules(self):
        return ["os", "platform", "sys", "Path"]

    def __import_common_modules(self):
        modules = {
            "numpy": ("np", None),
            "numpy.linalg": ("npl", None),
            "matplotlib.pyplot": ("plt", None),
            "scipy": ("sci", None),
            "pandas": ("pd", None),
        }
        return self.__import_modules(modules)

    def __import_rich_functions(self):
        root = "rich"
        modules = {
            "inspect": ("insp", root),
            "print": (None, root),
            "pprint": (None, f"{root}.pretty"),
        }
        return self.__import_modules(modules)

    # ---------------------------------------------------------------------------- #
    #                                    PS1/PS2                                   #
    # ---------------------------------------------------------------------------- #

    def __init_sys_ps(self):
        self.ps1 = self.__get_output_string(Text("--> ", style="color(81)"))
        self.ps2 = self.__get_output_string(Text("... ", style="color(24)"))
        if sys.platform != "win32":
            self.ps1 = self.ps1.replace("\x1b", "\x01\x1b").replace("m", "m\x02")
            self.ps2 = self.ps2.replace("\x1b", "\x01\x1b").replace("m", "m\x02")
        sys.ps1 = self.ps1
        sys.ps2 = self.ps2

    # ---------------------------------------------------------------------------- #
    #                               Custom functions                               #
    # ---------------------------------------------------------------------------- #

    def __import_custom_functions(self):
        custom_functions = ["cd", "import_path"]
        for funcname in custom_functions:
            globals()[funcname] = getattr(self, funcname)
        custom_shortcuts = {"q": exit}
        for shortcut, func in custom_shortcuts.items():
            globals()[shortcut] = func
        return custom_functions + list(custom_shortcuts.keys())

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

    # ---------------------------------------------------------------------------- #
    #                                    Utility                                   #
    # ---------------------------------------------------------------------------- #

    def __get_output_string(self, rendable):
        with self.console.capture() as capture:
            self.console.print(rendable, end="")
        return capture.get()


__pythonrc__ = __PYTHONRC__()
sys.ps1 = __pythonrc__.ps1
sys.ps2 = __pythonrc__.ps2


del __PYTHONRC__

sys.path.pop()
sys.path.pop()
del sys.modules["constants"]

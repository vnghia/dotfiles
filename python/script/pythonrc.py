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

# ---------------------------------------------------------------------------- #
#                Class to store all informations and formatting                #
# ---------------------------------------------------------------------------- #


class __PYTHONRC__:
    def __init__(self):
        sys.path.append(
            str(next(constants.PYVENV_LOCAL.glob("lib/python*/site-packages")))
        )
        self.virtual_env = Path(os.environ.get("VIRTUAL_ENV", "global"))
        self.virtual_home = constants.PYVENV_HOME
        self.cwd = Path.cwd()

        self.__init_rich()
        self.__init_sys_ps()
        sys.path.pop()

    # ---------------------------------------------------------------------------- #
    #                                     Rich                                     #
    # ---------------------------------------------------------------------------- #

    def __init_rich(self):
        from rich import pretty as richpretty
        from rich import traceback as richtraceback

        richpretty.install()
        richtraceback.install()
        del richpretty
        del richtraceback

        self.__rich_panel()

    # ------------------------------- Startup panel ------------------------------ #

    def __rich_panel(self):
        self.__rich_utilities()
        self.__rich_style()

        panel = Table.grid(expand=True)
        panel.add_column()
        panel.add_column()

        panel.add_row(Text("cwd", style=self.key_style), Text(f"{self.cwd}"))
        self.__rich_imported(panel)

        startup_title = f"[color(81)]{platform.python_version()} ~ {self.virtual_env.name}[/color(81)]"
        startup_text = Text.from_markup(startup_title, style="bold")
        self.console.print(Panel(panel, title=startup_text, style="color(81)"))

    # ------------------------ Imported functions/modules ------------------------ #

    def __rich_imported(self, table):
        for name in (
            "builtin_modules",
            "common_modules",
            "rich_functions",
            "custom_functions",
        ):
            imported = getattr(self, f"{self.__class__.__name__[1:]}__import_{name}")()
            if imported:
                style = self.module_style if "modules" in name else self.function_style
                row = self.__rich_row(name.replace("_", " "), sorted(imported), style)
                table.add_row(*row)

    # ------------------------------------ Row ----------------------------------- #

    def __rich_row(self, key, values, value_style):
        kT = Text(key, style=self.key_style)
        vT = Text()
        for value in values[:-1]:
            vT.append(value, style=value_style).append(" | ", style=self.divider_style)
        vT.append(values[-1], style=value_style)
        return kT, vT

    # --------------------------------- Utilities -------------------------------- #

    def __rich_utilities(self):
        names = ["Console", "Panel", "Table", "Text"]
        modules = {name: (None, f"rich.{name.lower()}") for name in names}
        imported = self.__import_modules(modules)
        assert len(imported) == len(modules)
        self.console = Console()

    def __rich_style(self):
        self.divider_style = "color(45)"
        self.key_style = "color(45)" + " bold"
        self.function_style = "color(136)"
        self.module_style = "color(70)"

    # ---------------------------------------------------------------------------- #
    #                                    Import                                    #
    # ---------------------------------------------------------------------------- #

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
        custom_functions = ["cd", "import_path", "on"]
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

    def on(self, venv):
        source = self.virtual_home / venv / "bin" / "activate"
        os.execlp("sh", "sh", "-c", f". {source} && python3")

    # ---------------------------------------------------------------------------- #
    #                                    Utility                                   #
    # ---------------------------------------------------------------------------- #

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

    def __get_output_string(self, rendable):
        with self.console.capture() as capture:
            self.console.print(rendable, end="")
        return capture.get()


__pythonrc__ = __PYTHONRC__()
del __PYTHONRC__

sys.path.pop()
del sys.modules["constants"]

from cx_Freeze import setup, Executable

base = None    

executables = [Executable("main.py", base=base)]

packages = ["idna", "os", "sys", "identify", "crawler", "analysis", "requests", "datetime", "urllib.request", "json", "re", "csv", "application", "difflib" ]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "CeeVee",
    options = options,
    version = "1.0",
    description = "For when you're feeling vulnerable",
    executables = executables
)
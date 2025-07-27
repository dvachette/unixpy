from unyx.FS import FS
from unyx._fs import File
def run_script(shell:FS, *args):
    if not args:
        print("No script provided.")
        return
    script_name = args[0]
    script_file:File = shell.current.find(script_name)
    if not isinstance(script_file, FS.File):
        return f"Script '{script_name}' not found."
    

    # When there will be a user based permissions system, this will be used to check if the user has permission to run the script.

    

    script_text = script_file.readf()

    for line in script_text:
        line = line.strip()
        



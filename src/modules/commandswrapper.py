def get_project_commands():
    """
    Gets the list of commands from the commands directory.
    @return: A commented list of the commands
    """
    ROOT_DIR=get_project_root()
    CARME_COMMANDS=os.path.join(ROOT_DIR, 'commands','carme-commands.yaml')
    if os.path.isfile(CARME_COMMANDS):
        commands=load_yaml_file(CARME_COMMANDS)
    else:
        print("No commands file found.")
        exit()
    return commands

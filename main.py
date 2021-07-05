import lib.levels

if __name__ == '__main__':
    lib.levels.setup_levels()
    level = lib.levels.get_level_map('Sandbox')
    if level is not None:
        print(level.name)
    else:
        print("Level was not available")

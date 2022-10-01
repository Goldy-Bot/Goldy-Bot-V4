# Development gang sheeet

if __name__ == '__main__':
    import sys

    sys.path.insert(0, './src')

    import GoldyBot

    print("Path >>> " + GoldyBot.paths.GOLDY_BOT)

    Goldy = GoldyBot.Goldy()

    Goldy.start()
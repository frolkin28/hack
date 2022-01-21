if __name__ == '__main__':
    from aiohttp.web import run_app
    from uvloop import install
    from hack.app import make_app
    from hack.config import CONFIG
    from logging import info

    info('{} started'.format('hack'))
    install()
    run_app(make_app(), port=CONFIG['port'])

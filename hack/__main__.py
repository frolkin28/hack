if __name__ == '__main__':
    import logging
    import os

    from aiohttp.web import run_app
    from uvloop import install
    from hack.app import make_app
    from hack.config import CONFIG

    log = logging.getLogger(__name__)

    if CONFIG['is_debug']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    install()

    port = int(os.environ.get('PORT', CONFIG['port']))

    log.info(
        'Server listen on {}:{}'.format(CONFIG['host'], port)
    )

    run_app(make_app(), host=CONFIG['host'], port=port)

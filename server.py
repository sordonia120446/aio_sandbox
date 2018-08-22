from aiohttp import web

from webapp.current_app import init_app


app = init_app()
web.run_app(app, port=3000)

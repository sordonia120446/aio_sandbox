from aiohttp import web
import jinja2
import aiohttp_jinja2

from webapp.views import routes


async def init_app():
    app = web.Application()
    app['websockets'] = {}
    app.on_shutdown.append(shutdown)

    pkg_loader = jinja2.PackageLoader('webapp', 'templates')
    aiohttp_jinja2.setup(app, loader=pkg_loader)

    app.add_routes(routes)
    return app


async def shutdown(app):
    for ws in app['websockets'].values():
        await ws.close()
    app['websockets'].clear()

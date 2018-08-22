from aiohttp import web, WSMsgType
import aiohttp_jinja2


routes = web.RouteTableDef()


@routes.view('/')
class IndexView(web.View):
    async def get(self):
        ws_current = web.WebSocketResponse()
        ws_ready = ws_current.can_prepare(self.request)
        if not ws_ready.ok:
            return aiohttp_jinja2.render_template('index.html', self.request, {})

        await ws_current.prepare(self.request)

        name = 'Sam O'

        await ws_current.send_json({'action': 'connect', 'name': name})

        for ws in self.request.app['websockets'].values():
            await ws.send_json({'action': 'join', 'name': name})
        self.request.app['websockets'][name] = ws_current

        while True:
            msg = await ws_current.receive()

            if msg.type == WSMsgType.text:
                for ws in self.request.app['websockets'].values():
                    if ws is not ws_current:
                        await ws.send_json(
                            {'action': 'sent', 'name': name, 'text': msg.data})
            else:
                break

        del self.request.app['websockets'][name]
        for ws in self.request.app['websockets'].values():
            await ws.send_json({'action': 'disconnect', 'name': name})

        return ws_current

    async def post(self):
        raise NotImplementedError

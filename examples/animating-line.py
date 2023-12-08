#!/usr/bin/env python3

import numpy
import cairo
import asyncio
import libacmchristmas.tree


async def main():
    url = "wss://blinktest.acmcsuf.com/ws/018c34d7-8826-7577-a03f-55e8cd8b0042"
    fps = 15

    tree = libacmchristmas.tree.TreeController(url)
    await tree.connect()
    assert tree.ix
    assert tree.iy

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, tree.ix, tree.iy)
    context = cairo.Context(surface)

    y = 0
    while True:
        y = (y + 1) % tree.iy

        context.set_source_rgb(1, 0, 0)
        context.paint()

        context.set_source_rgb(0, 0, 1)
        context.set_line_width(10)
        context.move_to(0, y)
        context.line_to(tree.ix, y)
        context.stroke()

        await tree.update_image(numpy.asarray(surface.get_data()))
        await asyncio.sleep(1 / fps)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

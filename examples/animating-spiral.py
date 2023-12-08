#!/usr/bin/env python3

import numpy
import cairo
import asyncio
import libacmchristmas.tree


async def main():
    url = "wss://blinktest.acmcsuf.com/ws/018c34d7-8826-7577-a03f-55e8cd8b0042"
    fps = 25

    tree = libacmchristmas.tree.TreeController(url)
    await tree.connect()
    assert tree.ix
    assert tree.iy

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, tree.ix, tree.iy)
    context = cairo.Context(surface)

    stepCount = 50
    loopCount = 20
    loopSpacing = 2
    rotationSpeed = 0.2
    strokeWidth = 5
    strokeColor = (1.0, 1.0, 1.0)

    # https://stackoverflow.com/a/12887250/5041327
    rotation = 0
    while True:
        rotation += rotationSpeed

        context.set_source_rgb(0, 0, 0)
        context.paint()

        context.set_source_rgb(*strokeColor)
        context.set_line_width(strokeWidth)

        stepSize = (2 * numpy.pi) / stepCount
        endAngle = 2 * numpy.pi * loopCount
        finished = False
        centerX = tree.ix / 2
        centerY = tree.iy / 2

        context.move_to(centerX, centerY)

        angle = 0
        while not finished:
            if angle > endAngle:
                angle = endAngle
                finished = True

            scalar = loopSpacing * angle
            rotatedAngle = angle + rotation
            x = centerX + scalar * numpy.cos(rotatedAngle)
            y = centerY + scalar * numpy.sin(rotatedAngle)

            context.line_to(x, y)
            angle += stepSize

        context.stroke()

        await tree.update_image(numpy.asarray(surface.get_data()))
        await asyncio.sleep(1 / fps)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

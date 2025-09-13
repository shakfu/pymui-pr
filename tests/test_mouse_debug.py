#!/usr/bin/env python3

import sys
import ctypes
import sdl2
from pathlib import Path

ROOTDIR = Path(__file__).parent.parent / "src"

try:
    from pymui import pymui
except ImportError:
    sys.path.insert(0, str(ROOTDIR))
    from pymui import pymui


def main():
    """Debug mouse input specifically"""
    # Initialize SDL
    if sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING) != 0:
        print(f"SDL_Init Error: {sdl2.SDL_GetError()}")
        return 1

    try:
        print("Initializing renderer...")
        pymui.renderer_init()
        print("Creating context...")
        ctx = pymui.Context()
        print("Mouse debug test started - move mouse and click to see events")

        running = True
        frame_count = 0

        while running and frame_count < 600:  # Max 10 seconds at 60fps
            frame_count += 1

            # Handle SDL events
            event = sdl2.SDL_Event()
            while sdl2.SDL_PollEvent(ctypes.byref(event)):
                if event.type == sdl2.SDL_QUIT:
                    print("Quit event received")
                    running = False
                elif event.type == sdl2.SDL_KEYDOWN and event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    print("Escape pressed")
                    running = False
                elif event.type == sdl2.SDL_MOUSEMOTION:
                    print(f"Mouse motion: ({event.motion.x}, {event.motion.y})")
                    ctx.input_mousemove(event.motion.x, event.motion.y)
                elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                    print(f"Mouse down: button={event.button.button} at ({event.button.x}, {event.button.y})")
                    btn = pymui.Mouse.LEFT if event.button.button == sdl2.SDL_BUTTON_LEFT else 0
                    if btn:
                        ctx.input_mousedown(event.button.x, event.button.y, btn)
                elif event.type == sdl2.SDL_MOUSEBUTTONUP:
                    print(f"Mouse up: button={event.button.button} at ({event.button.x}, {event.button.y})")
                    btn = pymui.Mouse.LEFT if event.button.button == sdl2.SDL_BUTTON_LEFT else 0
                    if btn:
                        ctx.input_mouseup(event.button.x, event.button.y, btn)

            # Process frame
            ctx.begin()

            # Simple button test
            if ctx.begin_window("Mouse Test", pymui.rect(100, 100, 200, 100)):
                if ctx.button("Test Button"):
                    print("*** BUTTON CLICKED! ***")
                ctx.end_window()

            ctx.end()

            # Render
            pymui.renderer_clear(pymui.color(32, 32, 32, 255))

            # Process commands
            ctx.reset_command_iterator()
            while True:
                cmd = ctx.next_command()
                if cmd is None:
                    break

                if cmd.type == pymui.Command.TEXT:
                    pymui.renderer_draw_text(cmd.text.encode('utf-8'), cmd.pos, cmd.color)
                elif cmd.type == pymui.Command.RECT:
                    pymui.renderer_draw_rect(cmd.rect, cmd.color)
                elif cmd.type == pymui.Command.ICON:
                    pymui.renderer_draw_icon(cmd.icon_id, cmd.rect, cmd.color)
                elif cmd.type == pymui.Command.CLIP:
                    pymui.renderer_set_clip_rect(cmd.rect)

            pymui.renderer_present()

        print("Mouse debug test completed")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        sdl2.SDL_Quit()

    return 0


if __name__ == "__main__":
    sys.exit(main())
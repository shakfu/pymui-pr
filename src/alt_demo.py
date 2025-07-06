#!/usr/bin/env python3
"""
Python version of the microui SDL demo using pymui
"""

import sys
import sdl2
import sdl2.ext
from pymui import Context, Rect, Color, Vec2, Option, Result, Mouse, Key, ColorIndex


class SDLRenderer:
    """Simple SDL2 renderer for microui"""
    
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        
        # Initialize SDL2
        sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
        
        # Create window
        self.window = sdl2.SDL_CreateWindow(
            b"PyMUI Demo",
            sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED,
            width, height,
            sdl2.SDL_WINDOW_SHOWN
        )
        
        # Create renderer
        self.renderer = sdl2.SDL_CreateRenderer(
            self.window, -1,
            sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC
        )
        
        # Initialize font (simple bitmap font)
        self.font_texture = None
        self.font_width = 8
        self.font_height = 12
        
    def init(self):
        """Initialize the renderer"""
        # Create a simple font texture (8x12 pixels per character)
        # This is a simplified version - in a real implementation you'd load a proper font
        font_surface = sdl2.SDL_CreateRGBSurface(
            0, 256 * self.font_width, self.font_height,
            32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000
        )
        
        # Fill with white pixels for basic text rendering
        sdl2.SDL_FillRect(font_surface, None, 0xFFFFFFFF)
        
        self.font_texture = sdl2.SDL_CreateTextureFromSurface(self.renderer, font_surface)
        sdl2.SDL_FreeSurface(font_surface)
    
    def draw_rect(self, rect, color):
        """Draw a rectangle"""
        sdl_rect = sdl2.SDL_Rect(rect.x, rect.y, rect.w, rect.h)
        sdl2.SDL_SetRenderDrawColor(self.renderer, color.r, color.g, color.b, color.a)
        sdl2.SDL_RenderFillRect(self.renderer, sdl_rect)
    
    def draw_text(self, text, pos, color):
        """Draw text (simplified)"""
        # This is a simplified text renderer
        # In a real implementation, you'd use SDL_ttf or a bitmap font
        x, y = pos.x, pos.y
        for char in text:
            if char == ' ':
                x += self.font_width
                continue
                
            # Simple character rendering (just draw a colored rectangle for each char)
            char_rect = sdl2.SDL_Rect(x, y, self.font_width, self.font_height)
            sdl2.SDL_SetRenderDrawColor(self.renderer, color.r, color.g, color.b, color.a)
            sdl2.SDL_RenderDrawRect(self.renderer, char_rect)
            x += self.font_width
    
    def draw_icon(self, icon_id, rect, color):
        """Draw an icon (simplified)"""
        # For simplicity, just draw a small rectangle
        icon_size = 8
        x = rect.x + (rect.w - icon_size) // 2
        y = rect.y + (rect.h - icon_size) // 2
        icon_rect = sdl2.SDL_Rect(x, y, icon_size, icon_size)
        sdl2.SDL_SetRenderDrawColor(self.renderer, color.r, color.g, color.b, color.a)
        sdl2.SDL_RenderFillRect(self.renderer, icon_rect)
    
    def get_text_width(self, text, length=-1):
        """Get text width"""
        if length == -1:
            length = len(text)
        return length * self.font_width
    
    def get_text_height(self):
        """Get text height"""
        return self.font_height
    
    def set_clip_rect(self, rect):
        """Set clip rectangle"""
        sdl_rect = sdl2.SDL_Rect(rect.x, rect.y, rect.w, rect.h)
        sdl2.SDL_RenderSetClipRect(self.renderer, sdl_rect)
    
    def clear(self, color):
        """Clear the screen"""
        sdl2.SDL_SetRenderDrawColor(self.renderer, color.r, color.g, color.b, color.a)
        sdl2.SDL_RenderClear(self.renderer)
    
    def present(self):
        """Present the rendered frame"""
        sdl2.SDL_RenderPresent(self.renderer)
    
    def cleanup(self):
        """Clean up SDL resources"""
        if self.font_texture:
            sdl2.SDL_DestroyTexture(self.font_texture)
        if self.renderer:
            sdl2.SDL_DestroyRenderer(self.renderer)
        if self.window:
            sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()


class Demo:
    """Main demo application"""
    
    def __init__(self):
        self.renderer = SDLRenderer()
        self.renderer.init()
        
        # Initialize microui context
        self.ctx = Context()
        
        # Set up text rendering callbacks
        # self.ctx.text_width = self.text_width
        # self.ctx.text_height = self.text_height
        
        # Demo state
        self.logbuf = ""
        self.logbuf_updated = False
        self.bg = [90.0, 95.0, 100.0]  # Use floats for sliders
        self.input_buf = ""
        
        # Input mapping
        self.button_map = {
            sdl2.SDL_BUTTON_LEFT: Mouse.LEFT,
            sdl2.SDL_BUTTON_RIGHT: Mouse.RIGHT,
            sdl2.SDL_BUTTON_MIDDLE: Mouse.MIDDLE,
        }
        
        self.key_map = {
            sdl2.SDLK_LSHIFT: Key.SHIFT,
            sdl2.SDLK_RSHIFT: Key.SHIFT,
            sdl2.SDLK_LCTRL: Key.CTRL,
            sdl2.SDLK_RCTRL: Key.CTRL,
            sdl2.SDLK_LALT: Key.ALT,
            sdl2.SDLK_RALT: Key.ALT,
            sdl2.SDLK_RETURN: Key.RETURN,
            sdl2.SDLK_BACKSPACE: Key.BACKSPACE,
        }
    
    def text_width(self, font, text, length=-1):
        """Text width callback"""
        if length == -1:
            length = len(text)
        return self.renderer.get_text_width(text, length)
    
    def text_height(self, font):
        """Text height callback"""
        return self.renderer.get_text_height()
    
    def write_log(self, text):
        """Write text to log buffer"""
        if self.logbuf:
            self.logbuf += "\n"
        self.logbuf += text
        self.logbuf_updated = True
    
    def test_window(self):
        """Create the main demo window"""
        if self.ctx.begin_window("Demo Window", Rect(40, 40, 300, 450)):
            # Window info
            if self.ctx.header("Window Info"):
                # Note: In the C version, this gets the current container
                # Python version doesn't expose this directly, so we'll skip it
                pass
            
            # Test buttons
            if self.ctx.header("Test Buttons", Option.EXPANDED):
                # Note: layout_row is commented out in pymui, so we'll use layout_width/height
                self.ctx.layout_width(86)
                self.ctx.label("Test buttons 1:")
                self.ctx.layout_width(-110)
                if self.ctx.button("Button 1"):
                    self.write_log("Pressed button 1")
                self.ctx.layout_width(-1)
                if self.ctx.button("Button 2"):
                    self.write_log("Pressed button 2")
                
                self.ctx.layout_width(86)
                self.ctx.label("Test buttons 2:")
                self.ctx.layout_width(-110)
                if self.ctx.button("Button 3"):
                    self.write_log("Pressed button 3")
                self.ctx.layout_width(-1)
                if self.ctx.button("Popup"):
                    self.ctx.open_popup("Test Popup")
                
                if self.ctx.begin_popup("Test Popup"):
                    self.ctx.button("Hello")
                    self.ctx.button("World")
                    self.ctx.end_popup()
            
            # Tree and text
            if self.ctx.header("Tree and Text", Option.EXPANDED):
                # Left column - tree
                self.ctx.layout_begin_column()
                self.ctx.layout_width(140)
                
                if self.ctx.begin_treenode("Test 1"):
                    if self.ctx.begin_treenode("Test 1a"):
                        self.ctx.label("Hello")
                        self.ctx.label("world")
                        self.ctx.end_treenode()
                    if self.ctx.begin_treenode("Test 1b"):
                        if self.ctx.button("Button 1"):
                            self.write_log("Pressed button 1")
                        if self.ctx.button("Button 2"):
                            self.write_log("Pressed button 2")
                        self.ctx.end_treenode()
                    self.ctx.end_treenode()
                
                if self.ctx.begin_treenode("Test 2"):
                    self.ctx.layout_width(54)
                    if self.ctx.button("Button 3"):
                        self.write_log("Pressed button 3")
                    self.ctx.layout_width(54)
                    if self.ctx.button("Button 4"):
                        self.write_log("Pressed button 4")
                    self.ctx.layout_width(54)
                    if self.ctx.button("Button 5"):
                        self.write_log("Pressed button 5")
                    self.ctx.layout_width(54)
                    if self.ctx.button("Button 6"):
                        self.write_log("Pressed button 6")
                    self.ctx.end_treenode()
                
                if self.ctx.begin_treenode("Test 3"):
                    checks = [1, 0, 1]  # Static state
                    self.ctx.checkbox("Checkbox 1", checks[0])
                    self.ctx.checkbox("Checkbox 2", checks[1])
                    self.ctx.checkbox("Checkbox 3", checks[2])
                    self.ctx.end_treenode()
                
                self.ctx.layout_end_column()
                
                # Right column - text
                self.ctx.layout_begin_column()
                self.ctx.layout_width(-1)
                self.ctx.text("Lorem ipsum dolor sit amet, consectetur adipiscing "
                            "elit. Maecenas lacinia, sem eu lacinia molestie, mi risus faucibus "
                            "ipsum, eu varius magna felis a nulla.")
                self.ctx.layout_end_column()
            
            # Background color sliders
            if self.ctx.header("Background Color", Option.EXPANDED):
                # Sliders
                self.ctx.layout_begin_column()
                self.ctx.layout_width(46)
                self.ctx.label("Red:")
                self.ctx.layout_width(-1)
                self.ctx.slider(self.bg[0], 0, 255)
                
                self.ctx.layout_width(46)
                self.ctx.label("Green:")
                self.ctx.layout_width(-1)
                self.ctx.slider(self.bg[1], 0, 255)
                
                self.ctx.layout_width(46)
                self.ctx.label("Blue:")
                self.ctx.layout_width(-1)
                self.ctx.slider(self.bg[2], 0, 255)
                self.ctx.layout_end_column()
                
                # Color preview
                r = self.ctx.layout_next()
                self.ctx.draw_rect(r, Color(int(self.bg[0]), int(self.bg[1]), int(self.bg[2]), 255))
                color_text = f"#{int(self.bg[0]):02X}{int(self.bg[1]):02X}{int(self.bg[2]):02X}"
                # Note: draw_control_text is not exposed in pymui, so we'll use draw_text
                self.ctx.draw_text(None, color_text, Vec2(r.x + r.w//2, r.y + r.h//2), Color(255, 255, 255, 255))
            
            self.ctx.end_window()
    
    def log_window(self):
        """Create the log window"""
        if self.ctx.begin_window("Log Window", Rect(350, 40, 300, 200)):
            # Output text panel
            self.ctx.layout_height(-25)
            self.ctx.begin_panel("Log Output")
            self.ctx.layout_height(-1)
            self.ctx.text(self.logbuf)
            self.ctx.end_panel()
            
            # Input textbox + submit button
            submitted = False
            self.ctx.layout_width(-70)
            
            # Note: textbox handling is simplified here
            # In a real implementation, you'd need to manage the buffer properly
            result = self.ctx.textbox(self.input_buf, 128)
            if result & Result.SUBMIT:
                submitted = True
            
            self.ctx.layout_width(-1)
            if self.ctx.button("Submit"):
                submitted = True
            
            if submitted and self.input_buf:
                self.write_log(self.input_buf)
                self.input_buf = ""
            
            self.ctx.end_window()
    
    def style_window(self):
        """Create the style editor window"""
        colors = [
            ("text:", ColorIndex.TEXT),
            ("border:", ColorIndex.BORDER),
            ("windowbg:", ColorIndex.WINDOWBG),
            ("titlebg:", ColorIndex.TITLEBG),
            ("titletext:", ColorIndex.TITLETEXT),
            ("panelbg:", ColorIndex.PANELBG),
            ("button:", ColorIndex.BUTTON),
            ("buttonhover:", ColorIndex.BUTTONHOVER),
            ("buttonfocus:", ColorIndex.BUTTONFOCUS),
            ("base:", ColorIndex.BASE),
            ("basehover:", ColorIndex.BASEHOVER),
            ("basefocus:", ColorIndex.BASEFOCUS),
            ("scrollbase:", ColorIndex.SCROLLBASE),
            ("scrollthumb:", ColorIndex.SCROLLTHUMB),
        ]
        
        if self.ctx.begin_window("Style Editor", Rect(350, 250, 300, 240)):
            # Note: get_current_container is not available, so we'll use a fixed width
            sw = 40  # Fixed width for sliders
            
            for label, color_idx in colors:
                self.ctx.layout_width(80)
                self.ctx.label(label)
                color = self.ctx.style.get_color(color_idx)
                
                # Create sliders for RGBA values
                self.ctx.layout_width(sw)
                self.ctx.slider(float(color.r), 0, 255)
                self.ctx.layout_width(sw)
                self.ctx.slider(float(color.g), 0, 255)
                self.ctx.layout_width(sw)
                self.ctx.slider(float(color.b), 0, 255)
                self.ctx.layout_width(sw)
                self.ctx.slider(float(color.a), 0, 255)
                
                self.ctx.layout_width(-1)
                self.ctx.draw_rect(self.ctx.layout_next(), color)
            
            self.ctx.end_window()
    
    def process_frame(self):
        """Process one frame of the UI"""
        self.ctx.begin()
        self.style_window()
        self.log_window()
        self.test_window()
        self.ctx.end()
    
    def handle_events(self):
        """Handle SDL events"""
        event = sdl2.SDL_Event()
        while sdl2.SDL_PollEvent(event):
            if event.type == sdl2.SDL_QUIT:
                return False
            
            elif event.type == sdl2.SDL_MOUSEMOTION:
                self.ctx.input_mousemove(event.motion.x, event.motion.y)
            
            elif event.type == sdl2.SDL_MOUSEWHEEL:
                self.ctx.input_scroll(0, event.wheel.y * -30)
            
            elif event.type == sdl2.SDL_TEXTINPUT:
                text = event.text.text.decode('utf-8')
                self.ctx.input_text(text)
            
            elif event.type in (sdl2.SDL_MOUSEBUTTONDOWN, sdl2.SDL_MOUSEBUTTONUP):
                button = self.button_map.get(event.button.button)
                if button:
                    if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                        self.ctx.input_mousedown(event.button.x, event.button.y, button)
                    else:
                        self.ctx.input_mouseup(event.button.x, event.button.y, button)
            
            elif event.type in (sdl2.SDL_KEYDOWN, sdl2.SDL_KEYUP):
                key = self.key_map.get(event.key.keysym.sym)
                if key:
                    if event.type == sdl2.SDL_KEYDOWN:
                        self.ctx.input_keydown(key)
                    else:
                        self.ctx.input_keyup(key)
        
        return True
    
    def render(self):
        """Render the frame"""
        self.renderer.clear(Color(int(self.bg[0]), int(self.bg[1]), int(self.bg[2]), 255))
        
        # Process microui commands
        # Note: This would need to be implemented based on how pymui exposes commands
        # For now, we'll just process the UI
        self.process_frame()
        
        self.renderer.present()
    
    def run(self):
        """Main application loop"""
        try:
            while True:
                if not self.handle_events():
                    break
                
                self.render()
                
                # Cap frame rate
                sdl2.SDL_Delay(16)  # ~60 FPS
        
        finally:
            self.renderer.cleanup()


def main():
    """Main entry point"""
    try:
        demo = Demo()
        demo.run()
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 
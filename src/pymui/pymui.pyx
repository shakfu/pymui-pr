from typing import TypeAlias

from libc.stdlib cimport malloc, calloc, realloc, free
from libc.string cimport memcpy, memset
# import numpy as np
# cimport numpy as np

cimport pymui



# Fused types
ctypedef fused number:
    int
    float

# Version function
def version() -> str:
    return MU_VERSION.decode()

def clamp(number x, number a, number b) -> number:
    return min(b, max(a, x))


# Basic struct classes
cdef class Vec2:
    cdef mu_Vec2 _vec
    
    def __cinit__(self, int x=0, int y=0):
        self._vec.x = x
        self._vec.y = y
    
    @property
    def x(self) -> int:
        return self._vec.x
    
    @x.setter
    def x(self, int value):
        self._vec.x = value
    
    @property
    def y(self) -> int:
        return self._vec.y
    
    @y.setter
    def y(self, int value):
        self._vec.y = value
    
    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"
    
    @staticmethod
    cdef Vec2 from_c(mu_Vec2 vec):
        cdef Vec2 result = Vec2.__new__(Vec2)
        result._vec = vec
        return result
    
    cdef mu_Vec2 to_c(self):
        return self._vec


cdef class Rect:
    cdef mu_Rect _rect
    
    def __cinit__(self, int x=0, int y=0, int w=0, int h=0):
        self._rect.x = x
        self._rect.y = y
        self._rect.w = w
        self._rect.h = h
    
    @property
    def x(self) -> int:
        return self._rect.x
    
    @x.setter
    def x(self, int value):
        self._rect.x = value
    
    @property
    def y(self) -> int:
        return self._rect.y
    
    @y.setter
    def y(self, int value):
        self._rect.y = value
    
    @property
    def w(self) -> int:
        return self._rect.w
    
    @w.setter
    def w(self, int value):
        self._rect.w = value
    
    @property
    def h(self) -> int:
        return self._rect.h
    
    @h.setter
    def h(self, int value):
        self._rect.h = value
    
    def __repr__(self):
        return f"Rect({self.x}, {self.y}, {self.w}, {self.h})"
    
    @staticmethod
    cdef Rect from_c(mu_Rect rect):
        cdef Rect result = Rect.__new__(Rect)
        result._rect = rect
        return result
    
    cdef mu_Rect to_c(self):
        return self._rect


cdef class Color:
    cdef mu_Color _color
    
    def __cinit__(self, int r=0, int g=0, int b=0, int a=255):
        self._color.r = r
        self._color.g = g
        self._color.b = b
        self._color.a = a
    
    @property
    def r(self) -> int:
        return self._color.r
    
    @r.setter
    def r(self, int value):
        self._color.r = value
    
    @property
    def g(self) -> int:
        return self._color.g
    
    @g.setter
    def g(self, int value):
        self._color.g = value
    
    @property
    def b(self) -> int:
        return self._color.b
    
    @b.setter
    def b(self, int value):
        self._color.b = value
    
    @property
    def a(self) -> int:
        return self._color.a
    
    @a.setter
    def a(self, int value):
        self._color.a = value
    
    def __repr__(self):
        return f"Color({self.r}, {self.g}, {self.b}, {self.a})"
    
    @staticmethod
    cdef Color from_c(mu_Color color):
        cdef Color result = Color.__new__(Color)
        result._color = color
        return result
    
    cdef mu_Color to_c(self):
        return self._color


cdef class Style:
    cdef mu_Style* ptr
    cdef bint _owner

    def __cinit__(self):
        self.ptr = NULL
        self.owner = False

    def __dealloc__(self):
        # De-allocate if not null and flag is set
        if self.ptr is not NULL and self.owner is True:
            free(self.ptr)
            self.ptr = NULL

    def __init__(self):
        # Prevent accidental instantiation from normal Python code
        # since we cannot pass a struct pointer into a Python constructor.
        raise TypeError("This class cannot be instantiated directly.")

    @staticmethod
    cdef Style from_ptr(mu_Style* ptr, bint owner=False):
        cdef Style wrapper = Style.__new__(Style)
        wrapper.ptr = ptr
        wrapper.owner = owner
        return wrapper

    @staticmethod
    cdef Style new():
        cdef mu_Style* _ptr = <mu_Style*>malloc(sizeof(mu_Style))
        if _ptr is NULL:
            raise MemoryError("Failed to allocate Style")
        memset(_ptr, 0, sizeof(mu_Style))
        return Style.from_ptr(_ptr, owner=True)

    # @property
    # def font(self):
    #     return <object>self.ptr.font
    
    # @font.setter
    # def font(self, font):
    #     self.ptr.font = <mu_Font>font
    
    @property
    def size(self) -> Vec2:
        return Vec2.from_c(self.ptr.size)
    
    @size.setter
    def size(self, Vec2 value):
        self.ptr.size = value.to_c()
    
    @property
    def padding(self) -> int:
        return self.ptr.padding
    
    @padding.setter
    def padding(self, int value):
        self.ptr.padding = value
    
    @property
    def spacing(self) -> int:
        return self.ptr.spacing
    
    @spacing.setter
    def spacing(self, int value):
        self.ptr.spacing = value
    
    @property
    def indent(self) -> int:
        return self.ptr.indent
    
    @indent.setter
    def indent(self, int value):
        self.ptr.indent = value
    
    @property
    def title_height(self) -> int:
        return self.ptr.title_height
    
    @title_height.setter
    def title_height(self, int value):
        self.ptr.title_height = value
    
    @property
    def scrollbar_size(self) -> int:
        return self.ptr.scrollbar_size
    
    @scrollbar_size.setter
    def scrollbar_size(self, int value):
        self.ptr.scrollbar_size = value
    
    @property
    def thumb_size(self) -> int:
        return self.ptr.thumb_size
    
    @thumb_size.setter
    def thumb_size(self, int value):
        self.ptr.thumb_size = value
    
    def get_color(self, int index) -> Color:
        if 0 <= index < MU_COLOR_MAX:
            return Color.from_c(self.ptr.colors[index])
        raise IndexError("Color index out of range")
    
    def set_color(self, int index, Color color):
        if 0 <= index < MU_COLOR_MAX:
            self.ptr.colors[index] = color.to_c()
        else:
            raise IndexError("Color index out of range")


# Main Context class
cdef class Context:
    cdef mu_Context* ptr
    cdef bint owner

    def __cinit__(self):
        self.ptr = NULL
        self.owner = False

    def __dealloc__(self):
        # De-allocate if not null and flag is set
        if self.ptr is not NULL and self.owner is True:
            free(self.ptr)
            self.ptr = NULL

    def __init__(self):
        self.ptr = <mu_Context*>malloc(sizeof(mu_Context))
        if self.ptr is NULL:
            raise MemoryError("Failed to allocate Context")
        mu_init(self.ptr)
        self.owner = True

    @staticmethod
    cdef Context from_ptr(mu_Context* ptr, bint owner=False):
        cdef Context wrapper = Context.__new__(Context)
        wrapper.ptr = ptr
        wrapper.owner = owner
        return wrapper

    @staticmethod
    cdef Context new():
        cdef mu_Context* _ptr = <mu_Context*>malloc(sizeof(mu_Context))
        if _ptr is NULL:
            raise MemoryError("Failed to allocate Context")
        mu_init(_ptr)
        return Context.from_ptr(_ptr, owner=True)

    @property
    def style(self) -> Style:
        return Style.from_ptr(<mu_Style*>self.ptr.style)

    def begin(self):
        """Start a new frame"""
        mu_begin(self.ptr)
    
    def end(self):
        """End the current frame"""
        mu_end(self.ptr)
    
    def set_focus(self, unsigned int id):
        """Set the focused widget"""
        mu_set_focus(self.ptr, id)
    
    # def get_id(self, data, int size) -> int:
    #     """Get an ID for the given data"""
    #     cdef bytes bdata
    #     if isinstance(data, str):
    #         bdata = data.encode('utf-8')
    #     elif isinstance(data, bytes):
    #         bdata = data
    #     else:
    #         bdata = str(data).encode('utf-8')
    #     return mu_get_id(self.ptr, bdata, len(bdata))
    
    # def push_id(self, data, int size):
    #     """Push an ID onto the ID stack"""
    #     cdef bytes bdata
    #     if isinstance(data, str):
    #         bdata = data.encode('utf-8')
    #     elif isinstance(data, bytes):
    #         bdata = data
    #     else:
    #         bdata = str(data).encode('utf-8')
    #     mu_push_id(self.ptr, bdata, len(bdata))
    
    def pop_id(self):
        """Pop an ID from the ID stack"""
        mu_pop_id(self.ptr)
    
    def push_clip_rect(self, Rect rect):
        """Push a clip rectangle"""
        mu_push_clip_rect(self.ptr, rect.to_c())
    
    def pop_clip_rect(self):
        """Pop a clip rectangle"""
        mu_pop_clip_rect(self.ptr)
    
    def get_clip_rect(self) -> Rect:
        """Get the current clip rectangle"""
        return Rect.from_c(mu_get_clip_rect(self.ptr))
    
    def check_clip(self, Rect rect) -> int:
        """Check if a rectangle is clipped"""
        return mu_check_clip(self.ptr, rect.to_c())
    
    # Input functions
    def input_mousemove(self, int x, int y):
        """Handle mouse movement"""
        mu_input_mousemove(self.ptr, x, y)
    
    def input_mousedown(self, int x, int y, int btn):
        """Handle mouse button press"""
        mu_input_mousedown(self.ptr, x, y, btn)
    
    def input_mouseup(self, int x, int y, int btn):
        """Handle mouse button release"""
        mu_input_mouseup(self.ptr, x, y, btn)
    
    def input_scroll(self, int x, int y):
        """Handle scroll input"""
        mu_input_scroll(self.ptr, x, y)
    
    def input_keydown(self, int key):
        """Handle key press"""
        mu_input_keydown(self.ptr, key)
    
    def input_keyup(self, int key):
        """Handle key release"""
        mu_input_keyup(self.ptr, key)
    
    def input_text(self, str text):
        """Handle text input"""
        cdef bytes btext = text.encode('utf-8')
        mu_input_text(self.ptr, btext)
    
    # Layout functions
    # def layout_row(self, int items, widths, int height):
    #     """Set up a row layout"""
    #     cdef int* width_array = NULL
    #     cdef int i
        
    #     if widths is not None:
    #         if isinstance(widths, (list, tuple)):
    #             width_array = <int*>malloc(items * sizeof(int))
    #             for i in range(min(items, len(widths))):
    #                 width_array[i] = widths[i]
    #         elif isinstance(widths, np.ndarray):
    #             width_array = <int*>np.PyArray_DATA(widths)
        
    #     mu_layout_row(self.ptr, items, width_array, height)
        
    #     if width_array is not NULL and not isinstance(widths, np.ndarray):
    #         free(width_array)
    
    def layout_width(self, int width):
        """Set layout width"""
        mu_layout_width(self.ptr, width)
    
    def layout_height(self, int height):
        """Set layout height"""
        mu_layout_height(self.ptr, height)
    
    def layout_begin_column(self):
        """Begin a column layout"""
        mu_layout_begin_column(self.ptr)
    
    def layout_end_column(self):
        """End a column layout"""
        mu_layout_end_column(self.ptr)
    
    def layout_set_next(self, Rect rect, int relative):
        """Set the next layout rectangle"""
        mu_layout_set_next(self.ptr, rect.to_c(), relative)
    
    def layout_next(self) -> Rect:
        """Get the next layout rectangle"""
        return Rect.from_c(mu_layout_next(self.ptr))
    
    # Widget functions
    def text(self, str text):
        """Draw text"""
        cdef bytes btext = text.encode('utf-8')
        mu_text(self.ptr, btext)
    
    def label(self, str text):
        """Draw a label"""
        cdef bytes btext = text.encode('utf-8')
        mu_label(self.ptr, btext)
    
    def button(self, str label, int icon=0, int opt=0) -> int:
        """Create a button"""
        cdef bytes blabel = label.encode('utf-8')
        return mu_button_ex(self.ptr, blabel, icon, opt)
    
    def checkbox(self, str label, int state) -> int:
        """Create a checkbox"""
        cdef bytes blabel = label.encode('utf-8')
        return mu_checkbox(self.ptr, blabel, &state)
    
    def textbox(self, str buf, int bufsz, int opt=0) -> int:
        """Create a textbox"""
        cdef bytes bbuf = buf.encode('utf-8')
        cdef char* cbuf = bbuf
        return mu_textbox_ex(self.ptr, cbuf, bufsz, opt)
    
    def slider(self, float value, float low, float high, float step=0, str fmt="%.2f", int opt=0) -> int:
        """Create a slider"""
        cdef bytes bfmt = fmt.encode('utf-8')
        return mu_slider_ex(self.ptr, &value, low, high, step, bfmt, opt)
    
    def number(self, float value, float step, str fmt="%.2f", int opt=0) -> int:
        """Create a number input"""
        cdef bytes bfmt = fmt.encode('utf-8')
        return mu_number_ex(self.ptr, &value, step, bfmt, opt)
    
    def header(self, str label, int opt=0) -> int:
        """Create a header"""
        cdef bytes blabel = label.encode('utf-8')
        return mu_header_ex(self.ptr, blabel, opt)
    
    def begin_treenode(self, str label, int opt=0) -> int:
        """Begin a tree node"""
        cdef bytes blabel = label.encode('utf-8')
        return mu_begin_treenode_ex(self.ptr, blabel, opt)
    
    def end_treenode(self):
        """End a tree node"""
        mu_end_treenode(self.ptr)
    
    def begin_window(self, str title, Rect rect, int opt=0) -> int:
        """Begin a window"""
        cdef bytes btitle = title.encode('utf-8')
        return mu_begin_window_ex(self.ptr, btitle, rect.to_c(), opt)
    
    def end_window(self):
        """End a window"""
        mu_end_window(self.ptr)
    
    def open_popup(self, str name):
        """Open a popup"""
        cdef bytes bname = name.encode('utf-8')
        mu_open_popup(self.ptr, bname)
    
    def begin_popup(self, str name) -> int:
        """Begin a popup"""
        cdef bytes bname = name.encode('utf-8')
        return mu_begin_popup(self.ptr, bname)
    
    def end_popup(self):
        """End a popup"""
        mu_end_popup(self.ptr)
    
    def begin_panel(self, str name, int opt=0):
        """Begin a panel"""
        cdef bytes bname = name.encode('utf-8')
        mu_begin_panel_ex(self.ptr, bname, opt)
    
    def end_panel(self):
        """End a panel"""
        mu_end_panel(self.ptr)
    
    # Drawing functions
    def draw_rect(self, Rect rect, Color color):
        """Draw a rectangle"""
        mu_draw_rect(self.ptr, rect.to_c(), color.to_c())
    
    def draw_box(self, Rect rect, Color color):
        """Draw a box"""
        mu_draw_box(self.ptr, rect.to_c(), color.to_c())
    
    def draw_text(self, font, str text, Vec2 pos, Color color):
        """Draw text"""
        cdef bytes btext = text.encode('utf-8')
        mu_draw_text(self.ptr, <mu_Font>font, btext, len(btext), pos.to_c(), color.to_c())
    
    def draw_icon(self, int id, Rect rect, Color color):
        """Draw an icon"""
        mu_draw_icon(self.ptr, id, rect.to_c(), color.to_c())
    
    # Utility functions
    @staticmethod
    def vec2(int x, int y) -> Vec2:
        """Create a Vec2"""
        return Vec2.from_c(mu_vec2(x, y))
    
    @staticmethod
    def rect(int x, int y, int w, int h) -> Rect:
        """Create a Rect"""
        return Rect.from_c(mu_rect(x, y, w, h))
    
    @staticmethod
    def color(int r, int g, int b, int a=255) -> Color:
        """Create a Color"""
        return Color.from_c(mu_color(r, g, b, a))
    
    # Mouse over check
    def mouse_over(self, Rect rect) -> int:
        """Check if mouse is over a rectangle"""
        return mu_mouse_over(self.ptr, rect.to_c())


# Constants for easy access
class Clip:
    PART = MU_CLIP_PART
    ALL = MU_CLIP_ALL

class Command:
    JUMP = MU_COMMAND_JUMP
    CLIP = MU_COMMAND_CLIP
    RECT = MU_COMMAND_RECT
    TEXT = MU_COMMAND_TEXT
    ICON = MU_COMMAND_ICON
    MAX = MU_COMMAND_MAX

class ColorIndex:
    TEXT = MU_COLOR_TEXT
    BORDER = MU_COLOR_BORDER
    WINDOWBG = MU_COLOR_WINDOWBG
    TITLEBG = MU_COLOR_TITLEBG
    TITLETEXT = MU_COLOR_TITLETEXT
    PANELBG = MU_COLOR_PANELBG
    BUTTON = MU_COLOR_BUTTON
    BUTTONHOVER = MU_COLOR_BUTTONHOVER
    BUTTONFOCUS = MU_COLOR_BUTTONFOCUS
    BASE = MU_COLOR_BASE
    BASEHOVER = MU_COLOR_BASEHOVER
    BASEFOCUS = MU_COLOR_BASEFOCUS
    SCROLLBASE = MU_COLOR_SCROLLBASE
    SCROLLTHUMB = MU_COLOR_SCROLLTHUMB
    MAX = MU_COLOR_MAX

class Icon:
    CLOSE = MU_ICON_CLOSE
    CHECK = MU_ICON_CHECK
    COLLAPSED = MU_ICON_COLLAPSED
    EXPANDED = MU_ICON_EXPANDED
    MAX = MU_ICON_MAX

class Result:
    ACTIVE = MU_RES_ACTIVE
    SUBMIT = MU_RES_SUBMIT
    CHANGE = MU_RES_CHANGE

class Option:
    ALIGNCENTER = MU_OPT_ALIGNCENTER
    ALIGNRIGHT = MU_OPT_ALIGNRIGHT
    NOINTERACT = MU_OPT_NOINTERACT
    NOFRAME = MU_OPT_NOFRAME
    NORESIZE = MU_OPT_NORESIZE
    NOSCROLL = MU_OPT_NOSCROLL
    NOCLOSE = MU_OPT_NOCLOSE
    NOTITLE = MU_OPT_NOTITLE
    HOLDFOCUS = MU_OPT_HOLDFOCUS
    AUTOSIZE = MU_OPT_AUTOSIZE
    POPUP = MU_OPT_POPUP
    CLOSED = MU_OPT_CLOSED
    EXPANDED = MU_OPT_EXPANDED

class Mouse:
    LEFT = MU_MOUSE_LEFT
    RIGHT = MU_MOUSE_RIGHT
    MIDDLE = MU_MOUSE_MIDDLE

class Key:
    SHIFT = MU_KEY_SHIFT
    CTRL = MU_KEY_CTRL
    ALT = MU_KEY_ALT
    BACKSPACE = MU_KEY_BACKSPACE
    RETURN = MU_KEY_RETURN


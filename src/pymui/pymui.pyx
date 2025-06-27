from libc.stdlib cimport malloc, calloc, realloc, free

cimport pymui

def version() -> str:
    return MU_VERSION.decode()


cdef class Context:
    cdef mu_Context* ptr
    cdef bint owner

    def __cinit__(self):
        self.ptr = NULL
        self.owner = False

    def __dealloc__(self):
        if self.ptr is not NULL and self.owner is True:
            free(self.ptr)
            self.ptr = NULL

    def __init__(self):
        self.ptr = <mu_Context*>malloc(sizeof(mu_Context))
        mu_init(self.ptr)
        self.owner = True

    def begin(self):
        mu_begin(self.ptr)

    def end(self):
        mu_end(self.ptr)


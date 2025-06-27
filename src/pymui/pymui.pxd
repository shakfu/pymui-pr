from libc.stdlib cimport malloc, calloc, realloc, free

cdef extern from "microui.h":

    cdef const char* MU_VERSION

    cdef int MU_COMMANDLIST_SIZE
    cdef int MU_ROOTLIST_SIZE
    cdef int MU_CONTAINERSTACK_SIZE
    cdef int MU_CLIPSTACK_SIZE
    cdef int MU_IDSTACK_SIZE
    cdef int MU_LAYOUTSTACK_SIZE
    cdef int MU_CONTAINERPOOL_SIZE
    cdef int MU_TREENODEPOOL_SIZE
    cdef int MU_MAX_WIDTHS


    # cdef enum:
    #     MU_CLIP_PART = 1
    #     MU_CLIP_ALL


    # ctypedef struct mu_Context: pass
    # ctypedef unsigned mu_Id
    # # ctypedef MU_REAL mu_Real
    # ctypedef void* mu_Font

    # cdef struct mu_Vec2:
    #     int x
    #     int y


    # etc

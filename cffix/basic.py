from cffi import FFI

ffi = FFI()

ffi.cdef(
    """int printf(const char *format, ...);   // copy-pasted from the man page""")

C = ffi.dlopen(None)

arg = ffi.new("char[]", "Testing".encode())


C.printf("Testing %s\n".encode(), arg)

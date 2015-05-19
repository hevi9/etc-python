from cffi import FFI
ffi = FFI()
ffi.cdef("""     // some declarations from the man page
    struct passwd {
        char *pw_name;
        ...;
    };
    struct passwd *getpwuid(int uid);
""")
C = ffi.verify("""   // passed to the real C compiler
#include <sys/types.h>
#include <pwd.h>
""", libraries=[])   # or a list of libraries to link with
p = C.getpwuid(0)

print(p)
print(ffi.string(p.pw_name))

assert ffi.string(p.pw_name) == b'root'    # on Python 3: b'root'
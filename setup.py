import sys
import os
import platform
from setuptools import setup, Extension
from distutils.command.build_ext import build_ext as BaseBuildExt
from distutils.unixccompiler import UnixCCompiler
from distutils.util import get_platform
from distutils.sysconfig import customize_compiler

from pybind11 import get_include


EXTRA_COMPILE_ARGS = ['-std=c++11'] if platform.system != "Windows" else []


# On Darwin, UnixCCompiler uses "-L" for runtime lib paths
class DarwinCompiler(UnixCCompiler):

    def runtime_library_dir_option(self, dir):
        return ["-rpath", dir]


class BuildExt(BaseBuildExt):

    # Copied from the base class, except for the Darwin workaround
    def run(self):
        from distutils.ccompiler import new_compiler
        if not self.extensions:
            return
        if self.distribution.has_c_libraries():
            build_clib = self.get_finalized_command('build_clib')
            self.libraries.extend(build_clib.get_library_names() or [])
            self.library_dirs.append(build_clib.build_clib)
        if sys.platform[:6] == "darwin":
            self.compiler = DarwinCompiler(None, self.dry_run, self.force)
        else:
            self.compiler = new_compiler(compiler=self.compiler,
                                         verbose=self.verbose,
                                         dry_run=self.dry_run,
                                         force=self.force)
        customize_compiler(self.compiler)
        if os.name == 'nt' and self.plat_name != get_platform():
            self.compiler.initialize(self.plat_name)
        if self.include_dirs is not None:
            self.compiler.set_include_dirs(self.include_dirs)
        if self.define is not None:
            for (name, value) in self.define:
                self.compiler.define_macro(name, value)
        if self.undef is not None:
            for macro in self.undef:
                self.compiler.undefine_macro(macro)
        if self.libraries is not None:
            self.compiler.set_libraries(self.libraries)
        if self.library_dirs is not None:
            self.compiler.set_library_dirs(self.library_dirs)
        if self.rpath is not None:
            self.compiler.set_runtime_library_dirs(self.rpath)
        if self.link_objects is not None:
            self.compiler.set_link_objects(self.link_objects)
        self.build_extensions()


ext = Extension(
    "ome_files",
    sources=["src/omefiles.cpp"],
    libraries=["ome-common", "ome-files", "ome-xml"],
    include_dirs=[get_include(), get_include(user=True)],
    extra_compile_args=EXTRA_COMPILE_ARGS,
)

setup(name="ome_files", cmdclass={"build_ext": BuildExt}, ext_modules=[ext])

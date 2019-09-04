from conans import ConanFile, AutoToolsBuildEnvironment, tools

class CurllibConan(ConanFile):
    name = "curl"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "conan file to build package for curl"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    requires = "openssl/0.0.1@jenkins/master"
    options = {"shared": [True, False]}
    default_options = "shared=False","openssl:no_asm=True"
    generators = "make"

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)
        self.run("cd .. && autoreconf -fsi ")
        autotools.configure(configure_dir="..",args=["--prefix=${PWD}"])
        autotools.make()
        autotools.install()

    def package(self):
        self.copy("*.h", dst="include", src="include/curl/include")
        self.copy("*", dst="lib", src="lib/lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [ "curl" ]

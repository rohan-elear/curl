import os
import fnmatch
from conans import ConanFile, AutoToolsBuildEnvironment, CMake, tools

class CurllibConan(ConanFile):
    name = "curl"
    version = "7.63.0"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "https://github.com/elear-solutions/curl"
    description = "conan file to build package for curl"
    topics = ("curl", "http", "requests")
    settings = "os", "compiler", "build_type", "arch"
    requires = "OpenSSL/1.0.2r@jenkins/master"
    options = {
        "shared": [True, False],
        'with_openssl': [True, False],
        'with_ldap': [True, False],
        'custom_cacert': [True, False],
        'darwin_ssl': [True, False],
        'with_libssh2': [True, False],
        'with_libidn': [True, False],
        'with_librtmp': [True, False],
        'with_libmetalink': [True, False],
        'with_ares': [True, False],
        'with_http': [True, False],
        'with_ftp': [True, False],
        'with_file': [True, False],
        'with_ldap': [True, False],
        'with_ldaps': [True, False],
        'with_rtsp': [True, False],
        'with_proxy': [True, False],
        'with_dict': [True, False],
        'with_telnet': [True, False],
        'with_tftp': [True, False],
        'with_pop3': [True, False],
        'with_imap': [True, False],
        'with_smb': [True, False],
        'with_smtp': [True, False],
        'with_gopher': [True, False],
        'with_ipv6': [True, False],
        'with_openssl_auto_load_config': [True, False],
        'with_versioned_symbols': [True, False],
        'with_threaded_resolver': [True, False],
        'with_pthread': [True, False],
        'with_cookies': [True, False],
        'with_zlib': [True, False],
        'with_brotli': [True, False],
        'with_winssl': [True, False],
        'with_darwinssl': [True, False],
        'with_ssl': [True, False],
        'with_gnutls': [True, False],
        'with_polarssl': [True, False],
        'with_mbedtls': [True, False],
        'with_cyassl': [True, False],
        'with_wolfssl': [True, False],
        'with_ca_bundle': [True, False],
        'with_libmetalink': [True, False],
        'with_libssh2': [True, False],
        'with_libssh': [True, False],
        'with_rtmp': [True, False],
        'with_winidn': [True, False],
        'with_libidn2': [True, False],
        'with_nghttp2': [True, False],
        'with_crypto_auth': [True, False],
        'with_manual': [True, False]
        }
    default_options = {key: False for key in options.keys()}
    default_options ['OpenSSL:no_asm'] = True
    default_options ['with_zlib'] = True
    default_options ['with_openssl'] = True
    default_options ['with_ssl'] = True
    default_options ['with_cookies'] = True
    default_options ['with_ipv6'] = True
    default_options ['with_crypto_auth'] = True
    default_options ['with_rtsp'] = True
    default_options ['with_threaded_resolver'] = False
    default_options ['with_http'] = True
    default_options ['with_smb'] = True
    default_options ['with_dict'] = True
    default_options ['with_ftp'] = True
    default_options ['with_file'] = True
    default_options ['with_tftp'] = True
    default_options ['with_smtp'] = True
    default_options ['with_gopher'] = True
    default_options ['with_pop3'] = True
    default_options ['with_imap'] = True
    default_options ['with_telnet'] = True

    generators = "cmake", "txt"
    _autotools = None
    _autotools_vars = None

    def _get_linux_arm_host(self):
        arch = None
        if self.settings.os == "Linux":
            arch = "arm-linux-gnu"
            # aarch64 could be added by user
            if "aarch64" in self.settings.arch:
                arch = "aarch64-linux-gnu"
            elif "arm" in self.settings.arch and "hf" in self.settings.arch:
                arch = "arm-linux-gnueabihf"
            elif "arm" in self.settings.arch and self._arm_version(str(self.settings.arch)) > 4:
                arch = "arm-linux-gnueabi"
        return arch

    def _arm_version(self, arch):
        version = None
        match = re.match(r"arm\w*(\d)", arch)
        if match:
            version = int(match.group(1))
        return version

    def _get_configure_command_args(self):
        enable_disable = lambda v: "enable" if v else "disable"
        with_without = lambda v: "with" if v else "without"
        params = [
            "--{}-ares".format(enable_disable(self.options.with_ares)),
            "--{}-http".format(enable_disable(self.options.with_http)),
            "--{}-ftp".format(enable_disable(self.options.with_ftp)),
            "--{}-file".format(enable_disable(self.options.with_file)),
            "--{}-ldap".format(enable_disable(self.options.with_ldap)),
            "--{}-ldaps".format(enable_disable(self.options.with_ldaps)),
            "--{}-rtsp".format(enable_disable(self.options.with_rtsp)),
            "--{}-proxy".format(enable_disable(self.options.with_proxy)),
            "--{}-dict".format(enable_disable(self.options.with_dict)),
            "--{}-telnet".format(enable_disable(self.options.with_telnet)),
            "--{}-tftp".format(enable_disable(self.options.with_tftp)),
            "--{}-pop3".format(enable_disable(self.options.with_pop3)),
            "--{}-imap".format(enable_disable(self.options.with_imap)),
            "--{}-smb".format(enable_disable(self.options.with_smb)),
            "--{}-smtp".format(enable_disable(self.options.with_smtp)),
            "--{}-gopher".format(enable_disable(self.options.with_gopher)),
            "--{}-ipv6".format(enable_disable(self.options.with_ipv6)),
            "--{}-openssl-auto-load-config".format(enable_disable(self.options.with_openssl_auto_load_config)),
            "--{}-versioned-symbols".format(enable_disable(self.options.with_versioned_symbols)),
            "--{}-threaded-resolver".format(enable_disable(self.options.with_threaded_resolver)),
            "--{}-pthread".format(enable_disable(self.options.with_pthread)),
            "--{}-cookies".format(enable_disable(self.options.with_cookies)),
            "--{}-crypto_auth".format(enable_disable(self.options.with_crypto_auth)),
            # "--{}-zlib".format(with_without(self.options.with_zlib)),
            "--{}-brotli".format(with_without(self.options.with_brotli)),
            "--{}-winssl".format(with_without(self.options.with_winssl)),
            "--{}-darwinssl".format(with_without(self.options.with_darwinssl)),
            # "--{}-ssl".format(with_without(self.options.with_ssl)),
            "--{}-gnutls".format(with_without(self.options.with_gnutls)),
            "--{}-polarssl".format(with_without(self.options.with_polarssl)),
            "--{}-mbedtls".format(with_without(self.options.with_mbedtls)),
            "--{}-cyassl".format(with_without(self.options.with_cyassl)),
            "--{}-wolfssl".format(with_without(self.options.with_wolfssl)),
            "--{}-ca-bundle".format(with_without(self.options.with_ca_bundle)),
            "--{}-libmetalink".format(with_without(self.options.with_libmetalink)),
            "--{}-libssh2".format(with_without(self.options.with_libssh2)),
            "--{}-libssh".format(with_without(self.options.with_libssh)),
            "--{}-rtmp".format(with_without(self.options.with_rtmp)),
            "--{}-winidn".format(with_without(self.options.with_winidn)),
            "--{}-libidn2".format(with_without(self.options.with_libidn2)),
            "--{}-nghttp2".format(with_without(self.options.with_nghttp2)),
            "--{}-manual".format(enable_disable(self.options.with_manual)),
        ]

        # Adds custom OpenSSL build as dependency
        if self.options.with_openssl and (not self.options.with_darwinssl and not self.options.with_winssl ):
            self.requires.add("OpenSSL/1.0.2r@jenkins/master", private= False)
            params.append("--with-ssl={!s}".format(self.deps_cpp_info["OpenSSL"].rootpath))
        params.append("--with-zlib={!s}".format(self.deps_cpp_info["zlib"].rootpath)) if self.options.with_zlib else args.append("--without-zlib")

        # Cross building flags
        if tools.cross_building(self.settings):
            if self.settings.os == "Linux" and "arm" in self.settings.arch:
                params.append("--host=%s" % self._get_linux_arm_host())
            elif self.settings.os == "iOS":
                params.append("--enable-threaded-resolver")
                params.append("--disable-verbose")
            elif self.settings.os == "Android":
                pass # this just works, conan is great!

        return params

    def _configure_autotools_vars(self):
        autotools_vars = self._autotools.vars
        # tweaks for mingw
        if self._is_mingw:
            autotools_vars["RCFLAGS"] = "-O COFF"
            if self.settings.arch == "x86":
                autotools_vars["RCFLAGS"] += " --target=pe-i386"
            else:
                autotools_vars["RCFLAGS"] += " --target=pe-x86-64"
        return autotools_vars

    def _configure_autotools(self):
        if self._autotools and self._autotools_vars:
            return self._autotools, self._autotools_vars

        self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)

        if self.settings.os != "Windows":
            self._autotools.fpic = self.options.get_safe("fPIC", True)

        self._autotools_vars = self._configure_autotools_vars()

        # tweaks for mingw
        if self._is_mingw:
            self._autotools.defines.append("_AMD64_")

        if tools.cross_building(self) and tools.is_apple_os(self.settings.os):
            self._autotools.defines.extend(['HAVE_SOCKET', 'HAVE_FCNTL_O_NONBLOCK'])

        configure_args = self._get_configure_command_args()

        if self.settings.os == "iOS" and self.settings.arch == "x86_64":
            # please do not autodetect --build for the iOS simulator, thanks!
            self._autotools.configure(vars=self._autotools_vars, args=configure_args, build=False)
        else:
            self._autotools.configure(vars=self._autotools_vars, args=configure_args)

        return self._autotools, self._autotools_vars

    def build(self):
        with tools.chdir("./.."):
            # autoreconf
            self.run("{} -fiv".format(tools.get_env("AUTORECONF") or "autoreconf"), win_bash=tools.os_info.is_windows, run_environment=True)

            # fix generated autotools files to have relocatable binaries
            if tools.is_apple_os(self.settings.os):
                tools.replace_in_file("configure", "-install_name \\$rpath/", "-install_name @rpath/")

            self.run("chmod +x configure")

            # run configure with *LD_LIBRARY_PATH env vars it allows to pick up shared openssl
            with tools.run_environment(self):
                autotools, autotools_vars = self._configure_autotools()
                autotools.make(vars=autotools_vars)
                autotools.install()

        # autotools = AutoToolsBuildEnvironment(self)
        # self.run("cd .. && autoreconf -fsi")
        # args = self.config_options()
        # if self.options.with_openssl and (not self.options.with_darwinssl and not self.options.with_winssl ):
        #     self.requires.add("OpenSSL/1.0.2r@jenkins/master", private= False)
        #     args.append("--with-ssl={!s}".format(self.deps_cpp_info["OpenSSL"].rootpath))
        # args.append("--with-zlib={!s}".format(self.deps_cpp_info["zlib"].rootpath)) if self.options.with_zlib else args.append("--without-zlib")
        # autotools.configure(configure_dir= "..",args= args, use_default_install_dirs=True)
        # autotools.make()
        # autotools.install()

    def package(self):
        self.copy("*.h", dst= "include", src= "include/curl/include")
        self.copy("*", dst= "lib", src= "lib/lib", keep_path= False)

    def package_info(self):
        self.cpp_info.libs = [ "curl" ]


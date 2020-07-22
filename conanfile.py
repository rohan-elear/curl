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
    default_options ['with_threaded_resolver'] = True
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

    @property
    def _targets(self):
        return {
            "iOS-x86-*": "i386-apple-ios",
            "iOS-x86_64-*": "x86_64-apple-ios"
        }

    def config_options(self):
        if self.settings.build_type == "Release":
         args = ["--prefix=${PWD}", "CFLAGS=-Os -s -ffunction-sections -fdata-sections"]
        else:
         args = ["--prefix=${PWD}"]

        args.append("--enable-ares") if self.options.with_ares else args.append("--disable-ares")
        args.append("--enable-http") if self.options.with_http else args.append("--disable-http")
        args.append("--enable-ftp") if self.options.with_ftp else args.append("--disable-ftp")
        args.append("--enable-file") if self.options.with_file else args.append("--disable-file")
        args.append("--enable-ldap") if self.options.with_ldap else args.append("--disable-ldap")
        args.append("--enable-ldaps") if self.options.with_ldaps else args.append("--disable-ldaps")
        args.append("--enable-rtsp") if self.options.with_rtsp else args.append("--disable-rtsp")
        args.append("--enable-proxy") if self.options.with_proxy else args.append("--disable-proxy")
        args.append("--enable-dict") if self.options.with_dict else args.append("--disable-dict")
        args.append("--enable-telnet") if self.options.with_telnet else args.append("--disable-telnet")
        args.append("--enable-tftp") if self.options.with_tftp else args.append("--disable-tftp")
        args.append("--enable-pop3") if self.options.with_pop3 else args.append("--disable-pop3")
        args.append("--enable-imap") if self.options.with_imap else args.append("--disable-imap")
        args.append("--enable-smb") if self.options.with_smb else args.append("--disable-smb")
        args.append("--enable-smtp") if self.options.with_smtp else args.append("--disable-smtp")
        args.append("--enable-gopher") if self.options.with_gopher else args.append("--disable-gopher")
        args.append("--enable-ipv6") if self.options.with_ipv6 else args.append("--disable-ipv6")
        args.append("--enable-openssl-auto-load-config") if self.options.with_openssl_auto_load_config else args.append("--disable-openssl-auto-load-config")
        args.append("--enable-versioned-symbols") if self.options.with_versioned_symbols else args.append("--disable-versioned-symbols")
        args.append("--enable-threaded-resolver") if self.options.with_threaded_resolver else args.append("--disable-threaded-resolver")
        args.append("--enable-pthread") if self.options.with_pthread else args.append("--disable-pthread")
        args.append("--enable-cookies") if self.options.with_cookies else args.append("--disable-cookies")
        args.append("--enable-crypto_auth") if self.options.with_crypto_auth else args.append("--disable-crypto-auth")
        # args.append("--with-zlib") if self.options.with_zlib else args.append("--without-zlib")
        args.append("--with-brotli") if self.options.with_brotli else args.append("--without-brotli")
        args.append("--with-winssl") if self.options.with_winssl else args.append("--without-winssl")
        args.append("--with-darwinssl") if self.options.with_darwinssl else args.append("--without-darwinssl")
        # args.append("--with-ssl") if self.options.with_ssl else args.append("--without-ssl")
        args.append("--with-gnutls") if self.options.with_gnutls else args.append("--without-gnutls")
        args.append("--with-polarssl") if self.options.with_polarssl else args.append("--without-polarssl")
        args.append("--with-mbedtls") if self.options.with_mbedtls else args.append("--without-mbedtls")
        args.append("--with-cyassl") if self.options.with_cyassl else args.append("--without-cyassl")
        args.append("--with-wolfssl") if self.options.with_wolfssl else args.append("--without-wolfssl")
        args.append("--with-ca-bundle") if self.options.with_ca_bundle else args.append("--without-ca-bundle")
        args.append("--with-libmetalink") if self.options.with_libmetalink else args.append("--without-libmetalink")
        args.append("--with-libssh2") if self.options.with_libssh2 else args.append("--without-libssh2")
        args.append("--with-libssh") if self.options.with_libssh else args.append("--without-libssh")
        args.append("--with-rtmp") if self.options.with_rtmp else args.append("--without-rtmp")
        args.append("--with-winidn") if self.options.with_winidn else args.append("--without-winidn")
        args.append("--with-libidn2") if self.options.with_libidn2 else args.append("--without-libidn2")
        args.append("--with-nghttp2") if self.options.with_nghttp2 else args.append("--without-nghttp2")
        args.append("--enable-manual") if self.options.with_manual else args.append("--disable-manual")
        return args

    def build(self):
        # print(self.deps_cpp_info["openssl"].rootpath)
        # print(self.deps_cpp_info["openssl"].include_paths)
        # print(self.deps_cpp_info["openssl"].lib_paths)
        # print(self.deps_cpp_info["openssl"].bin_paths)
        # print(self.deps_cpp_info["openssl"].libs)
        # print(self.deps_cpp_info["openssl"].defines)
        # print(self.deps_cpp_info["openssl"].cflags)
        # print(self.deps_cpp_info["openssl"].cppflags)
        # print(self.deps_cpp_info["openssl"].sharedlinkflags)
        # print(self.deps_cpp_info["openssl"].exelinkflags)
        autotools = AutoToolsBuildEnvironment(self)
        self.run("cd .. && autoreconf -fsi")
        args = self.config_options()
        if self.options.with_openssl and (not self.options.with_darwinssl and not self.options.with_winssl ):
            self.requires.add("OpenSSL/1.0.2r@jenkins/master", private= False)
            args.append("--with-ssl={!s}".format(self.deps_cpp_info["OpenSSL"].rootpath))
        args.append("--with-zlib={!s}".format(self.deps_cpp_info["zlib"].rootpath)) if self.options.with_zlib else args.append("--without-zlib")
        query = "%s-%s-%s" % (self.settings.os, self.settings.arch, self.settings.compiler)
        ancestor = next((self._targets[i] for i in self._targets if fnmatch.fnmatch(query, i)), None)
        if not ancestor:
            autotools.configure(configure_dir= "..",args= args, use_default_install_dirs=True)
        else:
            autotools.configure(configure_dir= "..",args= args, use_default_install_dirs=True, host= ancestor)
        autotools.make()
        autotools.install()

    def package(self):
        self.copy("*.h", dst= "include", src= "include/curl/include")
        self.copy("*", dst= "lib", src= "lib/lib", keep_path= False)

    def package_info(self):
        self.cpp_info.libs = [ "curl" ]


from conans import ConanFile, CMake, tools
import shutil
import glob


class WangleConan(ConanFile):
    name = "wangle"
    version = "2020.02.10.00"
    license = "Apache-2.0"
    author = "Ethan D. Twardy <edtwardy@mtu.edu>"
    url = "https://github.com/AmateurECE/conan-wangle"
    description = """C++ networking library
    Wangle is a library that makes it easy to build protocols, application
    clients, and application servers. It's like Netty + Finagle smooshed
    together, but in C++."""
    topics = ("facebook", "server", "client", "networking")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake_find_package"
    build_requires = "fmt/6.2.0"
    requires = "openssl/1.1.1d", "fizz/2020.02.17.00@edtwardy/deployment", \
        "folly/2019.10.21.00"

    def source(self):
        self.run("git clone https://github.com/facebook/wangle")
        self.run("git --git-dir=wangle/.git --work-tree=wangle checkout v{}"
                 .format(self.version))

    def build(self):
        # Copy the Find<Package> files to fizz's cmake directory
        for findPackageFile in glob.glob("Find*"):
            shutil.copyfile(findPackageFile, "wangle/wangle/cmake/"
                            + findPackageFile)

        with open("wangle/wangle/CMakeLists.txt") as oldFile, \
             open("CMakeLists.txt.new", "w") as newFile:
            for line in oldFile:
                if "find_package" in line and "CONFIG" in line:
                    newFile.write(line.replace(" CONFIG", ""))
                elif "FOLLY" in line:
                    newFile.write(line.replace("FOLLY", "folly"))
                elif "FIZZ" in line:
                    newFile.write(line.replace("FIZZ", "fizz"))
                else:
                    newFile.write(line)

        shutil.copyfile("CMakeLists.txt.new", "wangle/wangle/CMakeLists.txt")

        cmake = CMake(self)
        cmake.configure(source_folder="wangle/wangle",
                        build_folder="wangle/build")
        cmake.build()
        self.run("cd wangle/build && "
                 "ctest -E '(.*BroadcastPoolTest.*|.*BootstrapTest.*)'")

    def package(self):
        self.copy("*.h", dst="include/wangle", src="wangle/wangle",
                  excludes=("*Test*", "*test*"))
        self.copy("*wangle.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False, excludes=("*test*"))
        self.copy("*.so", dst="lib", keep_path=False, excludes=("*test*"))
        self.copy("*.dylib", dst="lib", keep_path=False, excludes=("*test*"))
        self.copy("*.a", dst="lib", keep_path=False, excludes=("*test*"))

    def package_info(self):
        self.cpp_info.libs = ["wangle"]


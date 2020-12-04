import os
from spack import *

class Openvdb(CMakePackage):

    """OpenVDB - a sparse volume data format."""

    homepage = "https://github.com/AcademySoftwareFoundation/openvdb"

    url      = "https://github.com/AcademySoftwareFoundation/openvdb/archive/v7.1.0.tar.gz"
    git      = "https://github.com/AcademySoftwareFoundation/openvdb.git"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers = ['eloop']

    # do we need a python2 variant?
    #depends_on('python@2.7.15')
    #depends_on('python@2.7.15')
    #depends_on('py-numpy@1.16')

    version('master', branch='master')
    version('7.1.0', '5c93246de7093475a4f58032b68552cf61d282e8')

    variant('python', default=False, description='Build the pyopenvdb python extension')

    extends('python', when='+python')

    depends_on('intel-tbb')
    depends_on('ilmbase')
    depends_on('openexr')
    depends_on('c-blosc')
    depends_on('boost+iostreams+system', when='~python')
    depends_on('python@3.7.4', when='+python')
    depends_on('boost+iostreams+system+python+numpy', when='+python')
    depends_on('py-numpy', when='+python')
    depends_on('git', type='build', when='@master')

    def cmake_args(self):

        spec = self.spec
        cmake_args = [
            '-DBUILD_SHARED_LIBS=ON'
        ]

        if '+python' in spec:
            cmake_args.extend([
                '-DUSE_NUMPY:BOOL=ON',
                '-DOPENVDB_BUILD_PYTHON_MODULE:BOOL=ON',
                ])

        return cmake_args

    @run_after('install')
    def post_install(self):

        spec = self.spec
        prefix = self.prefix

        if '+python' in spec:
            # this is where it's currently be put by the OpenVDB cmake installation
            src = os.path.join(os.path.split(site_packages_dir)[0],'pyopenvdb.so')
            dst = os.path.join(site_packages_dir,'pyopenvdb.so')
            mkdirp(site_packages_dir)
            os.rename(src, dst)

import os
from spack import *

class Openvdb(CMakePackage):

    """OpenVDB - a sparse volume data format."""

    homepage = "https://github.com/AcademySoftwareFoundation/openvdb"

    url      = "https://github.com/AcademySoftwareFoundation/openvdb/archive/v7.1.0.tar.gz"
    git      = "https://github.com/AcademySoftwareFoundation/openvdb.git"

    # Github account name for Drew.Whitehouse@gmail.com
    maintainers = ['eloop']

    version('develop', branch='develop')
    version('7.1.0', '5c93246de7093475a4f58032b68552cf61d282e8')

    variant('python', default=False, description='Build the pyopenvdb python extension')
    depends_on('py-numpy', when='+python')
    extends('python', when='+python')
    # For python2 these work well.
    #depends_on('python@2.7.15')
    #depends_on('py-numpy@1.16')

    depends_on('intel-tbb')
    depends_on('ilmbase')
    depends_on('openexr')
    depends_on('c-blosc')
    depends_on('boost+iostreams+system', when='~python')
    depends_on('boost+iostreams+system+python+numpy', when='+python')
    depends_on('git', type='build', when='@develop')

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

            # This is where the python extension is being put by
            # OpenVDB's cmake.
            src = os.path.join(os.path.split(site_packages_dir)[0],'pyopenvdb.so')

            # We want it in site-packages so "spack load openvdb" and
            # spack environments can work properly.
            dst = os.path.join(site_packages_dir,'pyopenvdb.so')

            mkdirp(site_packages_dir)
            os.rename(src, dst)

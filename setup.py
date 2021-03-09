from setuptools import setup

package_name = 'bwt901cl_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dorebom',
    maintainer_email='dorebom.b@gmail.com',
    description='Package for using sensor module BWT901CL',
    license='MIT License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'imu_bwt901cl = bwt901cl_pkg.imu_bwt901cl:main'
        ],
    },
    py_modules=["bwt901cl_pkg.src.bwt901cl"]
)

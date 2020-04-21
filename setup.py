from distutils.core import setup

setup(
    name='facepyok',
    packages=['facepyok'],
    version='0.0.1',
    license='MIT',
    description='Facebook API multi-purpose',
    author='buivd4',
    author_email='buivd4@hotmail.com',
    url='https://github.com/buivd4/facepyok',
    download_url='https://github.com/user/reponame/archive/v_01.tar.gz',  # I explain this later on
    keywords=['FACEBOOK', 'API', 'TOOL'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)

#!/usr/bin/env python2
from distutils.core import setup
from distutils.command.bdist_rpm import bdist_rpm

def tests():
    import os
    exList = os.listdir(os.curdir + '/tests/')
    result = []
    for ex in exList:
        if ex.split('.')[-1] == 'py':
            result = result + ['tests/' + ex]
    return result

def icons(ext_tuple):
    import os
    list = os.listdir(os.curdir + '/data/icons/')
    result = []
    for file in list:
        if file.split('.')[-1] in ext_tuple:
            result = result + ['data/icons/' + file]
    return result

setup (
        name = 'waktu',
        version = '0.1-alpha1',
        description = """Waktu is time tracking application that automatically watch application you have focus on.""",
        author = """Petr Sebek <petrsebek1@gmail.com>,
Martin Simon <martiin.siimon@gmail.com>""",
        url = 'http://github.com/Artimi/waktu',
        packages = ['waktu'],
		scripts = ['scripts/waktu'],
        data_files = [
                                ('share/doc/waktu/tests',
                                        tests() ),
                                ('share/waktu/ui', ['data/waktu.ui']),
                                ('share/applications', ['data/waktu.desktop']),
                                ('share/icons/hicolor/48x48/apps', icons('png')),
                                ('share/icons/hicolor/scalable/apps', icons('svg'))
                                ],
        cmdclass = {
                'bdist_rpm': bdist_rpm
                }
)

# vim: sw=4 ts=4 sts=4 noet ai

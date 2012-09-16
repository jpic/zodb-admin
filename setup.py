import os
import sys

from setuptools import setup, find_packages, Command

MODULE_NAME='zodb_admin'

# Utility function to read the README file.
# Used for the long_description. It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class RunTests(Command):
    description = "Run the django test suite from the testproj dir."

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        this_dir = os.getcwd()
        testproj_dir = os.path.join(this_dir, "test_project")
        os.chdir(testproj_dir)
        sys.path.append(testproj_dir)
        from django.core.management import execute_manager
        os.environ["DJANGO_SETTINGS_MODULE"] = 'test_project.settings'
        settings_file = os.environ["DJANGO_SETTINGS_MODULE"]
        settings_mod = __import__(settings_file, {}, {}, [''])
        execute_manager(settings_mod, argv=[
            __file__, "test", MODULE_NAME])
        os.chdir(this_dir)

if 'sdist' in sys.argv:
    # clear compiled mo files before building the distribution
    walk = os.walk(os.path.join(os.getcwd(), MODULE_NAME +'/locale'))
    for dirpath, dirnames, filenames in walk:
        if not filenames:
            continue

        if 'django.mo' in filenames:
            os.unlink(os.path.join(dirpath, 'django.mo'))
            print 'unlink', os.path.join(dirpath, 'django.mo')
else:
    # if django is there, compile the po files to mo,
    try:
        import django
    except ImportError:
        pass
    else:
        dir = os.getcwd()
        os.chdir(os.path.join(dir, MODULE_NAME))
        os.system('django-admin.py compilemessages')
        os.chdir(dir)

setup(
    name='django-zodb-admin',
    version='0.0.1',
    description='Schemaless, customizable admin, create forms, views, objects, etc, etc ...',
    author='James Pic',
    author_email='jamespic@gmail.com',
    url='http://django-zodb-admin.rtfd.org',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    long_description=read('README.rst'),
    license='MIT',
    keywords='django zodb',
    cmdclass={'test': RunTests},
    install_requires=[
        'django',
        'django-zodb',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

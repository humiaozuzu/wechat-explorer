from setuptools import setup


setup(
    name='wechat-explorer',
    version='0.1.0',
    url='https://github.com/humiaozuzu/wechat-explorer',
    license='MIT',
    author='Maple',
    author_email='maplevalley8@gmail.com',
    description='Wechat data explorer',
    packages=['we', 'we.contrib'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'biplist',
        'xmltodict',
        'jinja2',
    ],
    entry_points="""
    [console_scripts]
    wexp = we.run:main
    """,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)

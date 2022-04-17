from setuptools import setup, find_packages
 
classifiers = [
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'Operating System :: POSIX :: Linux',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.8',
  'Programming Language :: Python :: 3.9'
]
 
setup(
  name='GoldyBot',
  version='4.0a1',
  description='Yet another rewrite of Goldy Bot, a discord bot that I develop for FUN.', 
  long_description=open('README.txt').read(), 
  url='https://github.com/Goldy-Bot', 
  project_urls={"Bug Tracker": "https://github.com/Goldy-Bot/Goldy-Bot-V4/issues"}, 
  author='Dev Goldy', 
  author_email='goldy@novauniverse.net', 
  license='MIT', 
  classifiers=classifiers, 
  keywords=["goldy bot", "Goldy Bot", "Goldy Bot V4", "Goldy Bot V3", "goldy"], 
  packages=find_packages(), 
  include_package_data=True,
  install_requires=["requests", "motor", "pymongo", "nextcord==2.0.0a9", "dnspython", "psutil"],
  python_requires=">=3.8"
)
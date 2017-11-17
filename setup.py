from setuptools import setup, find_packages
 
 
 
setup(name='django-AB-project',
      version='1.0',
      url='https://github.com/Vadim-Karpenko/django-AB-project',
      license='MIT',
      author='Vadim Karpenko',
      author_email='j.rell@protonmail.com',
      description='Simple and easy-to-use project for A/B testing.',
      packages=find_packages(exclude=["ab"]),
      long_description=open('README.md').read(),
      zip_safe=False,
      setup_requires=['django>=1.11'],
)
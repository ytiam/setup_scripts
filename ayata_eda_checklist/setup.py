import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='EDA',  
     version='0.1',
     scripts=['EDA'] ,
     author="Ayata",
     author_email="atanu.maity@ayata.com",
     description="Ayata's own personalized data independent EDA module",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/javatechy/dokr",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
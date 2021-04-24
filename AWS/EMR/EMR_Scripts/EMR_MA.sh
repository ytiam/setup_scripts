#!/bin/bash

#########################################################################
# Script  to set environment on UBUNTU for Meta-Algorithms with anaconda 
# File Author / Maintainer
# MAINTAINER Kanchan Kumar Rohit 
#########################################################################

#########################################
#setup necessary folders on root
#######################################


sudo su

echo -e "\e[1;32m********************check/setup necessary folders on root.********************\e[0m"
cd /
if [ ! -d "$ayata" ]; then
  sudo mkdir ayata
  cd ayata
  sudo mkdir datasources
  sudo mkdir model
  sudo mkdir data
  sudo mkdir log
  sudo mkdir temp
  sudo mkdir meta-config
  cd datasources
  sudo mkdir completion
  cd ..
fi
cd ..
sudo chmod -R 777 ayata/
sudo chmod -R +x ayata/
cd ~

echo -e "\e[1;32m********************update/upgrade.********************\e[0m"
sudo yum update
sudo yum -y upgrade

#####################################################
#Check/install JAVA 1.7
#####################################################

echo -e "\e[1;32m********************check/install Java.********************\e[0m"
if type -p java; then
    echo found java executable in PATH
    _java=java
elif [[ -n "$JAVA_HOME" ]] && [[ -x "$JAVA_HOME/bin/java" ]];  then
    echo found java executable in JAVA_HOME     
    _java="$JAVA_HOME/bin/java"
else
    yes "" | sudo apt-add-repository ppa:webupd8team/java
    sudo yum update
    sudo yum -y install oracle-java8-installer
fi

if [[ "$_java" ]]; then
    version=$("$_java" -version 2>&1 | awk -F '"' '/version/ {print $2}')
    echo version "$version"
    if [[ "$version" > "1.7" ]]; then
        echo version is more than 1.7
    else         
        yes "" | sudo apt-add-repository ppa:webupd8team/java
    	sudo yum update
    	sudo yum -y install oracle-java8-installer
    fi
fi

############################################################################################
#check/install/upgrade pip, xmlrunner, coverage, coverage2clover for default python version
############################################################################################

echo -e "\e[1;32m********************check/install pip.********************\e[0m"
if [ $(dpkg-query -W -f='${Status}' python-pip 2>/dev/null | grep -c "ok installed") -eq 0 ]; then
    
    sudo yum -y install python-pip;
    sudo yum -y install python-devel;
    sudo yum groupinstall 'Development Tools'

    #sudo yum -y install build-essential;
  else
    echo "python-pip installed"
fi 

echo -e "\e[1;32m********************check/install GIT-CORE.********************\e[0m"
if [ $(dpkg-query -W -f='${Status}' git-core 2>/dev/null | grep -c "ok installed") -eq 0 ]; then
  
    sudo yum -y install git-core;
  else
    echo "git-core installed"
fi 

echo -e "\e[1;32m**********check/install/upgrade xmlrunner,coverage,coverage2clover for default python version.**********\e[0m"
python -c 'import xmlrunner' 2>/dev/null && echo "python unittest-xml-reporting modules install" || sudo pip install unittest-xml-reporting
python -c 'import coverage' 2>/dev/null && echo "python coverage modules install" || sudo pip install coverage
python -c 'import clover' 2>/dev/null && echo "python coverage2clover modules install" || sudo pip install coverage2clover
sudo pip install -U pip
sudo pip install -U coverage
sudo pip install -U coverage2clover
sudo pip install -U unittest-xml-reporting

############################################################################
#install  anaconda3 virtenv to have all the required python3.5 and packages
############################################################################
cd ~/
echo -e "\e[1;32m**********check/install  anaconda3 virtenv to have all the required python3.5 and packages.**********\e[0m"
version=$(python -c 'import platform; print(platform.python_version())')

if [[ "$version" < "3.5.1" ]]; then
   
   sudo yum -y install wget
   sudo wget http://repo.continuum.io/archive/Anaconda3-2.5.0-Linux-x86_64.sh   
   sudo bash Anaconda3-2.5.0-Linux-x86_64.sh
   sudo chmod +x anaconda3/
   sudo chmod 777 anaconda3/
   #sudo rm Anaconda3-2.5.0-Linux-x86_64.sh
 else
    echo "conda installed"
fi

###################################################
#update python alternatives
###################################################

echo -e "\e[1;32m********************update python alternatives.********************\e[0m"
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python ~/anaconda3/bin/python3.5 2
sudo update-alternatives --config python

####################################################################################
#install/upgrade pip,xmlrunner,coverage,coverage2clover for  python latest version
####################################################################################

echo -e "\e[1;32m********************update packages for python3.5.********************\e[0m"
 pip install -U pip
 pip install -U coverage
 pip install -U coverage2clover
 pip install -U unittest-xml-reporting

################################################################################
#install seaborn, scoop, flask-restful, flask, corbetura2clover,ipython, gensim  
################################################################################

echo -e "\e[1;32m********************check/install seaborn.********************\e[0m"
python -c 'import seaborn' 2>/dev/null && echo "python seaborn modules install" ||  pip install seaborn

echo -e "\e[1;32m********************check/install scoop.********************\e[0m"
python -c 'import scoop' 2>/dev/null && echo "python scoop modules install" ||  pip install scoop

echo -e "\e[1;32m********************check/install flask restful.********************\e[0m"
python -c 'import flask-restful' 2>/dev/null && echo "python flask-restful modules install" ||  pip install flask-restful
python -c 'import flask' 2>/dev/null && echo "python flask modules install" ||  pip install flask

echo -e "\e[1;32m********************check/install corbetura to clover.********************\e[0m"
python -c 'import lxml cobertura-clover-transform' 2>/dev/null && echo "python cobertura-clover-transform modules install" || pip install lxml cobertura-clover-transform

echo -e "\e[1;32m********************check/install ipython notebook.********************\e[0m"
python -c 'import notebook' 2>/dev/null && echo "python ipython notebook modules install" || sudo yum install ipython

echo -e "\e[1;32m********************check/install gensim.********************\e[0m"
python -c 'import gensim' 2>/dev/null && echo "python gensim modules install" ||  pip install -U gensim

##################################################################################################
#install GSL, MLPY, Scikits talkbox, Simplejson, eyed3, dask, scikit-learn, cloudpickle, pycrypto
##################################################################################################

echo -e "\e[1;32m********************check/install GSL.********************\e[0m"
python -c 'ldconfig -p | grep gsl' 2>/dev/null && echo "python GSL modules install" || sudo yum -y install gsl-devel

echo -e "\e[1;32m********************check/install MLPY.********************\e[0m"
python -c 'import mlpy' 2>/dev/null && echo "python MLPY modules install" || wget http://sourceforge.net/projects/mlpy/files/mlpy%203.5.0/mlpy-3.5.0.tar.gz; tar xvf mlpy-3.5.0.tar.gz; cd mlpy-3.5.0; python setup.py install; cd .. ; sudo rm mlpy-3.5.0.tar.gz

echo -e "\e[1;32m********************check/install Scikits talkbox.********************\e[0m"
python -c 'import scikits' 2>/dev/null && echo "python scikits modules install" ||  pip install scikits.talkbox

echo -e "\e[1;32m********************check/install Simplejson.********************\e[0m"
python -c 'import simplejson' 2>/dev/null && echo "python simplejson modules install" ||  pip install simplejson

echo -e "\e[1;32m********************check/install eyed3.********************\e[0m"
python -c 'import eyed3' 2>/dev/null && echo "python eyed3 modules install" || pip install eyed3

echo -e "\e[1;32m********************check/install scikit-learn.********************\e[0m"
python -c 'import sklearn' 2>/dev/null && echo "python scikit-learn modules install" ||  pip install -U scikit-learn

echo -e "\e[1;32m********************check/install dask.********************\e[0m"
python -c 'import dask' 2>/dev/null && echo "python dask modules install" || pip install dask

echo -e "\e[1;32m********************check/install cloudpickle.********************\e[0m"
python -c 'import cloudpickle' 2>/dev/null && echo "python cloudpickle modules install" ||  pip install cloudpickle

echo -e "\e[1;32m********************check/install scikit-image.********************\e[0m"
python -c 'import skimage' 2>/dev/null && echo "python scikit-image modules install" || pip install -U scikit-image

echo -e "\e[1;32m********************check/install tkinter.********************\e[0m"
python -c 'import _tkinter' 2>/dev/null && echo "python tkinter modules install" || sudo yum -y install python3.5-tk

echo -e "\e[1;32m********************check/install pytesseract.********************\e[0m"
python -c 'import pytesseract' 2>/dev/null && echo "python pytesseract modules install" ||  pip install pytesseract

echo -e "\e[1;32m********************check/install pydub.********************\e[0m"
python -c 'import pydub' 2>/dev/null && echo "python pydub modules install" ||  pip install pydub

echo -e "\e[1;32m********************check/install wordcloud.********************\e[0m"
python -c 'import wordcloud' 2>/dev/null && echo "python wordcloud modules install" || pip install wordcloud

echo -e "\e[1;32m********************check/install pycrypto.********************\e[0m"
python -c 'import pycrypto' 2>/dev/null && echo "python pycrypto modules install" || sudo git clone --recursive https://github.com/dlitz/pycrypto; cd pycrypto; python setup.py install; cd..;

#################################
#install tensor flow
#################################

echo -e "\e[1;32m********************check/install TensorFlow.********************\e[0m"

################# Tensorflow-0.9#########################
#python -c 'import tensorflow' 2>/dev/null && echo "python TensorFlow modules install" || sudo pip install https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.9.0rc0-cp35-cp35m-linux_x86_64.whl

################# Tensorflow-0.10 #########################
conda install -c jjhelmus tensorflow=0.10.0rc0

################################
#install xgboost
################################

echo -e "\e[1;32m********************check/install xgboost.********************\e[0m"
python -c 'import xgboost' 2>/dev/null && echo "python xgboost modules install" || sudo git clone --recursive https://github.com/dmlc/xgboost; cd xgboost; sudo make -j4; cd python-package; python setup.py install; cd ..; cd ..
echo "export PYTHONPATH=$HOME/xgboost/python-package"  >> ~/.bashrc

#############################################
#install Deap 1.1.0 for optimisations
#############################################

echo -e "\e[1;32m********************check/install deap.********************\e[0m"
python -c 'import deap' 2>/dev/null && echo "python deap modules install" || pip install git+https://github.com/DEAP/deap

#########################
#install nltk, nltk_data  
#########################

echo -e "\e[1;32m********************check/install NLTK.********************\e[0m"
python -c 'import nltk' 2>/dev/null && echo "python nltk modules install" ||  pip install -U nltk

echo -e "\e[1;32m********************check/install nltk_data(stopwords).********************\e[0m"
cd ~/
if [ ! -d "$nltk_data" ]; then
  python -m nltk.downloader stopwords
  python -m nltk.downloader punkt
  #python -m nltk.downloader all-corpora
fi


#################################
#install maven
#################################

echo -e "\e[1;32m********************check/install maven executable.********************\e[0m"
if [ $(dpkg-query -W -f='${Status}' maven 2>/dev/null | grep -c "ok installed") -eq 0 ]; then
    
    sudo wget http://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo -O /etc/yum.repos.d/epel-apache-maven.repo
    sudo sed -i s/\$releasever/6/g /etc/yum.repos.d/epel-apache-maven.repo
    sudo yum install -y apache-maven
    mvn --version
  else
    echo "maven installed"
fi

#################################
#install GSTREAMER
#################################

echo -e "\e[1;32m********************install GSTREAMER.********************\e[0m"
# sudo yum -y install ffmpeg libav-tools
# sudo yum -y install libavdevice-dev libavformat-dev libavfilter-dev libavcodec-dev libswscale-dev libavutil-dev
# yes "" | sudo add-apt-repository ppa:mc3man/trusty-media
# sudo yum update
# sudo yum -y install gstreamer0.10-ffmpeg

# echo -e "\e[1;32m********************update/upgrade.********************\e[0m"
# sudo yum update
# sudo yum -y upgrade

# ################################
# #install opencv
# ################################

# echo -e "\e[1;32m********************install the dependencies required for OpenCV.********************\e[0m"
# sudo yum -y install libgstreamer0.10-0 libgstreamer0.10-dev gstreamer0.10-tools gstreamer0.10-plugins-base libgstreamer-plugins-base0.10-dev gstreamer0.10-plugins-good
# sudo yum -y install libhdf5-dev
pip install -U h5py
sudo yum update

#Download Opencv & opencv_contrib
# cd ~/
# echo -e "\e[1;32m********************Dowload Opencv 3.1.0.********************\e[0m"
# git clone https://github.com/Itseez/opencv.git

# echo -e "\e[1;32m********************Dowload Opencv_contrib.********************\e[0m"
# git clone https://github.com/Itseez/opencv_contrib.git

# cd opencv
# git checkout 3.1.0
# cd ..
# cd opencv_contrib
# git checkout 3.1.0
# cd ..

# #Install opencv

# echo -e "\e[1;32m********************install opencv-3.********************\e[0m"
# cd opencv
# mkdir build
# cd build
# sudo apt -y install cmake
# cmake -DBUILD_TIFF=ON -DBUILD_opencv_java=OFF -DWITH_CUDA=OFF -DWITH_FFMPEG=OFF -DENABLE_AVX=ON -DWITH_OPENGL=ON -DWITH_OPENCL=ON -DWITH_IPP=ON -DWITH_TBB=ON -DWITH_EIGEN=ON -DWITH_V4L=ON -DBUILD_TESTS=OFF -DBUILD_PERF_TESTS=OFF -DCMAKE_BUILD_TYPE=RELEASE -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules -DCMAKE_INSTALL_PREFIX=$(python3 -c "import sys; print(sys.prefix)") -DPYTHON3_EXECUTABLE=$(which python3.5) -DPYTHON3_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") -DPYTHON3_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") ..
# sudo make
# sudo make install
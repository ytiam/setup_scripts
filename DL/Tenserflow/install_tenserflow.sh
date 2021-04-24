#!/bin/bash

#############################################################
# Script  to install Tenserflow on Linux 
# File Author / Maintainer
# MAINTAINER Mubbashir Nazir 
############################################################

#########################################
#Download Tenserflow
#######################################

wget https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.8.0-cp34-cp34m-linux_x86_64.whl



#------------>Rename Tenseflow file to work for python 3.5
mv tensorflow-0.8.0-cp34-cp34m-linux_x86_64.whl tensorflow-0.8.0-cp35-cp35m-linux_x86_64.whl 


#----------> install tenseflow

sudo pip install tensorflow-0.8.0-cp35-cp35m-linux_x86_64.whl



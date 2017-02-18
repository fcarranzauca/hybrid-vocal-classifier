#!/usr/bin/env python

from distutils.core import setup

setup(name='Hybrid Vocal Classifier',
      version='1.0',
      description='Python package for automated analysis of birdsong',
      author='David Nicholson',
      author_email='nicholdav at gmail dot com',
      url='https://github.com/NickleDave/hybrid-vocal-classifier',
      packages=['hvc','hvc.utils','hvc.audio','hvc.neuralnet'],
      )
      

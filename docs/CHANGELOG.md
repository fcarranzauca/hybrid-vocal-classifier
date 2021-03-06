# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
- refactor repository with `./src` folder
- use Kenneth Reitz style `setup.py`

## 0.2.1b1
### added
- unit tests for high-level extract, select, and predict functions (see 'changed')
- Allow supplying annotation as csv; this will get replaced by using `Crowsetta` to
  deal with annotation shortly

### changed
- **change to API**: Provides direct access to hvc.extract, select, and predict 
  through functions, instead of requiring YAML config files. Can still use YAML though.
- add `FeatureExtractor` class to `hvc.features`
  + high-level `hvc.extract` function basically instantiates a `FeatureExtractor` for the
    user

### fixed
- fix bugs in how `koumura` functions parse xml (error in loop logic that failed to parse
  last sequence)

## 0.1.b2
### Added
- can now train scikit-learn models with 'predict probability' set to `True`

### Fixed
- `flatwindow` model in Keras works
- `svm` feature extraction deals appropriately with segments from which it can't 
  extract features by returning zeros instead; 
  this reproduces approach of Tachibana Okinaya paper

##  0.1.b1 
### Fixed
- Fix setup.py issues, stupid syntax errors that are causing errors with conda build

## 0.1.0-beta
### Added
- predict module working
- can convert predictions to at least one file format
- hence going to beta

## 0.1.0-alpha
- First release

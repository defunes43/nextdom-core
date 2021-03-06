#!/bin/bash

#echo "--DEBUG--"
#echo "TRAVIS_REPO_SLUG: $TRAVIS_REPO_SLUG"
#echo "TRAVIS_PHP_VERSION: $TRAVIS_PHP_VERSION"
#echo "TRAVIS_PULL_REQUEST: $TRAVIS_PULL_REQUEST"

if [ "$TRAVIS_REPO_SLUG" == "nextdom/core" ] && [ "$TRAVIS_PULL_REQUEST" == "false" ] && [ "$TRAVIS_PHP_VERSION" == "5.6" ] && [ "$TRAVIS_BRANCH" == "beta" ]; then
  echo -e "Publishing PHPDoc...\n"
  cp -R build/docs $HOME/docs-latest
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "travis-ci"
  mkdir -p /usr/nextdom
  cd /usr/nextdom
  git clone --branch=gh-pages https://${GH_TOKEN}@github.com/nextdom/documentation.git
  if [ ! -f /usr/nextdom/documentation/phpdoc ]; then
    mkdir -p /usr/nextdom/documentation/phpdoc
  fi
  cd /usr/nextdom/documentation/phpdoc
  rm -rf /usr/nextdom/documentation/phpdoc/*
  cp -Rf $HOME/docs-latest/* /usr/nextdom/documentation/phpdoc/
  cd /usr/nextdom/documentation
  git add -f .
  git commit -m "PHPDocumentor (Travis Build : $TRAVIS_BUILD_NUMBER  - Branch : $TRAVIS_BRANCH)"
  git push -fq origin gh-pages
  echo -e "Published PHPDoc.\n"
else
  echo "No doc to generate : "
  echo "TRAVIS_REPO_SLUG : $TRAVIS_REPO_SLUG"
  echo "TRAVIS_PULL_REQUEST : $TRAVIS_PULL_REQUEST"
  echo "TRAVIS_PHP_VERSION : $TRAVIS_PHP_VERSION"
  echo "TRAVIS_BRANCH : $TRAVIS_BRANCH"
fi
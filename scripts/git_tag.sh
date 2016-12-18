#!/bin/bash

cd ..

git tag -a v${1} -m 'version ${1}'; git push origin --tags
#!/bin/bash
sed -i "s/v = '${1}'/v = '${2}'/g" ${3}

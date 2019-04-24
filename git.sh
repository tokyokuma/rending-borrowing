#!/bin/sh
git add -A
git commit -am "ver1.0"
git push heroku master
git push github master

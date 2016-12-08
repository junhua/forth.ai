# forth.ai.backend
==

[![Build Status](https://travis-ci.org/junhua/forth.ai.backend.svg?branch=master)](https://travis-ci.org/junhua/forth.ai.backend)
[![Coverage Status](https://coveralls.io/repos/github/junhua/forth.ai.backend/badge.svg?branch=master)](https://coveralls.io/github/junhua/forth.ai.backend?branch=master)

## Stack
- python 2.7
- django and django rest framework
- postgres
- nginx

## Dev Setup

1. Create a docker-machine environment:
`docker-machine create --driver virtualbox dev`

1. Change to dev environment: 
`eval $(docker-machine env dev)`

1. Run compose
`docker-compose build` then 
`docker-compose up -d`

1. Check ip
`docker-machine ip dev`
and copy it to browser to access the web
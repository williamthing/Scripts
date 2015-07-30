#!/bin/bash

# Calculates Stock dividends with a 2k investment
# in the course of one year
# first arg is stock value 2nd arg is dividends amount
# doesn't support float values

let shares=(2000.00/$1)
let apr=($shares*$2*4.00)
echo $apr

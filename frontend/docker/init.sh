#!/bin/sh

BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

printf "\n\n\n${RED}Start${NC} Node\n\n\n"

printf "\n\n\n${GREEN}voidcms FrontEnd${NC} installed\n\n\n"

cd /frontend/

yarn serve
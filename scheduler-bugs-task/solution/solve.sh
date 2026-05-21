#!/bin/bash
set -e
cd /app
patch -p0 < /solution/fix.patch

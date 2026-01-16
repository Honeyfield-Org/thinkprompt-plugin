#!/bin/bash
# detect-project-type.sh
# Detects the project type (Next.js, NestJS, or unknown) based on project files

PROJECT_DIR="${1:-.}"

# Check for Next.js
if [ -f "$PROJECT_DIR/next.config.js" ] || [ -f "$PROJECT_DIR/next.config.mjs" ] || [ -f "$PROJECT_DIR/next.config.ts" ]; then
    echo "nextjs"
    exit 0
fi

# Check package.json for Next.js dependency
if [ -f "$PROJECT_DIR/package.json" ]; then
    if grep -q '"next"' "$PROJECT_DIR/package.json" 2>/dev/null; then
        echo "nextjs"
        exit 0
    fi
fi

# Check for NestJS
if [ -f "$PROJECT_DIR/nest-cli.json" ]; then
    echo "nestjs"
    exit 0
fi

# Check package.json for NestJS dependency
if [ -f "$PROJECT_DIR/package.json" ]; then
    if grep -q '"@nestjs/core"' "$PROJECT_DIR/package.json" 2>/dev/null; then
        echo "nestjs"
        exit 0
    fi
fi

# Unknown project type
echo "unknown"
exit 0

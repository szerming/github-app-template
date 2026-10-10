#!/usr/bin/env bash
# Load a .env file into the environment without overriding variables that are
# already set. Convention, as dotenv has it: the real environment wins over the
# file, so an explicit WEBHOOK_SECRET or PORT on the command line is not
# silently replaced by a developer's local one.
load_env() {
    local file="$1" line key
    [ -f "$file" ] || return 0
    while IFS= read -r line || [ -n "$line" ]; do
        case "$line" in
            '' | '#'*) continue ;;
        esac
        key="${line%%=*}"
        case "$key" in
            *[!A-Za-z0-9_]*) continue ;;
        esac
        if [ -z "${!key:-}" ]; then
            export "${key}=${line#*=}"
        fi
    done <"$file"
}

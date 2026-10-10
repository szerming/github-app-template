#!/usr/bin/env bash
# Load a .env file into the environment without overriding variables that are
# already set -- even when one is set to the empty string. Convention, as dotenv
# has it: the real environment wins over the file, so an explicit WEBHOOK_SECRET
# or PORT on the command line is not silently replaced by a developer's local
# one (and an explicitly empty secret stays empty, so the service refuses to
# start instead of being filled in from the file).
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
        if [ -z "${!key+x}" ]; then
            export "${key}=${line#*=}"
        fi
    done <"$file"
}

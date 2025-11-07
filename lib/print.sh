#!/bin/sh

# ==============================================================================
# Print helper functions for consistent messaging across GitEx commands.
#
# These functions provide standardized, colored output for different message
# types. All functions use ANSI color codes defined in ./ansi-codes.sh.
#
# Usage:
#   . "$(dirname "$0")/../lib/print.sh"
#   print_error "something went wrong"
#   print_hint "try this instead"
# ==============================================================================

# Source ANSI color codes.
# shellcheck source=lib/ansi-codes.sh
. "$(dirname "$0")/../lib/ansi-codes.sh"

# Print an error message to stderr in red.
# Usage: print_error "message"
print_error() {
  printf "%berror:%b %s\n" "${BOLD}${RED}" "${RESET}" "$1" >&2
}

# Print a hint message to stderr in cyan.
# Usage: print_hint "message"
print_hint() {
  printf "%bhint:%b %s\n" "${BOLD}${CYAN}" "${RESET}" "$1" >&2
}

# Print an info message to stdout (no color).
# Usage: print_info "message"
print_info() {
  printf "%s\n" "$1"
}

# Print a success message to stdout in green.
# Usage: print_success "message"
print_success() {
  printf "%b%s%b\n" "${GREEN}" "$1" "${RESET}"
}

# Print a warning message to stderr in yellow.
# Usage: print_warning "message"
print_warning() {
  printf "%bwarning:%b %s\n" "${BOLD}${YELLOW}" "${RESET}" "$1" >&2
}

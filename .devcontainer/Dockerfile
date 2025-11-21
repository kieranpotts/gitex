# Ultra-lightweight base image.
FROM alpine:3.20

# Install system dependencies.
RUN apk add --no-cache \
    sudo \
    curl \
    bash \
    git \
    python3 \
    pipx \
    shellcheck

# Install Poetry via pipx.
RUN pipx install poetry

# Add '/root/.local/bin to PATH environment variable - required for Poetry.
ENV PATH="/root/.local/bin:$PATH"

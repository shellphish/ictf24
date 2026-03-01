# iCTF Challenge Author Guide

This guide walks you through everything you need to know to create a challenge for the iCTF competition. Challenges are deployed via [CTFd](https://ctfd.io) using [`ctfcli`](https://docs.ctfd.io/docs/management/ctfcli/challenges/), and must follow the conventions described below.

For questions, contact the administrators at [ictf-admin@googlegroups.com](mailto:ictf-admin@googlegroups.com).

Author: D3xt3r

---

## Table of Contents

1. [Challenge Types](#1-challenge-types)
2. [Directory Structure](#2-directory-structure)
3. [challenge.yml Reference](#3-challengeyml-reference)
4. [Creating a Local Challenge](#4-creating-a-local-challenge)
5. [Creating a Remote Challenge](#5-creating-a-remote-challenge)
6. [Creating an LLM Challenge](#6-creating-an-llm-challenge)
7. [Flag Format](#7-flag-format)
8. [Writeup Requirements](#8-writeup-requirements)
9. [Exploit Script Template](#9-exploit-script-template)
10. [Submission Checklist](#10-submission-checklist)

---

## 1. Challenge Types

There are three kinds of challenges:

### Local (data-only)
The challenge is a bundle of files. Players download the files and find the flag through offline analysis — no server connection required. Use this for categories like forensics, cryptography, reverse engineering, or steganography.

> **Reference:** `challenges/samplelocal`

### Remote (interactive service)
Players connect to a live service running inside a Docker container and exploit it to retrieve the flag. The challenge directory includes a `Dockerfile` that defines the service.

> **Reference:** `challenges/sampleremote`

### Remote LLM
A special case of a remote challenge where the service wraps a Large Language Model. Players interact with the LLM and must craft prompts to extract the flag.

> **Reference:** `challenges/samplellm`

---

## 2. Directory Structure

Every challenge lives in its own directory under `challenges/`. The name of the directory is the challenge slug.

### Local challenge layout

```
challenges/my-challenge/
├── challenge.yml          # Required: CTFd metadata
├── README.md              # Required: one-line challenge description
├── materials/
│   └── README.md          # Optional: notes on any extra materials
├── src/
│   └── <challenge files>  # Files distributed to players
└── writeup/
    └── README.md          # Required: solution walkthrough
```

### Remote challenge layout

```
challenges/my-challenge/
├── challenge.yml          # Required: CTFd metadata
├── README.md              # Required: one-line challenge description
├── Dockerfile             # Required: container definition
├── Makefile               # Required if compiled (C/C++)
├── materials/
│   └── README.md          # Optional: notes on any extra materials
├── src/
│   ├── <source files>     # Service source code
│   ├── flag.txt           # The flag
│   └── <service config>   # e.g. xinetd.conf or service.sh
├── ro/
│   └── .gitkeep           # Placeholder; compiled binaries go here at build time
├── rw/
│   └── .gitkeep           # Placeholder; writable directory for the service at runtime
└── writeup/
    ├── README.md          # Required: solution walkthrough
    └── exploit.py         # Required: working exploit script
```

**`ro/` vs `rw/`:** The `ro/` directory holds files that should be read-only at runtime (e.g., compiled binaries). The `rw/` directory is owned by the `challenge` user and is writable at runtime (e.g., for temporary files). Neither directory should contain committed files beyond `.gitkeep`.

---

## 3. `challenge.yml` Reference

This file is the single source of truth for CTFd. It must be present in every challenge directory.

```yaml
# ── Required fields ──────────────────────────────────────────────────────────

name: "my-challenge"          # Unique slug; matches the directory name
author: "your-username"       # Your handle
category: forensics           # e.g. forensics, pwn, web, crypto, source code, misc
description: >
  A short player-facing description of the challenge.
  Explain the goal, not the solution.
value: 100                    # Points awarded (discuss with admins for difficulty scaling)
type: standard                # "standard" for fixed points; see dynamic scoring below

# ── Docker deployment ────────────────────────────────────────────────────────
# Local challenge (no container):
image: null
protocol: null
host: null

# Remote challenge (local Dockerfile):
# image: .
# protocol: tcp
# host: null

# ── Flags ────────────────────────────────────────────────────────────────────
flags:
    - ictf{YourFlagHere}              # static, case-sensitive (most common)

    # Case-insensitive static flag:
    # - { type: "static", content: "ictf{YourFlag}", data: "case_insensitive" }

    # Regex flag:
    # - { type: "regex", content: "ictf\\{pattern.*\\}", data: "case_insensitive" }

# ── Files distributed to players ─────────────────────────────────────────────
files:
    - src/my-file.pdf         # Paths are relative to this challenge.yml

# ── Tagging ──────────────────────────────────────────────────────────────────
topics:                       # Admin-only; describe the technique(s) required
    - document forensics
tags:                         # Public; shown to players
    - forensics
    - pdf

# ── Optional fields ──────────────────────────────────────────────────────────

connection_info: null         # Human-readable connection instructions shown to players
                              # Set this after deployment, e.g. "nc hostname 7631"

healthcheck: null             # Path to a script that verifies the service is alive
                              # Receives connection info via --connection-info flag

# Hints (purchasable by players):
# hints:
#     - { content: "Think about copy-paste.", cost: 50 }

# Prerequisite challenges (must be solved before this one unlocks):
# requirements:
#     - "Warmup"

state: visible                # "visible" or "hidden"
version: "0.1"

# ── Dynamic scoring (alternative to fixed "value") ───────────────────────────
# Set type: dynamic and uncomment the block below:
# extra:
#     initial: 500            # Starting point value
#     decay: 100              # How fast points decay as solves increase
#     minimum: 50             # Minimum point floor
```

---

## 4. Creating a Local Challenge

Local challenges require no server. The workflow is:

1. **Prepare your challenge files.** Place them in `src/`. These are the files players will download. Only list the files players need in `challenge.yml` under `files:` — do not expose solution artifacts.

2. **Hide the flag.** The flag must be non-trivially hidden in the distributed files. Examples:
   - Redacted text in a PDF (see `samplelocal`)
   - Hidden data in image metadata (EXIF, LSB steganography)
   - Encrypted or encoded payload in a binary file
   - Data embedded in a network capture (PCAP)

3. **Fill in `challenge.yml`.** Set `image: null`, `protocol: null`, `host: null`.

4. **Write the writeup.** Document the exact steps to find the flag in `writeup/README.md`. No exploit script is required for local challenges.

### Example `challenge.yml` for a local challenge

```yaml
name: "my-forensics"
author: "you"
category: forensics
description: "Something is hiding in this file. Find the flag."
value: 100
type: standard
image: null
protocol: null
host: null
flags:
    - ictf{HiddenInPlainSight}
files:
    - src/document.pdf
topics:
    - steganography
tags:
    - forensics
state: visible
version: "0.1"
```

---

## 5. Creating a Remote Challenge

Remote challenges run as a Docker container. Players connect via TCP and exploit the service.

### 5.1 Dockerfile

Follow this structure closely. It enforces the security conventions required by the competition.

```dockerfile
FROM gcc                          # or ubuntu:20.04, python:3.x, etc.

# Install only what you need; keep the image small
RUN apt-get update -y \
    && apt-get install --no-install-recommends -y xinetd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Place the flag at /flag.txt, world-readable
COPY ./src/flag.txt /flag.txt
RUN chmod 644 /flag.txt

# Create the unprivileged service user (UID 31337 by convention)
RUN useradd -u 31337 -ms /bin/bash challenge
# Lock down the home directory — the user cannot write to it
RUN chown root:root /home/challenge
RUN chmod 755 /home/challenge

# Copy source, read-only output, and writable directories
COPY src /home/challenge/src
COPY ro  /home/challenge/ro       # compiled binaries land here
COPY rw  /home/challenge/rw
RUN chown challenge:challenge /home/challenge/rw
RUN chmod 755 /home/challenge/rw

# Build the application
COPY Makefile /home/challenge/Makefile
WORKDIR /home/challenge
RUN make

# Install the xinetd service config
RUN mv /home/challenge/src/xinetd.conf /etc/xinetd.d/my-challenge

EXPOSE 7631
CMD ["/usr/sbin/xinetd", "-dontfork"]
```

**Key rules:**
- The service must run as UID 31337 (`challenge` user), never as root.
- `/flag.txt` must be readable by the `challenge` user (`chmod 644`).
- The home directory (`/home/challenge`) must not be writable by `challenge`.
- Only `rw/` should be writable at runtime.

### 5.2 Service wrapper: xinetd

xinetd is the recommended wrapper for compiled (C/C++) services. It spawns a new process for each connection.

Create `src/xinetd.conf`:

```
service my-challenge
{
  disable       = no
  type          = UNLISTED
  wait          = no
  server        = /home/challenge/ro/application
  socket_type   = stream
  protocol      = tcp
  user          = 31337
  port          = 7631
  flags         = REUSE
}
```

> **Important:** The `port` here must match the `EXPOSE` value in your Dockerfile.

### 5.3 Service wrapper: socat

socat is a simpler alternative, well-suited for Python or shell script services. Add it to the `CMD` in your Dockerfile instead of using xinetd:

```dockerfile
EXPOSE 11301
CMD ["socat", "TCP-LISTEN:11301,reuseaddr,fork",
     "EXEC:'/home/challenge/src/service.sh',pty,rawer,stderr,su=challenge"]
```

`su=challenge` ensures each connection runs as the unprivileged user.

### 5.4 Makefile (compiled challenges)

For C/C++ challenges, provide a `Makefile` that compiles into `ro/`:

```makefile
default:
	gcc -g -Wall -o ro/application src/application.c

clean:
	rm -fr ro/application*
```

The `ro/` directory must exist before `make` runs. The `.gitkeep` placeholder handles this.

### 5.5 `challenge.yml` for a remote challenge

```yaml
name: "my-remote"
author: "you"
category: pwn
description: >
  Exploit the service and read /flag.txt.
  Source code is provided.
value: 100
type: standard
image: .                          # "." means use the local Dockerfile
protocol: tcp
host: null
flags:
    - ictf{ExploitedSuccessfully}
files:
    - src/application.c           # give players the source if the challenge calls for it
topics:
    - buffer overflow
tags:
    - pwn
    - remote
state: visible
version: "0.1"
```

### 5.6 Testing your container locally

```bash
# Build the image
docker build -t my-challenge .

# Run it
docker run -d -p 7631:7631 my-challenge

# Test the connection
nc localhost 7631

# Stop and remove
docker rm -f $(docker ps -a -q --filter ancestor=my-challenge)
```

---

## 6. Creating an LLM Challenge

LLM challenges are remote challenges where the service interacts with a language model. Players must craft prompts to extract the flag.

### 6.1 Required extra setup

The challenge needs an OpenAI-compatible API key. Configure it in `src/rate_limiter.py`:

```python
import os

OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_API_KEY  = os.environ.get("OPENAI_API_KEY",  "sk-YOUR-API-KEY")
OPENAI_MODEL    = os.environ.get("OPENAI_MODEL",    "gpt-4o-mini")
```

The script writes these to `/tmp/ictf.env` so the challenge script can source them. You can also point `OPENAI_BASE_URL` at a [LiteLLM](https://github.com/BerriAI/litellm) proxy to use alternative models without changing your challenge code.

### 6.2 Service launcher (`service.sh`)

Use this pattern to enforce timeouts and load credentials before starting the challenge:

```bash
#!/bin/bash
timeout 180 /home/challenge/src/rate_limiter.py &&
source /tmp/ictf.env &&
timeout 180 /home/challenge/src/challenge.py
```

The 180-second timeouts prevent connections from hanging open indefinitely.

### 6.3 Dockerfile for LLM challenges

Use socat as the service wrapper and install Python + API dependencies:

```dockerfile
FROM ubuntu:20.04

RUN apt-get update -y \
    && apt-get install --no-install-recommends -y coreutils build-essential socat python3 python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install requests openai rich

RUN useradd -u 31337 -ms /bin/bash challenge
RUN chown root:root /home/challenge
RUN chmod 755 /home/challenge

COPY src /home/challenge/src
RUN chmod 755 /home/challenge/src/rate_limiter.py
RUN chmod 755 /home/challenge/src/challenge.py
RUN chmod 755 /home/challenge/src/service.sh

WORKDIR /home/challenge/src
ENV TERM=xterm

EXPOSE 11301
CMD ["socat", "TCP-LISTEN:11301,reuseaddr,fork",
     "EXEC:'/home/challenge/src/service.sh',pty,rawer,stderr,su=challenge"]
```

---

## 7. Flag Format

All flags must follow this format:

```
ictf{descriptive_phrase_here}
```

**Rules:**
- Must start with `ictf{` and end with `}`.
- The content should be a meaningful phrase that hints at the exploit or category (e.g., `ictf{AnInjectionOfSecurity}`, `ictf{RedactingIsThisChallengeUndoing}`).
- No spaces inside the braces; use camelCase or underscores.
- The flag in `src/flag.txt` (for remote challenges) and the flag in `challenge.yml` under `flags:` must be identical.

---

## 8. Writeup Requirements

Every challenge must include a `writeup/` directory.

### `writeup/README.md` (required for all challenges)

Write a clear, step-by-step solution that a skilled player could follow from scratch. Include:
- The vulnerability or technique being exploited
- The exact steps to reproduce the solution
- Any tools needed
- The expected output (the flag)

### `writeup/exploit.py` (required for remote challenges)

A fully working automated exploit. See [Section 9](#9-exploit-script-template) for the required format.

---

## 9. Exploit Script Template

All remote challenge exploit scripts must:

- Use `pwntools`
- Accept the host and port as positional command-line arguments
- Print the flag to stdout in the format `ictf{...}`

**Minimal template:**

```python
#!/usr/bin/env python3
import pwn
import re
import sys

# Usage: python exploit.py <host> <port>
conn = pwn.remote(sys.argv[1], sys.argv[2])

# --- interact with the service here ---
conn.recvuntil(b"prompt: ")
conn.sendline(b"your payload here")

# --- collect output and extract flag ---
complete_output = ""
while True:
    try:
        output = str(conn.recv())
    except:
        break
    if not output:
        break
    complete_output += output

m = re.search(r"ictf\{[^}]+\}", complete_output)
print(m.group(0))
```

Test it against your running container before submitting:

```bash
python writeup/exploit.py localhost 7631
# Expected output: ictf{YourFlag}
```

---

## 10. Submission Checklist

Before submitting your challenge, verify every item below.

### All challenge types
- [ ] Directory name matches `name:` in `challenge.yml`
- [ ] `challenge.yml` is present and all required fields are filled in
- [ ] `flags:` in `challenge.yml` contains the correct flag
- [ ] `files:` lists only the files players should receive (no solutions, no flag)
- [ ] `writeup/README.md` explains the solution clearly
- [ ] Flag format is `ictf{...}` and is meaningful
- [ ] `state: visible` (or `hidden` if coordinating a staged release with admins)

### Local challenges
- [ ] All files listed under `files:` exist in `src/`
- [ ] The flag is non-trivially hidden — it cannot be found by a simple `strings` or `grep`

### Remote challenges
- [ ] `image: .` and `protocol: tcp` are set in `challenge.yml`
- [ ] `docker build -t test-challenge .` succeeds with no errors
- [ ] Service starts correctly: `docker run -d -p <port>:<port> test-challenge`
- [ ] Manual connection works: `nc localhost <port>`
- [ ] `flag.txt` is at `/flag.txt` inside the container and readable by the `challenge` user
- [ ] Service runs as UID 31337, not root
- [ ] `writeup/exploit.py` runs successfully against the local container and prints the flag
- [ ] The exposed port in `Dockerfile` matches the port in `xinetd.conf` / `socat` command

### LLM challenges
- [ ] `src/rate_limiter.py` is present and reads API credentials from environment variables
- [ ] `src/service.sh` enforces timeouts
- [ ] The challenge has been tested with a real API key
- [ ] `writeup/exploit.py` (or usage instructions) demonstrates how to extract the flag

---
Author: D3xt3r

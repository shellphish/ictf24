# Challenges
The challenges of this class follow the specification of the CTFd challenges, and are meant to be deployed using `ctfcli`.
See: https://docs.ctfd.io/docs/management/ctfcli/challenges/

Note that for challenges that require remote interaction, the author should provide under the directory `writeup` both a `README.md` file with the description of how to exploit the service and an `exploit.py` that, when executed passing the host and port of the service, returns the flag (e.g., `ictf{ThisIsTheFlag}`).
Please use `pwntools` for the exploit script.

## Sample Challenges

### `samplelocal`

This challenge is representative of a data-only service, in which a user has to download a file, which contains the flag (usually well-hidden).
This challenge does not use any containers.

### `sampleremote`

This challenge is representative of a remote access service, in which a user has to connect to a host and exploit a service to obtain the flag.
This challenge uses a single container.

# iCTF 24

The 2024 iCTF is an educational challenge-based Capture The Flag competition focused on AI and Cybersecurity.
The 2024 iCTF is sponsored by the [NSF AI ACTION Institute](https://action.ucsb.edu), and it is organized by the Women in Computer Science (WiCS) at UCSB together with [Shellphish](http://www.shellphish.net).

The 2024 iCTF has two tracks, one for high school students and one for undergraudate students, hosted on different servers.
Each track has a set of challenges with a wide variety of difficulty.

Please see [ictf.cs.ucsb.edu](https://ictf.cs.ucsb.edu) for rules and registration procedures.
The infrastructure is hosted by [CTFd](https://CTFd.io).

## Challenges

Challenges are of two kinds:
1. Self-contained: The challenge is composed of a bundle of data, which contains all the information necessary to extract the flag.
2. Interactive: The challenge provides some data (e.g., some code or a description pf the challenge), but the actual exploitation of the challenge requires connecting to a host at a specific port. The service is hosted in a docker container.

Examples of this challenges are in the repo under `challenges/samplelocal` and `challenges/sampleremote`, respectively.
An example of a (remote) challenge that uses an LLM (Large Language Model) is in `challenges/samplellm`.

For any questions about challenge development please contact the administrators at [ictf-admin@googlegroups.com](mailto:ictf-admin@googlegroups.com).

# Pangolin

A proof-of-concept of a web proxy.

## Introduction

### What is a web proxy, and how could it help us?

A web proxy is a server that facilitates the exchange of data between the client and the target
website.

Some countries or administrators censor certain websites for many reasons, including from hiding
sensitive information to blocking inappropriate websites. However, such censorship may be
problematic, such as how the Great Firewall of China prevents people that are in China from accessing many
non-Chinese sites, including Google, CNN, and Fox News. Using a web proxy solves these problems by
allowing users to bypass their network's firewall and access websites that they otherwise can't.

## Implementation

The proxy's main files consists of [`application.py`][application.py], [`helpers.py`][helpers.py],
and [`request_capture.js`][request_capture.js].

### [`application.py`][application.py]

This file is the core of the back-end of the proxy. It renders the home page as well as loading
files from target websites and serving them to the user.

### [`helpers.py`][helpers.py]

This file includes helper functions that [`application.py`][application.py] uses, including
handling cookies and injecting the script tags with [`request_capture.js`][request_capture.js] and
the [xhook library][xhook.js] into queried HTML files.

### [`request_capture.js`][request_capture.js]

This file includes the javascript that redirects all requests from the front-end to the proxy.

## Limitations

### Cannot support cookies or logins on certain websites

Most websites go out of their way to ward off [man-in-the-middle (MITM)](//en.wikipedia.org/wiki/Man-in-the-middle_attack) attacks. Because a proxy
could potentially be used to carry out MITM attacks, many websites would prevent successful logins
or prevent successful site access if it detects a MITM attack such as by a proxy. Bypassing such
security measures of such websites would take large amounts of effort.

### Does not work with a firewall that uses whitelists

If a firewall uses whitelists, this proxy would probably not work because the proxy would be
blocked, preventing the use of this proxy.

## Further improvement

Even though this proxy successfully redirects requests to target websites, there are still some
room for improvement.

### Support cookies and login on websites sensitive to MITM attacks

This is an improvement that would take an extremely long time because it would require inventing
new and practical techniques to carry out MITM attacks (this requires reverse-engineering these
websites' MITM-preventing techniques, which would take too much effort) or creating and
implementing a new protocol that would allow certain, trusted entities to intercept the connection.
I have tried supporting cookies by serializing cookies from each website into cookie jars, but
supporting cookies resulted in Facebook locking my account, which means that these websites,
especially Facebook, uses methods, including cookies, to detect MITM attacks, and just supporting
cookies would trigger MITM-preventing mechanisms on specific sites.

### Encrypt the connection between the client and the proxy

This would be a relatively feasible improvement that would include the client first loading a page
that implements sending and receiving data encrypted via asymmetric encryption, preventing firewall
administrators from intercepting and analyzing the traffic.

[application.py]: application.py "application.py"
[helpers.py]: helpers.py "helpers.py"
[request_capture.js]: static/request_capture.js "request_capture.js"
[xhook.js]: //unpkg.com/xhook@latest "xhook.js"
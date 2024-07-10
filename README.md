# inventree-cups-plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![CI](https://github.com/wolflu05/inventree-cups-plugin/actions/workflows/ci.yml/badge.svg)

A label printer driver plugin for [InvenTree](https://inventree.org), which provides support for [Cups label printing servers](https://www.cups.org). If your printer is not cups compatible, you can setup a cups printing server. This [article](https://nerdig.es/labelwriter-im-netz-teil1/) describes how to setup a cups printing server for the DYMO LabelWriter 450 Duo. If you have a Dymo printer, you might also want to check out the dedicated inventree-dymo-plugin which is the recommended choice because it works more performant.

## Installation

> [!IMPORTANT]
> This plugin needs `cups-devel` installed to install its dependencies. You can read more about the requirements at [`pycups`](https://github.com/OpenPrinting/pycups). If you're using `apt` as a package manager run `apt install libcups2-dev` before. For docker see [below](#docker).

> [!IMPORTANT]
> For InvenTree<0.16 use this package with version `0.1.0`

Goto "Settings > Plugins > Install Plugin" and enter `inventree-cups-plugin` as package name.

### Docker

For docker installs you need to build your own docker image based on the inventree image to install the required system dependencies. The following `Dockerfile` is using a multistage build to only install what is needed onto the inventree image and do the building in a separate stage.

> [!NOTE]
> This only works for the inventree alpine based docker image which is shipped with inventree>=0.13.

To use it you have to do some slight modifications of the `docker-compose.yml` file and create the `Dockerfile` as follows:

<details><summary>docker-compose.yml changes</summary>

```diff
diff --git a/docker-compose.yml b/docker-compose.yml
index 8adee63..dc3993c 100644
--- a/docker-compose.yml
+++ b/docker-compose.yml
@@ -69,7 +69,14 @@ services:
     # Uses gunicorn as the web server
     inventree-server:
         # If you wish to specify a particular InvenTree version, do so here
-        image: inventree/inventree:${INVENTREE_TAG:-stable}
+        image: inventree/inventree:${INVENTREE_TAG:-stable}-printing
+        pull_policy: never
+        build:
+          context: .
+          dockerfile: Dockerfile
+          target: production
+          args:
+            INVENTREE_TAG: ${INVENTREE_TAG:-stable}
         # Only change this port if you understand the stack.
         # If you change this you have to change:
         # - the proxy settings (on two lines)
@@ -88,7 +95,8 @@ services:
     # Background worker process handles long-running or periodic tasks
     inventree-worker:
         # If you wish to specify a particular InvenTree version, do so here
-        image: inventree/inventree:${INVENTREE_TAG:-stable}
+        image: inventree/inventree:${INVENTREE_TAG:-stable}-printing
+        pull_policy: never
         command: invoke worker
         depends_on:
             - inventree-server
```

</details>

<details><summary>Dockerfile</summary>

```dockerfile
ARG INVENTREE_TAG

# prebuild stage - needs a lot of build dependencies
FROM python:3.10-alpine3.18 as prebuild

RUN apk add --no-cache cups-dev gcc git musl-dev && \
    pip install --user --no-cache-dir git+https://github.com/wolflu05/inventree-cups-plugin

# production image - only install the cups shared library
FROM inventree/inventree:${INVENTREE_TAG} as production

RUN apk add --no-cache cups-libs
COPY --from=prebuild /root/.local /root/.local
```

</details>

## Configuration Options

| Name     | Description                                                                   | Example             |
| -------- | ----------------------------------------------------------------------------- | ------------------- |
| Server   | IP/Hostname to connect to the cups server                                     | `192.168.1.5`       |
| Port     | Port to connect to the cups server                                            | `631`               |
| User     | User to connect to the cups server                                            | _can also be empty_ |
| Password | Password to connect to the cups server                                        | _can also be empty_ |
| Printer  | Printer from cups server, can be selected if valid connection options are set | `myprinter`         |

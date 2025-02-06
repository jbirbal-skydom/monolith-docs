---
sidebar_position: 7
title: Dev environment (HOST)
draft: false
---

Most development environment setup is the same. Essentially install:

* [VScode](https://code.visualstudio.com/)
* [Rust](https://www.rust-lang.org/tools/install)
  * rust target
* Clone the repo
  
    ```sh
    git clone https://github.com/jbirbal-skydom/monolith.git
    cd monolith
    git submodule init
    git submodule update
    ```

* Build

:::info

 **OSX and Mac users** you will need [`xcode`](https://developer.apple.com/xcode/).

:::
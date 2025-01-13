---
sidebar_position: 2
title: iOS Development
---

Install [xcode](https://developer.apple.com/xcode/)
Install VScode

Clone repo

Add target:
    rustup target add aarch64-apple-ios x86_64-apple-ios

Build library

    ```sh
    cargo build --target x86_64-apple-ios --release
    cargo build --target aarch64-apple-ios --release
    cargo run --bin uniffi-bindgen generate \
    --library target/x86_64-apple-ios/release/libmonolithcore.a \
    --language swift \
    --out-dir out
    ```

Compile module (if needed):

    ```sh
swiftc \
    -module-name MonolithCore \
    -emit-library -o libmonolithcore.a \
    -emit-module -emit-module-path ./out/ \
    -parse-as-library \
    -L ./target/x86_64-apple-ios/release \
    -lmonolithcore \
    -Xcc -fmodule-map-file=out/MonolithFFIFile.modulemap \
    -target x86_64-apple-ios10.0-simulator \
    -sdk $(xcrun --sdk iphonesimulator --show-sdk-path) \
    out/MonolithCore.swift

    ```

xframe

```sh
xcodebuild -create-xcframework \
  -library ./target/x86_64-apple-ios/release/libmonolithcore.a \
  -headers ./out/ \
  -output ./MonolithCore.xcframework

```
drop the files into xcode project

    ```bash
    MyXcodeProject/
    ├── MonolithIntegration/  # New folder for Rust-related files
    │   ├── MonolithCore.swift
    │   ├── MonolithFFIFile.h
    │   ├── MonolithFFIFile.modulemap
    │   ├── libmonolithcore.a
    ```

Build settings> Library Search Paths / Import Path >$(PROJECT_DIR)/MonolithIntegration
General>Frameworks, Libraries, and Embedded Content>Add Other...>libmonolithcore.a


create application
click on the project name on the  Project Navigator

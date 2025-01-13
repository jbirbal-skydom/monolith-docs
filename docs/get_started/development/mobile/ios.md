---
sidebar_position: 2
title: iOS Development
---

Install [xcode](https://developer.apple.com/xcode/)
Install VScode

Clone repo

Add target:

    ```sh
    rustup target add aarch64-apple-ios x86_64-apple-ios
    ```

Build library

    ```sh
    cargo build --target x86_64-apple-ios --release
    cargo build --target aarch64-apple-ios --release
    ```

Combine the library

    ```sh
    lipo -create -output libmonolithcore.a \
    target/x86_64-apple-ios/release/libmonolithcore.a \
    target/aarch64-apple-ios/release/libmonolithcore.a
    ```

Generate the binding

    ```sh
    cargo run --bin uniffi-bindgen generate src/monolith.udl --language swift --out-dir out
    ```

Test the file

    ```sh
    swiftc -I /Users/skydom/Desktop/lessons/math/MonolithIntegration \
        -L /Users/skydom/Desktop/lessons/math/MonolithIntegration \
        -Xcc -fmodule-map-file=/Users/skydom/Desktop/lessons/math/MonolithIntegration/MonolithFFI.modulemap \
        -lmonolithcore -emit-executable ./MonolithIntegration/test.swift
    ```

drop the files into xcode project

    ```bash
    MyXcodeProject/
    ├── MonolithIntegration/  # New folder for Rust-related files
    │   ├── Monolithcore-Bridging-Header.h
    │   ├── MonolithCore.swift
    │   ├── MonolithFFI.h
    │   ├── MonolithFFI.modulemap
    │   ├── libmonolithcore.a
    ```

Build settings> `Library Search Paths` and  `Import Path` >

    ```sh
    $(PROJECT_DIR)/MonolithIntegration
    ```

Build settings> `Objective-C Bridging Header` >

    ```sh
    $(PROJECT_DIR)/MonolithIntegration/Monolithcore-Bridging-Header.h
    ```

General > Frameworks, Libraries, and Embedded Content > `Add Other...` >

    ```sh
    libmonolithcore.a
    ```

Other Swift Flags >

    ```sh
    -Xcc
    -fmodule-map-file=$(SRCROOT)/MonolithIntegration/MonolithFFI.modulemap
    ```

Build

you can access the functions directly like:

    ```swift
    let result_outside = add(a: 3, b: 4)
    ```

## Extra

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

xcframework

    ```sh
    xcodebuild -create-xcframework \
    -library ./target/x86_64-apple-ios/release/libmonolithcore.a \
    -headers ./out/ \
    -output ./MonolithCore.xcframework
    ```

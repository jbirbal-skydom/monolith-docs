---
sidebar_position: 3
title: Android specific instructions
---

Insall [Android Studio](https://developer.android.com/studio)
Install the NDK under hte SDK manager on the Android Studio

<!-- ktlint

* install [Java](https://learn.microsoft.com/en-us/java/openjdk/download#openjdk-17)
* [ktlint](https://github.com/pinterest/ktlint/releases)
  * download `.bat` and `.zip`
  * place in same folder
  * add `.bat` to the path -->

add target:
`rustup target add aarch64-linux-android armv7-linux-androideabi i686-linux-android x86_64-linux-android`

add ndk:
download android studio install the ndk add to path

```bash
set ANDROID_NDK_HOME=<NDK_PATH>
set NDK_HOME=<NDK_PATH>
```

* windows
  * value: `C:\Android\ndk\<VERSION>`
* linux
  * value:  `ANDROID_NDK_HOME=~/Android/sdk/ndk/<VERSION>`

add binary for toolchain in path
`%ANDROID_NDK_HOME%\toolchains\llvm\prebuilt\windows-x86_64\bin`

create a `.cargo/config.toml` and add the proper linker:

* linux

    ```toml
    [target.x86_64-linux-android]
    ar = "${ANDROID_NDK_HOME}/toolchains/llvm/prebuilt/windows-x86_64/bin/llvm-ar"
    linker = "${ANDROID_NDK_HOME}/toolchains/llvm/prebuilt/windows-x86_64/bin/x86_64-linux-android21-clang"
    [target.aarch64-linux-android]
    ar = "${ANDROID_NDK_HOME}/toolchains/llvm/prebuilt/windows-x86_64/bin/llvm-ar"
    linker = "${ANDROID_NDK_HOME}/toolchains/llvm/prebuilt/windows-x86_64/bin/aarch64-linux-android21-clang"
    [target.armv7-linux-androideabi]
    ar = "${ANDROID_NDK_HOME}/toolchains/llvm/prebuilt/windows-x86_64/bin/llvm-ar"
    linker = "${ANDROID_NDK_HOME}/toolchains/llvm/prebuilt/windows-x86_64/bin/armv7a-linux-androideabi21-clang"
    [target.i686-linux-android]
    ar = "${ANDROID_NDK_HOME}/toolchains/llvm/prebuilt/windows-x86_64/bin/llvm-ar"
    linker = "${ANDROID_NDK_HOME}/toolchains/llvm/prebuilt/windows-x86_64/bin/i686-linux-android21-clang"

    ```

* windows

    ```toml
    [target.x86_64-linux-android]
    ar = "C:\\Android\\ndk\\27.0.11902837\\toolchains\\llvm\\prebuilt\\windows-x86_64\\bin\\llvm-ar.exe"
    linker = "C:\\Android\\ndk\\27.0.11902837\\toolchains\\llvm\\prebuilt\\windows-x86_64\\bin\\x86_64-linux-android21-clang.cmd"

    [target.aarch64-linux-android]
    ar = "C:\\Android\\ndk\\27.0.11902837\\toolchains\\llvm\\prebuilt\\windows-x86_64\\bin\\llvm-ar.exe"
    linker = "C:\\Android\\ndk\\27.0.11902837\\toolchains\\llvm\\prebuilt\\windows-x86_64\\bin\\aarch64-linux-android21-clang.cmd"

    [target.armv7-linux-androideabi]
    ar = "C:\\Android\\ndk\\27.0.11902837\\toolchains\\llvm\\prebuilt\\windows-x86_64\\bin\\llvm-ar.exe"
    linker = "C:\\Android\\ndk\\27.0.11902837\\toolchains\\llvm\\prebuilt\\windows-x86_64\\bin\\armv7a-linux-androideabi21-clang.cmd"

    [target.i686-linux-android]
    ar = "C:\\Android\\ndk\\27.0.11902837\\toolchains\\llvm\\prebuilt\\windows-x86_64\\bin\\llvm-ar.exe"
    linker = "C:\\Android\\ndk\\27.0.11902837\\toolchains\\llvm\\prebuilt\\windows-x86_64\\bin\\i686-linux-android21-clang.cmd"
    ```

build

* Release

```sh
cargo build --release --target x86_64-linux-android
cargo run --bin uniffi-bindgen generate --library target/x86_64-linux-android/release/libmonolithcore.so --language kotlin --out-dir out
```

* debug
  `cargo build --target x86_64-linux-android`

Android

* create project
* create `jnilibs` directory to house the `arch`
  * cd `app/src/main/`
    * Add Architecture-Specific Folders:

    ```sh
    jniLibs/arm64-v8a/
    jniLibs/armeabi-v7a/
    jniLibs/x86_64/
    ```

  * Place `.so` in the specific folder
* Add bindings
  * copy the entire folder to `app/src/main/java` eg `app/src/main/java/ai/skydom/monolith/core/`
* Add dependencies `build.gradle`
  * Add dependencies in `app/build.gradle`
    * uniffi
      * JNA and Coroutines

        ```kotlin
        dependencies {
            implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.6.4")
            implementation("net.java.dev.jna:jna:5.12.0@aar")
        }
        ```

    * rust

      ```json
      android.sourceSets["main"].jniLibs.srcDirs("src/main/jniLibs")
      ```

* Initialize on `MainActivity.kt` under `AppCompatActivity`
  
  ```kotlin

  object MonolithLib {
      init {
          System.loadLibrary("monolithcore") // Ensure this matches the library name
      }
  }
  ```

---
sidebar_position: 1
title: Get Started
---

## 👋 Welcome to the Monolith Docs

Hey there! Before we dive in, let me save you some time and explain how these docs work. Because let's face it - nobody wants to read documentation longer than they have to.

But i want to give thanks to our [sponsors](/resources/sponsorship.md) too.

### 🎯 How These Docs Are Organized

I've organized everything based on how people actually use docs (you know, in real life). Here's the deal:

#### 🌱 User Level - The "Just Make It Work" Zone

Look, you probably just want to use Monolith and get on with your life. These sections are casual, friendly, and packed with practical examples. Expect dad jokes, pop culture references, and zero judgment if you copy-paste code. We've all been there.

#### 🔧 Source Level - The "Tell Me More" Zone

This is where you'll find the meaty stuff - implementation notes, architecture decisions, and the "why" behind features. It's like the director's commentary track, but for code. Still friendly, just more detailed.

#### 🤓 Technical Level - The "I Need to Know Everything" Zone

Welcome to the matrix! This section is for when you need to know exactly how the sausage is made. It's detailed, it's thorough, and yes, it might make your eyes glaze over. Perfect for 3 AM debugging sessions.

### 🧭 Finding Your Way Around

#### If You're a User

Start with [Quick Start](/get_started/quick-start.md). It's like microwaving instructions - quick, simple, gets the job done.

#### If You're Running a Business

Check out [Use Cases](/get_started/usage/use-cases.md) and [Integration Guides](/get_started/usage/integration-guides/index.md). We'll help you figure out how to make Monolith work for your needs.

#### If You're an Engineer

The [API Documentation](../api/sample-api.info.mdx) and [Core Concepts](/concepts/barcode-structure.md) are your new best friends. Don't worry, we've included plenty of code examples.

We do have a rust sandbox:

##### Your First Rust Program

import CodeAPI from '@site/src/components/rust/CodeAPI';

Let's start with a simple "Hello, World!" program:

```rust
    println!("Hello, World!");
```

<CodeAPI
  sandbox="rust"
  files={{
    'main.rs': `fn main() {
    println!("Hello, World!");
}`
  }}
/>

:::warning

`Rust` is a **compiled** language which does take a while to compile and run. Give it time. Check [The `Rust` examples](/resources/extras/rust/rust-basic.md).

:::

#### If You're Really Into This

First off, you're awesome! 🌟 The [Full Directory](#psychos---full-directory) below shows you everything we've got. Dive as deep as you want.

### 📚 Pro Tips

- Lost in the terminology? Hit up our [Glossary](/resources/glossary.md). No judgment here.
- Need help? The [Community](/resources/community.md) section is full of people who love helping out.
- Found a bug? Want to contribute? Check out our [Development Guide](/get_started/development/host.md).

Remember: take what you need, skip what you don't. These docs are here to help, not to overwhelm.

Now, let's get you started! What kind of user are you? 👆

### Psychos - Full Directory

```sh
.
├── api
│   ├── get-a-list-of-users.api.mdx
│   ├── sample-api.info.mdx
│   └── sidebar.ts
├── concepts
│   ├── barcode-structure.md
│   ├── color-models.md
│   ├── concepts.md
│   ├── error-correction.md
│   ├── finder-patterns.md
│   └── hexagonal-tiling.md
├── get_started
│   ├── development
│   │   ├── ci-cd.md
│   │   ├── desktop
│   │   │   ├── desktop.md
│   │   │   ├── linux.md
│   │   │   ├── macos.md
│   │   │   └── windows.md
│   │   ├── development.md
│   │   ├── docker.md
│   │   ├── embedded
│   │   │   ├── A7.md
│   │   │   ├── M4.md
│   │   │   └── embedded.md
│   │   ├── host.md
│   │   └── mobile
│   │       ├── android.md
│   │       ├── ios.md
│   │       └── mobile.md
│   ├── faq.md
│   ├── get_started.md
│   ├── install.md
│   ├── quick-start.md
│   ├── troubleshooting.md
│   └── usage
│       ├── deployment.md
│       ├── integration-guides
│       │   ├── mobile-apps.md
│       │   └── wordpress.md
│       └── use-cases.md
└── resources
    ├── community.md
    ├── extras
    │   ├── about.md
    │   ├── changelog.md
    │   ├── extra.md
    │   └── rust
    │       └── rust-basic.md
    ├── glossary.md
    ├── research
    │   ├── datasets
    │   │   ├── color-calibration.md
    │   │   └── test-images.md
    │   ├── experiments
    │   │   ├── camera-tests.md
    │   │   └── printer-tests.md
    │   ├── papers
    │   │   ├── layered-hexagons.md
    │   │   └── monolith-overview.md
    │   └── research.md
    ├── resource.md
    ├── sponsorship.md
    └── tools.md

17 directories, 48 files
```

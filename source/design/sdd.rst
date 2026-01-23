Software Design Document
========================

Introduction
---------------

This SDD describes the architecture and design of AirGap Transfer’s MVP.

**Guiding document:** :doc:`Principles <../../meta/principles>`

--------------

Architecture Overview
------------------------

System Context
~~~~~~~~~~~~~~

::

   ┌────────────────────────────────────────────────────────┐
   │                 Pure Rust CLI Application              │
   ├────────────────────────────────────────────────────────┤
   │                                                        │
   │   ┌──────────────┐       ┌──────────────┐              │
   │   │  CLI Parser  │──────►│   Commands   │              │
   │   │   (clap)     │       │ (pack/unpack)│              │
   │   └──────────────┘       └──────┬───────┘              │
   │                                 │                      │
   │                  ┌──────────────┼──────────────┐       │
   │                  ▼              ▼              ▼       │
   │       ┌──────────────┐  ┌─────────────┐  ┌─────────┐   │
   │       │   Chunker    │  │  Verifier   │  │  State  │   │
   │       │  (streaming) │  │  (SHA-256)  │  │ (JSON)  │   │
   │       └──────┬───────┘  └─────────────┘  └─────────┘   │
   │              │                                         │
   │              ▼                                         │
   │       ┌───────────────┐                                │
   │       │  USB/Disk I/O │                                │
   │       └───────────────┘                                │
   └────────────────────────────────────────────────────────┘

Design Rationale
~~~~~~~~~~~~~~~~

====================== ==============================================
Decision               Rationale
====================== ==============================================
Pure Rust              Memory safety, cross-platform, minimal runtime
CLI only               Focus on functionality, defer GUI to post-MVP
Streaming architecture Handle files larger than available RAM
JSON manifest          Human-readable, easy to inspect and debug
SHA-256 verification   Industry-standard cryptographic integrity
No compression         Simplicity, defer to post-MVP
====================== ==============================================

--------------

File Structure
-----------------

Per `principles.md <../../principles.md>`__: **Flat structure, minimal modules**

::

   airgap-transfer/
   ├── src/
   │   ├── main.rs          # Entry point, CLI setup
   │   ├── commands/
   │   │   ├── pack.rs      # Pack operation implementation
   │   │   ├── unpack.rs    # Unpack operation implementation
   │   │   └── list.rs      # List operation implementation
   │   ├── chunker.rs       # Streaming chunk creation/reconstruction
   │   ├── verifier.rs      # SHA-256 checksum operations
   │   ├── manifest.rs      # Manifest file handling (JSON)
   │   └── usb.rs           # USB detection and capacity checks
   ├── Cargo.toml
   ├── vendor/              # Vendored dependencies (for air-gap builds)
   └── .cargo/
       └── config.toml      # Points to vendor directory

--------------

Data Design
--------------

Manifest Structure
~~~~~~~~~~~~~~~~~~

**Single JSON file per transfer operation**

.. code:: json

   {
     "version": "1.0",
     "operation": "pack",
     "source_path": "/path/to/source",
     "total_size_bytes": 10737418240,
     "chunk_size_bytes": 1073741824,
     "chunk_count": 10,
     "chunks": [
       {
         "index": 0,
         "filename": "chunk_000.tar",
         "size_bytes": 1073741824,
         "checksum_sha256": "abc123...",
         "status": "completed"
       }
     ],
     "created_utc": "2026-01-04T12:00:00Z",
     "last_updated_utc": "2026-01-04T12:15:00Z"
   }

Chunk File Format
~~~~~~~~~~~~~~~~~

- **Format:** tar archive (standard Unix format)
- **Naming:** ``chunk_XXX.tar`` (zero-padded, 3-digit index)
- **Size:** Fixed size (except final chunk which may be smaller)
- **Contents:** Raw file data, preserving directory structure

State Persistence
~~~~~~~~~~~~~~~~~

**Manifest file location:**

- **Pack operation:** Written to USB alongside chunks
- **Unpack operation:** Read from USB chunk location
- **Resume:** Manifest status field tracks completed chunks

--------------

Component Design
-------------------

CLI Parser (main.rs)
~~~~~~~~~~~~~~~~~~~~

**Command structure:**

.. code-block:: bash

   airgap-transfer <command> [options]

   Commands:
     pack <source> <dest>      Split files into chunks
     unpack <source> <dest>    Reconstruct from chunks
     list <chunk-location>     Show chunk inventory

**Global options:** ``--dry-run``, ``--verbose``, ``--verify``, ``--chunk-size``

Chunker (chunker.rs)
~~~~~~~~~~~~~~~~~~~~

**Core responsibility:** Streaming chunk creation and reconstruction

**Pack behavior:**

- Stream source files into tar format
- Write fixed-size chunks directly to USB
- Calculate checksum during streaming (single-pass)
- Update manifest progressively

**Unpack behavior:**

- Verify chunk checksums before processing
- Extract tar chunks sequentially to destination
- Reconstruct original directory structure

Verifier (verifier.rs)
~~~~~~~~~~~~~~~~~~~~~~

**Core responsibility:** Cryptographic integrity verification

**Functions:**

- Generate SHA-256 checksum during streaming
- Verify chunk checksum matches manifest
- Report verification failures with details

Manifest (manifest.rs)
~~~~~~~~~~~~~~~~~~~~~~

**Core responsibility:** Metadata persistence and state management

**Functions:**

- Create manifest from pack operation parameters
- Update chunk status as operations complete
- Read and validate manifest during unpack
- Support resume by tracking completion status

USB Handler (usb.rs)
~~~~~~~~~~~~~~~~~~~~

**Core responsibility:** Removable media detection and capacity checks

**Functions:**

- Detect USB mount points (platform-specific)
- Query available capacity
- Auto-determine optimal chunk size
- Sync filesystem before USB removal prompt

--------------

Interaction Flows
--------------------

Pack Operation
~~~~~~~~~~~~~~

::

   User                     App                      USB
    │                        │                        │
    │ pack source usb        │                        │
    │───────────────────────►│                        │
    │                        │ Detect USB capacity    │
    │                        │───────────────────────►│
    │                        │ Calculate chunk count  │
    │                        │                        │
    │                        │ Stream chunk 0 to USB  │
    │                        │───────────────────────►│
    │                        │ Update manifest        │
    │                        │                        │
    │ "Insert next USB"      │                        │
    │◄───────────────────────│                        │
    │                        │ Stream chunk 1 to USB  │
    │                        │───────────────────────►│
    │                        │ Sync and finish        │
    │ "Complete: 2 chunks"   │                        │
    │◄───────────────────────│                        │

Unpack Operation
~~~~~~~~~~~~~~~~

::

   User                     App                      USB
    │                        │                        │
    │ unpack usb dest        │                        │
    │───────────────────────►│                        │
    │                        │ Read manifest          │
    │                        │───────────────────────►│
    │                        │ Verify all chunks      │
    │                        │───────────────────────►│
    │                        │ Extract chunk 0        │
    │                        │ Extract chunk 1        │
    │                        │ Verify final output    │
    │ "Complete: verified"   │                        │
    │◄───────────────────────│                        │

--------------

Dependencies
---------------

**Minimal crates:** Target ≤10 direct dependencies

See :doc:`Principles <../../meta/principles>` for dependency guidelines.

**Expected dependencies:**

- clap_ - CLI argument parsing
- serde_ / serde_json_ - Manifest serialization
- sha2_ - SHA-256 checksums
- tar_ - Tar archive creation/extraction
- Platform-specific filesystem libs (stdlib where possible)

--------------

Security & Privacy
---------------------

**Privacy by architecture:** No network code exists in the application.

================= ==========================================
Threat            Mitigation
================= ==========================================
Data exfiltration No network crates in dependency tree
Path traversal    Validate and sanitize all paths
Checksum bypass   Mandatory verification (with –verify flag)
Malicious chunks  Verify checksums before extraction
================= ==========================================

--------------

Deployment
-------------

Air-Gap Support
~~~~~~~~~~~~~~~

The application supports deployment on air-gapped systems (no internet access).

**Requirements:**

- Pure Rust, single binary
- Vendored dependencies via ``cargo vendor``
- Offline build: ``cargo build --release --offline``

Platform Packages
~~~~~~~~~~~~~~~~~

======== ================== =================================
Platform Format             Notes
======== ================== =================================
macOS    Binary             Universal binary (x86_64 + ARM64)
Windows  .exe               Standalone executable
Linux    Binary + .deb/.rpm Static binary preferred
======== ================== =================================

--------------

Platform Considerations
---------------------------

USB Detection
~~~~~~~~~~~~~

======== ================================
Platform Approach
======== ================================
macOS    ``/Volumes/*`` directory listing
Linux    ``/media/$USER/*`` or ``/mnt/*``
Windows  DriveInfo API via WinAPI
======== ================================

Filesystem Sync
~~~~~~~~~~~~~~~

=========== ========================
Platform    Command
=========== ========================
macOS/Linux ``sync`` syscall
Windows     ``FlushFileBuffers`` API
=========== ========================

.. _clap: https://docs.rs/clap/latest/clap/
.. _serde: https://docs.rs/serde/latest/serde/
.. _serde_json: https://docs.rs/serde_json/latest/serde_json/
.. _sha2: https://docs.rs/sha2/latest/sha2/
.. _tar: https://docs.rs/tar/latest/tar/

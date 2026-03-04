Design
======

Introduction
---------------

This SDD describes the architecture and design of AirGap Transfer’s MVP.

**Guiding document:** `Principles <https://cleanroomlabs.dev/docs/meta/principles.html>`_

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
   │       │  (streaming) │  │ (pluggable) │  │ (JSON)  │   │
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
Pluggable hash verify  Trait-based interface; SHA-256 default, extensible to future algorithms
No compression         Simplicity, defer to post-MVP
====================== ==============================================

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
   │   ├── error.rs         # Unified error type (thiserror)
   │   ├── manifest.rs      # Manifest file handling (JSON)
   │   ├── progress.rs      # Progress tracking utilities (indicatif)
   │   ├── prompt.rs        # User interaction and confirmation prompts
   │   ├── usb.rs           # USB detection and capacity checks
   │   └── verifier.rs      # Pluggable hash verification (HashAlgorithm trait)
   ├── Cargo.toml
   ├── vendor/              # Vendored dependencies (for air-gap builds)
   └── .cargo/
       └── config.toml      # Points to vendor directory

Data Design
-----------

See :ref:`Design Conventions <chunk-format-conventions>` in the
Requirements for the canonical manifest schema and chunk naming
convention.

State Persistence
~~~~~~~~~~~~~~~~~

**Manifest file location:**

- **Pack operation:** Written to USB alongside chunks
- **Unpack operation:** Read from USB chunk location
- **Resume:** Manifest status field tracks completed chunks

Component Design
----------------

CLI Parser (main.rs)
~~~~~~~~~~~~~~~~~~~~

**Command structure:**

.. code-block:: bash

   airgap-transfer <command> [options]

   Commands:
     pack <source> <dest>      Split files into chunks
     unpack <source> <dest>    Reconstruct from chunks
     list <chunk-location>     Show chunk inventory

**Global options:** ``--dry-run``, ``--verbose``, ``--no-verify``, ``--force``, ``--resume``, ``--chunk-size``, ``--hash-algorithm``

Chunker (chunker.rs)
~~~~~~~~~~~~~~~~~~~~

**Core responsibility:** Streaming chunk creation and reconstruction

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

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

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

**Functions:**

- Generate checksum during streaming using configured algorithm
- Verify chunk checksum matches manifest (algorithm-aware)
- Report verification failures with details

The verifier implements a ``HashAlgorithm`` trait. New algorithms are added by implementing
this trait — no changes to the chunker, manifest, or CLI modules required.

Manifest (manifest.rs)
~~~~~~~~~~~~~~~~~~~~~~

**Core responsibility:** Metadata persistence and state management

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

**Functions:**

- Create manifest from pack operation parameters
- Update chunk status as operations complete
- Read and validate manifest during unpack
- Support resume by tracking completion status

USB Handler (usb.rs)
~~~~~~~~~~~~~~~~~~~~

**Core responsibility:** Removable media detection and capacity checks

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

**Functions:**

- Detect USB mount points (platform-specific)
- Query available capacity
- Auto-determine optimal chunk size
- Sync filesystem before USB removal prompt

Interaction Flows
-----------------

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

Dependencies
---------------

**10 direct runtime crates** (target ≤10). Dev-only dependencies
(``assert_cmd``, ``predicates``, ``tempfile``) and transitive
dependencies are excluded from this count.

See `Principles <https://cleanroomlabs.dev/docs/meta/principles.html>`_ for dependency guidelines.

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

**Direct runtime dependencies:**

- clap_ - CLI argument parsing
- serde_ / serde_json_ - Manifest serialization
- sha2_ - SHA-256 checksums (default backend); trait interface supports additional backends
- tar_ - Tar archive creation/extraction
- chrono_ - UTC timestamps in manifest (``created_utc``, ``last_updated_utc``)
- colored_ - Terminal color output
- indicatif_ - Progress bars for long operations
- libc_ - Platform-specific filesystem sync and USB detection (macOS/Linux)
- thiserror_ - Derive-based error type implementation

Security & Privacy
------------------

**Privacy by architecture:** No network code exists in the application.

================= ==========================================
Threat            Mitigation
================= ==========================================
Data exfiltration No network crates in dependency tree
Path traversal    Validate and sanitize all paths
Checksum bypass   Verification enabled by default (disable with --no-verify)
Malicious chunks  Verify checksums before extraction
USB interception  v1.2: Optional AEAD encryption at rest (ChaCha20-Poly1305)
Manifest tamper   v1.2: Keyed MAC authentication of manifest
================= ==========================================

v1.2 Encryption Design (Planned)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The v1.0 checksum-based verification detects accidental corruption but does not protect
against intentional tampering or unauthorized reading of intercepted USB media. v1.2
introduces optional AEAD encryption (see :doc:`SRS v1.2 requirements <../requirements/srs>`)
to address these threats.

**Design principle:** Encryption is opt-in. When no passphrase is provided, behavior is
identical to v1.0. This preserves the simple default workflow while enabling encryption
for users with higher-security threat models.

**Key architecture decisions:**

- AEAD (not separate encrypt-then-MAC) to eliminate composition errors
- Passphrase-based key derivation via Argon2id (no PKI infrastructure required)
- Manifest remains human-readable JSON, authenticated via keyed MAC
- Trait-based AEAD backend mirrors existing ``HashAlgorithm`` pattern

Deployment
----------

Air-Gap Support
~~~~~~~~~~~~~~~

The application supports deployment on air-gapped systems (no internet access).

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

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

Platform Considerations
-----------------------

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
.. _chrono: https://docs.rs/chrono/latest/chrono/
.. _colored: https://docs.rs/colored/latest/colored/
.. _indicatif: https://docs.rs/indicatif/latest/indicatif/
.. _libc: https://docs.rs/libc/latest/libc/
.. _thiserror: https://docs.rs/thiserror/latest/thiserror/

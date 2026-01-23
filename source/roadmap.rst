Project Roadmap
===============

Build an air-gap file transfer tool you can trust. Ship it. See what happens.

**Guiding document:** :doc:`Principles <../meta/principles>`

--------------

v1.0.0 Release
--------------

**Release Goal:** This project will reach v1.0.0 as part of a coordinated release with AirGap Whisper and AirGap Deploy.

**v1.0.0 Scope:** The MVP features documented in this roadmap.

**Cross-Project Integration:** v1.0.0 validates the multi-USB transfer scenario works end-to-end with AirGap Deploy.

**Release Coordination:** See :doc:`Release Roadmap </meta/release-roadmap>` for cross-project timeline and integration milestones.

**Target Date:** [TBD - see Release Roadmap]

--------------

Current Status
--------------

**Phase:** Planning Complete

**Next:** Begin MVP implementation

All requirements, design, and test specifications are complete. Ready to start Milestone 1.

**MVP Goal:** Successfully transfer 10GB dataset across air-gap with checksum verification.

--------------

MVP Scope
---------

============ =========================================
Feature      Implementation
============ =========================================
Pack files   Split into chunks, write to USB
Unpack files Reconstruct from chunks with verification
List chunks  Show inventory and status
Integrity    SHA-256 checksums for all operations
Resume       Continue interrupted transfers
CLI          Command-line interface with options
============ =========================================

--------------

Implementation Milestones
-------------------------

Milestone 1: Project Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Cargo project with CLI skeleton.

- ☐ Create Cargo project with minimal dependencies
- ☐ Add CLI argument parsing (clap)
- ☐ Create module structure per SDD
- ☐ Verify basic command execution (–help)

**Done when:** ``airgap-transfer --help`` shows usage.

--------------

Milestone 2: Chunker Core
~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Stream files into fixed-size chunks.

- ☐ Implement tar archive creation
- ☐ Stream data in fixed-size blocks
- ☐ Write chunks to specified destination
- ☐ Handle final chunk (may be smaller)

**Done when:** Can create chunk files from source directory.

--------------

Milestone 3: Checksum Verification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Generate and verify SHA-256 checksums.

- ☐ Calculate checksum during chunk creation
- ☐ Store checksums in manifest
- ☐ Verify chunk checksums during unpack
- ☐ Report verification failures

**Done when:** Chunks are verified before unpacking.

--------------

Milestone 4: Manifest Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Track operation state in JSON manifest.

- ☐ Create manifest structure (per SDD schema)
- ☐ Write manifest during pack operation
- ☐ Update chunk status as operations complete
- ☐ Read manifest during unpack/list operations

**Done when:** Manifest persists state across operations.

--------------

Milestone 5: Unpack Operation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Reconstruct files from chunks.

- ☐ Read and validate manifest
- ☐ Verify all chunks present
- ☐ Extract chunks to destination
- ☐ Verify final output integrity

**Done when:** Files reconstructed match original.

--------------

Milestone 6: USB Handling
~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Detect USB and manage capacity.

- ☐ Detect USB mount points (platform-specific)
- ☐ Query available capacity
- ☐ Auto-calculate optimal chunk size
- ☐ Sync filesystem before removal prompts

**Done when:** Auto-detects USB capacity and adjusts chunk size.

--------------

Milestone 7: Resume Capability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Continue interrupted operations.

- ☐ Track completed chunks in manifest
- ☐ Skip already-completed chunks on resume
- ☐ Handle partial chunk cleanup
- ☐ Support resume for both pack and unpack

**Done when:** Can resume after interruption.

--------------

Milestone 8: List Command
~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Display chunk inventory and status.

- ☐ Read manifest from chunk location
- ☐ Display chunk count and sizes
- ☐ Show verification status
- ☐ Identify missing or corrupted chunks

**Done when:** ``airgap-transfer list`` shows complete inventory.

--------------

Milestone 9: Polish
~~~~~~~~~~~~~~~~~~~

**Goal:** Production-ready CLI.

- ☐ Error handling with clear messages
- ☐ Progress indicators for long operations
- ☐ Dry-run mode for all commands
- ☐ Confirmation prompts for destructive operations
- ☐ Comprehensive help text

**Done when:** Ready for daily use without frustration.

--------------

Definition of Done
------------------

MVP is complete when:

☐ Pack 10GB dataset into chunks
☐ Transfer chunks across air-gap (manual USB movement)
☐ Unpack and verify integrity on destination
☐ Resume interrupted pack operation
☐ List chunk inventory shows all expected chunks
☐ All operations work offline
☐ Use successfully for one week

--------------

What's NOT in MVP
-----------------

Defer all of this until after shipping:

- Compression (gzip, zstd)
- Encryption
- Parallel chunk processing
- GUI
- Automatic USB detection and swapping
- Network transfer modes
- Tests
- CI/CD
- Performance optimization

Build it. Use it. Then improve it.

--------------

After MVP
---------

**Personal Use** — Use it for real air-gap transfers
**Integration** — Integrate with AirGap Deploy workflows
**Refine** — Add compression, encryption based on real needs
**Share** — Consider public release if valuable to others

--------------

Key Documents
-------------

============================================== =======================================
Document                                       Purpose
============================================== =======================================
:doc:`Principles <../meta/principles>`         Design principles (read first)
:doc:`Requirements (SRS) <requirements/srs>`   Functional and non-functional requirements
:doc:`Design (SDD) <design/sdd>`               Architecture and component design
:doc:`Test Plan <testing/plan>`                Test cases with traceability
============================================== =======================================

--------------

Progress Log
------------

========== =======================================
Date       Activity
========== =======================================
2026-01-04 Created specification and documentation
========== =======================================

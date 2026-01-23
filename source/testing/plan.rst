Test Plan
=========

Introduction
---------------

This test plan covers MVP requirements (:need_count:`type=='req' and 'transfer' in tags` functional requirements, :need_count:`type=='nfreq' and 'transfer' in tags` non-functional requirements).

--------------

Test Strategy
----------------

Test Levels
~~~~~~~~~~~

=========== ====================== ======================
Level       Scope                  Tools
=========== ====================== ======================
Unit        Individual functions   Rust ``#[test]``
Integration Component interactions Rust integration tests
System      End-to-end workflows   Manual testing
=========== ====================== ======================

Features Not Tested
~~~~~~~~~~~~~~~~~~~

===================== ===================
Feature               Reason
===================== ===================
USB hardware failures External dependency
Filesystem internals  Platform dependency
Tar format compliance Third-party library
===================== ===================

Test Automation Approach
~~~~~~~~~~~~~~~~~~~~~~~~

**MVP:** Manual testing primarily. Unit tests for core logic.

**Unit tests (automatable):**

=========== ========================================
Component   What to Test
=========== ========================================
chunker.rs  Chunk size calculations, streaming logic
verifier.rs Checksum generation and verification
manifest.rs JSON serialization, state management
=========== ========================================

**Integration tests (partially automatable):**

====================== ====================
Test                   Automation Notes
====================== ====================
Pack + Unpack workflow Use temp directories
Manifest persistence   In-memory filesystem
Checksum verification  Known test vectors
====================== ====================

**System tests (manual only):**

========================= ===================================
Test                      Why Manual
========================= ===================================
USB detection             Requires physical USB hardware
Cross-platform behavior   Requires multiple test machines
Large file handling       Time-intensive, requires disk space
Resume after interruption Requires manual interruption
========================= ===================================

--------------

Test Cases by Category
-------------------------

Pack Operation Tests
~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: test
   :filter: "transfer" in tags and "pack" in tags
   :columns: id,title,tests,priority
   :colwidths: 20,40,20,20
   :style: table
   :sort: id

.. test:: Pack Single File into Chunks
   :id: TC-PCK-001
   :status: approved
   :tags: transfer, pack, chunking
   :tests: FR-TRANSFER-001
   :priority: high

   Verify pack operation splits single file into chunks

.. test:: Pack Directory into Chunks
   :id: TC-PCK-002
   :status: approved
   :tags: transfer, pack, directory
   :tests: FR-TRANSFER-001
   :priority: high

   Verify pack operation handles directory with multiple files

.. test:: Auto-Detect USB Capacity
   :id: TC-PCK-003
   :status: approved
   :tags: transfer, pack, usb
   :tests: FR-TRANSFER-002
   :priority: high

   Verify automatic detection of USB drive capacity

.. test:: Generate Chunk Checksums
   :id: TC-PCK-004
   :status: approved
   :tags: transfer, pack, checksum
   :tests: FR-TRANSFER-003
   :priority: high

   Verify SHA-256 checksums generated for each chunk

.. test:: Create Manifest File
   :id: TC-PCK-005
   :status: approved
   :tags: transfer, pack, manifest
   :tests: FR-TRANSFER-004
   :priority: high

   Verify manifest file creation with chunk metadata

.. test:: Stream Without Temp Files
   :id: TC-PCK-006
   :status: approved
   :tags: transfer, pack, streaming
   :tests: FR-TRANSFER-005
   :priority: high

   Verify pack operation streams data without intermediate temp files

.. test:: Manual Chunk Size Specification
   :id: TC-PCK-007
   :status: approved
   :tags: transfer, pack, chunk-size
   :tests: FR-TRANSFER-006
   :priority: medium

   Verify manual chunk size override functionality

.. test:: Progress Reporting
   :id: TC-PCK-008
   :status: approved
   :tags: transfer, pack, progress
   :tests: FR-TRANSFER-007
   :priority: medium

   Verify progress reporting during pack operation

.. test:: USB Swapping Prompt
   :id: TC-PCK-009
   :status: approved
   :tags: transfer, pack, usb, ui
   :tests: FR-TRANSFER-008
   :priority: medium

   Verify system prompts for USB swapping when multiple chunks needed

Unpack Operation Tests
~~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: test
   :filter: "transfer" in tags and "unpack" in tags
   :columns: id,title,tests,priority
   :colwidths: 20,40,20,20
   :style: table
   :sort: id

.. test:: Reconstruct Files from Chunks
   :id: TC-UNP-001
   :status: approved
   :tags: transfer, unpack, reconstruction
   :tests: FR-TRANSFER-009
   :priority: high

   Verify unpack reconstructs original files from chunks

.. test:: Verify Chunk Checksums
   :id: TC-UNP-002
   :status: approved
   :tags: transfer, unpack, checksum
   :tests: FR-TRANSFER-010
   :priority: high

   Verify chunk checksums before reconstruction

.. test:: Place Files in Destination
   :id: TC-UNP-003
   :status: approved
   :tags: transfer, unpack, destination
   :tests: FR-TRANSFER-011
   :priority: high

   Verify files placed in correct destination directory

.. test:: Validate Chunk Completeness
   :id: TC-UNP-004
   :status: approved
   :tags: transfer, unpack, validation
   :tests: FR-TRANSFER-012
   :priority: high

   Verify all required chunks present before unpack

.. test:: Resume Partial Unpack
   :id: TC-UNP-005
   :status: approved
   :tags: transfer, unpack, resume
   :tests: FR-TRANSFER-013
   :priority: medium

   Verify unpack can resume after interruption

.. test:: Delete Chunks After Unpack
   :id: TC-UNP-006
   :status: approved
   :tags: transfer, unpack, cleanup
   :tests: FR-TRANSFER-014
   :priority: medium

   Verify optional chunk deletion after successful unpack

.. test:: Unpack Progress Display
   :id: TC-UNP-007
   :status: approved
   :tags: transfer, unpack, ui, progress
   :tests: FR-TRANSFER-015
   :priority: medium

   Verify progress reporting during file reconstruction

List Operation Tests
~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: test
   :filter: "transfer" in tags and "list" in tags
   :columns: id,title,tests,priority
   :colwidths: 20,40,20,20
   :style: table
   :sort: id

.. test:: Display Chunk Inventory
   :id: TC-LST-001
   :status: approved
   :tags: transfer, list, inventory
   :tests: FR-TRANSFER-016
   :priority: high

   Verify list command displays all available chunks

.. test:: Show Chunk Sizes and Status
   :id: TC-LST-002
   :status: approved
   :tags: transfer, list, status
   :tests: FR-TRANSFER-017
   :priority: high

   Verify list shows chunk sizes and completion status

.. test:: Identify Missing Chunks
   :id: TC-LST-003
   :status: approved
   :tags: transfer, list, missing
   :tests: FR-TRANSFER-018
   :priority: medium

   Verify list identifies missing chunks from manifest

.. test:: Show Estimated Total Size
   :id: TC-LST-004
   :status: approved
   :tags: transfer, list, size
   :tests: FR-TRANSFER-019
   :priority: medium

   Verify list shows estimated total transfer size

Integrity Tests
~~~~~~~~~~~~~~~

.. needtable::
   :types: test
   :filter: "transfer" in tags and "integrity" in tags
   :columns: id,title,tests,priority
   :colwidths: 20,40,20,20
   :style: table
   :sort: id

.. test:: Generate SHA-256 Checksums
   :id: TC-INT-001
   :status: approved
   :tags: transfer, integrity, checksum
   :tests: FR-TRANSFER-020
   :priority: critical

   Verify SHA-256 checksums generated for all chunks

.. test:: Verify Checksums During Unpack
   :id: TC-INT-002
   :status: approved
   :tags: transfer, integrity, verification
   :tests: FR-TRANSFER-021
   :priority: critical

   Verify checksums validated during unpack operation

.. test:: Detect Corrupted Chunks
   :id: TC-INT-003
   :status: approved
   :tags: transfer, integrity, corruption
   :tests: FR-TRANSFER-022
   :priority: critical

   Verify corrupted chunks detected via checksum mismatch

.. test:: Verify Final File Integrity
   :id: TC-INT-004
   :status: approved
   :tags: transfer, integrity, final
   :tests: FR-TRANSFER-023
   :priority: high

   Verify final reconstructed file integrity matches original

State Management Tests
~~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: test
   :filter: "transfer" in tags and "state" in tags
   :columns: id,title,tests,priority
   :colwidths: 20,40,20,20
   :style: table
   :sort: id

.. test:: Persist Operation State
   :id: TC-STA-001
   :status: approved
   :tags: transfer, state, persistence
   :tests: FR-TRANSFER-024
   :priority: high

   Verify operation state persisted to disk

.. test:: Track Chunk Completion
   :id: TC-STA-002
   :status: approved
   :tags: transfer, state, tracking
   :tests: FR-TRANSFER-025
   :priority: high

   Verify chunk completion tracked in state file

.. test:: Resume Interrupted Pack
   :id: TC-STA-003
   :status: approved
   :tags: transfer, state, resume, pack
   :tests: FR-TRANSFER-026
   :priority: medium

   Verify pack operation can resume after interruption

.. test:: Resume Interrupted Unpack
   :id: TC-STA-004
   :status: approved
   :tags: transfer, state, resume, unpack
   :tests: FR-TRANSFER-027
   :priority: medium

   Verify unpack operation can resume after interruption

Command Interface Tests
~~~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: test
   :filter: "transfer" in tags and "cli" in tags
   :columns: id,title,tests,priority
   :colwidths: 20,40,20,20
   :style: table
   :sort: id

.. test:: Pack Command Syntax
   :id: TC-TRANSFER-CLI-001
   :status: approved
   :tags: transfer, cli, pack
   :tests: FR-TRANSFER-028
   :priority: high

   Verify pack command accepts correct syntax and arguments

.. test:: Unpack Command Syntax
   :id: TC-TRANSFER-CLI-002
   :status: approved
   :tags: transfer, cli, unpack
   :tests: FR-TRANSFER-029
   :priority: high

   Verify unpack command accepts correct syntax and arguments

.. test:: List Command Syntax
   :id: TC-TRANSFER-CLI-003
   :status: approved
   :tags: transfer, cli, list
   :tests: FR-TRANSFER-030
   :priority: high

   Verify list command accepts correct syntax and arguments

.. test:: Dry-Run Mode
   :id: TC-TRANSFER-CLI-004
   :status: approved
   :tags: transfer, cli, dry-run
   :tests: FR-TRANSFER-031
   :priority: high

   Verify dry-run mode previews operation without execution

.. test:: Verify Flag
   :id: TC-TRANSFER-CLI-005
   :status: approved
   :tags: transfer, cli, verify
   :tests: FR-TRANSFER-032
   :priority: high

   Verify --verify flag enables checksum verification

.. test:: Chunk Size Flag
   :id: TC-TRANSFER-CLI-006
   :status: approved
   :tags: transfer, cli, configuration
   :tests: FR-TRANSFER-033
   :priority: medium

   Verify --chunk-size flag allows manual chunk size specification

.. test:: Verbose Flag
   :id: TC-TRANSFER-CLI-007
   :status: approved
   :tags: transfer, cli, logging
   :tests: FR-TRANSFER-034
   :priority: medium

   Verify --verbose flag enables detailed output logging

Error Handling Tests
~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: test
   :filter: "transfer" in tags and "error" in tags
   :columns: id,title,tests,priority
   :colwidths: 20,40,20,20
   :style: table
   :sort: id

.. test:: Insufficient USB Capacity Error
   :id: TC-TRANSFER-ERR-001
   :status: approved
   :tags: transfer, error, usb
   :tests: FR-TRANSFER-035
   :priority: high

   Verify error when USB capacity insufficient for chunk

.. test:: Missing Chunks Error
   :id: TC-TRANSFER-ERR-002
   :status: approved
   :tags: transfer, error, missing
   :tests: FR-TRANSFER-036
   :priority: high

   Verify error when required chunks missing during unpack

.. test:: Clear Error Messages
   :id: TC-TRANSFER-ERR-003
   :status: approved
   :tags: transfer, error, usability
   :tests: FR-TRANSFER-037
   :priority: high

   Verify all error messages clear and actionable

Safety Tests
~~~~~~~~~~~~

.. needtable::
   :types: test
   :filter: "transfer" in tags and "safety" in tags
   :columns: id,title,tests,priority
   :colwidths: 20,40,20,20
   :style: table
   :sort: id

.. test:: Confirm File Overwrite
   :id: TC-SAF-001
   :status: approved
   :tags: transfer, safety, overwrite
   :tests: FR-TRANSFER-038
   :priority: high

   Verify confirmation required before overwriting existing files

.. test:: Validate Destination Paths
   :id: TC-SAF-002
   :status: approved
   :tags: transfer, safety, validation
   :tests: FR-TRANSFER-039
   :priority: high

   Verify destination paths validated before write

.. test:: USB Sync Before Removal
   :id: TC-SAF-003
   :status: approved
   :tags: transfer, safety, sync
   :tests: FR-TRANSFER-040
   :priority: high

   Verify USB synced before prompting for removal

.. test:: Atomic Operations
   :id: TC-SAF-004
   :status: approved
   :tags: transfer, safety, reliability
   :tests: FR-TRANSFER-041
   :priority: high

   Verify operations are atomic where possible (no partial state on failure)

Deployment Tests
~~~~~~~~~~~~~~~~

.. test:: Offline Build Dependencies
   :id: TC-TRANSFER-DEP-001
   :status: approved
   :tags: transfer, deployment, offline
   :tests: FR-TRANSFER-042
   :priority: critical

   Verify all dependencies available for offline build via cargo vendor

.. test:: Internet-Free Build
   :id: TC-TRANSFER-DEP-002
   :status: approved
   :tags: transfer, deployment, offline
   :tests: FR-TRANSFER-043
   :priority: critical

   Verify build process works without internet after initial setup

.. test:: Single Static Binary Deployment
   :id: TC-TRANSFER-DEP-003
   :status: approved
   :tags: transfer, deployment
   :tests: FR-TRANSFER-044
   :priority: high

   Verify deployment produces single, static binary with no external dependencies

--------------

Non-Functional Tests
~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: test
   :filter: "transfer" in tags and "performance" in tags
   :columns: id,title,tests,priority
   :colwidths: 20,40,20,20
   :style: table
   :sort: id

.. test:: Pack 10GB in < 10 Minutes
   :id: TC-TRANSFER-NFR-001
   :status: approved
   :tags: transfer, performance, pack
   :tests: NFR-TRANSFER-001
   :priority: high

   Verify 10GB file packs in under 10 minutes

.. test:: Memory Usage < 100 MB
   :id: TC-TRANSFER-NFR-002
   :status: approved
   :tags: transfer, performance, memory
   :tests: NFR-TRANSFER-002
   :priority: medium

   Verify memory usage stays under 100 MB during operations

.. test:: Offline Functionality
   :id: TC-TRANSFER-NFR-003
   :status: approved
   :tags: transfer, offline, privacy
   :tests: NFR-TRANSFER-004
   :priority: critical

   Verify 100% functionality with network disconnected

.. test:: Cross-Platform Compatibility
   :id: TC-TRANSFER-NFR-004
   :status: approved
   :tags: transfer, portability, cross-platform
   :tests: NFR-TRANSFER-006
   :priority: high

   Verify functionality on Linux, macOS, Windows

.. test:: Privacy Guarantee Verification
   :id: TC-TRANSFER-NFR-005
   :status: approved
   :tags: transfer, privacy, security
   :tests: NFR-TRANSFER-003
   :priority: critical

   Verify no network calls under any circumstance (monitor with network sniffer)

.. test:: Air-Gap Deployment Test
   :id: TC-TRANSFER-NFR-006
   :status: approved
   :tags: transfer, deployment, offline
   :tests: NFR-TRANSFER-005
   :priority: critical

   Verify build and execution on air-gapped system with vendored dependencies

.. test:: Checksum Verification Reliability
   :id: TC-TRANSFER-NFR-007
   :status: approved
   :tags: transfer, reliability, integrity
   :tests: NFR-TRANSFER-007
   :priority: critical

   Verify all chunks verified with SHA-256 checksums before reconstruction

.. test:: Idempotent Pack Operation
   :id: TC-TRANSFER-NFR-008
   :status: approved
   :tags: transfer, reliability
   :tests: NFR-TRANSFER-008
   :priority: high

   Verify running pack operation multiple times produces same output without errors

.. test:: Graceful Interruption Handling
   :id: TC-TRANSFER-NFR-009
   :status: approved
   :tags: transfer, reliability, error-handling
   :tests: NFR-TRANSFER-009
   :priority: high

   Verify Ctrl+C during pack/unpack allows resume without data loss

.. test:: Data Corruption Detection
   :id: TC-TRANSFER-NFR-010
   :status: approved
   :tags: transfer, reliability, integrity
   :tests: NFR-TRANSFER-010
   :priority: critical

   Verify corrupted chunks detected via checksum mismatch with clear error message

.. test:: Progress Indicator Display
   :id: TC-TRANSFER-NFR-011
   :status: approved
   :tags: transfer, usability, ui
   :tests: NFR-TRANSFER-011
   :priority: medium

   Verify progress indicators shown for operations >2 seconds

.. test:: Error Message Clarity
   :id: TC-TRANSFER-NFR-012
   :status: approved
   :tags: transfer, usability, error-handling
   :tests: NFR-TRANSFER-012
   :priority: high

   Verify error messages include failure details and suggested fixes

.. test:: Help Text Availability
   :id: TC-TRANSFER-NFR-013
   :status: approved
   :tags: transfer, usability, cli
   :tests: NFR-TRANSFER-013
   :priority: high

   Verify --help flag provides comprehensive help for all commands

.. test:: First-Time User Experience
   :id: TC-TRANSFER-NFR-014
   :status: approved
   :tags: transfer, usability
   :tests: NFR-TRANSFER-014
   :priority: medium

   Verify new user can transfer file in <5 minutes using provided examples

.. test:: Test Coverage Verification
   :id: TC-TRANSFER-NFR-015
   :status: approved
   :tags: transfer, maintainability, testing
   :tests: NFR-TRANSFER-015
   :priority: high

   Verify codebase achieves ≥80% test coverage via cargo tarpaulin

.. test:: API Documentation Completeness
   :id: TC-TRANSFER-NFR-016
   :status: approved
   :tags: transfer, maintainability, documentation
   :tests: NFR-TRANSFER-016
   :priority: high

   Verify all public APIs have rustdoc documentation

.. test:: Clippy Compliance Check
   :id: TC-TRANSFER-NFR-017
   :status: approved
   :tags: transfer, maintainability, code-quality
   :tests: NFR-TRANSFER-017
   :priority: high

   Verify cargo clippy passes with zero warnings

.. test:: Code Formatting Check
   :id: TC-TRANSFER-NFR-018
   :status: approved
   :tags: transfer, maintainability, code-quality
   :tests: NFR-TRANSFER-018
   :priority: high

   Verify code formatted with rustfmt (cargo fmt --check)

.. test:: Large File Support
   :id: TC-TRANSFER-NFR-019
   :status: approved
   :tags: transfer, scalability
   :tests: NFR-TRANSFER-019
   :priority: medium

   Verify successful pack/unpack of 100GB file

.. test:: Streaming Architecture Verification
   :id: TC-TRANSFER-NFR-020
   :status: approved
   :tags: transfer, scalability, performance
   :tests: NFR-TRANSFER-020
   :priority: high

   Verify files larger than RAM handled via streaming (monitor memory usage)

.. test:: Concurrent Chunk Processing
   :id: TC-TRANSFER-NFR-021
   :status: approved
   :tags: transfer, scalability, performance
   :tests: NFR-TRANSFER-021
   :priority: low

   Verify concurrent chunk verification improves performance

--------------

Test Procedures
------------------

Offline Operation Test (TC-NFR-003)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Preconditions:**

- App installed
- Network disconnected (airplane mode or air-gapped system)

**Steps:**

Disconnect network
Pack 1GB test dataset
Unpack and verify
Check all operations completed

**Pass Criteria:** All operations complete successfully with no network.

Checksum Verification Test (TC-INT-003)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Preconditions:**

- Valid chunk files
- Manifest with checksums

**Steps:**

Corrupt one chunk file (modify 1 byte)
Run unpack operation
Verify error is reported
Confirm unpack aborts

**Pass Criteria:** Corrupted chunk detected, unpack aborted with clear error.

--------------

Pass/Fail Criteria
---------------------

- **All Critical tests must pass** before release
- **All High priority tests must pass** before release
- **Medium priority tests:** 90% pass rate acceptable


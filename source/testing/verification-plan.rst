Verification Planning
=====================

Test Strategy
-------------

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

Test Procedures
---------------

Offline Operation Test (TC-TRANSFER-NFR-003)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Preconditions:**

- App installed
- Network disconnected (airplane mode or an air-gapped system)

**Steps:**

- Disconnect network
- Pack 1GB test dataset
- Unpack and verify
- Check all operations completed

**Pass Criteria:** All operations complete successfully with no network.

Checksum Verification Test (TC-INT-003)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Preconditions:**

- Valid chunk files
- Manifest with checksums

**Steps:**

- Corrupt one chunk file (modify 1 byte)
- Run unpack operation
- Verify error is reported
- Confirm unpack aborts

**Pass Criteria:** Corrupted chunk detected, unpack aborted with clear error.

Pass/Fail Criteria
---------------------

- **All Critical tests must pass** before release
- **All High priority tests must pass** before release
- **Medium priority tests:** 90% pass rate acceptable

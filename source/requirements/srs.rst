Software Requirements Specification
===================================

Introduction
------------

Purpose
~~~~~~~

This SRS defines MVP requirements for AirGap Transfer, a command-line utility for safely transferring large files across air-gap boundaries.

Scope
~~~~~

**Product:** AirGap Transfer — a minimal CLI tool for chunked file transfers via removable media.

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

**In Scope:**

- Split large datasets into chunks for USB transfer
- Reconstruct files from chunks with integrity verification
- Resume interrupted transfers
- Cross-platform support (macOS, Windows, Linux)

**Out of Scope:**

- Network transfers, cloud sync, auto-updates
- Compression or encryption (defer to post-MVP; cryptographic agility for hashing is in scope)
- GUI interface
- Real-time synchronization
- Ollama-specific logic (general-purpose only)

Definitions
~~~~~~~~~~~

+-----------------------+------------------------------------------------------------------+
| Term                  | Definition                                                       |
+=======================+==================================================================+
| Air-gap               | Physical separation between systems with no network connectivity |
+-----------------------+------------------------------------------------------------------+
| Chunk                 | A fixed-size tar archive containing a portion of source data     |
+-----------------------+------------------------------------------------------------------+
| Pack                  | Operation to split source files into chunks                      |
+-----------------------+------------------------------------------------------------------+
| Unpack                | Operation to reconstruct files from chunks                       |
+-----------------------+------------------------------------------------------------------+
| Manifest              | Metadata file describing chunk inventory and checksums           |
+-----------------------+------------------------------------------------------------------+
| Cryptographic agility | Ability to swap hash algorithms without rearchitecting the system|
+-----------------------+------------------------------------------------------------------+

Overall Description
----------------------

Product Perspective
~~~~~~~~~~~~~~~~~~~

Standalone CLI tool for transferring data across air-gap boundaries using removable media.
All operations occur locally with no network connectivity.
See the :doc:`Software Design Document <../design/sdd>` for architecture diagrams and component details.

Constraints
~~~~~~~~~~~

============= ==========================================================
Constraint    Description
============= ==========================================================
Offline-only  Zero network calls at runtime
Air-gap ready Deployable without internet access
Platforms     macOS, Windows, Linux
UI model      Command-line interface only (no GUI)
Media         Works with standard removable media (USB, external drives)
============= ==========================================================

Functional Requirements
--------------------------

Pack Operation
~~~~~~~~~~~~~~

.. needtable::
   :types: req
   :filter: "transfer" in tags and "pack" in tags
   :columns: id,priority,title
   :colwidths: 20,20,60
   :style: table
   :sort: id

.. req:: Split Files into Chunks
   :id: FR-TRANSFER-001
   :status: approved
   :tags: transfer, pack, chunking
   :priority: must
   :release: v1.0

   Split source files/directories into fixed-size chunks

.. req:: Auto-Detect USB Capacity
   :id: FR-TRANSFER-002
   :status: approved
   :tags: transfer, pack, usb
   :priority: must
   :release: v1.0

   Auto-detect USB capacity and set chunk size accordingly

.. req:: Generate Chunk Checksums
   :id: FR-TRANSFER-003
   :status: approved
   :tags: transfer, pack, checksum, security
   :priority: must
   :release: v1.0

   Generate checksums for each chunk using the configured hash algorithm (default: SHA-256)

.. req:: Create Manifest File
   :id: FR-TRANSFER-004
   :status: approved
   :tags: transfer, pack, manifest
   :priority: must
   :release: v1.0

   Create manifest file with chunk metadata and checksums

.. req:: Stream Data to USB
   :id: FR-TRANSFER-005
   :status: approved
   :tags: transfer, pack, streaming, performance
   :priority: must
   :release: v1.0

   Stream data directly to USB without intermediate temp files

.. req:: Manual Chunk Size Specification
   :id: FR-TRANSFER-006
   :status: approved
   :tags: transfer, pack, configuration
   :priority: should
   :release: v1.0

   Support manual chunk size specification

.. req:: Show Pack Progress
   :id: FR-TRANSFER-007
   :status: approved
   :tags: transfer, pack, ui, progress
   :priority: should
   :release: v1.0

   Show progress during chunk creation

.. req:: Prompt for USB Swapping
   :id: FR-TRANSFER-008
   :status: approved
   :tags: transfer, pack, usb, ui
   :priority: should
   :release: v1.0

   Prompt for USB swapping when multiple chunks needed

Unpack Operation
~~~~~~~~~~~~~~~~

.. needtable::
   :types: req
   :filter: "transfer" in tags and "unpack" in tags
   :columns: id,priority,title
   :colwidths: 20,20,60
   :style: table
   :sort: id

.. req:: Reconstruct Files from Chunks
   :id: FR-TRANSFER-009
   :status: approved
   :tags: transfer, unpack, reconstruction
   :priority: must
   :release: v1.0

   Reconstruct original files from chunks

.. req:: Verify Chunk Checksums Before Unpack
   :id: FR-TRANSFER-010
   :status: approved
   :tags: transfer, unpack, verification, security
   :priority: must
   :release: v1.0

   Verify chunk checksums before reconstruction

.. req:: Place Files in Destination
   :id: FR-TRANSFER-011
   :status: approved
   :tags: transfer, unpack, filesystem
   :priority: must
   :release: v1.0

   Place reconstructed files in specified destination

.. req:: Validate Chunk Completeness
   :id: FR-TRANSFER-012
   :status: approved
   :tags: transfer, unpack, validation
   :priority: must
   :release: v1.0

   Validate chunk completeness (all chunks present)

.. req:: Resume Partial Unpacks
   :id: FR-TRANSFER-013
   :status: approved
   :tags: transfer, unpack, resume, reliability
   :priority: should
   :release: v1.0

   Resume partial unpacks if interrupted

.. req:: Delete Chunks After Unpack
   :id: FR-TRANSFER-014
   :status: approved
   :tags: transfer, unpack, cleanup
   :priority: should
   :release: v1.0

   Optionally delete chunks after successful reconstruction

.. req:: Show Unpack Progress
   :id: FR-TRANSFER-015
   :status: approved
   :tags: transfer, unpack, ui, progress
   :priority: should
   :release: v1.0

   Show progress during reconstruction

List Operation
~~~~~~~~~~~~~~

.. needtable::
   :types: req
   :filter: "transfer" in tags and "list" in tags
   :columns: id,priority,title
   :colwidths: 20,20,60
   :style: table
   :sort: id

.. req:: Display Chunk Inventory
   :id: FR-TRANSFER-016
   :status: approved
   :tags: transfer, list, manifest
   :priority: must
   :release: v1.0

   Display chunk inventory from manifest

.. req:: Show Chunk Sizes and Status
   :id: FR-TRANSFER-017
   :status: approved
   :tags: transfer, list, verification
   :priority: must
   :release: v1.0

   Show chunk sizes and verification status

.. req:: Identify Missing Chunks
   :id: FR-TRANSFER-018
   :status: approved
   :tags: transfer, list, validation
   :priority: should
   :release: v1.0

   Identify missing or corrupted chunks

.. req:: Display Estimated Total Size
   :id: FR-TRANSFER-019
   :status: approved
   :tags: transfer, list, ui
   :priority: should
   :release: v1.0

   Display estimated total size after reconstruction

Integrity Verification
~~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: req
   :filter: "transfer" in tags and "verification" in tags
   :columns: id,priority,title
   :colwidths: 20,20,60
   :style: table
   :sort: id

.. req:: Generate Checksums
   :id: FR-TRANSFER-020
   :status: approved
   :tags: transfer, verification, checksum, security
   :priority: must
   :release: v1.0

   Generate checksums during pack using the configured hash algorithm (default: SHA-256)

.. req:: Verify Checksums During Unpack
   :id: FR-TRANSFER-021
   :status: approved
   :tags: transfer, verification, checksum, security
   :priority: must
   :release: v1.0

   Verify checksums during unpack

.. req:: Detect Corrupted Chunks
   :id: FR-TRANSFER-022
   :status: approved
   :tags: transfer, verification, error-handling
   :priority: must
   :release: v1.0

   Detect corrupted chunks and report errors

.. req:: Verify Final File Checksum
   :id: FR-TRANSFER-023
   :status: approved
   :tags: transfer, verification, checksum, security
   :priority: should
   :release: v1.0

   Verify final reconstructed file against original checksum

Cryptographic Agility
~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: req
   :filter: "transfer" in tags and "crypto-agility" in tags
   :columns: id,priority,title
   :colwidths: 20,20,60
   :style: table
   :sort: id

.. req:: Configurable Hash Algorithm
   :id: FR-TRANSFER-045
   :status: approved
   :tags: transfer, crypto-agility, security
   :priority: must
   :release: v1.0

   The system SHALL allow users to select a hash algorithm via CLI flag (``--hash-algorithm``). Default: SHA-256.

.. req:: Algorithm Identified in Manifest
   :id: FR-TRANSFER-046
   :status: approved
   :tags: transfer, crypto-agility, manifest, security
   :priority: must
   :release: v1.0

   The manifest SHALL record which hash algorithm was used, so unpack can verify with the correct algorithm.

.. req:: Pluggable Hash Backend
   :id: FR-TRANSFER-047
   :status: approved
   :tags: transfer, crypto-agility, security
   :priority: must
   :release: v1.0

   The hash module SHALL use a trait-based interface so new algorithms can be added without modifying existing code.

State Management
~~~~~~~~~~~~~~~~

.. needtable::
   :types: req
   :filter: "transfer" in tags and "state" in tags
   :columns: id,priority,content
   :colwidths: 20,20,60
   :style: table
   :sort: id

.. req:: Maintain Operation State
   :id: FR-TRANSFER-024
   :status: approved
   :tags: transfer, state, manifest
   :priority: must
   :release: v1.0

   Maintain operation state in manifest file

.. req:: Track Chunk Completion
   :id: FR-TRANSFER-025
   :status: approved
   :tags: transfer, state, tracking
   :priority: must
   :release: v1.0

   Track chunk completion status

.. req:: Resume Interrupted Pack
   :id: FR-TRANSFER-026
   :status: approved
   :tags: transfer, state, resume, pack
   :priority: should
   :release: v1.0

   Support resume for interrupted pack operations

.. req:: Resume Interrupted Unpack
   :id: FR-TRANSFER-027
   :status: approved
   :tags: transfer, state, resume, unpack
   :priority: should
   :release: v1.0

   Support resume for interrupted unpack operations

Command Interface
~~~~~~~~~~~~~~~~~

.. needtable::
   :types: req
   :filter: "transfer" in tags and "cli" in tags
   :columns: id,priority,title
   :colwidths: 20,20,60
   :style: table
   :sort: id

.. req:: Pack Command
   :id: FR-TRANSFER-028
   :status: approved
   :tags: transfer, cli, pack
   :priority: must
   :release: v1.0

   ``airgap-transfer pack <source> <dest>`` command

.. req:: Unpack Command
   :id: FR-TRANSFER-029
   :status: approved
   :tags: transfer, cli, unpack
   :priority: must
   :release: v1.0

   ``airgap-transfer unpack <source> <dest>`` command. The ``<source>`` argument is a single directory path containing chunk files and the manifest. When chunks span multiple USB drives, the user connects drives sequentially and the tool prompts for swaps.

.. req:: List Command
   :id: FR-TRANSFER-030
   :status: approved
   :tags: transfer, cli, list
   :priority: must
   :release: v1.0

   ``airgap-transfer list <chunk-location>`` command

.. req:: Dry Run Flag
   :id: FR-TRANSFER-031
   :status: approved
   :tags: transfer, cli, dry-run
   :priority: must
   :release: v1.0

   ``--dry-run`` flag for all operations

.. req:: No-Verify Flag
   :id: FR-TRANSFER-032
   :status: approved
   :tags: transfer, cli, verification
   :priority: must
   :release: v1.0

   Checksum verification SHALL be enabled by default for all operations. The ``--no-verify`` flag SHALL disable verification. This ensures integrity checking is the default behavior per FR-TRANSFER-010.

.. req:: Chunk Size Flag
   :id: FR-TRANSFER-033
   :status: approved
   :tags: transfer, cli, configuration
   :priority: should
   :release: v1.0

   ``--chunk-size`` flag for manual chunk size specification

.. req:: Verbose Flag
   :id: FR-TRANSFER-034
   :status: approved
   :tags: transfer, cli, logging
   :priority: should
   :release: v1.0

   ``--verbose`` flag for detailed output

Error Handling
~~~~~~~~~~~~~~

.. needtable::
   :types: req
   :filter: "transfer" in tags and "error-handling" in tags
   :columns: id,priority,content
   :colwidths: 20,20,60
   :style: table
   :sort: id

.. req:: Detect Insufficient USB Capacity
   :id: FR-TRANSFER-035
   :status: approved
   :tags: transfer, error-handling, usb
   :priority: must
   :release: v1.0

   Detect and report insufficient USB capacity

.. req:: Handle Missing Chunks
   :id: FR-TRANSFER-036
   :status: approved
   :tags: transfer, error-handling, chunks
   :priority: must
   :release: v1.0

   Handle missing chunks gracefully

.. req:: Clear Error Messages
   :id: FR-TRANSFER-037
   :status: approved
   :tags: transfer, error-handling, usability
   :priority: must
   :release: v1.0

   Provide clear error messages with suggested actions

Safety Features
~~~~~~~~~~~~~~~

.. needtable::
   :types: req
   :filter: "transfer" in tags and "safety" in tags
   :columns: id,priority,content
   :colwidths: 20,20,60
   :style: table
   :sort: id

.. req:: Confirm File Overwrite
   :id: FR-TRANSFER-038
   :status: approved
   :tags: transfer, safety, filesystem
   :priority: must
   :release: v1.0

   Confirm overwrite of existing files

.. req:: Validate Destination Paths
   :id: FR-TRANSFER-039
   :status: approved
   :tags: transfer, safety, validation
   :priority: must
   :release: v1.0

   Validate destination paths and permissions

.. req:: Sync USB Safely
   :id: FR-TRANSFER-040
   :status: approved
   :tags: transfer, safety, usb
   :priority: must
   :release: v1.0

   Safely sync USB before prompting for removal

.. req:: Atomic Operations
   :id: FR-TRANSFER-041
   :status: approved
   :tags: transfer, safety, reliability
   :priority: should
   :release: v1.0

   Atomic operations where possible

Deployment
~~~~~~~~~~

.. needtable::
   :types: req
   :filter: "transfer" in tags and "deployment" in tags
   :columns: id,priority,content
   :colwidths: 20,20,60
   :style: table
   :sort: id

.. req:: Offline Build Dependencies
   :id: FR-TRANSFER-042
   :status: approved
   :tags: transfer, deployment, offline
   :priority: must
   :release: v1.0

   All dependencies available for offline build

.. req:: Internet-Free Build
   :id: FR-TRANSFER-043
   :status: approved
   :tags: transfer, deployment, offline
   :priority: must
   :release: v1.0

   Build process works without internet after initial setup

.. req:: Single, Static Binary Deployment
   :id: FR-TRANSFER-044
   :status: approved
   :tags: transfer, deployment
   :priority: should
   :release: v1.0

   Single, static binary deployment

Non-Functional Requirements
------------------------------

.. needtable::
   :types: nfreq
   :filter: "transfer" in tags
   :columns: id,priority,content
   :colwidths: 20,20,60
   :style: table
   :sort: id

Performance
~~~~~~~~~~~

.. nfreq:: Chunk Creation Performance
   :id: NFR-TRANSFER-001
   :status: approved
   :tags: transfer, performance
   :priority: should
   :release: v1.0

   Chunk creation time < 10 minutes for 10GB dataset

.. nfreq:: Memory Footprint
   :id: NFR-TRANSFER-002
   :status: approved
   :tags: transfer, performance, memory
   :priority: must
   :release: v1.0

   Memory footprint < 100 MB during streaming operations

Reliability
~~~~~~~~~~~

.. nfreq:: Checksum Verification Reliability
   :id: NFR-TRANSFER-007
   :status: approved
   :tags: transfer, reliability, integrity
   :priority: must
   :release: v1.0

   The system SHALL verify all chunks using the hash algorithm specified in the manifest before reconstruction

.. nfreq:: Idempotent Operations
   :id: NFR-TRANSFER-008
   :status: approved
   :tags: transfer, reliability
   :priority: must
   :release: v1.0

   Pack and unpack operations SHALL be idempotent (safe to run multiple times)

.. nfreq:: Graceful Interruption Handling
   :id: NFR-TRANSFER-009
   :status: approved
   :tags: transfer, reliability, error-handling
   :priority: must
   :release: v1.0

   The system SHALL handle interruptions gracefully (Ctrl+C, system shutdown) and allow resume

.. nfreq:: Data Corruption Detection
   :id: NFR-TRANSFER-010
   :status: approved
   :tags: transfer, reliability, integrity
   :priority: must
   :release: v1.0

   The system SHALL detect and report data corruption via checksum mismatch

Usability
~~~~~~~~~

.. nfreq:: Clear Progress Indicators
   :id: NFR-TRANSFER-011
   :status: approved
   :tags: transfer, usability, ui
   :priority: must
   :release: v1.0

   Progress indicators SHALL be shown for all operations taking longer than 2 seconds

.. nfreq:: Detailed Error Messages
   :id: NFR-TRANSFER-012
   :status: approved
   :tags: transfer, usability, error-handling
   :priority: must
   :release: v1.0

   Error messages SHALL include specific details about the failure and suggested fixes

.. nfreq:: Command Help Text
   :id: NFR-TRANSFER-013
   :status: approved
   :tags: transfer, usability, cli
   :priority: must
   :release: v1.0

   The CLI SHALL provide help text accessible via --help for all commands

.. nfreq:: First-Time User Experience
   :id: NFR-TRANSFER-014
   :status: approved
   :tags: transfer, usability
   :priority: should
   :release: v1.0

   First-time users SHALL be able to transfer a file within 5 minutes using provided examples

Maintainability
~~~~~~~~~~~~~~~

.. nfreq:: Test Coverage
   :id: NFR-TRANSFER-015
   :status: approved
   :tags: transfer, maintainability, testing
   :priority: must
   :release: v1.0

   The codebase SHALL achieve at least 80% test coverage

.. nfreq:: API Documentation
   :id: NFR-TRANSFER-016
   :status: approved
   :tags: transfer, maintainability, documentation
   :priority: must
   :release: v1.0

   All public APIs SHALL have rustdoc documentation

.. nfreq:: Clippy Compliance
   :id: NFR-TRANSFER-017
   :status: approved
   :tags: transfer, maintainability, code-quality
   :priority: must
   :release: v1.0

   The code SHALL pass cargo clippy with zero warnings

.. nfreq:: Code Formatting
   :id: NFR-TRANSFER-018
   :status: approved
   :tags: transfer, maintainability, code-quality
   :priority: must
   :release: v1.0

   The code SHALL be formatted with rustfmt

Portability
~~~~~~~~~~~

.. nfreq:: Cross-Platform Support
   :id: NFR-TRANSFER-006
   :status: approved
   :tags: transfer, portability
   :priority: must
   :release: v1.0

   Support macOS, Windows, Linux

Scalability
~~~~~~~~~~~

.. nfreq:: Large File Support
   :id: NFR-TRANSFER-019
   :status: approved
   :tags: transfer, scalability
   :priority: should
   :release: v1.0

   The system SHALL handle files up to 100GB in size

.. nfreq:: Streaming Architecture
   :id: NFR-TRANSFER-020
   :status: approved
   :tags: transfer, scalability, performance
   :priority: must
   :release: v1.0

   Chunk operations SHALL use streaming architecture to handle files larger than available RAM

.. nfreq:: Concurrent Chunk Processing
   :id: NFR-TRANSFER-021
   :status: approved
   :tags: transfer, scalability, performance
   :priority: could
   :release: v1.0

   The system SHOULD support concurrent chunk verification to improve performance

Security & Privacy
~~~~~~~~~~~~~~~~~~

.. nfreq:: Privacy Guarantee
   :id: NFR-TRANSFER-003
   :status: approved
   :tags: transfer, privacy, security
   :priority: must
   :release: v1.0

   All data stays on local/removable media; no network calls

.. nfreq:: Cryptographic Agility
   :id: NFR-TRANSFER-022
   :status: approved
   :tags: transfer, security, crypto-agility
   :priority: must
   :release: v1.0

   The system SHALL be designed for cryptographic agility: hash algorithms are pluggable via a common trait interface, enabling adoption of new standards (e.g., post-quantum algorithms) without architectural changes.

Deployment
~~~~~~~~~~

.. nfreq:: Offline Functionality
   :id: NFR-TRANSFER-004
   :status: approved
   :tags: transfer, offline
   :priority: must
   :release: v1.0

   100% functional offline

.. nfreq:: Air-Gap Deployment
   :id: NFR-TRANSFER-005
   :status: approved
   :tags: transfer, deployment, offline
   :priority: must
   :release: v1.0

   Build and run on systems with no internet access

v1.1 — SBOM-Aware Transfer Manifests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following requirements are planned for v1.1 and are not in scope for the MVP release.

.. req:: Reference SBOM in Transfer Manifest
   :id: FR-TRANSFER-048
   :status: proposed
   :tags: transfer, v1.1, sbom
   :priority: could
   :release: v1.1

   When a CycloneDX SBOM file (``sbom.cdx.json``) is present among the files being transferred, the transfer manifest SHALL include an ``sbom`` field referencing the SBOM filename.

.. req:: Log SBOM in Transfer Audit Trail
   :id: FR-TRANSFER-049
   :status: proposed
   :tags: transfer, v1.1, sbom, audit
   :priority: could
   :release: v1.1

   The system SHALL log the presence and filename of any SBOM file in the transfer audit trail, providing chain-of-custody documentation for compliance purposes.

.. _error-handling-1:

Error Handling
-----------------

+-----------------------------------+--------------------------------------------------------+
| Scenario                          | Behavior                                               |
+===================================+========================================================+
| Insufficient USB capacity         | Warn user, suggest smaller chunk size or larger USB    |
+-----------------------------------+--------------------------------------------------------+
| Missing chunks during unpack      | List missing chunks, abort with clear error            |
+-----------------------------------+--------------------------------------------------------+
| Checksum mismatch                 | Identify corrupted chunk, abort with error             |
+-----------------------------------+--------------------------------------------------------+
| Disk full during pack             | Stop operation, clean up partial chunk                 |
+-----------------------------------+--------------------------------------------------------+
| Permission denied                 | Clear error message with required permissions          |
+-----------------------------------+--------------------------------------------------------+
| USB disconnected during operation | Detect failure, allow resume from last completed chunk |
+-----------------------------------+--------------------------------------------------------+

Appendix: Chunk Format Specification
------------------------------------

Manifest Structure
~~~~~~~~~~~~~~~~~~

.. code:: json

   {
     "version": "1.0",
     "operation": "pack",
     "source_path": "/path/to/source",
     "total_size_bytes": 10737418240,
     "chunk_size_bytes": 1073741824,
     "chunk_count": 10,
     "hash_algorithm": "sha256",
     "chunks": [
       {
         "index": 0,
         "filename": "chunk_000.tar",
         "size_bytes": 1073741824,
         "checksum": "sha256:abc123...",
         "status": "completed"
       }
     ],
     "created_utc": "2026-01-04T12:00:00Z",
     "last_updated_utc": "2026-01-04T12:15:00Z"
   }

The ``hash_algorithm`` field identifies which algorithm was used. The checksum value prefix (e.g., ``sha256:``) is redundant but kept for readability when inspecting manifests manually.

Chunk Naming Convention
~~~~~~~~~~~~~~~~~~~~~~~

- Format: ``chunk_XXX.tar`` where XXX is zero-padded chunk index
- Manifest: ``airgap-transfer-manifest.json``


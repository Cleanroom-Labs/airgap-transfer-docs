Requirements
============

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

Assumptions and Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**User assumptions:**

- Operators have basic command-line literacy and can navigate filesystems.
- Operators understand the air-gap transfer workflow: pack on the source machine,
  physically move USB media, unpack on the destination machine.
- Operators have write access to both the source directory and the USB media.

**System assumptions:**

- At least one USB drive or removable storage device is available and mounted at
  a standard OS mount point (``/Volumes/*`` on macOS, ``/media/$USER/*`` or
  ``/mnt/*`` on Linux, drive letters on Windows).
- The filesystem on the destination media supports files up to the configured
  chunk size (e.g., FAT32 has a 4 GB limit).
- Power remains stable during write operations. Interrupted writes are handled
  via the resume mechanism, but data written during a power loss may be corrupt.

**Build dependencies:**

- Rust toolchain (stable channel) for compilation.
- ``cargo vendor`` for offline/air-gap builds when crates.io is not reachable.
- Python 3.10+ and Sphinx for documentation builds.

**Runtime dependencies:**

- No network access required or expected. The binary is fully self-contained.
- No external libraries at runtime — statically linked Rust binary.

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
   :links: DC-TRANSFER-CHUNK-NAMING-001
   :verified_by: TC-PCK-001; TC-PCK-002
   :realized_by: IMPL-CHUNKER-001

   Split source files/directories into fixed-size chunks.
   See :need:`DC-TRANSFER-CHUNK-NAMING-001` for chunk naming conventions.

.. needflow::
   :filter: id == 'FR-TRANSFER-001' or 'FR-TRANSFER-001' in links or 'FR-TRANSFER-001' in links_back or 'FR-TRANSFER-001' in specifies or 'FR-TRANSFER-001' in verified_by_back or 'FR-TRANSFER-001' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Auto-Detect USB Capacity
   :id: FR-TRANSFER-002
   :status: approved
   :tags: transfer, pack, usb, interface:usb
   :priority: must
   :release: v1.0
   :verified_by: TC-PCK-003
   :realized_by: IMPL-USB-001

   Auto-detect USB capacity and set chunk size accordingly

.. needflow::
   :filter: id == 'FR-TRANSFER-002' or 'FR-TRANSFER-002' in links or 'FR-TRANSFER-002' in links_back or 'FR-TRANSFER-002' in specifies or 'FR-TRANSFER-002' in verified_by_back or 'FR-TRANSFER-002' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Generate Chunk Checksums
   :id: FR-TRANSFER-003
   :status: approved
   :tags: transfer, pack, checksum, security
   :priority: must
   :release: v1.0
   :verified_by: TC-PCK-004
   :realized_by: IMPL-VERIFIER-001

   Generate checksums for each chunk using the configured hash algorithm (default: SHA-256)

.. needflow::
   :filter: id == 'FR-TRANSFER-003' or 'FR-TRANSFER-003' in links or 'FR-TRANSFER-003' in links_back or 'FR-TRANSFER-003' in specifies or 'FR-TRANSFER-003' in verified_by_back or 'FR-TRANSFER-003' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Create Manifest File
   :id: FR-TRANSFER-004
   :status: approved
   :tags: transfer, pack, manifest
   :priority: must
   :release: v1.0
   :links: DC-TRANSFER-MANIFEST-001
   :verified_by: TC-PCK-005
   :realized_by: IMPL-MANIFEST-001

   Create manifest file with chunk metadata and checksums.
   See :need:`DC-TRANSFER-MANIFEST-001` for the manifest schema.

.. needflow::
   :filter: id == 'FR-TRANSFER-004' or 'FR-TRANSFER-004' in links or 'FR-TRANSFER-004' in links_back or 'FR-TRANSFER-004' in specifies or 'FR-TRANSFER-004' in verified_by_back or 'FR-TRANSFER-004' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Stream Data to USB
   :id: FR-TRANSFER-005
   :status: approved
   :tags: transfer, pack, streaming, performance
   :priority: must
   :release: v1.0
   :verified_by: TC-PCK-006
   :realized_by: IMPL-CHUNKER-002

   Stream data directly to USB without intermediate temp files

.. needflow::
   :filter: id == 'FR-TRANSFER-005' or 'FR-TRANSFER-005' in links or 'FR-TRANSFER-005' in links_back or 'FR-TRANSFER-005' in specifies or 'FR-TRANSFER-005' in verified_by_back or 'FR-TRANSFER-005' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Manual Chunk Size Specification
   :id: FR-TRANSFER-006
   :status: approved
   :tags: transfer, pack, configuration
   :priority: should
   :release: v1.0
   :verified_by: TC-PCK-007
   :realized_by: IMPL-PACK-002

   Support manual chunk size specification

.. needflow::
   :filter: id == 'FR-TRANSFER-006' or 'FR-TRANSFER-006' in links or 'FR-TRANSFER-006' in links_back or 'FR-TRANSFER-006' in specifies or 'FR-TRANSFER-006' in verified_by_back or 'FR-TRANSFER-006' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Show Pack Progress
   :id: FR-TRANSFER-007
   :status: approved
   :tags: transfer, pack, ui, progress, interface:cli
   :priority: should
   :release: v1.0
   :verified_by: TC-PCK-008
   :realized_by: IMPL-PACK-003

   Show progress during chunk creation

.. needflow::
   :filter: id == 'FR-TRANSFER-007' or 'FR-TRANSFER-007' in links or 'FR-TRANSFER-007' in links_back or 'FR-TRANSFER-007' in specifies or 'FR-TRANSFER-007' in verified_by_back or 'FR-TRANSFER-007' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Prompt for USB Swapping
   :id: FR-TRANSFER-008
   :status: approved
   :tags: transfer, pack, usb, ui, interface:usb
   :priority: should
   :release: v1.0
   :verified_by: TC-PCK-009
   :realized_by: IMPL-PACK-004

   Prompt for USB swapping when multiple chunks needed

.. needflow::
   :filter: id == 'FR-TRANSFER-008' or 'FR-TRANSFER-008' in links or 'FR-TRANSFER-008' in links_back or 'FR-TRANSFER-008' in specifies or 'FR-TRANSFER-008' in verified_by_back or 'FR-TRANSFER-008' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


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
   :verified_by: TC-UNP-001
   :realized_by: IMPL-CHUNKER-003

   Reconstruct original files from chunks

.. needflow::
   :filter: id == 'FR-TRANSFER-009' or 'FR-TRANSFER-009' in links or 'FR-TRANSFER-009' in links_back or 'FR-TRANSFER-009' in specifies or 'FR-TRANSFER-009' in verified_by_back or 'FR-TRANSFER-009' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Verify Chunk Checksums Before Unpack
   :id: FR-TRANSFER-010
   :status: approved
   :tags: transfer, unpack, verification, security
   :priority: must
   :release: v1.0
   :verified_by: TC-UNP-002
   :realized_by: IMPL-VERIFIER-002

   Verify chunk checksums before reconstruction

.. needflow::
   :filter: id == 'FR-TRANSFER-010' or 'FR-TRANSFER-010' in links or 'FR-TRANSFER-010' in links_back or 'FR-TRANSFER-010' in specifies or 'FR-TRANSFER-010' in verified_by_back or 'FR-TRANSFER-010' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Place Files in Destination
   :id: FR-TRANSFER-011
   :status: approved
   :tags: transfer, unpack, filesystem
   :priority: must
   :release: v1.0
   :verified_by: TC-UNP-003
   :realized_by: IMPL-CHUNKER-004

   Place reconstructed files in specified destination

.. needflow::
   :filter: id == 'FR-TRANSFER-011' or 'FR-TRANSFER-011' in links or 'FR-TRANSFER-011' in links_back or 'FR-TRANSFER-011' in specifies or 'FR-TRANSFER-011' in verified_by_back or 'FR-TRANSFER-011' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Validate Chunk Completeness
   :id: FR-TRANSFER-012
   :status: approved
   :tags: transfer, unpack, validation
   :priority: must
   :release: v1.0
   :verified_by: TC-UNP-004
   :realized_by: IMPL-UNPACK-002

   Validate chunk completeness (all chunks present)

.. needflow::
   :filter: id == 'FR-TRANSFER-012' or 'FR-TRANSFER-012' in links or 'FR-TRANSFER-012' in links_back or 'FR-TRANSFER-012' in specifies or 'FR-TRANSFER-012' in verified_by_back or 'FR-TRANSFER-012' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Resume Partial Unpacks
   :id: FR-TRANSFER-013
   :status: approved
   :tags: transfer, unpack, resume, reliability
   :priority: should
   :release: v1.0
   :verified_by: TC-UNP-005
   :realized_by: IMPL-UNPACK-003

   Resume partial unpacks if interrupted

.. needflow::
   :filter: id == 'FR-TRANSFER-013' or 'FR-TRANSFER-013' in links or 'FR-TRANSFER-013' in links_back or 'FR-TRANSFER-013' in specifies or 'FR-TRANSFER-013' in verified_by_back or 'FR-TRANSFER-013' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Delete Chunks After Unpack
   :id: FR-TRANSFER-014
   :status: approved
   :tags: transfer, unpack, cleanup
   :priority: should
   :release: v1.0
   :verified_by: TC-UNP-006
   :realized_by: IMPL-UNPACK-004

   Optionally delete chunks after successful reconstruction

.. needflow::
   :filter: id == 'FR-TRANSFER-014' or 'FR-TRANSFER-014' in links or 'FR-TRANSFER-014' in links_back or 'FR-TRANSFER-014' in specifies or 'FR-TRANSFER-014' in verified_by_back or 'FR-TRANSFER-014' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Show Unpack Progress
   :id: FR-TRANSFER-015
   :status: approved
   :tags: transfer, unpack, ui, progress, interface:cli
   :priority: should
   :release: v1.0
   :verified_by: TC-UNP-007
   :realized_by: IMPL-UNPACK-005

   Show progress during reconstruction

.. needflow::
   :filter: id == 'FR-TRANSFER-015' or 'FR-TRANSFER-015' in links or 'FR-TRANSFER-015' in links_back or 'FR-TRANSFER-015' in specifies or 'FR-TRANSFER-015' in verified_by_back or 'FR-TRANSFER-015' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


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
   :verified_by: TC-LST-001
   :realized_by: IMPL-LIST-002

   Display chunk inventory from manifest

.. needflow::
   :filter: id == 'FR-TRANSFER-016' or 'FR-TRANSFER-016' in links or 'FR-TRANSFER-016' in links_back or 'FR-TRANSFER-016' in specifies or 'FR-TRANSFER-016' in verified_by_back or 'FR-TRANSFER-016' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Show Chunk Sizes and Manifest Status
   :id: FR-TRANSFER-017
   :status: approved
   :tags: transfer, list, verification
   :priority: must
   :release: v1.0
   :verified_by: TC-LST-002
   :realized_by: IMPL-LIST-003

   Display each chunk's size and manifest status (pending, in_progress, completed, or failed) as recorded in the manifest. This does not perform live checksum verification.

.. needflow::
   :filter: id == 'FR-TRANSFER-017' or 'FR-TRANSFER-017' in links or 'FR-TRANSFER-017' in links_back or 'FR-TRANSFER-017' in specifies or 'FR-TRANSFER-017' in verified_by_back or 'FR-TRANSFER-017' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Identify Missing Chunks
   :id: FR-TRANSFER-018
   :status: approved
   :tags: transfer, list, validation
   :priority: should
   :release: v1.0
   :verified_by: TC-LST-003
   :realized_by: IMPL-LIST-004

   Check file presence for each chunk listed in the manifest and flag missing files. Corruption detection requires ``--verify`` (FR-TRANSFER-057).

.. needflow::
   :filter: id == 'FR-TRANSFER-018' or 'FR-TRANSFER-018' in links or 'FR-TRANSFER-018' in links_back or 'FR-TRANSFER-018' in specifies or 'FR-TRANSFER-018' in verified_by_back or 'FR-TRANSFER-018' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Display Estimated Total Size
   :id: FR-TRANSFER-019
   :status: approved
   :tags: transfer, list, ui
   :priority: should
   :release: v1.0
   :verified_by: TC-LST-004
   :realized_by: IMPL-LIST-005

   Display estimated total size after reconstruction

.. needflow::
   :filter: id == 'FR-TRANSFER-019' or 'FR-TRANSFER-019' in links or 'FR-TRANSFER-019' in links_back or 'FR-TRANSFER-019' in specifies or 'FR-TRANSFER-019' in verified_by_back or 'FR-TRANSFER-019' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: List Verify Flag
   :id: FR-TRANSFER-057
   :status: approved
   :tags: transfer, list, validation, verification
   :priority: should
   :release: v1.0
   :verified_by: TC-LST-005
   :realized_by: IMPL-LIST-006

   ``--verify`` flag on the list command SHALL compute checksums for present chunks and compare against manifest values, reporting mismatches as corrupted.

.. needflow::
   :filter: id == 'FR-TRANSFER-057' or 'FR-TRANSFER-057' in links or 'FR-TRANSFER-057' in links_back or 'FR-TRANSFER-057' in specifies or 'FR-TRANSFER-057' in verified_by_back or 'FR-TRANSFER-057' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


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
   :verified_by: TC-INT-001
   :realized_by: IMPL-VERIFIER-001

   Generate checksums during pack using the configured hash algorithm (default: SHA-256)

.. needflow::
   :filter: id == 'FR-TRANSFER-020' or 'FR-TRANSFER-020' in links or 'FR-TRANSFER-020' in links_back or 'FR-TRANSFER-020' in specifies or 'FR-TRANSFER-020' in verified_by_back or 'FR-TRANSFER-020' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Verify Checksums During Unpack
   :id: FR-TRANSFER-021
   :status: approved
   :tags: transfer, verification, checksum, security
   :priority: must
   :release: v1.0
   :verified_by: TC-INT-002
   :realized_by: IMPL-VERIFIER-002

   Verify checksums during unpack

.. needflow::
   :filter: id == 'FR-TRANSFER-021' or 'FR-TRANSFER-021' in links or 'FR-TRANSFER-021' in links_back or 'FR-TRANSFER-021' in specifies or 'FR-TRANSFER-021' in verified_by_back or 'FR-TRANSFER-021' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Detect Corrupted Chunks
   :id: FR-TRANSFER-022
   :status: approved
   :tags: transfer, verification, error-handling
   :priority: must
   :release: v1.0
   :verified_by: TC-INT-003
   :realized_by: IMPL-VERIFIER-003

   Detect corrupted chunks and report errors

.. needflow::
   :filter: id == 'FR-TRANSFER-022' or 'FR-TRANSFER-022' in links or 'FR-TRANSFER-022' in links_back or 'FR-TRANSFER-022' in specifies or 'FR-TRANSFER-022' in verified_by_back or 'FR-TRANSFER-022' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Verify Final File Checksum
   :id: FR-TRANSFER-023
   :status: approved
   :tags: transfer, verification, checksum, security
   :priority: should
   :release: v1.0
   :verified_by: TC-INT-004
   :realized_by: IMPL-VERIFY-FINAL

   Verify final reconstructed file against original checksum

.. needflow::
   :filter: id == 'FR-TRANSFER-023' or 'FR-TRANSFER-023' in links or 'FR-TRANSFER-023' in links_back or 'FR-TRANSFER-023' in specifies or 'FR-TRANSFER-023' in verified_by_back or 'FR-TRANSFER-023' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


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
   :verified_by: TC-CRA-001; TC-CRA-002; TC-CRA-006
   :realized_by: IMPL-VERIFIER-004

   The system SHALL allow users to select a hash algorithm via CLI flag (``--hash-algorithm``). Default: SHA-256.

.. needflow::
   :filter: id == 'FR-TRANSFER-045' or 'FR-TRANSFER-045' in links or 'FR-TRANSFER-045' in links_back or 'FR-TRANSFER-045' in specifies or 'FR-TRANSFER-045' in verified_by_back or 'FR-TRANSFER-045' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Algorithm Identified in Manifest
   :id: FR-TRANSFER-046
   :status: approved
   :tags: transfer, crypto-agility, manifest, security
   :priority: must
   :release: v1.0
   :verified_by: TC-CRA-003; TC-CRA-004
   :realized_by: IMPL-MANIFEST-003

   The manifest SHALL record which hash algorithm was used, so unpack can verify with the correct algorithm.

.. needflow::
   :filter: id == 'FR-TRANSFER-046' or 'FR-TRANSFER-046' in links or 'FR-TRANSFER-046' in links_back or 'FR-TRANSFER-046' in specifies or 'FR-TRANSFER-046' in verified_by_back or 'FR-TRANSFER-046' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Pluggable Hash Backend
   :id: FR-TRANSFER-047
   :status: approved
   :tags: transfer, crypto-agility, security
   :priority: must
   :release: v1.0
   :verified_by: TC-CRA-005
   :realized_by: IMPL-VERIFIER-005

   The hash module SHALL use a trait-based interface so new algorithms can be added without modifying existing code.

.. needflow::
   :filter: id == 'FR-TRANSFER-047' or 'FR-TRANSFER-047' in links or 'FR-TRANSFER-047' in links_back or 'FR-TRANSFER-047' in specifies or 'FR-TRANSFER-047' in verified_by_back or 'FR-TRANSFER-047' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


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
   :verified_by: TC-STA-001
   :realized_by: IMPL-MANIFEST-002

   Maintain operation state in manifest file

.. needflow::
   :filter: id == 'FR-TRANSFER-024' or 'FR-TRANSFER-024' in links or 'FR-TRANSFER-024' in links_back or 'FR-TRANSFER-024' in specifies or 'FR-TRANSFER-024' in verified_by_back or 'FR-TRANSFER-024' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Track Chunk Completion
   :id: FR-TRANSFER-025
   :status: approved
   :tags: transfer, state, tracking
   :priority: must
   :release: v1.0
   :verified_by: TC-STA-002
   :realized_by: IMPL-MANIFEST-002

   Track chunk completion status

.. needflow::
   :filter: id == 'FR-TRANSFER-025' or 'FR-TRANSFER-025' in links or 'FR-TRANSFER-025' in links_back or 'FR-TRANSFER-025' in specifies or 'FR-TRANSFER-025' in verified_by_back or 'FR-TRANSFER-025' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Resume Interrupted Pack
   :id: FR-TRANSFER-026
   :status: approved
   :tags: transfer, state, resume, pack
   :priority: should
   :release: v1.0
   :verified_by: TC-STA-003
   :realized_by: IMPL-CHUNKER-005; IMPL-RESUME-001

   Support resume for interrupted pack operations

.. needflow::
   :filter: id == 'FR-TRANSFER-026' or 'FR-TRANSFER-026' in links or 'FR-TRANSFER-026' in links_back or 'FR-TRANSFER-026' in specifies or 'FR-TRANSFER-026' in verified_by_back or 'FR-TRANSFER-026' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Resume Interrupted Unpack
   :id: FR-TRANSFER-027
   :status: approved
   :tags: transfer, state, resume, unpack
   :priority: should
   :release: v1.0
   :verified_by: TC-STA-004
   :realized_by: IMPL-RESUME-002

   Support resume for interrupted unpack operations

.. needflow::
   :filter: id == 'FR-TRANSFER-027' or 'FR-TRANSFER-027' in links or 'FR-TRANSFER-027' in links_back or 'FR-TRANSFER-027' in specifies or 'FR-TRANSFER-027' in verified_by_back or 'FR-TRANSFER-027' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


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
   :tags: transfer, cli, pack, interface:cli
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-CLI-001
   :realized_by: IMPL-CLI-001; IMPL-PACK-001

   ``airgap-transfer pack <source> <dest>`` command

.. needflow::
   :filter: id == 'FR-TRANSFER-028' or 'FR-TRANSFER-028' in links or 'FR-TRANSFER-028' in links_back or 'FR-TRANSFER-028' in specifies or 'FR-TRANSFER-028' in verified_by_back or 'FR-TRANSFER-028' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Unpack Command
   :id: FR-TRANSFER-029
   :status: approved
   :tags: transfer, cli, unpack, interface:cli
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-CLI-002
   :realized_by: IMPL-UNPACK-001

   ``airgap-transfer unpack <source> <dest>`` command. The ``<source>`` argument is a single directory path containing chunk files and the manifest. When chunks span multiple USB drives, the user connects drives sequentially and the tool prompts for swaps.

.. needflow::
   :filter: id == 'FR-TRANSFER-029' or 'FR-TRANSFER-029' in links or 'FR-TRANSFER-029' in links_back or 'FR-TRANSFER-029' in specifies or 'FR-TRANSFER-029' in verified_by_back or 'FR-TRANSFER-029' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: List Command
   :id: FR-TRANSFER-030
   :status: approved
   :tags: transfer, cli, list, interface:cli
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-CLI-003
   :realized_by: IMPL-LIST-001

   ``airgap-transfer list <chunk-location>`` command

.. needflow::
   :filter: id == 'FR-TRANSFER-030' or 'FR-TRANSFER-030' in links or 'FR-TRANSFER-030' in links_back or 'FR-TRANSFER-030' in specifies or 'FR-TRANSFER-030' in verified_by_back or 'FR-TRANSFER-030' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Dry Run Flag
   :id: FR-TRANSFER-031
   :status: approved
   :tags: transfer, cli, dry-run, interface:cli
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-CLI-004
   :realized_by: IMPL-CLI-002

   ``--dry-run`` flag for all operations

.. needflow::
   :filter: id == 'FR-TRANSFER-031' or 'FR-TRANSFER-031' in links or 'FR-TRANSFER-031' in links_back or 'FR-TRANSFER-031' in specifies or 'FR-TRANSFER-031' in verified_by_back or 'FR-TRANSFER-031' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: No-Verify Flag
   :id: FR-TRANSFER-032
   :status: approved
   :tags: transfer, cli, verification, interface:cli
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-CLI-005
   :realized_by: IMPL-CLI-003

   Checksum verification SHALL be enabled by default for all operations. The ``--no-verify`` flag SHALL disable verification. This ensures integrity checking is the default behavior per FR-TRANSFER-010.

.. needflow::
   :filter: id == 'FR-TRANSFER-032' or 'FR-TRANSFER-032' in links or 'FR-TRANSFER-032' in links_back or 'FR-TRANSFER-032' in specifies or 'FR-TRANSFER-032' in verified_by_back or 'FR-TRANSFER-032' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Chunk Size Flag
   :id: FR-TRANSFER-033
   :status: approved
   :tags: transfer, cli, configuration, interface:cli
   :priority: should
   :release: v1.0
   :verified_by: TC-TRANSFER-CLI-006
   :realized_by: IMPL-CLI-004

   ``--chunk-size`` flag for manual chunk size specification

.. needflow::
   :filter: id == 'FR-TRANSFER-033' or 'FR-TRANSFER-033' in links or 'FR-TRANSFER-033' in links_back or 'FR-TRANSFER-033' in specifies or 'FR-TRANSFER-033' in verified_by_back or 'FR-TRANSFER-033' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Verbose Flag
   :id: FR-TRANSFER-034
   :status: approved
   :tags: transfer, cli, logging, interface:cli
   :priority: should
   :release: v1.0
   :verified_by: TC-TRANSFER-CLI-007
   :realized_by: IMPL-CLI-005

   ``--verbose`` flag for detailed output

.. needflow::
   :filter: id == 'FR-TRANSFER-034' or 'FR-TRANSFER-034' in links or 'FR-TRANSFER-034' in links_back or 'FR-TRANSFER-034' in specifies or 'FR-TRANSFER-034' in verified_by_back or 'FR-TRANSFER-034' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Force Flag
   :id: FR-TRANSFER-056
   :status: approved
   :tags: transfer, cli, safety, interface:cli
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-CLI-008
   :realized_by: IMPL-CLI-006

   ``--force`` flag on pack and unpack commands to bypass overwrite protection (FR-TRANSFER-038).

.. needflow::
   :filter: id == 'FR-TRANSFER-056' or 'FR-TRANSFER-056' in links or 'FR-TRANSFER-056' in links_back or 'FR-TRANSFER-056' in specifies or 'FR-TRANSFER-056' in verified_by_back or 'FR-TRANSFER-056' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


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
   :tags: transfer, error-handling, usb, interface:usb
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-ERR-001
   :realized_by: IMPL-ERROR-001

   Detect and report insufficient USB capacity

.. needflow::
   :filter: id == 'FR-TRANSFER-035' or 'FR-TRANSFER-035' in links or 'FR-TRANSFER-035' in links_back or 'FR-TRANSFER-035' in specifies or 'FR-TRANSFER-035' in verified_by_back or 'FR-TRANSFER-035' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Handle Missing Chunks
   :id: FR-TRANSFER-036
   :status: approved
   :tags: transfer, error-handling, chunks
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-ERR-002
   :realized_by: IMPL-ERROR-002

   Handle missing chunks gracefully

.. needflow::
   :filter: id == 'FR-TRANSFER-036' or 'FR-TRANSFER-036' in links or 'FR-TRANSFER-036' in links_back or 'FR-TRANSFER-036' in specifies or 'FR-TRANSFER-036' in verified_by_back or 'FR-TRANSFER-036' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Clear Error Messages
   :id: FR-TRANSFER-037
   :status: approved
   :tags: transfer, error-handling, usability
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-ERR-003
   :realized_by: IMPL-ERROR-003

   Provide clear error messages with suggested actions

.. needflow::
   :filter: id == 'FR-TRANSFER-037' or 'FR-TRANSFER-037' in links or 'FR-TRANSFER-037' in links_back or 'FR-TRANSFER-037' in specifies or 'FR-TRANSFER-037' in verified_by_back or 'FR-TRANSFER-037' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


Safety Features
~~~~~~~~~~~~~~~

.. needtable::
   :types: req
   :filter: "transfer" in tags and "safety" in tags
   :columns: id,priority,content
   :colwidths: 20,20,60
   :style: table
   :sort: id

.. req:: Overwrite Protection
   :id: FR-TRANSFER-038
   :status: approved
   :tags: transfer, safety, filesystem
   :priority: must
   :release: v1.0
   :verified_by: TC-SAF-001; TC-SAF-005
   :realized_by: IMPL-PACK-005

   The system SHALL abort with an error when the destination contains existing data: for pack, an existing manifest file; for unpack, a non-empty destination directory. The error message SHALL suggest ``--force`` to bypass this check.

.. needflow::
   :filter: id == 'FR-TRANSFER-038' or 'FR-TRANSFER-038' in links or 'FR-TRANSFER-038' in links_back or 'FR-TRANSFER-038' in specifies or 'FR-TRANSFER-038' in verified_by_back or 'FR-TRANSFER-038' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Validate Destination Paths
   :id: FR-TRANSFER-039
   :status: approved
   :tags: transfer, safety, validation
   :priority: must
   :release: v1.0
   :verified_by: TC-SAF-002
   :realized_by: IMPL-SAFETY-001

   Validate destination paths and permissions

.. needflow::
   :filter: id == 'FR-TRANSFER-039' or 'FR-TRANSFER-039' in links or 'FR-TRANSFER-039' in links_back or 'FR-TRANSFER-039' in specifies or 'FR-TRANSFER-039' in verified_by_back or 'FR-TRANSFER-039' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Sync USB Safely
   :id: FR-TRANSFER-040
   :status: approved
   :tags: transfer, safety, usb, interface:usb
   :priority: must
   :release: v1.0
   :verified_by: TC-SAF-003
   :realized_by: IMPL-USB-002

   Safely sync USB before prompting for removal

.. needflow::
   :filter: id == 'FR-TRANSFER-040' or 'FR-TRANSFER-040' in links or 'FR-TRANSFER-040' in links_back or 'FR-TRANSFER-040' in specifies or 'FR-TRANSFER-040' in verified_by_back or 'FR-TRANSFER-040' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Atomic Operations
   :id: FR-TRANSFER-041
   :status: approved
   :tags: transfer, safety, reliability
   :priority: should
   :release: v1.0
   :verified_by: TC-SAF-004
   :realized_by: IMPL-SAFETY-002

   Atomic operations where possible

.. needflow::
   :filter: id == 'FR-TRANSFER-041' or 'FR-TRANSFER-041' in links or 'FR-TRANSFER-041' in links_back or 'FR-TRANSFER-041' in specifies or 'FR-TRANSFER-041' in verified_by_back or 'FR-TRANSFER-041' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


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
   :verified_by: TC-TRANSFER-DEP-001
   :realized_by: IMPL-BUILD-001

   All dependencies available for offline build

.. needflow::
   :filter: id == 'FR-TRANSFER-042' or 'FR-TRANSFER-042' in links or 'FR-TRANSFER-042' in links_back or 'FR-TRANSFER-042' in specifies or 'FR-TRANSFER-042' in verified_by_back or 'FR-TRANSFER-042' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Internet-Free Build
   :id: FR-TRANSFER-043
   :status: approved
   :tags: transfer, deployment, offline
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-DEP-002
   :realized_by: IMPL-BUILD-001

   Build process works without internet after initial setup

.. needflow::
   :filter: id == 'FR-TRANSFER-043' or 'FR-TRANSFER-043' in links or 'FR-TRANSFER-043' in links_back or 'FR-TRANSFER-043' in specifies or 'FR-TRANSFER-043' in verified_by_back or 'FR-TRANSFER-043' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. req:: Single, Static Binary Deployment
   :id: FR-TRANSFER-044
   :status: approved
   :tags: transfer, deployment
   :priority: should
   :release: v1.0
   :verified_by: TC-TRANSFER-DEP-003
   :realized_by: IMPL-BUILD-002

   Single, static binary deployment

.. needflow::
   :filter: id == 'FR-TRANSFER-044' or 'FR-TRANSFER-044' in links or 'FR-TRANSFER-044' in links_back or 'FR-TRANSFER-044' in specifies or 'FR-TRANSFER-044' in verified_by_back or 'FR-TRANSFER-044' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


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
   :verified_by: TC-TRANSFER-NFR-001

   Chunk creation time < 10 minutes for 10GB dataset

.. needflow::
   :filter: id == 'NFR-TRANSFER-001' or 'NFR-TRANSFER-001' in links or 'NFR-TRANSFER-001' in links_back or 'NFR-TRANSFER-001' in specifies or 'NFR-TRANSFER-001' in verified_by_back or 'NFR-TRANSFER-001' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. nfreq:: Memory Footprint
   :id: NFR-TRANSFER-002
   :status: approved
   :tags: transfer, performance, memory
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-002

   Memory footprint < 100 MB during streaming operations

.. needflow::
   :filter: id == 'NFR-TRANSFER-002' or 'NFR-TRANSFER-002' in links or 'NFR-TRANSFER-002' in links_back or 'NFR-TRANSFER-002' in specifies or 'NFR-TRANSFER-002' in verified_by_back or 'NFR-TRANSFER-002' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


Reliability
~~~~~~~~~~~

.. nfreq:: Checksum Verification Reliability
   :id: NFR-TRANSFER-007
   :status: approved
   :tags: transfer, reliability, integrity
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-007

   The system SHALL verify all chunks using the hash algorithm specified in the manifest before reconstruction

.. needflow::
   :filter: id == 'NFR-TRANSFER-007' or 'NFR-TRANSFER-007' in links or 'NFR-TRANSFER-007' in links_back or 'NFR-TRANSFER-007' in specifies or 'NFR-TRANSFER-007' in verified_by_back or 'NFR-TRANSFER-007' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. nfreq:: Idempotent Operations
   :id: NFR-TRANSFER-008
   :status: approved
   :tags: transfer, reliability
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-008

   Pack and unpack operations SHALL be idempotent (safe to run multiple times)

.. needflow::
   :filter: id == 'NFR-TRANSFER-008' or 'NFR-TRANSFER-008' in links or 'NFR-TRANSFER-008' in links_back or 'NFR-TRANSFER-008' in specifies or 'NFR-TRANSFER-008' in verified_by_back or 'NFR-TRANSFER-008' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. nfreq:: Graceful Interruption Handling
   :id: NFR-TRANSFER-009
   :status: approved
   :tags: transfer, reliability, error-handling
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-009

   The system SHALL handle interruptions gracefully (Ctrl+C, system shutdown) and allow resume

.. needflow::
   :filter: id == 'NFR-TRANSFER-009' or 'NFR-TRANSFER-009' in links or 'NFR-TRANSFER-009' in links_back or 'NFR-TRANSFER-009' in specifies or 'NFR-TRANSFER-009' in verified_by_back or 'NFR-TRANSFER-009' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. nfreq:: Data Corruption Detection
   :id: NFR-TRANSFER-010
   :status: approved
   :tags: transfer, reliability, integrity
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-010

   The system SHALL detect and report data corruption via checksum mismatch

.. needflow::
   :filter: id == 'NFR-TRANSFER-010' or 'NFR-TRANSFER-010' in links or 'NFR-TRANSFER-010' in links_back or 'NFR-TRANSFER-010' in specifies or 'NFR-TRANSFER-010' in verified_by_back or 'NFR-TRANSFER-010' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


Usability
~~~~~~~~~

.. nfreq:: Clear Progress Indicators
   :id: NFR-TRANSFER-011
   :status: approved
   :tags: transfer, usability, ui
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-011

   Progress indicators SHALL be shown for all operations taking longer than 2 seconds

.. needflow::
   :filter: id == 'NFR-TRANSFER-011' or 'NFR-TRANSFER-011' in links or 'NFR-TRANSFER-011' in links_back or 'NFR-TRANSFER-011' in specifies or 'NFR-TRANSFER-011' in verified_by_back or 'NFR-TRANSFER-011' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. nfreq:: Detailed Error Messages
   :id: NFR-TRANSFER-012
   :status: approved
   :tags: transfer, usability, error-handling
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-012

   Error messages SHALL include specific details about the failure and suggested fixes

.. needflow::
   :filter: id == 'NFR-TRANSFER-012' or 'NFR-TRANSFER-012' in links or 'NFR-TRANSFER-012' in links_back or 'NFR-TRANSFER-012' in specifies or 'NFR-TRANSFER-012' in verified_by_back or 'NFR-TRANSFER-012' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. nfreq:: Command Help Text
   :id: NFR-TRANSFER-013
   :status: approved
   :tags: transfer, usability, cli
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-013

   The CLI SHALL provide help text accessible via --help for all commands

.. needflow::
   :filter: id == 'NFR-TRANSFER-013' or 'NFR-TRANSFER-013' in links or 'NFR-TRANSFER-013' in links_back or 'NFR-TRANSFER-013' in specifies or 'NFR-TRANSFER-013' in verified_by_back or 'NFR-TRANSFER-013' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. nfreq:: First-Time User Experience
   :id: NFR-TRANSFER-014
   :status: approved
   :tags: transfer, usability
   :priority: should
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-014

   First-time users SHALL be able to transfer a file within 5 minutes using provided examples

.. needflow::
   :filter: id == 'NFR-TRANSFER-014' or 'NFR-TRANSFER-014' in links or 'NFR-TRANSFER-014' in links_back or 'NFR-TRANSFER-014' in specifies or 'NFR-TRANSFER-014' in verified_by_back or 'NFR-TRANSFER-014' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


Maintainability
~~~~~~~~~~~~~~~

.. nfreq:: Test Coverage
   :id: NFR-TRANSFER-015
   :status: approved
   :tags: transfer, maintainability, testing
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-015

   The codebase SHALL achieve at least 80% test coverage

.. needflow::
   :filter: id == 'NFR-TRANSFER-015' or 'NFR-TRANSFER-015' in links or 'NFR-TRANSFER-015' in links_back or 'NFR-TRANSFER-015' in specifies or 'NFR-TRANSFER-015' in verified_by_back or 'NFR-TRANSFER-015' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. nfreq:: API Documentation
   :id: NFR-TRANSFER-016
   :status: approved
   :tags: transfer, maintainability, documentation
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-016

   All public APIs SHALL have rustdoc documentation

.. needflow::
   :filter: id == 'NFR-TRANSFER-016' or 'NFR-TRANSFER-016' in links or 'NFR-TRANSFER-016' in links_back or 'NFR-TRANSFER-016' in specifies or 'NFR-TRANSFER-016' in verified_by_back or 'NFR-TRANSFER-016' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. nfreq:: Clippy Compliance
   :id: NFR-TRANSFER-017
   :status: approved
   :tags: transfer, maintainability, code-quality
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-017

   The code SHALL pass cargo clippy with zero warnings

.. needflow::
   :filter: id == 'NFR-TRANSFER-017' or 'NFR-TRANSFER-017' in links or 'NFR-TRANSFER-017' in links_back or 'NFR-TRANSFER-017' in specifies or 'NFR-TRANSFER-017' in verified_by_back or 'NFR-TRANSFER-017' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. nfreq:: Code Formatting
   :id: NFR-TRANSFER-018
   :status: approved
   :tags: transfer, maintainability, code-quality
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-018

   The code SHALL be formatted with rustfmt

.. needflow::
   :filter: id == 'NFR-TRANSFER-018' or 'NFR-TRANSFER-018' in links or 'NFR-TRANSFER-018' in links_back or 'NFR-TRANSFER-018' in specifies or 'NFR-TRANSFER-018' in verified_by_back or 'NFR-TRANSFER-018' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


Portability
~~~~~~~~~~~

.. nfreq:: Cross-Platform Support
   :id: NFR-TRANSFER-006
   :status: approved
   :tags: transfer, portability
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-004

   Support macOS, Windows, Linux

.. needflow::
   :filter: id == 'NFR-TRANSFER-006' or 'NFR-TRANSFER-006' in links or 'NFR-TRANSFER-006' in links_back or 'NFR-TRANSFER-006' in specifies or 'NFR-TRANSFER-006' in verified_by_back or 'NFR-TRANSFER-006' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


Scalability
~~~~~~~~~~~

.. nfreq:: Large File Support
   :id: NFR-TRANSFER-019
   :status: approved
   :tags: transfer, scalability
   :priority: should
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-019

   The system SHALL handle files up to 100GB in size

.. needflow::
   :filter: id == 'NFR-TRANSFER-019' or 'NFR-TRANSFER-019' in links or 'NFR-TRANSFER-019' in links_back or 'NFR-TRANSFER-019' in specifies or 'NFR-TRANSFER-019' in verified_by_back or 'NFR-TRANSFER-019' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. nfreq:: Streaming Architecture
   :id: NFR-TRANSFER-020
   :status: approved
   :tags: transfer, scalability, performance
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-020

   Chunk operations SHALL use streaming architecture to handle files larger than available RAM

.. needflow::
   :filter: id == 'NFR-TRANSFER-020' or 'NFR-TRANSFER-020' in links or 'NFR-TRANSFER-020' in links_back or 'NFR-TRANSFER-020' in specifies or 'NFR-TRANSFER-020' in verified_by_back or 'NFR-TRANSFER-020' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. nfreq:: Concurrent Chunk Processing
   :id: NFR-TRANSFER-021
   :status: approved
   :tags: transfer, scalability, performance
   :priority: could
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-021

   The system SHOULD support concurrent chunk verification to improve performance

.. needflow::
   :filter: id == 'NFR-TRANSFER-021' or 'NFR-TRANSFER-021' in links or 'NFR-TRANSFER-021' in links_back or 'NFR-TRANSFER-021' in specifies or 'NFR-TRANSFER-021' in verified_by_back or 'NFR-TRANSFER-021' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


Security & Privacy
~~~~~~~~~~~~~~~~~~

.. nfreq:: Privacy Guarantee
   :id: NFR-TRANSFER-003
   :status: approved
   :tags: transfer, privacy, security
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-005

   All data stays on local/removable media; no network calls

.. needflow::
   :filter: id == 'NFR-TRANSFER-003' or 'NFR-TRANSFER-003' in links or 'NFR-TRANSFER-003' in links_back or 'NFR-TRANSFER-003' in specifies or 'NFR-TRANSFER-003' in verified_by_back or 'NFR-TRANSFER-003' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. nfreq:: Cryptographic Agility
   :id: NFR-TRANSFER-022
   :status: approved
   :tags: transfer, security, crypto-agility
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-022

   The system SHALL be designed for cryptographic agility: hash algorithms are pluggable via a common trait interface, enabling adoption of new standards (e.g., post-quantum algorithms) without architectural changes.

.. needflow::
   :filter: id == 'NFR-TRANSFER-022' or 'NFR-TRANSFER-022' in links or 'NFR-TRANSFER-022' in links_back or 'NFR-TRANSFER-022' in specifies or 'NFR-TRANSFER-022' in verified_by_back or 'NFR-TRANSFER-022' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


Deployment
~~~~~~~~~~

.. nfreq:: Offline Functionality
   :id: NFR-TRANSFER-004
   :status: approved
   :tags: transfer, offline
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-003

   100% functional offline

.. needflow::
   :filter: id == 'NFR-TRANSFER-004' or 'NFR-TRANSFER-004' in links or 'NFR-TRANSFER-004' in links_back or 'NFR-TRANSFER-004' in specifies or 'NFR-TRANSFER-004' in verified_by_back or 'NFR-TRANSFER-004' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. nfreq:: Air-Gap Deployment
   :id: NFR-TRANSFER-005
   :status: approved
   :tags: transfer, deployment, offline
   :priority: must
   :release: v1.0
   :verified_by: TC-TRANSFER-NFR-006

   Build and run on systems with no internet access

.. needflow::
   :filter: id == 'NFR-TRANSFER-005' or 'NFR-TRANSFER-005' in links or 'NFR-TRANSFER-005' in links_back or 'NFR-TRANSFER-005' in specifies or 'NFR-TRANSFER-005' in verified_by_back or 'NFR-TRANSFER-005' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. _chunk-format-conventions:

Appendix: Design Conventions
-----------------------------

.. convention:: Transfer Manifest Schema
   :id: DC-TRANSFER-MANIFEST-001
   :status: approved
   :tags: transfer, manifest, format
   :release: v1.0

   The transfer manifest (``airgap-transfer-manifest.json``) is a JSON document
   with the following structure:

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

   The ``hash_algorithm`` field identifies which algorithm was used. The checksum
   value prefix (e.g., ``sha256:``) is redundant but kept for readability when
   inspecting manifests manually.

   **Rationale.** JSON was chosen because it is human-readable for debugging in
   air-gap environments where tooling may be limited, requires no additional
   parser dependency beyond ``serde_json`` (already in the dependency set), and
   can be inspected on any platform with a text editor. The ``status`` field per
   chunk enables resume after interruption without re-reading chunk contents.

.. needflow::
   :filter: id == 'DC-TRANSFER-MANIFEST-001' or 'DC-TRANSFER-MANIFEST-001' in links or 'DC-TRANSFER-MANIFEST-001' in links_back or 'DC-TRANSFER-MANIFEST-001' in specifies or 'DC-TRANSFER-MANIFEST-001' in verified_by_back or 'DC-TRANSFER-MANIFEST-001' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by


.. convention:: Chunk Naming Convention
   :id: DC-TRANSFER-CHUNK-NAMING-001
   :status: approved
   :tags: transfer, chunk, format
   :release: v1.0

   - Chunk files: ``chunk_XXX.tar`` where XXX is a zero-padded 3-digit index
   - Manifest: ``airgap-transfer-manifest.json``

   **Rationale.** Three-digit zero-padding supports up to 1000 chunks, which is
   sufficient for most transfers given configurable chunk sizes. The ``.tar``
   extension signals the archive format to operators inspecting USB contents. The
   ``chunk_`` prefix prevents namespace collisions with the manifest file and any
   other files that may be present on the destination media.

.. needflow::
   :filter: id == 'DC-TRANSFER-CHUNK-NAMING-001' or 'DC-TRANSFER-CHUNK-NAMING-001' in links or 'DC-TRANSFER-CHUNK-NAMING-001' in links_back or 'DC-TRANSFER-CHUNK-NAMING-001' in specifies or 'DC-TRANSFER-CHUNK-NAMING-001' in verified_by_back or 'DC-TRANSFER-CHUNK-NAMING-001' in realized_by_back
   :link_types: links, specifies, verified_by, realized_by



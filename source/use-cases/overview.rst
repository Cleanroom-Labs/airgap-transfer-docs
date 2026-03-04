Use Case Analysis
=================

Purpose
-------

This document provides an overview of primary use cases for AirGap Transfer, a tool for safely transferring large files and datasets across air-gap boundaries using removable media.

User Personas
-------------

IT Administrator
~~~~~~~~~~~~~~~~

- **Needs:** Move deployment packages and updates to air-gapped servers
- **Environment:** air-gapped data centers, secure facilities
- **Priority:** Reliability, verification, clear progress reporting

Data Scientist / Researcher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Needs:** Transfer large datasets (ML models, experiment data) to isolated compute
- **Environment:** Research lab with air-gapped GPU cluster
- **Priority:** Handle multi-GB files, resume interrupted transfers

Security Operations Staff
~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Needs:** Move patches, tools, and forensic data across security boundaries
- **Environment:** Government, military, or compliance-sensitive infrastructure
- **Priority:** Integrity verification, chain-of-custody support, audit trail

Field Technician
~~~~~~~~~~~~~~~~

- **Needs:** Deliver software updates to remote air-gapped installations
- **Environment:** Industrial control systems, remote sites with limited USB capacity
- **Priority:** Multi-USB coordination, simple CLI, error recovery

Workflow Use Cases
------------------

Happy-path scenarios covering the core pack → transfer → unpack workflow
across different data sizes and transfer configurations.

Large File Transfer
~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** Transfer a single large file (e.g., VM image, video file) that exceeds USB drive capacity.

.. raw:: html

   <div style="margin-top: 1.5em;"></div>

**Key Requirements:**

- Split file into chunks
- Verify integrity after reconstruction
- Resume if interrupted

:doc:`Use Case: Large File Transfer <use-case-large-file>`

Large Directory Transfer
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** Transfer a directory containing many files (e.g., dataset, codebase) across air-gap.

**Key Requirements:**

- Preserve directory structure
- Handle mixed file sizes efficiently
- Batch verification

:doc:`Use Case: Large Directory Transfer <use-case-large-directory>`

Multiple USB Workflow
~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** Transfer dataset larger than any single USB drive, requiring multiple USB drives.

**Key Requirements:**

- Coordinate multiple USBs
- Track which chunks are on which USB
- Resume with any available USB

:doc:`Use Case: Multi-USB Dataset Transfer <use-case-multiple-usb>`

SBOM Transfer *(v1.1)*
~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** Transfer a deployment package containing a CycloneDX SBOM, with automatic SBOM detection and audit trail logging.

**Key Requirements:**

- Detect SBOM in transfer manifest
- Log SBOM presence in audit trail
- Chain-of-custody documentation

:need:`UC-TRANSFER-004`

Diagnostic & Operational Use Cases
-----------------------------------

Scenarios focused on inspection, verification, and pre-transfer checks —
what operators do *before* committing to an unpack.

Verify Transfer Integrity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** Operator receives USB drives and inspects chunk inventory, checks checksums, and identifies missing or corrupted chunks before unpacking.

**Key Requirements:**

- Display chunk inventory and sizes
- Identify missing chunks
- Verify checksums against manifest

:doc:`Use Case: Verify Transfer Integrity <use-case-verify-integrity>`

Error Recovery & Safety Use Cases
----------------------------------

Scenarios covering what happens when things go wrong — interrupted
operations, insufficient space, accidental overwrites — and how the
tool helps operators recover safely.

Recover from Transfer Failure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** Pack or unpack is interrupted by insufficient USB space, power loss, or missing chunks. Operator uses resume to recover.

**Key Requirements:**

- Manifest-based state tracking
- Resume from last completed chunk
- Clear error messages with recovery hints

:doc:`Use Case: Recover from Transfer Failure <use-case-error-recovery>`

Protect Against Data Loss
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** Operator accidentally targets a directory with existing files. The tool's safety features prevent silent overwrites.

**Key Requirements:**

- Overwrite protection by default
- Explicit ``--force`` opt-in
- Safe USB synchronization before ejection

:doc:`Use Case: Protect Against Data Loss <use-case-data-protection>`

Common Requirements Across All Use Cases
----------------------------------------

+--------------------------------------+-----------------------------------------------+
| Requirement                          | Rationale                                     |
+======================================+===============================================+
| Checksum verification                | Ensure data integrity across air-gap boundary |
+--------------------------------------+-----------------------------------------------+
| Resume capability                    | Handle interruptions without data loss        |
+--------------------------------------+-----------------------------------------------+
| Progress reporting                   | User awareness during long operations         |
+--------------------------------------+-----------------------------------------------+
| Dry-run mode                         | Preview operations before execution           |
+--------------------------------------+-----------------------------------------------+
| Clear error messages                 | Guide user through recovery procedures        |
+--------------------------------------+-----------------------------------------------+

Integration with AirGap Deploy
------------------------------

AirGap Transfer is designed to integrate with the AirGap Deploy project for complete air-gap deployment workflows:

- **AirGap Deploy:** Orchestrates overall deployment process, prepares packages
- **AirGap Transfer:** Handles chunked data transfer when packages exceed USB capacity
- **Cleanroom Whisper:** Example application deployed using AirGap Deploy

**See:** `AirGap Deploy workflow examples <https://cleanroomlabs.dev/docs/deploy/use-cases/overview.html>`_

Out of Scope
------------

The following are explicitly NOT supported in MVP:

+----------------------------------+-------------------------------------------+
| Use Case                         | Why Not in MVP                            |
+==================================+===========================================+
| Real-time sync                   | Requires complexity beyond MVP scope      |
+----------------------------------+-------------------------------------------+
| Network transfer                 | Violates air-gap design principle         |
+----------------------------------+-------------------------------------------+
| Automatic USB hot-swap detection | Hardware-dependent, defer to post-MVP     |
+----------------------------------+-------------------------------------------+
| Compression during transfer      | Adds complexity, defer to post-MVP        |
+----------------------------------+-------------------------------------------+
| Encryption                       | Planned for v1.2 (AEAD + key derivation)  |
+----------------------------------+-------------------------------------------+

Success Metrics
---------------

============================ =======================================
Metric                       Target
============================ =======================================
Transfer accuracy            100% (verified by checksums)
Resume success rate          > 95% (interrupted transfers)
User errors                  < 5% (clear guidance prevents mistakes)
Cross-platform compatibility macOS, Windows, Linux
============================ =======================================


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
- **Environment:** Air-gapped data centers, secure facilities
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

Primary Use Cases
-----------------

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

**See:** :doc:`AirGap Deploy workflow examples <../../airgap-deploy/use-cases/overview>`

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
| Automatic USB detection/swapping | Hardware-dependent, defer to post-MVP     |
+----------------------------------+-------------------------------------------+
| Compression during transfer      | Adds complexity, defer to post-MVP        |
+----------------------------------+-------------------------------------------+
| Encryption                       | Adds key management complexity, defer     |
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

See Also
--------

- :doc:`Requirements (SRS) <../requirements/srs>` - Detailed functional requirements
- :doc:`Design (SDD) <../design/sdd>` - Architecture and implementation
- :doc:`Test Plan <../testing/plan>` - Test cases and verification
- :doc:`Roadmap <../roadmap>` - Implementation roadmap
- :doc:`Principles </meta/principles>` - Design principles guiding all decisions

Use Case Analysis
=================

Purpose
-------

This document provides an overview of primary use cases for AirGap Transfer, a tool for safely transferring large files and datasets across air-gap boundaries using removable media.

--------------

Primary Use Cases
-----------------

Large File Transfer
~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** Transfer a single large file (e.g., VM image, video file) that exceeds USB drive capacity.

**Key Requirements:**

- Split file into chunks
- Verify integrity after reconstruction
- Resume if interrupted

:doc:`Workflow: Large File Transfer <workflow-large-file>`

--------------

Large Directory Transfer
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** Transfer a directory containing many files (e.g., dataset, codebase) across air-gap.

**Key Requirements:**

- Preserve directory structure
- Handle mixed file sizes efficiently
- Batch verification

:doc:`Workflow: Large Directory Transfer <workflow-large-directory>`

--------------

Multiple USB Workflow
~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** Transfer dataset larger than any single USB drive, requiring multiple USB drives.

**Key Requirements:**

- Coordinate multiple USBs
- Track which chunks are on which USB
- Resume with any available USB

:doc:`Workflow: Multi-USB Dataset Transfer <workflow-multiple-usb>`

--------------

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

--------------

Integration with AirGap Deploy
------------------------------

AirGap Transfer is designed to integrate with the AirGap Deploy project for complete air-gap deployment workflows:

- **AirGap Deploy:** Orchestrates overall deployment process, prepares packages
- **AirGap Transfer:** Handles chunked data transfer when packages exceed USB capacity
- **AirGap Whisper:** Example application deployed using AirGap Deploy

**See:** :doc:`AirGap Deploy workflow examples <../../airgap-deploy/use-cases/overview>`

--------------

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

--------------

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

--------------

See Also
--------

- :doc:`Requirements <../requirements/srs>`
- :doc:`Design <../design/sdd>`
- :doc:`Roadmap <../roadmap>`

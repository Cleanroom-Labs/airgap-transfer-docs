Use Case: Protect Against Data Loss
=====================================

Scenario
--------

An IT administrator accidentally targets a directory containing existing files during an unpack operation. The tool's safety features — overwrite protection, destination validation, and safe USB sync — prevent accidental data loss.

.. usecase:: Protect Against Data Loss
   :id: UC-TRANSFER-007
   :status: approved
   :tags: transfer, safety, error-handling
   :release: v1.0
   :specifies: FR-TRANSFER-038; FR-TRANSFER-039; FR-TRANSFER-040; FR-TRANSFER-041; FR-TRANSFER-056

   Prevent accidental data loss through overwrite protection, destination path validation, safe USB synchronization, and atomic write operations.

   **Default behavior:** Refuse to overwrite existing files or write to invalid destinations.

   **Explicit override:** The ``--force`` flag allows intentional overwrites when the operator understands the consequences.

   **Safe media handling:** USB writes are synced to ensure data is flushed to disk before ejection.

   **Acceptance Criteria:** No accidental data loss, clear warnings before destructive operations, safe USB handling.

--------------

Prerequisites
-------------

- **Transfer media:** USB drive(s) with a completed pack operation
- **Destination:** Target directory on the destination machine

--------------

Workflow Steps
--------------

Scenario A: Overwrite Protection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Attempt unpack to an existing directory**

.. code:: bash

   airgap-transfer unpack /media/usb-drive ~/existing-project/

::

   error: destination already contains files. Use --force to overwrite.

The tool refuses to write, protecting the existing data.

**2. Operator reviews and corrects**

The operator realizes they specified the wrong path:

.. code:: bash

   airgap-transfer unpack /media/usb-drive ~/restored-project/

Transfer proceeds to the correct (empty) directory.

**3. Or: intentional overwrite**

If the operator intentionally wants to replace outdated files:

.. code:: bash

   airgap-transfer unpack /media/usb-drive ~/existing-project/ --force

The tool overwrites existing files with the transferred data.

Scenario B: Pack to Occupied Destination
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Attempt pack to a directory with an existing manifest**

.. code:: bash

   airgap-transfer pack ~/data/ /media/usb-drive

::

   error: destination already contains a manifest. Use --force to overwrite or --resume to continue.

The tool detects a prior pack operation and stops. This prevents accidental overwrite of an in-progress transfer.

**2. Operator chooses action**

- ``--resume``: Continue the interrupted pack
- ``--force``: Discard prior state and start fresh
- Neither: Abort and investigate

Scenario C: Safe USB Ejection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Pack completes**

.. code:: bash

   airgap-transfer pack ~/data/ /media/usb-drive

After writing all chunks, the tool calls the platform's filesystem sync to flush all buffered writes to the USB drive.

::

   Syncing writes to /media/usb-drive...
   Pack complete. Safe to eject USB drive.

**2. Ejection without sync risks**

Without the sync step, ejecting a USB immediately after a write could result in corrupted chunk files (data still in the OS write cache). The tool's explicit sync eliminates this risk.

--------------

Acceptance Criteria
-------------------

- Existing files are never silently overwritten
- Clear error messages explain what would be overwritten and how to proceed
- ``--force`` is an explicit opt-in, not a default
- USB writes are flushed to disk before the tool reports completion
- Atomic operations prevent partial state on unexpected termination

--------------

Error Scenarios
---------------

============================= ================================ =================================
Error                         Cause                            Recovery
============================= ================================ =================================
"Destination contains files"  Existing data at target path     Choose different path or --force
"Manifest already exists"     Prior pack at same destination   Use --resume or --force
"Destination not writable"    Permissions issue                Fix permissions, retry
============================= ================================ =================================

--------------

Related Documents
-----------------

- :doc:`Error Recovery <use-case-error-recovery>` — Resume after failures
- :doc:`Large File Transfer <use-case-large-file>` — Standard transfer workflow

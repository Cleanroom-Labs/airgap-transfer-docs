Use Case: Recover from Transfer Failure
========================================

Scenario
--------

A field technician's pack operation is interrupted mid-way — the USB drive runs out of space, or the process is killed by a power loss. The tool's state management and resume capability allow the operator to recover without starting over.

.. usecase:: Recover from Transfer Failure
   :id: UC-TRANSFER-006
   :status: approved
   :tags: transfer, error-recovery, resume, state
   :release: v1.0
   :links: FR-TRANSFER-024; FR-TRANSFER-025; FR-TRANSFER-027; FR-TRANSFER-035; FR-TRANSFER-036; FR-TRANSFER-037

   Recover from an interrupted pack or unpack operation using manifest-based state tracking and the ``--resume`` flag.

   **Failure:** Operation interrupted by insufficient USB space, power loss, or user abort.

   **Diagnose:** Tool provides clear error message explaining what went wrong and how to recover.

   **Resume:** User runs the same command with ``--resume``. The tool reads the manifest, identifies the last completed chunk, and continues from there.

   **Success Criteria:** Transfer completes successfully after recovery with no data loss or corruption.

--------------

Prerequisites
-------------

- **Prior operation:** A pack or unpack that was interrupted mid-operation
- **Manifest:** ``airgap-transfer-manifest.json`` written before the failure (contains chunk completion state)
- **Transfer media:** USB drive(s) with partial transfer data

--------------

Workflow Steps
--------------

Scenario A: Pack Interrupted by Insufficient Space
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Pack starts normally**

.. code:: bash

   airgap-transfer pack ~/large-dataset/ /media/usb-drive

The tool begins writing ``chunk_000.tar``. Midway through ``chunk_001.tar``, the USB runs out of space.

**2. Tool reports clear error**

::

   error: insufficient space on /media/usb-drive (1.2 GB available, 8 GB needed for chunk_001)
   Hint: Free space or insert a larger USB, then run with --resume

The manifest records ``chunk_000`` as completed and ``chunk_001`` as in-progress.

**3. Operator swaps USB and resumes**

.. code:: bash

   # Insert fresh USB drive
   airgap-transfer pack ~/large-dataset/ /media/usb-drive --resume

The tool reads the manifest, sees ``chunk_000`` is complete, and resumes from ``chunk_001``.

**4. Pack completes**

::

   Resuming from chunk 1 (1 of 4 already complete)
   ...
   Pack complete. 4 chunks created, all verified.

Scenario B: Unpack Interrupted by Power Loss
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Unpack starts on air-gapped machine**

.. code:: bash

   airgap-transfer unpack /media/usb-drive ~/restored/

The tool extracts ``chunk_000.tar`` and ``chunk_001.tar`` successfully. Power is lost during ``chunk_002.tar``.

**2. After power restoration, check state**

.. code:: bash

   airgap-transfer list /media/usb-drive

Shows chunks 0 and 1 as completed, chunk 2 as in-progress.

**3. Resume unpack**

.. code:: bash

   airgap-transfer unpack /media/usb-drive ~/restored/ --resume

The tool re-extracts ``chunk_002.tar`` from the beginning (partial extraction is discarded) and continues through the remaining chunks.

Scenario C: Missing Chunks During Unpack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Unpack with incomplete USB set**

.. code:: bash

   airgap-transfer unpack /media/usb-drive ~/restored/

::

   error: chunk_002.tar not found at /media/usb-drive/chunk_002.tar
   Hint: Connect the USB containing chunk_002, then run with --resume

**2. Connect correct USB and resume**

.. code:: bash

   # Mount USB containing chunk_002
   airgap-transfer unpack /media/usb-drive ~/restored/ --resume

--------------

Success Criteria
----------------

- Interrupted operations resume from the last completed chunk, not from scratch
- Clear error messages explain what failed and how to recover
- No data loss or corruption after recovery
- Manifest accurately tracks chunk completion state across interruptions

--------------

Error Scenarios
---------------

============================== ================================ ===============================
Error                          Cause                            Recovery
============================== ================================ ===============================
"Insufficient space"           USB full during pack             Swap USB, ``--resume``
"chunk_002 not found"          Missing USB during unpack        Connect correct USB, ``--resume``
"Manifest incompatible"        Resume with different arguments  Use ``--force`` to start fresh
"All chunks already complete"  Resume on finished transfer      Nothing to do — already done
============================== ================================ ===============================

--------------

Related Documents
-----------------

- :doc:`Large File Transfer <use-case-large-file>` — Standard pack/unpack workflow
- :doc:`Multi-USB Transfer <use-case-multiple-usb>` — Multi-drive coordination with resume
- :doc:`SRS <../requirements/srs>` — State management and resume requirements

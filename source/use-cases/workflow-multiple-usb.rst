Workflow: Multi-USB Dataset Transfer
====================================

Scenario
--------

Transfer a large dataset (e.g., machine learning models, video collection) that requires multiple USB drive swaps due to size constraints.

.. usecase:: Multi-USB Dataset Transfer
   :id: UC-TRANSFER-003
   :status: approved
   :tags: transfer, workflow, multi-usb, swap

   Transfer large dataset (30GB) requiring multiple USB swaps with small capacity drives (4x 8GB USBs).

   **Pack:** Split dataset into chunks matching USB capacity, prompt for USB swaps during packing, write manifest to each USB for independent verification.

   **Transfer:** Transport all USB drives across air-gap (together or separately).

   **Unpack:** Support progressive unpack with USB swaps, process USBs in any order, verify each chunk before extraction, resume if interrupted mid-swap.

   **Success Criteria:** Handle 4+ USB swaps without errors, clear prompts for USB insertion, verify integrity across all chunks, work with USBs in any order.

--------------

Prerequisites
-------------

- **Source machine:** Connected system with data to transfer
- **Destination machine:** Air-gapped system
- **Transfer media:** Four 8GB USB drives (only have small USBs available)
- **Dataset:** ``~/ml-models/`` (30GB total)

--------------

Workflow Steps
--------------

Phase 1: Pack with Multiple USB Swaps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Initial pack command**

   .. code:: bash

      airgap-transfer pack ~/ml-models/ /media/usb-drive --chunk-size 8GB

**USB swap sequence**

   - **USB #1:** Writes ``chunk_000.tar`` (8GB)

     - Tool: “Chunk 1 of 4 complete. Insert next USB.”
     - User: Eject USB #1, insert USB #2

   - **USB #2:** Writes ``chunk_001.tar`` (8GB)

     - Tool: “Chunk 2 of 4 complete. Insert next USB.”
     - User: Eject USB #2, insert USB #3

   - **USB #3:** Writes ``chunk_002.tar`` (8GB)

     - Tool: “Chunk 3 of 4 complete. Insert next USB.”
     - User: Eject USB #3, insert USB #4

   - **USB #4:** Writes ``chunk_003.tar`` (6GB, final chunk)

     - Tool: “Pack complete. 4 chunks created.”

**Manifest on each USB**

   - Each USB contains a copy of ``airgap-transfer-manifest.json``
   - Manifest lists all 4 chunks with checksums
   - User can verify any USB independently

Phase 2: Physical Transfer
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Transport all 4 USB drives across air-gap
- USBs can be transported together or separately

Phase 3: Unpack on Destination
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Check available chunks**

   - Connect USB #1

   .. code:: bash

      airgap-transfer list /media/usb-1

   Shows: chunk_000 available (1 of 4)

**Progressive unpack**

   - Option A: Connect all USBs, unpack once

   .. code:: bash

      # Mount all USBs
      airgap-transfer unpack /media/usb-drives ~/restored-models/

   - Option B: Connect USBs one at a time

   .. code:: bash

      # Connect USB #1
      airgap-transfer unpack /media/usb-1 ~/restored-models/
      # Tool: "Waiting for chunk_001. Insert USB with chunk_001."
      # User swaps to USB #2, tool continues

**Verification**

   - Tool verifies each chunk before extraction
   - Final verification after all chunks extracted
   - Reports: “30GB transferred across 4 USBs, verified”

--------------

Success Criteria
----------------

- ✅ Handle 4+ USB swaps without errors
- ✅ Resume if interrupted mid-swap
- ✅ Clear prompts for USB insertion
- ✅ Verify integrity across all chunks
- ✅ Work with USBs in any order

--------------

Edge Cases
----------

+-----------------------------------+-------------------------------------------+
| Scenario                          | Behavior                                  |
+===================================+===========================================+
| USBs inserted out of order        | Tool processes in chunk index order       |
+-----------------------------------+-------------------------------------------+
| Missing USB during unpack         | Tool prompts for specific chunk number    |
+-----------------------------------+-------------------------------------------+
| Duplicate chunk on multiple USBs  | Tool uses first found, warns of duplicate |
+-----------------------------------+-------------------------------------------+
| Interrupted during USB swap       | Resume from last completed chunk          |
+-----------------------------------+-------------------------------------------+

--------------

User Experience Notes
---------------------

**Prompts should be clear and specific:**

- ❌ Bad: “Insert next USB”
- ✅ Good: “Chunk 2 of 4 complete. Insert USB for chunk 3.”

**Progress indication:**

- Show overall progress: “18GB of 30GB transferred (60%)”
- Show chunk progress: “Chunk 3/4: 8GB written”

--------------

Related Documents
-----------------

- :doc:`SRS <../requirements/srs>` - Multi-chunk requirements
- :doc:`SDD <../design/sdd>` - State management for resume
- :doc:`Roadmap <../roadmap>` - USB handling milestone

API Reference
=============

.. note::

   API documentation will be auto-generated from Rust source code once implementation begins.
   This page serves as a placeholder and integration guide for future developers.

Planned Architecture
--------------------

Based on :doc:`../design/sdd`, AirGap Transfer will consist of these modules:

CLI Module (``cli``)
~~~~~~~~~~~~~~~~~~~~

**Purpose:** Command-line interface for pack/unpack/list operations

**Key Components:**

- ``PackCommand`` - Pack operation handler
- ``UnpackCommand`` - Unpack operation handler
- ``ListCommand`` - List operation handler
- ``Args`` - Argument parser using clap


Chunker Module (``chunker``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** Split files into fixed-size chunks

**Key Components:**

- ``Chunker`` - Main chunking logic
- ``ChunkWriter`` - Write chunks to tar archives
- ``StreamingReader`` - Memory-efficient file reading


Assembler Module (``assembler``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** Reconstruct files from chunks

**Key Components:**

- ``Assembler`` - Main reassembly logic
- ``ChunkReader`` - Read chunks from tar archives
- ``FileWriter`` - Write reconstructed files


Hash Module (``hash``)
~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** SHA-256 checksum generation and verification

**Key Components:**

- ``Hasher`` - SHA-256 computation
- ``ChecksumVerifier`` - Verify chunk integrity
- ``ManifestValidator`` - Validate manifest checksums


Manifest Module (``manifest``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** Manage transfer metadata and state

**Key Components:**

- ``Manifest`` - Transfer metadata structure
- ``ChunkMetadata`` - Individual chunk information
- ``StateManager`` - Operation state persistence


USB Module (``usb``)
~~~~~~~~~~~~~~~~~~~~

**Purpose:** USB device detection and management

**Key Components:**

- ``UsbDetector`` - Detect USB drive capacity
- ``MountMonitor`` - Monitor mount/unmount events
- ``SpaceChecker`` - Verify available space


Developer Resources
-------------------

See `Rust API Documentation Integration Guide <../../meta/rust-integration-guide.html>`__ for doc comment guidelines, sphinxcontrib-rust configuration, and traceability linking.

Future Enhancements
-------------------

When implementation begins:

- Add ``.. impl::`` directives for each module
- Link implementations to requirements in traceability matrix
- Auto-generate API docs with sphinxcontrib-rust
- Document async operation patterns
- Add workflow examples with code snippets


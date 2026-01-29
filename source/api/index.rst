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


Integration with Sphinx
------------------------

Rust Doc Comment Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Write doc comments that reference requirements for traceability:

.. code-block:: rust

   /// Splits files and directories into fixed-size chunks for air-gap transfer.
   ///
   /// The chunker reads input files in a streaming fashion to minimize memory
   /// usage, writing chunks directly to tar archives without intermediate files.
   ///
   /// # Implements
   ///
   /// - [`FR-TRANSFER-001`]: Split files into chunks
   /// - [`FR-TRANSFER-002`]: Auto-detect USB capacity
   /// - [`FR-TRANSFER-005`]: Stream without temp files
   ///
   /// # Example
   ///
   /// ```no_run
   /// use airgap_transfer::chunker::Chunker;
   ///
   /// let chunker = Chunker::new(16 * 1024 * 1024 * 1024); // 16GB chunks
   /// chunker.pack("vm-image.qcow2", "/media/usb-drive")?;
   /// ```
   pub struct Chunker {
       chunk_size: u64,
       progress: ProgressReporter,
   }

Async Operations Example
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rust

   /// Assembles chunks back into original files with integrity verification.
   ///
   /// # Implements
   ///
   /// - [`FR-TRANSFER-009`]: Reconstruct files from chunks
   /// - [`FR-TRANSFER-010`]: Verify chunk checksums before unpack
   /// - [`FR-TRANSFER-013`]: Resume interrupted unpack
   ///
   pub struct Assembler {
       manifest: Manifest,
       state: StateManager,
   }

   impl Assembler {
       /// Unpacks chunks to the destination directory.
       ///
       /// # Implements
       ///
       /// - [`FR-TRANSFER-011`]: Place files in destination
       ///
       pub async fn unpack(&self, dest: &Path) -> Result<()> {
           // Verify all chunks present
           self.verify_completeness()?;

           // Resume from last completed chunk if interrupted
           let start_chunk = self.state.last_completed_chunk()?;

           for chunk in start_chunk..self.manifest.chunk_count {
               self.verify_and_extract_chunk(chunk, dest).await?;
               self.state.mark_completed(chunk)?;
           }

           Ok(())
       }
   }

Using sphinxcontrib-rust
~~~~~~~~~~~~~~~~~~~~~~~~

Once code exists, integrate with Sphinx:

**Generate Rust docs:**

   .. code-block:: bash

      cargo doc --no-deps --document-private-items

**Configure sphinxcontrib-rust in conf.py:**

   .. code-block:: python

      extensions = [
          # ... existing extensions
          'sphinxcontrib.rust',
      ]

      rust_crates = {
          'airgap-transfer': '../airgap-transfer',
      }

**Reference Rust items in RST:**

   .. code-block:: rst

      See :rust:struct:`Chunker` for file chunking.
      See :rust:struct:`Assembler` for chunk reassembly.

**Build documentation:**

   .. code-block:: bash

      cd sphinx-docs
      make html

Traceability Linking
~~~~~~~~~~~~~~~~~~~~

Link implementations back to requirements:

.. code-block:: rst

   .. impl:: Chunker Implementation
      :id: IMPL-TRANSFER-001
      :implements: FR-TRANSFER-001, FR-TRANSFER-002, FR-TRANSFER-005
      :status: planned
      :location: src/chunker/mod.rs

      Streaming file chunker with auto USB capacity detection

Future Enhancements
-------------------

When implementation begins:

- Add ``.. impl::`` directives for each module
- Link implementations to requirements in traceability matrix
- Auto-generate API docs with sphinxcontrib-rust
- Document async operation patterns
- Add workflow examples with code snippets

See Also
--------

- :doc:`../requirements/srs` - Requirements this API implements
- :doc:`../design/sdd` - Detailed design specifications
- :doc:`../testing/plan` - Test cases validating this API
- :doc:`../use-cases/use-case-large-file` - Real-world usage example

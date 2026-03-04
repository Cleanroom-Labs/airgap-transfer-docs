Future Requirements
===================

Requirements planned for future releases. These are not in scope for the
v1.0 MVP release and are maintained here for planning visibility.

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

v1.2 — Authenticated Encryption (AEAD) for Chunks at Rest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following requirements are planned for v1.2 and are not in scope for the MVP release.
These address the threat of USB interception by providing encryption at rest for chunk
data and tamper detection for the transfer manifest.

.. req:: Optional AEAD Encryption of Chunks
   :id: FR-TRANSFER-050
   :status: proposed
   :tags: transfer, v1.2, encryption, aead, security
   :priority: should
   :release: v1.2

   The system SHALL support optional authenticated encryption of chunk data using an AEAD
   construction. When a user provides a passphrase via ``--passphrase`` (interactive prompt)
   or ``--passphrase-file`` (read from file), all chunk data SHALL be encrypted during pack
   and decrypted during unpack. When no passphrase is provided, the system SHALL behave
   identically to v1.0 (plaintext chunks with checksum verification).

.. req:: AEAD Algorithm Default and Agility
   :id: FR-TRANSFER-051
   :status: proposed
   :tags: transfer, v1.2, encryption, aead, crypto-agility, security
   :priority: should
   :release: v1.2

   The default AEAD algorithm SHALL be ChaCha20-Poly1305. The system SHALL support
   algorithm selection via ``--aead-algorithm`` CLI flag. The AEAD module SHALL use a
   trait-based interface consistent with the existing ``HashAlgorithm`` trait pattern
   (FR-TRANSFER-047), enabling future algorithm adoption without architectural changes.

.. req:: Passphrase-Based Key Derivation
   :id: FR-TRANSFER-052
   :status: proposed
   :tags: transfer, v1.2, encryption, key-management, security
   :priority: should
   :release: v1.2

   The system SHALL derive encryption keys from user-provided passphrases using a
   memory-hard key derivation function (Argon2id recommended). KDF parameters (algorithm,
   memory cost, time cost, salt) SHALL be recorded in the manifest so the unpack operation
   can reproduce the same derived key.

.. req:: Unique Nonce Per Chunk
   :id: FR-TRANSFER-053
   :status: proposed
   :tags: transfer, v1.2, encryption, aead, security
   :priority: must
   :release: v1.2

   Each chunk SHALL be encrypted with a unique nonce. Nonces SHALL be stored alongside
   chunk metadata in the manifest. Nonce reuse across chunks with the same key SHALL be
   treated as a fatal error.

.. req:: Manifest Authentication via Keyed MAC
   :id: FR-TRANSFER-054
   :status: proposed
   :tags: transfer, v1.2, encryption, authentication, security
   :priority: should
   :release: v1.2

   When AEAD encryption is enabled, the manifest SHALL be authenticated using a keyed MAC
   (HMAC-SHA256, KMAC, or BLAKE3 keyed mode) derived from the same passphrase. The manifest
   SHALL remain human-readable (unencrypted JSON) but SHALL include a MAC field that the
   unpack operation verifies before processing any chunks. Verification failure SHALL abort
   the unpack operation.

.. req:: Record Encryption Metadata in Manifest
   :id: FR-TRANSFER-055
   :status: proposed
   :tags: transfer, v1.2, encryption, manifest, security
   :priority: should
   :release: v1.2

   When encryption is enabled, the manifest SHALL record: the AEAD algorithm used, the KDF
   algorithm and parameters (excluding the passphrase), per-chunk nonces, and the MAC
   algorithm used for manifest authentication. This metadata SHALL be sufficient for the
   unpack operation to decrypt and verify without out-of-band configuration.

.. nfreq:: Passphrase Handling Security
   :id: NFR-TRANSFER-023
   :status: proposed
   :tags: transfer, v1.2, encryption, security, privacy
   :priority: must
   :release: v1.2

   The system SHALL NOT write passphrases or derived keys to disk, logs, or the manifest
   in plaintext. Passphrases SHALL be read from an interactive terminal prompt (with echo
   disabled) or from a file descriptor, and SHALL be zeroized from memory after key
   derivation completes.

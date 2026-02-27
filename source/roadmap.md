# Project Roadmap

Build an air-gap file transfer tool you can trust. Ship it. See what happens.

<br>

**Guiding document:** [Principles](https://cleanroomlabs.dev/docs/meta/principles.html)

## v1.0.0 Release

**Release Goal:** This project will reach v1.0.0 as part of a coordinated release with Cleanroom Whisper and AirGap Deploy.

**v1.0.0 Scope:** The MVP features documented in this roadmap.

**Cross-Project Integration:** v1.0.0 validates the multi-USB transfer scenario works end-to-end with AirGap Deploy.

**Release Coordination:** See [Release Roadmap](https://cleanroomlabs.dev/docs/meta/release-roadmap.html) for cross-project timeline and integration milestones.

<br>

**Target:** Suite Milestone 4 (Month 8) — MVP Complete

## Current Status

**Phase:** Implementation (Phases 1–8 mostly complete — documentation and large-file testing remain)

**Next:** API docs, user guide, large-file integration testing, 80% coverage verification, multi-USB swapping

Core MVP features are implemented and passing 49 unit tests with zero clippy warnings. CI/CD pipeline runs on Linux, macOS, and Windows. Integration tests cover roundtrip, error scenarios, and resume.

<br>

**MVP Goal:** Successfully transfer 10GB dataset across air-gap with checksum verification.

## MVP Scope

| Feature | Implementation |
|---------|----------------|
| Pack files | Split into chunks, write to USB |
| Unpack files | Reconstruct from chunks with verification |
| List chunks | Show inventory and status |
| Integrity | SHA-256 checksums for all operations |
| Cryptographic agility | Configurable hash algorithm, trait-based backend |
| Resume | Continue interrupted transfers |
| CLI | Command-line interface with options |

## Implementation Phases

### Phase 1: Core Infrastructure

**Target:** Suite Milestone 3 (Month 6)

**Goal:** Establish project structure and core abstractions

**Project Setup:**

- [x] Create Cargo project with minimal dependencies
- [x] Set up CI/CD (GitHub Actions)
- [x] Configure cargo-deny for license compliance
- [x] Add basic README, CONTRIBUTING.md

**Core Types** (src/core/):

- [x] Chunk — chunk metadata and I/O
- [x] Manifest — JSON manifest structure (using serde)
- [x] HashBackend — trait for pluggable hash algorithms
- [x] Error — unified error type (using thiserror)

**CLI Skeleton** (src/cli.rs, src/main.rs):

- [x] Command parsing (using clap)
- [x] `airgap-transfer pack <source> <dest>` command stub
- [x] `airgap-transfer unpack <source> <dest>` command stub
- [x] `airgap-transfer list <chunk-location>` command stub
- [x] `--help` for all commands

**Done when:** Working CLI skeleton with command stubs, core type definitions, CI/CD pipeline running.

### Phase 2: Pack Operation

**Target:** Suite Milestone 3

**Goal:** Split files into chunks with USB awareness

**Chunker** (src/chunker.rs):

- [x] Implement tar archive creation from source files/directories
- [x] Stream data in fixed-size blocks (streaming architecture, memory < 100MB)
- [x] Write chunks to specified destination
- [x] Handle final chunk (may be smaller)

**USB Handling** (src/usb.rs):

- [x] Detect USB mount points (platform-specific)
- [x] Query available capacity
- [ ] Auto-calculate optimal chunk size based on USB capacity
- [x] Manual chunk size specification (`--chunk-size` flag)
- [ ] Prompt for USB swapping when multiple chunks needed
- [x] Sync filesystem before removal prompts

**Done when:** Can create chunk files from source directory, auto-detects USB capacity.

### Phase 3: Integrity & Cryptographic Agility

**Target:** Suite Milestone 3

**Goal:** Pluggable hash verification with SHA-256 default

**Hash Backend** (src/verifier.rs):

- [x] Trait-based hash interface (pluggable backend)
- [x] SHA-256 implementation (default)
- [x] Configurable hash algorithm via `--hash-algorithm` CLI flag
- [x] Calculate checksum during chunk creation
- [x] Store checksums in manifest with algorithm identifier
- [x] Verify chunk checksums during unpack
- [x] Report verification failures with corrupted chunk identification
- [ ] Verify final reconstructed file against original checksum

**Done when:** Chunks are verified before unpacking, hash algorithm is configurable and recorded in manifest.

### Phase 4: State Management & Resume

**Target:** Suite Milestone 3–4

**Goal:** Track operation state and support resume

**Manifest Manager** (src/manifest.rs):

- [x] Create manifest structure (per SDD schema)
- [x] Write manifest during pack operation
- [x] Update chunk status as operations complete
- [x] Read manifest during unpack/list operations
- [x] Record hash algorithm in manifest

**Resume:**

- [x] Track completed chunks in manifest
- [ ] Skip already-completed chunks on resume
- [ ] Handle partial chunk cleanup
- [ ] Support resume for both pack and unpack
- [ ] Handle interruptions gracefully (Ctrl+C, system shutdown)

**Done when:** Manifest persists state across operations, can resume after interruption.

### Phase 5: Unpack & List

**Target:** Suite Milestone 4

**Goal:** Reconstruct files and display inventory

**Unpack Operation** (src/commands/unpack.rs):

- [x] Read and validate manifest
- [x] Verify all chunks present (validate completeness)
- [x] Verify chunk checksums using manifest-specified algorithm
- [x] Extract chunks to destination
- [ ] Verify final output integrity
- [x] Optionally delete chunks after successful reconstruction

**List Command** (src/commands/list.rs):

- [x] Read manifest from chunk location
- [x] Display chunk count and sizes
- [x] Show verification status
- [x] Identify missing or corrupted chunks
- [x] Display estimated total size after reconstruction

**Done when:** Files reconstructed match original, `airgap-transfer list` shows complete inventory.

### Phase 6: Safety & Validation

**Target:** Suite Milestone 4

**Goal:** Safety features and deployment validation

**Safety Features:**

- [x] Confirm overwrite of existing files
- [x] Validate destination paths and permissions
- [x] Safely sync USB before prompting for removal
- [ ] Atomic operations where possible

**Deployment:**

- [x] Offline build dependencies (cargo vendor)
- [x] Internet-free build after initial setup
- [x] Static binary deployment target

**Done when:** Safety features prevent accidental data loss, deployment pipeline validated.

### Phase 7: CLI Polish

**Target:** Suite Milestone 4

**Goal:** Production-ready CLI experience

**User Experience:**

- [x] Colored output (using colored crate)
- [x] Progress bars for long operations (using indicatif)
- [x] Clear error messages with suggested actions
- [x] `--verbose` flag for detailed output
- [x] `--dry-run` flag for pack operations
- [x] `--no-verify` flag to disable checksum verification (verification on by default)
- [x] Comprehensive help text

**Done when:** Ready for daily use without frustration.

### Phase 8: Testing & Documentation

**Target:** Suite Milestone 4 (Month 8) — MVP Complete

**Goal:** Comprehensive testing and documentation

**Unit Tests:**

- [x] Core types (chunk, manifest, hash backend)
- [x] Chunker logic (splitting, streaming)
- [x] Hash verification (SHA-256, pluggable backends)
- [x] Manifest management (state tracking)

**Integration Tests:**

- [x] End-to-end: pack → transfer → unpack → verify
- [x] Multi-platform testing (Linux, macOS, Windows via CI)
- [x] Error scenarios (missing chunks, corrupted data, insufficient USB)
- [ ] Large file handling (multi-GB datasets)
- [x] Resume scenarios (interrupted pack, interrupted unpack)

**Documentation:**

- [ ] API documentation (rustdoc)
- [ ] User guide — Getting started, commands reference, USB workflow
- [ ] Developer guide — Architecture, contributing
- [ ] Examples — 10GB dataset transfer, multi-USB workflow

**CI/CD:**

- [x] Run tests on Linux, macOS, Windows
- [x] Clippy lints (deny warnings)
- [x] rustfmt checks
- [x] cargo-deny license checks
- [ ] Release automation (GitHub releases)

**Done when:** 80%+ code coverage, complete documentation, working examples, CI/CD pipeline.

## Definition of Done

MVP is complete when:

- [ ] Pack 10GB dataset into chunks
- [ ] Transfer chunks across air-gap (manual USB movement)
- [x] Unpack and verify integrity on destination
- [ ] Resume interrupted pack operation
- [x] List chunk inventory shows all expected chunks
- [x] All operations work offline
- [ ] 80%+ code coverage
- [x] Zero clippy warnings
- [x] All dependency licenses compatible with AGPL-3.0
- [ ] Documentation covers all use cases
- [ ] Use successfully for one week

## What's NOT in MVP

Defer all of this until after shipping:

- Compression (gzip, zstd)
- Parallel chunk processing
- GUI
- Automatic USB detection and swapping
- Network transfer modes
- Performance optimization

## After MVP

### v1.1 — SBOM-Aware Transfer Manifests

- [ ] Reference CycloneDX SBOM in transfer manifest when present
- [ ] Log SBOM presence in transfer audit trail

### v1.2 — Authenticated Encryption (AEAD) for Chunks at Rest

Addresses the USB interception threat: if a drive is lost or intercepted, chunk data
should be unreadable and manifest tampering should be detectable.

- [ ] Optional AEAD encryption of chunks via `--passphrase` / `--passphrase-file`
- [ ] ChaCha20-Poly1305 default, trait-based pluggable AEAD backend
- [ ] Argon2id key derivation from user passphrase (KDF params stored in manifest)
- [ ] Unique nonce per chunk (nonce reuse = fatal error)
- [ ] Manifest authentication via keyed MAC (HMAC-SHA256, KMAC, or BLAKE3 keyed)
- [ ] Encryption metadata recorded in manifest (algorithm, KDF params, nonces, MAC)
- [ ] Passphrase never written to disk/logs; zeroized after key derivation

**Design notes:** AEAD chosen over separate encrypt-then-HMAC to eliminate composition
errors. Digital signatures rejected — this is a closed-world scenario (same operator
packs and unpacks) with no need for non-repudiation or third-party verification.
Symmetric crypto is also inherently PQC-resilient (Grover's algorithm halves effective
key strength; ChaCha20-Poly1305 with 256-bit keys retains ~128-bit security under
quantum attack).

### Future

**Compression & Performance:**
- Compression support (gzip, zstd)
- Parallel chunk processing
- Performance optimization for large datasets

**Automation & Integration:**
- Automatic USB detection and swapping
- Integration API for AirGap Deploy workflows

## Key Documents

| Document | Purpose |
|----------|---------|
| [Principles](https://cleanroomlabs.dev/docs/meta/principles.html) | Design principles (read first) |
| [Requirements (SRS)](requirements/srs) | Functional and non-functional requirements |
| [Design (SDD)](design/sdd) | Architecture and component design |
| [Test Plan](testing/plan) | Test cases with traceability |

## See Also

- [Meta-Architecture](https://cleanroomlabs.dev/docs/meta/meta-architecture.html) — How AirGap Transfer fits in the AirGap suite
- [Specification Overview](https://cleanroomlabs.dev/docs/meta/specification-overview.html) — Project statistics and traceability overview
- [AirGap Deploy](https://cleanroomlabs.dev/docs/deploy/readme.html) — Deployment packaging companion tool
- [Cleanroom Whisper](https://cleanroomlabs.dev/docs/whisper/readme.html) — Offline transcription app

## Progress Log

| Date | Activity |
|------|----------|
| 2026-01-28 | Created specification and documentation |
| 2026-01-31 | Updated roadmap to align with 6-milestone release plan |
| 2026-02-16 | Requirements specified and ready for implementation |
| 2026-02-22 | Core implementation: chunker, manifest, verifier, error types |
| 2026-02-23 | Pack command with streaming, checksums, dry-run, space checks |
| 2026-02-24 | Unpack command with verification, chunk cleanup, overwrite protection |
| 2026-02-25 | List command with --verify, CLI polish, 49 unit tests passing |
| 2026-02-25 | Updated requirements (FR-TRANSFER-056/057), clarified FR-038/017/018 |
| 2026-02-25 | Updated roadmap to reflect implementation progress |
| 2026-02-26 | Synced roadmap and SDD to reflect CI/CD, integration tests, and new source modules |

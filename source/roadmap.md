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

**Phase:** Preliminary Planning Complete

**Next:** Finalize plan and begin MVP implementation

Requirements, design, and test specifications need some minor adjustments and a final review.

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

- [ ] Create Cargo project with minimal dependencies
- [ ] Set up CI/CD (GitHub Actions)
- [ ] Configure cargo-deny for license compliance
- [ ] Add basic README, CONTRIBUTING.md

**Core Types** (src/core/):

- [ ] Chunk — chunk metadata and I/O
- [ ] Manifest — JSON manifest structure (using serde)
- [ ] HashBackend — trait for pluggable hash algorithms
- [ ] Error — unified error type (using thiserror)

**CLI Skeleton** (src/cli.rs, src/main.rs):

- [ ] Command parsing (using clap)
- [ ] `airgap-transfer pack <source> <dest>` command stub
- [ ] `airgap-transfer unpack <source> <dest>` command stub
- [ ] `airgap-transfer list <chunk-location>` command stub
- [ ] `--help` for all commands

**Done when:** Working CLI skeleton with command stubs, core type definitions, CI/CD pipeline running.

### Phase 2: Pack Operation

**Target:** Suite Milestone 3

**Goal:** Split files into chunks with USB awareness

**Chunker** (src/chunker.rs):

- [ ] Implement tar archive creation from source files/directories
- [ ] Stream data in fixed-size blocks (streaming architecture, memory < 100MB)
- [ ] Write chunks to specified destination
- [ ] Handle final chunk (may be smaller)

**USB Handling** (src/usb.rs):

- [ ] Detect USB mount points (platform-specific)
- [ ] Query available capacity
- [ ] Auto-calculate optimal chunk size based on USB capacity
- [ ] Manual chunk size specification (`--chunk-size` flag)
- [ ] Prompt for USB swapping when multiple chunks needed
- [ ] Sync filesystem before removal prompts

**Done when:** Can create chunk files from source directory, auto-detects USB capacity.

### Phase 3: Integrity & Cryptographic Agility

**Target:** Suite Milestone 3

**Goal:** Pluggable hash verification with SHA-256 default

**Hash Backend** (src/hash.rs):

- [ ] Trait-based hash interface (pluggable backend)
- [ ] SHA-256 implementation (default)
- [ ] Configurable hash algorithm via `--hash-algorithm` CLI flag
- [ ] Calculate checksum during chunk creation
- [ ] Store checksums in manifest with algorithm identifier
- [ ] Verify chunk checksums during unpack
- [ ] Report verification failures with corrupted chunk identification
- [ ] Verify final reconstructed file against original checksum

**Done when:** Chunks are verified before unpacking, hash algorithm is configurable and recorded in manifest.

### Phase 4: State Management & Resume

**Target:** Suite Milestone 3–4

**Goal:** Track operation state and support resume

**Manifest Manager** (src/manifest.rs):

- [ ] Create manifest structure (per SDD schema)
- [ ] Write manifest during pack operation
- [ ] Update chunk status as operations complete
- [ ] Read manifest during unpack/list operations
- [ ] Record hash algorithm in manifest

**Resume** (src/resume.rs):

- [ ] Track completed chunks in manifest
- [ ] Skip already-completed chunks on resume
- [ ] Handle partial chunk cleanup
- [ ] Support resume for both pack and unpack
- [ ] Handle interruptions gracefully (Ctrl+C, system shutdown)

**Done when:** Manifest persists state across operations, can resume after interruption.

### Phase 5: Unpack & List

**Target:** Suite Milestone 4

**Goal:** Reconstruct files and display inventory

**Unpack Operation** (src/unpack.rs):

- [ ] Read and validate manifest
- [ ] Verify all chunks present (validate completeness)
- [ ] Verify chunk checksums using manifest-specified algorithm
- [ ] Extract chunks to destination
- [ ] Verify final output integrity
- [ ] Optionally delete chunks after successful reconstruction

**List Command** (src/list.rs):

- [ ] Read manifest from chunk location
- [ ] Display chunk count and sizes
- [ ] Show verification status
- [ ] Identify missing or corrupted chunks
- [ ] Display estimated total size after reconstruction

**Done when:** Files reconstructed match original, `airgap-transfer list` shows complete inventory.

### Phase 6: Safety & Validation

**Target:** Suite Milestone 4

**Goal:** Safety features and deployment validation

**Safety Features:**

- [ ] Confirm overwrite of existing files
- [ ] Validate destination paths and permissions
- [ ] Safely sync USB before prompting for removal
- [ ] Atomic operations where possible

**Deployment:**

- [ ] Offline build dependencies (cargo vendor)
- [ ] Internet-free build after initial setup
- [ ] Static binary deployment target

**Done when:** Safety features prevent accidental data loss, deployment pipeline validated.

### Phase 7: CLI Polish

**Target:** Suite Milestone 4

**Goal:** Production-ready CLI experience

**User Experience:**

- [ ] Colored output (using colored crate)
- [ ] Progress bars for long operations (using indicatif)
- [ ] Clear error messages with suggested actions
- [ ] `--verbose` flag for detailed output
- [ ] `--dry-run` flag for all operations
- [ ] `--no-verify` flag to disable checksum verification (verification on by default)
- [ ] Comprehensive help text

**Done when:** Ready for daily use without frustration.

### Phase 8: Testing & Documentation

**Target:** Suite Milestone 4 (Month 8) — MVP Complete

**Goal:** Comprehensive testing and documentation

**Unit Tests:**

- [ ] Core types (chunk, manifest, hash backend)
- [ ] Chunker logic (splitting, streaming)
- [ ] Hash verification (SHA-256, pluggable backends)
- [ ] Manifest management (state tracking, resume)

**Integration Tests:**

- [ ] End-to-end: pack → transfer → unpack → verify
- [ ] Multi-platform testing (Linux, macOS, Windows via CI)
- [ ] Error scenarios (missing chunks, corrupted data, insufficient USB)
- [ ] Large file handling (multi-GB datasets)
- [ ] Resume scenarios (interrupted pack, interrupted unpack)

**Documentation:**

- [ ] API documentation (rustdoc)
- [ ] User guide — Getting started, commands reference, USB workflow
- [ ] Developer guide — Architecture, contributing
- [ ] Examples — 10GB dataset transfer, multi-USB workflow

**CI/CD:**

- [ ] Run tests on Linux, macOS, Windows
- [ ] Clippy lints (deny warnings)
- [ ] rustfmt checks
- [ ] cargo-deny license checks
- [ ] Release automation (GitHub releases)

**Done when:** 80%+ code coverage, complete documentation, working examples, CI/CD pipeline.

## Definition of Done

MVP is complete when:

- [ ] Pack 10GB dataset into chunks
- [ ] Transfer chunks across air-gap (manual USB movement)
- [ ] Unpack and verify integrity on destination
- [ ] Resume interrupted pack operation
- [ ] List chunk inventory shows all expected chunks
- [ ] All operations work offline
- [ ] 80%+ code coverage
- [ ] Zero clippy warnings
- [ ] All dependency licenses compatible with AGPL-3.0
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

**Post-MVP: Encryption** (deferred from MVP per SRS scope):
- Encrypt chunks during pack operation
- Decrypt chunks during unpack operation
- Key management (passphrase-based)
- Encryption algorithm selection

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

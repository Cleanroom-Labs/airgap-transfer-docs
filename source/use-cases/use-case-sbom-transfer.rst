Use Case: Transfer Deployment Package with SBOM
=================================================

Scenario
--------

Transfer an AirGap Deploy package that includes a CycloneDX SBOM across the air gap. The transfer manifest references the SBOM file, and the audit trail records its presence for chain-of-custody documentation.

.. usecase:: Transfer Deployment Package with SBOM Metadata
   :id: UC-TRANSFER-004
   :status: proposed
   :tags: transfer, v1.1, sbom, workflow
   :priority: could
   :release: v1.1

   Transfer a deployment archive containing an SBOM file. AirGap Transfer detects the SBOM in the manifest and logs its presence in the audit trail, providing chain-of-custody documentation for the bill of materials.

   **Pack:** SBOM file (``sbom.cdx.json``) detected among files in the deployment archive. Transfer manifest records the SBOM reference.

   **Transfer:** SBOM verified by the same SHA-256 integrity checks as all other files.

   **Unpack:** SBOM extracted alongside application files. Audit trail includes SBOM reference for compliance documentation.

   **Success Criteria:** SBOM file integrity verified after transfer, SBOM reference recorded in transfer manifest and audit trail.

--------------

Prerequisites
-------------

- **Deployment archive:** Package created by AirGap Deploy v1.1 with ``--sbom`` flag (includes ``sbom.cdx.json``)
- **AirGap Transfer v1.1:** Version with SBOM-aware manifest support
- **USB drive(s):** Sufficient capacity for the deployment archive

--------------

Workflow Steps
--------------

Pack with SBOM
~~~~~~~~~~~~~~

When packing a deployment archive that contains an SBOM, AirGap Transfer detects the ``sbom.cdx.json`` file and records it in the transfer manifest:

.. code:: bash

   # Pack deployment archive (SBOM is inside the archive)
   airgap-transfer pack secure-app-v1.0.0.tar.gz /media/usb-drive

   # Transfer manifest automatically references the SBOM

Transfer
~~~~~~~~

Physical transfer proceeds as normal. The SBOM file is verified by the same SHA-256 integrity checks as every other chunk:

- Physically move USB drive(s) across air-gap boundary
- Chain of custody maintained — the SBOM reference in the manifest provides additional documentation of what was transferred

Unpack with Audit Trail
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   # On air-gapped machine
   airgap-transfer unpack /media/usb-drive ~/deployment/

   # Audit trail includes:
   # - Transfer timestamp
   # - File manifest with checksums
   # - SBOM reference (sbom.cdx.json location within archive)
   # - Verification status

The SBOM is now available on the air-gapped system for vulnerability scanning with ``airgap-deploy scan``.

--------------

Success Criteria
----------------

- SBOM file integrity verified after transfer (SHA-256 checksum match)
- SBOM reference recorded in transfer manifest
- SBOM reference included in audit trail
- No additional user intervention required — SBOM handling is automatic

--------------

Related Requirements
--------------------

- :need:`FR-TRANSFER-048` — Reference SBOM in Transfer Manifest
- :need:`FR-TRANSFER-049` — Log SBOM in Audit Trail

--------------

Related Documents
-----------------

- :doc:`Large File Transfer <use-case-large-file>` — Standard file transfer workflow
- :doc:`Multiple USB Transfer <use-case-multiple-usb>` — Multi-drive transfer for large packages
- `SBOM Generation (AirGap Deploy) <https://cleanroomlabs.dev/docs/deploy/use-cases/use-case-sbom-generation.html>`_ — How SBOMs are generated
- `Vulnerability Scanning (AirGap Deploy) <https://cleanroomlabs.dev/docs/deploy/use-cases/use-case-vulnerability-scanning.html>`_ — Using SBOMs for offline scanning

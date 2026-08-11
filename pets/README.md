# Pet Packages

This directory owns reusable pet metadata and spritesheet assets for Codex-compatible pet packages.

## Package Contract

Each package uses this shape:

```text
pets/<pet-id>/
├── pet.json
└── spritesheet.webp
```

`pet.json` contains:

| Field | Requirement |
| --- | --- |
| `id` | Required lowercase kebab-case identifier matching the package directory name. |
| `displayName` | Required non-empty user-facing name. |
| `description` | Required concise user-facing description. |
| `spritesheetPath` | Required package-relative path to the spritesheet; use `spritesheet.webp` for the current contract. |

Do not add metadata fields unless the consuming runtime supports them and the runtime change is validated in the same pass.

## Spritesheet Baseline

- Use WebP with a transparent background.
- Preserve the current `1536 × 1872` canvas and established frame placement unless the consuming runtime contract is intentionally changed and validated.
- Keep the referenced spritesheet inside the same package directory.
- Compare a new sheet with an existing package and verify it in the consuming runtime when that runtime is available; file format alone does not prove compatibility.

## Add Or Update A Package

1. Create or select `pets/<pet-id>/`.
2. Add `pet.json` using the package contract above.
3. Add the referenced WebP spritesheet.
4. Confirm that `id` matches the directory and `spritesheetPath` resolves locally.
5. Run the static checks below.
6. Verify rendered animation behavior in the consuming runtime when possible.

## Static Validation

Replace `<pet-id>` before running:

```sh
python3 -m json.tool pets/<pet-id>/pet.json >/dev/null
file pets/<pet-id>/spritesheet.webp
```

On macOS, verify dimensions with:

```sh
sips -g pixelWidth -g pixelHeight -g format pets/<pet-id>/spritesheet.webp
```

On other platforms, use an equivalent image inspector for the same format and dimension checks.

Expected current baseline:

- valid JSON
- WebP format
- `1536 × 1872` dimensions
- `spritesheetPath` resolves to an existing package-local file

## Ownership And Provenance

- The package directory owns its runtime metadata and spritesheet.
- Confirm that the repository is authorized to store and distribute the asset before adding it.
- Add a package-local `SOURCE.md` only when provenance, attribution, or license terms must travel with the asset; that file owns those terms and is not runtime metadata.
- When the runtime package contract changes, update this guide and every affected package in the same pass.

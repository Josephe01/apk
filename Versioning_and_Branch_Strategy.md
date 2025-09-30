# Versioning & Branch Strategy

This section defines how we version the Inventory Management System and manage branches for development, releases, and hotfixes.

---

## Versioning

- We use **Semantic Versioning (SemVer)**: `MAJOR.MINOR.PATCH` (e.g. `5.2.1`)
  - **MAJOR**: Breaking changes, incompatible API updates.
  - **MINOR**: Backwards-compatible feature additions.
  - **PATCH**: Backwards-compatible bug fixes.
- Version numbers are updated in `composer.json` and release notes.
- Tag releases in Git using:  
  ```bash
  git tag -a vX.Y.Z -m "Release vX.Y.Z"
  git push origin vX.Y.Z
  ```

---

## Branching Model

We follow a simplified **Git Flow**:

### Main Branches

- **main**: Always deployable; contains latest stable release.
- **develop**: Default branch for development; features and fixes are merged here.

### Supporting Branches

- **feature/xxx**: For new features.  
  Example: `feature/barcode-scanning`
- **fix/xxx**: For bug fixes.  
  Example: `fix/rounding-error`
- **hotfix/xxx**: For urgent patches to production.  
  Example: `hotfix/security-issue`
- **release/x.y.z**: For preparing a new release; includes final testing and documentation.

---

## Branch Workflow

1. **Start new work**:  
   Create a `feature/xxx` or `fix/xxx` branch from `develop`.
2. **Commit and push** changes to your branch.
3. **Open a Pull Request** against `develop`.
4. **Review & merge** PRs after all checks pass.
5. **Prepare release**:  
   - Merge `develop` into `main` via `release/x.y.z` branch.
   - Tag and push the release.
6. **Hotfixes**:  
   - Branch from `main`.
   - Merge back into both `main` and `develop`.

---

## Branch Naming Conventions

- Use lowercase, hyphen-separated names.
- Prefix branches as described (`feature/`, `fix/`, `hotfix/`, `release/`).

---

## Release Process

- Update version numbers and changelog.
- Tag release in Git.
- Announce release and update documentation.

---

## Automation

- Use GitHub Actions to automate tests and releases.
- All PRs must pass CI/CD checks before merging.

---

*Update this section as your workflow evolves!*
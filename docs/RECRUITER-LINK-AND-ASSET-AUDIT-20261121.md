# Public GitHub profile — recruiter reachability and asset audit

**Observed:** 21 November 2026 · **Scope:** public [profile README](../README.md) as committed on `main`, external links and repository-local visual references. The check used an independent Windows PowerShell 7 + `curl.exe` session with a 12-second timeout and no signed-in browser, cookies, private GitHub APIs or employer accounts.

## Results

| Inspection | Result | Exactly what this establishes |
|---|---:|---|
| HTTP(S) links extracted from the README in the audited host allowlist | **34/34 returned HTTP 2xx (all 200)** | Each HTTP HEAD destination was reachable at the observed instant. Includes portfolio case-study URLs, CI run pages, public demo source/readmes and approved company/site URLs. |
| Repository-local `assets/` paths referenced in HTML or Markdown | **86/86 present** | The `main` Git tree contains all 77 referenced SVG and 9 WebP paths. This is a path/existence test, not a visual render inspection. |
| Git tree completeness | **116 blobs, not truncated** | Entire main-branch tree was used to verify referenced asset paths; no guessed path or unseen file. |
| Published test evidence linked by quick view | **3 original synthetic runnable demos + 1 academic UI case study** | Links point to real public repositories; test results below retain their precise limitations. |

## Public engineering proof directly linked from the profile

| Project | Public original example | Recorded test and CI result | What it does **not** certify |
|---|---|---|---|
| MIYTO | [Room State Lab](https://github.com/a7medgamil/miyto-smart-rooms-showcase/tree/main/demo/room-state-lab) | 26 Node tests and [main Actions success](https://github.com/a7medgamil/miyto-smart-rooms-showcase/actions/runs/44894982610) | Live MIYTO audio, real rooms, capacity or production incidents |
| SMI | [Operations Case Lab](https://github.com/a7medgamil/smi-digital-operations-showcase/tree/main/demo/operations-case-lab) | 39 Node tests and [main Actions success](https://github.com/a7medgamil/smi-digital-operations-showcase/actions/runs/44895321053) | Access to actual student records, measured institutional ROI or production SMI systems |
| QADHA | [Battle Rules Lab](https://github.com/a7medgamil/qadha-platform-showcase/tree/main/demo/battle-rule-lab) | 36 Node tests and [main Actions success](https://github.com/a7medgamil/qadha-platform-showcase/actions/runs/44896934520) | Real competition authorization, payment, video or live reliability |
| AIU | [Fictional academic UI screenshots and QA scope](https://github.com/a7medgamil/aiu-smart-hr-showcase/blob/main/docs/MILESTONE1-SYNTHETIC-QA-EVIDENCE.md) | Public preview and bounded description of *private-source* tests | Publicly reproducible source, completed NLP/AI model, deployed HR platform or recruitment accuracy |

All three runnable examples use **independent fictional data**. They are not copies of private operational systems. Academic AIU source and CI require authorized private access.

## Method boundaries

- HTTP HEAD status does **not** prove page body correctness, form submission, working app sessions, checkout, SMTP, company legal standing, email deliverability, accessibility, or that the URL's internal fragment anchor exists.
- The README contains relative SVG/WebP files; matching the Git tree only confirms files exist. It does not prove that the entire browser screenshot, font, logo, image load, alt text, color contrast or dark/light theme renders correctly.
- A `200` for GitHub Actions pages confirms a page can open; the historical run's conclusion must be read independently from Actions metadata (the run links above correspond to verified successful main-branch checks).
- Some portfolio case-study links may use application redirects. The audit permitted redirects and did not inspect resulting HTML headings.
- Asset paths were extracted from the README's `src`, `srcset`, `href`, and Markdown `assets/` expressions and compared against the GitHub `main` tree returned as `truncated: false`.
- The audit does **not** independently validate owner identity, degree completion, institutional graduation statistics or legal company history. Those require approved source documents and transparent claim dates.

## Outstanding acceptance before using the profile in formal applications

- [ ] Verify profile name versus CV/legal name, chronological evidence, institutional outcome numbers and education claims with user-approved documents.
- [ ] Confirm the public contact email and response path; a mailto link cannot be tested for actual deliverability by this script.
- [ ] Inspect mobile and desktop image rendering and keyboard/screen-reader behavior in an ordinary signed-out browser, beyond static link/path checks.
- [ ] Audit public source licenses, original-asset redistribution rights and screenshots before any broader promotion.
- [ ] Verify account-specific two-factor authentication and pinned-repository selection in GitHub's own account UI; repository audits cannot change or certify those settings.

**Interpretation:** The profile's source links and local visual references are **reachable/present** at the audit date. This supports recruiter navigation, not a quality score, hiring probability, third-party accreditation or security certification.

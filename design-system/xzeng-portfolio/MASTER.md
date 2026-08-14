# Xzeng Portfolio · Design System

## Scope and decision

This document is the source of truth for shared structure, interaction and accessibility across the personal homepage, project index, project Case Studies, writing entry, resume placeholder and 404 page. Visual identity overrides for the homepage and each project live in `pages/` and are implemented in `assets/css/themes.css`.

The UI/UX design search recommended a portfolio grid, category filters, fast loading, visible focus and reduced-motion support. Those structural recommendations are adopted. Its generic light palette and red CTA are intentionally rejected because the existing site and project brief explicitly require continuity with the current dark, professional, technical blue/green system.

## Principles

1. Content first: a visitor should identify the person, direction, representative projects, core skills and contact path in under ten seconds.
2. Evidence over decoration: real screenshots and verified project facts only.
3. Progressive enhancement: HTML is complete and readable without JavaScript; motion and filtering are optional enhancements.
4. Quiet professionalism: terminal motifs are limited to the 404 page and small technical labels.
5. Native and lightweight: HTML, CSS and JavaScript only; no runtime framework, remote font or analytics dependency.
6. Distinct but related: every project may change palette, geometry, visual rhythm and hero composition, while navigation, semantics, focus behavior, responsive breakpoints and content truth remain shared.

## Color tokens

| Token | Value | Use |
| --- | --- | --- |
| `--bg` | `#08111f` | Primary background |
| `--bg-deep` | `#050b14` | Deep panels / terminal |
| `--surface` | `#0f1b2e` | Cards and navigation |
| `--surface-raised` | `#14243a` | Raised surfaces |
| `--text` | `#f8fafc` | Primary text |
| `--text-soft` | `#cbd5e1` | Secondary text |
| `--muted` | `#8fa3bd` | Metadata |
| `--primary` | `#79a7ff` | Links and focus |
| `--primary-strong` | `#a9c7ff` | High-contrast blue |
| `--accent` | `#22c98b` | Primary CTA / success |
| `--accent-strong` | `#55e3ac` | Labels and active accents |

Text/background pairings must remain at least WCAG AA. Color is never the only indicator of state.

Project themes override these semantic tokens rather than introducing raw colors into page HTML. The project index mirrors the same identities through `data-project-theme` so each card visually predicts its destination.

## Typography

- Heading stack: Lexend fallback to Segoe UI / Microsoft YaHei / sans-serif.
- Body stack: Source Sans 3 fallback to Segoe UI / Microsoft YaHei / sans-serif.
- No remote font request is required; fallbacks are part of the design.
- Body: 16 px minimum, line-height approximately 1.68.
- H1: fluid `clamp()`, tight tracking, 1.04–1.08 line-height.
- Eyebrows and technical labels: 12–13 px, high weight, increased letter spacing; never used for paragraphs.

## Spacing and layout

- Content container: 1180 px maximum with 20 px desktop and 12–16 px mobile gutters.
- Sections: 104 px desktop, 72 px mobile.
- Standard gaps: 8, 12, 16, 20, 24, 32, 40, 52, 64 px.
- Page structure is linear on mobile; no masonry.
- Main breakpoints: 1024 px, 768 px and 420 px.
- Minimum supported viewport: 320 px without horizontal page scrolling.

## Radius and elevation

- Small radius: 12 px.
- Standard card radius: 20 px.
- Feature / callout radius: 32 px.
- Shadows are soft and low-opacity; borders carry most separation.

## Components

### Buttons and links

- Minimum interactive height: 44 px; primary buttons use 48 px.
- Primary CTA: green fill and dark text.
- Secondary CTA: subtle blue surface and blue border.
- Text link: visible label plus optional directional arrow.
- Hover, active and `:focus-visible` states are required.

### Project cards

- Required content: category, name, verified description, highlight and tag list.
- Status is shown only when confirmed.
- Links are omitted when no public destination exists.
- Featured project may include a real screenshot and a stronger border.
- Each project card uses `data-project-theme="lanexam|music|asr|carmaker|racecar"`; the accent must match its Case Study page.

### Tags

- Use only `.project-tag-list` and `.project-tag`.
- Tags describe technology or domain; they are not decorative status pills.

### Project image carousel

- Project pages use one shared `[data-carousel]` component; do not create project-specific carousel CSS.
- No autoplay. Visitors control slides with previous/next buttons, pagination dots, ArrowLeft/ArrowRight, Home and End.
- Controls are at least 44×44 px and include descriptive accessible names.
- The current position is announced through a small `aria-live="polite"` status.
- Without JavaScript, every figure stays visible as a normal image gallery and the controls remain hidden.
- Placeholder images must be visibly labeled as placeholders and must never look like a real product screenshot.
- Real images require dimensions, accurate alt text, lazy loading below the fold and a concise figcaption.

### Sections

- Each section starts with eyebrow, H2 and optional short supporting paragraph.
- Copy is compact; project cards should not become README replacements.

## Motion

- Reveal uses opacity and translate only, around 420 ms.
- HTML is visible by default. `.js` enables the pre-reveal state.
- `prefers-reduced-motion: reduce` removes motion and smooth scrolling.
- No particles, parallax, mouse tracking, canvas or continuous GPU animation.

## Accessibility

- Preserve skip links, semantic landmarks and logical heading levels.
- All icon-only controls require accessible names.
- Keyboard focus uses a 3 px blue outline with offset.
- Mobile navigation synchronizes `aria-expanded`, closes on link click, outside click and Escape, and resets at desktop width.
- Images require dimensions and meaningful alt text; decorative SVGs use `aria-hidden="true"`.
- Project filtering uses native buttons and `aria-pressed`; without JavaScript all projects remain visible.

## Performance

- Target: homepage HTML under 100 KB, CSS under 50 KB, JS under 20 KB.
- Below-fold images use lazy loading and async decoding.
- Reserve image dimensions to prevent layout shift.
- No client-side API calls, remote analytics, PWA or runtime rendering.

## Pre-delivery viewports

- 320×568 minimum-width check.
- 375×812 mobile portrait.
- 768×1024 tablet.
- 1024×768 small desktop.
- 1440×900 desktop.

Also verify keyboard navigation, Escape behavior, JavaScript disabled content, reduced motion, internal links and GitHub Pages paths.

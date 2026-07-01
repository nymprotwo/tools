---
name: Nympro Tools
description: Dark minimal tool suite for creators and makers at tools.nympro.studio
version: alpha
colors:
  bg: "#0b0b10"
  surface: "#111118"
  surface-2: "#18181f"
  border: "rgba(255,255,255,0.07)"
  accent: "#7c6fe0"
  accent-dim: "rgba(124,111,224,0.15)"
  text: "#e8e8f0"
  muted: "#5a5a70"
  success: "#4caf87"
  error: "#e05c5c"
typography:
  h1:
    fontFamily: Inter
    fontSize: clamp(36px, 5vw, 64px)
    fontWeight: 700
    letterSpacing: -0.04em
    lineHeight: 1.1
  h3:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 600
  body:
    fontFamily: Inter
    fontSize: 14px
    lineHeight: 1.6
  label:
    fontFamily: Inter
    fontSize: 10px
    fontWeight: 600
    letterSpacing: 0.1em
  nav:
    fontFamily: Inter
    fontSize: 13.5px
    fontWeight: 500
  caption:
    fontFamily: Inter
    fontSize: 12px
rounded:
  sm: 8px
  md: 10px
  lg: 16px
  xl: 20px
  pill: 999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 36px
  xxl: 48px
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "#ffffff"
    rounded: "{rounded.md}"
    padding: "14px 24px"
  button-primary-hover:
    backgroundColor: "{colors.accent}"
    textColor: "#ffffff"
  button-secondary:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: "10px 16px"
  nav-bar:
    backgroundColor: "rgba(11,11,16,0.85)"
    height: 56px
  nav-item:
    backgroundColor: "transparent"
    textColor: "{colors.muted}"
    rounded: "{rounded.sm}"
    padding: "6px 12px"
  nav-item-hover:
    backgroundColor: "rgba(255,255,255,0.05)"
    textColor: "{colors.text}"
  dropdown:
    backgroundColor: "#13131b"
    rounded: "{rounded.lg}"
    padding: "8px"
  card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.xl}"
    padding: "36px"
  chip:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.muted}"
    rounded: "{rounded.pill}"
    padding: "7px 16px"
  chip-active:
    backgroundColor: "{colors.accent}"
    textColor: "#ffffff"
  input:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: "12px 14px"
  badge-new:
    backgroundColor: "{colors.accent-dim}"
    textColor: "{colors.accent}"
    rounded: "4px"
  badge-soon:
    backgroundColor: "rgba(255,255,255,0.07)"
    textColor: "{colors.muted}"
    rounded: "4px"
---

## Overview

A dark, tool-focused platform for creators and makers. The aesthetic is that of a professional software dashboard — something a solo builder would leave open all day. There is no marketing, no gradients, no hero animations. The chrome recedes; the tools take center stage.

The UI references high-quality developer tools (Linear, Vercel, Raycast) rather than consumer apps. Dark by default — not "dark mode", this is the native environment. Surfaces are near-black with slight blue-grey undertones, not warm charcoal.

The accent color `{colors.accent}` (a muted indigo-violet) is the single interactive color. It appears on primary actions, active states, and focus rings only. It should feel calm, not aggressive.

## Colors

Near-black page canvas `{colors.bg}` with a slight blue cast — cooler than pure black, warmer than a terminal. Surfaces step up in lightness in two increments: `{colors.surface}` for cards/panels, `{colors.surface-2}` for inputs and nested backgrounds.

- **bg** `{colors.bg}` — page background. Nothing sits behind this.
- **surface** `{colors.surface}` — cards, panels, the nav bar background (with blur). Barely distinguishable from bg in isolation; the contrast only reads as depth within context.
- **surface-2** `{colors.surface-2}` — inputs, chip defaults, code backgrounds, nested containers within cards.
- **border** `{colors.border}` — all dividing lines. Intentionally very faint (7% white). Borders separate without shouting.
- **accent** `{colors.accent}` — the only interactive color. Primary buttons, active chips, focus rings, progress fills, logo accent. Do not use it decoratively.
- **accent-dim** `{colors.accent-dim}` — background tint for active/hover states on cards. Not a button color.
- **text** `{colors.text}` — all body copy, headings, active UI labels. Slightly blue-warm, not pure white.
- **muted** `{colors.muted}` — placeholders, metadata, inactive nav items, secondary descriptions. Never used for anything interactive.
- **success** `{colors.success}` — completion states, green status dots only.
- **error** `{colors.error}` — error messages and error borders only.

## Typography

Single font family throughout: Inter. No display typefaces, no serifs.

Weight is the primary way to create hierarchy — not size. A 14px bold label reads as a heading; a 14px regular reads as body. Size differences are kept small (10px–28px range for UI, never larger except the hero headline).

- **h1** — hero headline only. Large, tight letter-spacing, high weight. One per page.
- **h3** — card titles, section labels. 14px / 600. No letter-spacing.
- **body** — default for all readable content. 14px / 400 / 1.6 line-height.
- **label** — field labels, section headers above chips. ALL CAPS, 10px, 600 weight, wide tracking. Creates structure without competing with content.
- **nav** — navigation buttons. 13.5px / 500. Slightly smaller than body to let content win.
- **caption** — tool descriptions, metadata, secondary copy. 12px / 400 / {colors.muted}.

## Layout

Fixed-top navigation bar at 56px height. All page content begins below it (`padding-top: 56px`). The nav contains: logo left, nav items center-left, status/metadata right.

Pages are full-viewport-height below the nav. Tool pages use a two-zone layout: a slim topbar (branded to the specific tool, ~44px) and a scrollable body area.

Content within the body area is centered with `max-width: 600px` for forms and single-column interfaces. No sidebars. Tools are focused, not dashboards.

Horizontal padding: 24px on all containers. Internal card padding: 36px.

Grid: 4px base. All spacing values are multiples: 4, 8, 12, 16, 24, 36, 48.

## Elevation & Depth

Three levels only:
1. **Page** — `{colors.bg}`, no shadow
2. **Card** — `{colors.surface}`, 1px `{colors.border}` border. No box-shadow on cards — the border provides the separation.
3. **Dropdown / Float** — `#13131b`, 1px `{colors.border}` border, `box-shadow: 0 24px 64px rgba(0,0,0,0.6)`. The heavy shadow is the only place shadows appear.

The nav bar uses `backdrop-filter: blur(16px)` and the `{components.nav-bar.backgroundColor}` semi-transparent background. This is the only blur in the UI.

## Shapes

Rounded corners only — no sharp edges anywhere in the product.

- Pills `{rounded.pill}` — chips, badges, status tags
- Large `{rounded.xl}` — main content cards (the primary canvas)
- Default `{rounded.lg}` — dropdowns, modals, image previews
- Medium `{rounded.md}` — buttons, inputs, smaller cards, tool icon frames
- Small `{rounded.sm}` — nav buttons, inline tags

## Components

**Navigation bar** — Frosted glass effect. Logo (icon + wordmark) left, nav items in a row, status right. Nav items show a subtle background on hover. Active items have the same background permanently. Dropdowns open on hover with a 180ms ease transition. The chevron icon rotates 180° when open.

**Dropdown** — Opens below the nav item with an 8px gap. Rounded 16px. Contains a section header in label style, then tool cards with icon + name + description. Coming-soon items are shown at 40% opacity, non-interactive. Smooth appear/disappear with translateY(-6px) → 0 and opacity 0 → 1.

**Tool card (in dropdown)** — 36px square icon with a rounded border, name in h3, description in caption. Full row is clickable. Hover: subtle `rgba(255,255,255,0.05)` background. Active: `{colors.accent-dim}` background.

**Home tool card** — Larger version for the landing page grid. Emoji icon, name, one-line description. Hover: accent border glow. Dimmed + non-interactive for "coming soon" tools.

**Primary button** — Full accent fill. On hover: `brightness(1.1)` + `box-shadow: 0 4px 24px {colors.accent-dim}`. Disabled: 40% opacity, not clickable. Never outlined, never ghost.

**Secondary button** — `{colors.surface-2}` fill, border, muted text. Hover: accent border + accent-dim background. Used for secondary actions next to the primary (download, new video, etc.).

**Chip** — Pill-shaped toggle. Default: `{colors.surface-2}` bg, `{colors.muted}` text. Active: `{colors.accent}` bg, white text, subtle glow ring. Used for selecting options (aspect ratio, language). Never used as navigation.

**Input / Textarea** — Matches chip background `{colors.surface-2}`. Border becomes `{colors.accent}` on focus with a `0 0 0 3px {colors.accent-dim}` glow ring. Placeholder text in `{colors.muted}`. No label inside the input — labels are always above in label style.

**Progress bar** — 3px tall track in `{colors.surface-2}`. Fill in `{colors.accent}`. Indeterminate state: fixed-width fill animates across the track. Determinate: smooth CSS transition on width. Never circular spinners.

**Status dot** — 7px circle in `{colors.success}` with a 2s pulse animation. Appears in the nav right area to indicate "live" status.

**Badges** — Two types: `NEW` in accent colors, `SOON` in muted. Small (10px), 4px radius, all-caps. Appear inline next to tool names or nav items. Never standalone decorative elements.

## Do's and Don'ts

**Do:**
- Use `{colors.accent}` for exactly one primary action per screen
- Keep surface differences subtle — the UI should feel like one material
- Use label-style (CAPS, small, tracked) text for all field labels and section headers
- Let whitespace do the separating — trust spacing over decorative dividers
- Show "coming soon" tools dimmed and non-interactive rather than hiding them

**Don't:**
- Use gradients anywhere except the hero wordmark text-clip gradient (one exception)
- Add decorative borders, shadows, or glows that don't carry semantic meaning
- Use `{colors.accent}` decoratively — it must always signal interactivity
- Create new surface levels beyond the three defined above
- Use different font families — Inter only, everywhere
- Build modals or overlays — keep all UI inline and within-page

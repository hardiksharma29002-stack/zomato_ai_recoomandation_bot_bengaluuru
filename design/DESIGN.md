---
name: Zomato AI Design System
colors:
  surface: '#051424'
  surface-dim: '#051424'
  surface-bright: '#2c3a4c'
  surface-container-lowest: '#010f1f'
  surface-container-low: '#0d1c2d'
  surface-container: '#122131'
  surface-container-high: '#1c2b3c'
  surface-container-highest: '#273647'
  on-surface: '#d4e4fa'
  on-surface-variant: '#e4bebc'
  inverse-surface: '#d4e4fa'
  inverse-on-surface: '#233143'
  outline: '#ab8987'
  outline-variant: '#5b403f'
  surface-tint: '#ffb3b1'
  primary: '#ffb3b1'
  on-primary: '#680011'
  primary-container: '#ff535a'
  on-primary-container: '#5b000e'
  inverse-primary: '#bb162c'
  secondary: '#c8c6c5'
  on-secondary: '#313030'
  secondary-container: '#4a4949'
  on-secondary-container: '#bab8b7'
  tertiary: '#4ae183'
  on-tertiary: '#003919'
  tertiary-container: '#00a657'
  on-tertiary-container: '#003115'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#e5e2e1'
  secondary-fixed-dim: '#c8c6c5'
  on-secondary-fixed: '#1c1b1b'
  on-secondary-fixed-variant: '#474646'
  tertiary-fixed: '#6bfe9c'
  tertiary-fixed-dim: '#4ae183'
  on-tertiary-fixed: '#00210c'
  on-tertiary-fixed-variant: '#005228'
  background: '#051424'
  on-background: '#d4e4fa'
  surface-variant: '#273647'
typography:
  display-lg:
    fontFamily: Outfit
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Outfit
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Outfit
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
  headline-md:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 40px
  xl: 64px
  container-max: 1200px
  gutter: 20px
---

## Brand & Style
The design system is engineered to feel like a high-end concierge service—sophisticated, intelligent, and appetizing. It targets food enthusiasts who value both speed and curation. The aesthetic merges **Modern Corporate** precision with **Glassmorphism**, creating a layered interface that feels deep and immersive. 

The emotional response is one of "effortless discovery." By utilizing deep charcoals and translucent surfaces, the UI recedes to let high-quality food photography take center stage, while the signature crimson maintains a strong brand connection and triggers appetite.

## Colors
The palette is rooted in a "Deep Slate" dark mode to provide a premium backdrop. 
- **Primary (Crimson):** Used for critical actions, brand presence, and highlighting "Hero" recommendations.
- **Surface (Charcoal/Slate):** A range of grays from `#0F172A` (base) to `#1E293B` (elevated cards) provides structure without the harshness of pure black.
- **Status (Vibrant):** Rating badges use a high-chroma palette—`#2ECC71` (Success/High Rating) and `#F1C40F` (Warning/Average Rating)—to ensure they pop against dark backgrounds.
- **Glass Effects:** Translucent layers use white or primary color overlays at 5-10% opacity with a 20px background blur.

## Typography
This design system employs a dual-font strategy to balance character with utility. **Outfit** is used for headlines to provide a modern, geometric, and premium feel. Its tight tracking at larger sizes creates a confident, editorial look. **Inter** is used for all functional text, body copy, and UI labels to ensure maximum legibility at small sizes and high-density data views. Contrast is achieved through weight—headlines should rarely go below Semi-Bold (600).

## Layout & Spacing
The layout follows a **Fluid Grid** logic with a focus on generous internal padding to support the "high-end" feel. 
- **Mobile:** 4-column grid with 16px margins. Elements usually span the full width or 2 columns.
- **Desktop:** 12-column grid with a 1200px max-width container. 
Spacing follows an 8px scale, but 4px increments are allowed for tight component grouping (e.g., icons next to text labels). Large vertical gaps (40px+) are encouraged between different sections of the AI's recommendations to prevent cognitive overload.

## Elevation & Depth
Depth is created through **Glassmorphism** and subtle, colored shadows rather than traditional gray-scale shadows.
- **Level 1 (Base):** Deep Slate background.
- **Level 2 (Cards/Surfaces):** Translucent background (10% white overlay) with a 16px background blur. A 1px subtle inner border (stroke) at 10% white adds definition.
- **Level 3 (Modals/Popovers):** Higher opacity glass with a 32px blur and a "Crimson Glow" shadow—an ambient shadow tinted with the primary color at very low (5%) opacity to simulate light reflection from the UI elements.

## Shapes
The shape language is overtly friendly and modern. In this design system, `rounded-2xl` is the default for all major containers and restaurant cards, creating a soft, approachable silhouette. 
- **Buttons & Chips:** Use the "Pill" (full round) approach for a tactile, touch-friendly feel.
- **Interactive Inputs:** Follow the `rounded-lg` (1rem) standard to maintain structural integrity.

## Components
- **Buttons:** Primary buttons are solid Crimson (#E23744) with white text. Secondary buttons use a glass background with a white stroke.
- **AI Recommendation Cards:** Use `rounded-xl` corners, a glassmorphic background, and a "Crimson-to-Transparent" gradient border to signify AI-generated content.
- **Rating Badges:** Small, pill-shaped containers with high-saturation backgrounds (Green #2ECC71) and bold white typography.
- **Lists:** High-density lists use subtle 1px dividers in Slate-800. Each list item should have a minimum tap target height of 48px.
- **Input Fields:** Search bars should be prominent, featuring a glass effect and an icon-prefix. The focus state uses a 2px Crimson glow.
- **Chips/Filters:** Pill-shaped, using a dark gray background when inactive and solid Crimson when active.
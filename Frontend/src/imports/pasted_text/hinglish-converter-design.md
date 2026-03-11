Design a modern, user-friendly web application for converting Hinglish (Hindi + English mixed text) into three outputs: Hindi (Devanagari), Finglish (Roman Hindi), and English translation.

Design Style & Theme
Visual Identity:

Style: Modern, clean, minimalist with subtle Indian cultural elements
Aesthetic: Professional yet approachable, emphasizing clarity and readability
Color Palette:
Primary: Vibrant saffron/orange gradient (#FF6B35 → #F7931E) — represents Indian flag colors
Secondary: Deep indigo/blue (#4A5568 → #2D3748)
Accent: Emerald green (#10B981) for success states
Background: Soft warm white (#FAFAF9) or light cream (#FFF8F3)
Text: Dark charcoal (#1A202C) for primary, gray (#4A5568) for secondary
Typography:
Headings: Poppins Bold (modern, supports Devanagari)
Body text: Inter Regular/Medium
Hindi text: Noto Sans Devanagari
Monospace output: JetBrains Mono for code-like display
Layout Structure
Hero Section (Top ~40% of viewport):

Large, centered heading: "Indian Language Converter"
Subheading: "Transform Hinglish into Hindi, Finglish & English instantly"
Decorative background: Subtle geometric patterns inspired by Indian rangoli (very light, ~5% opacity)
Floating illustration: Abstract representation of text transformation (input → output arrows)
Main Input Area:

Large text area with placeholder: "Type your Hinglish text here... (e.g., 'kal meeting hai office me')"
Character counter in bottom-right corner
Rounded corners (12px), subtle shadow, focus state with glowing border
Sample text button: "Try Example" — fills textarea with demo text
Clear button (X icon) in top-right when text is present
Action Button:

Prominent "Convert" button below input
Width: 200px, Height: 48px
Gradient background (saffron to orange)
Icon: Arrow pointing right or sparkle icon
Hover state: Slight elevation + darker gradient
Loading state: Animated spinner replaces icon
Output Section (Cards Layout)
Create three beautiful output cards arranged horizontally (desktop) or stacked (mobile):

Card 1: Hindi (हिंदी)

Header with Devanagari icon/symbol
Output text in large, readable Devanagari font (20px)
Background: Light gradient (cream to white)
Copy button in top-right corner
Visual indicator: Small Indian flag colors in corner decoration
Card 2: Finglish (Roman Hindi)

Header with Roman script icon
Output text in clean sans-serif (18px)
Background: Soft blue-gray gradient
Copy button in top-right corner
Visual indicator: Dotted border pattern
Card 3: English Translation

Header with English/translation icon
Output text in professional font (18px)
Background: Light green to white gradient
Copy button in top-right corner
Visual indicator: Small globe or translation icon
Card Specifications:

Each card:
Min-height: 200px
Border-radius: 16px
Box-shadow: 0 4px 12px rgba(0,0,0,0.08)
Padding: 24px
Hover effect: Subtle lift (translate Y -4px)
Additional UI Elements
Top Navigation Bar:

Logo on left: Stylized "LC" or language symbols intertwined
Nav items: Home | About | API Docs | GitHub
Dark/Light mode toggle on right
Sticky on scroll with backdrop blur
Features Section (Below fold):
Three feature cards with icons:

"🚀 Instant Conversion" — Lightning-fast NLP processing
"🔒 100% Offline" — No data sent to external servers
"🎯 Accurate Results" — ML-powered transliteration & translation
How It Works Section:
Visual flow diagram with numbered steps:

Input Hinglish → 2. AI Processing → 3. Three Outputs
Use gentle connecting arrows with gradient colors
Footer:

Minimal design with links (Privacy | Terms | Contact)
Built with FastAPI + Transformers badge
Social media icons
Interactions & Animations
Input to Output Flow:

When "Convert" is clicked, show loading dots animation
Output cards slide up from bottom with staggered timing (0.1s delay between each)
Text fade-in animation as it appears
Copy Button States:

Default: Light gray outline button
Hover: Filled with primary color
Clicked: Show "Copied!" tooltip for 2 seconds + checkmark animation
Micro-interactions:

Button hover: Subtle scale (1.02) and shadow increase
Card hover: Lift effect with enhanced shadow
Input focus: Glowing border animation (pulse once)
Responsive Breakpoints
Desktop (1200px+):

Three output cards side-by-side
Hero section with illustration on right
Tablet (768px - 1199px):

Output cards in 2-column grid (3rd card full width below)
Smaller hero section
Mobile (< 768px):

Single column layout
Stacked output cards
Floating "Convert" button
Collapsible example text
Component States to Design
Empty State: Before any conversion (show example prompts)
Loading State: Animated spinner + "Processing..." text
Success State: All three outputs populated
Error State: Red banner with error message + retry button
Dark Mode: Alternative color scheme (navy bg, cream text)
Accessibility Requirements
High contrast ratios (WCAG AA compliant)
Clear focus indicators for keyboard navigation
Screen reader labels for all interactive elements
Font size minimum: 16px for body text
Touch targets: Minimum 44x44px
Key Design Files to Create
Landing page with hero + converter interface
Output cards component (3 variations)
Loading states and animations
Mobile responsive views
Dark mode variant
Component library (buttons, inputs, cards)
Inspiration References
Google Translate (clean, functional)
Notion (modern, spacious)
Linear (gradient accents, smooth animations)
Add subtle Indian design elements (patterns, colors) without being overwhelming

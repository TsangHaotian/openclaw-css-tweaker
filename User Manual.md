# OpenClaw Frontend Interface Customization Guide

This tutorial will guide you through modifying OpenClaw's interface styles, including: background images, navbar colors, sidebar colors, chat bubble colors, button colors, avatars, and more.

---

## 1. Prerequisites

1. Locate the CSS file to modify

   `C:\Users\Users\AppData\Roaming\npm\node_modules\openclaw-cn\dist\control-ui\assets\index-wLSqyTVo.css`

   **Recommendation**: Backup the original file before modifying, so you can restore it if something goes wrong.

---

## 2. Modify Global Background Image

Find the `.shell` style rule and add the following code at the end:

```css
.shell {
    /* ... Keep existing code unchanged ... */

    /* New background image */
    background-image: url('background.png');  /* Change to your image path */
    background-size: cover;                  /* Cover entire area */
    background-position: center;             /* Center the image */
    background-repeat: no-repeat;            /* No repeat tiling */
}
```

> 💡 **Tip**: Replace `background.png` with your own image filename, and make sure the image is in the correct folder.

---

## 3. Modify Top Navigation Bar Color

Find the `.topbar` style rule and modify the `background` property:

```css
.topbar {
    /* ... Keep existing code unchanged ... */
    background: rgba(255, 192, 203, 0.5);  /* Pink, 50% transparency */
}
```

---

## 4. Modify Sidebar (Left Navigation) Color

Find the `.nav` style rule and modify the `background` property:

```css
.nav {
    /* ... Keep existing code unchanged ... */
    background: rgba(255, 192, 203, 0.5) !important;  /* Pink, 50% transparency */
}
```

---

## 5. Modify AI Reply Bubble Colors

### 5.1 Modify Reply Bubble Background Color

```css
.chat-bubble.has-copy {
    padding-right: 36px;
    background: rgba(0, 120, 255, 0.3);  /* Blue, 30% transparency */
}
```

### 5.2 Modify Copy Button Color Inside Bubble (Shown on Hover)

```css
.chat-bubble:hover .chat-copy-btn {
    opacity: 1;
    background: rgba(238, 5, 5, 0.3);  /* Red, 30% transparency */
    pointer-events: auto;
}
```

### 5.3 Modify Bubble Background Color on Hover

```css
.chat-bubble:hover {
    background: rgba(238, 5, 5, 0.3);  /* Red, 30% transparency */
}
```

### 5.4 Modify File Operation Reply Box Background Color

```css
.chat-bubble {
    border: 1px solid transparent;
    background: rgba(94, 5, 238, 0.3);  /* Purple, 30% transparency */
    border-radius: var(--radius-lg);
    padding: 10px 14px;
    min-width: 0;
}
```

### 5.5 Modify File Operation Card Internal Background Color

```css
.chat-tool-card {
    margin-top: 8px;
    padding: 10px 12px;
    border-radius: var(--radius-md);
    border: 1px solid var(--border);
    background: rgba(5, 238, 44, 0.3);  /* Green, 30% transparency */
    display: grid;
    gap: 4px;
}
```

### 5.6 Modify File Operation Card Background Color on Hover

```css
.chat-tool-card:hover {
    border-color: var(--border-strong);
    background: rgba(234, 238, 5, 0.3);  /* Yellow, 30% transparency */
}
```

---

## 6. Modify User Sent Bubble Colors

### 6.1 Modify User Bubble Background Color

```css
.chat-group.user .chat-bubble {
    background: rgba(5, 238, 36, 0.3);  /* Green, 30% transparency */
    border-color: transparent;
}
```

### 6.2 Modify User Bubble Background Color on Hover

```css
.chat-group.user .chat-bubble:hover {
    background: rgba(94, 5, 238, 0.3);  /* Purple, 30% transparency */
}
```

---

## 7. Modify Global Card Color (Affects Multiple Areas)

Find the `--card` variable at the beginning of the CSS file in `:root` or `html`:

```css
:root {
    --card: rgba(5, 238, 55, 0.3);  /* Green, 30% transparency */
    --card-foreground: #f4f4f5;
    --card-highlight: rgba(255, 255, 255, .05);
}
```

> ⚠️ **Note**: Modifying `--card` will affect background colors in multiple areas, including the left sidebar cards and user input box. Please adjust with caution.

---

## 8. Modify Bottom Input Area

### 8.1 Make Input Area Background Fully Transparent

```css
.chat-compose {
    position: sticky;
    bottom: 0;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: auto;
    padding: 12px 4px 4px;
    background: transparent !important;  /* Fully transparent */
    z-index: 10;
}
```

### 8.2 Modify Input Box Background Color

```css
.chat-compose .chat-compose__field textarea {
    width: 100%;
    min-height: 40px;
    height: auto;
    max-height: clamp(160px, 50vh, 320px);
    overflow-y: auto;
    padding: 9px 12px;
    border-radius: 8px;
    resize: vertical;
    white-space: pre-wrap;
    font-family: var(--font-body);
    font-size: 14px;
    line-height: 1.45;
    background: rgba(216, 9, 44, 0.3) !important;  /* Dark red, 30% transparency */
}
```

---

## 9. Modify Button Colors (New Session, Send Button)

```css
.chat-compose .chat-compose__actions .btn {
    padding: 0 16px;
    font-size: 13px;
    height: 40px;
    min-height: 40px;
    max-height: 40px;
    line-height: 1;
    white-space: nowrap;
    background: rgba(236, 233, 6, 0.3);  /* Semi-transparent yellow */
    box-sizing: border-box;
}
```

---

## 10. Modify Avatars (AI and User)

Replace the `.chat-avatar` related styles completely:

```css
.chat-avatar {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    background: var(--panel-strong);
    display: grid;
    place-items: center;
    font-weight: 600;
    font-size: 0;           /* Hide default text */
    flex-shrink: 0;
    align-self: flex-end;
    margin-bottom: 4px;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

/* User avatar */
.chat-avatar.user {
    background: var(--accent-subtle);
    color: var(--accent);
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-image: url('user.webp');  /* Replace with your user avatar */
}

/* AI/Assistant/Tool avatar */
.chat-avatar.assistant,
.chat-avatar.other,
.chat-avatar.tool {
    background: var(--secondary);
    color: var(--muted);
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-image: url('ai.png');     /* Replace with your AI avatar */
}

/* If using img tag avatars */
img.chat-avatar {
    display: block;
    object-fit: cover;
    object-position: center;
}
```

> 💡 **Tip**: Replace `user.webp` and `ai.png` with your own image filenames.

---

## Quick Color Reference Table

| Color | RGBA Value |
|:---|:---|
| Pink | `rgba(255, 192, 203, 0.5)` |
| Blue | `rgba(0, 120, 255, 0.3)` |
| Red | `rgba(238, 5, 5, 0.3)` |
| Green | `rgba(5, 238, 36, 0.3)` |
| Purple | `rgba(94, 5, 238, 0.3)` |
| Yellow | `rgba(236, 233, 6, 0.3)` |
| Dark Red | `rgba(216, 9, 44, 0.3)` |
| Transparent | `transparent` |

---

## Transparency Adjustment Guide

- `0.1` = 10% transparency (very light)
- `0.3` = 30% transparency (moderate, recommended)
- `0.5` = 50% transparency (semi-transparent)
- `0.7` = 70% transparency (more noticeable)
- `0.9` = 90% transparency (close to solid color)

---

## FAQ

### Q: Changes have no effect?

1. Check if the file was saved
2. Refresh the browser (Ctrl+F5 for hard refresh)
3. Check if the CSS selector is correct
4. Check if `!important` is being overridden by other styles

### Q: Image not displaying?

1. Confirm the image path is correct
2. Confirm the image filename case matches
3. Confirm the image format is supported (jpg, png, webp, svg, etc.)

### Q: Want to revert to original colors?

Restore from backup file, or simply delete the added code.

---

## Tutorial End

Happy customizing! 🎉

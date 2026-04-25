# openclaw-css-tweaker

🎨 A simple and easy-to-use OpenClaw interface customization tool. No need to understand CSS syntax - modify colors with just a few clicks in the graphical interface.

Before using, it is recommended to manually import the CSS file from the documentation to your local environment and replace it first. Otherwise, you may encounter issues where CSS modifications are not recognized.

---


## 
<img width="1919" height="1036" alt="image" src="https://github.com/user-attachments/assets/fb90a4eb-55b9-4fd2-9277-fc06e3f6d637" />



## Features

- 🖱️ **Graphical Interface** - Just click the mouse to modify, no coding required
- 🎨 **Multiple Color Options** - Color picker, 10 preset colors, transparency slider
- 🖼️ **Image Support** - Modify background images, AI avatars, user avatars
- 📝 **Real-time Preview** - Instantly display CSS code modification effects
- 🔄 **Safe & Reliable** - Reset function to restore original state
- ✨ **Modern UI** - Rounded design style, dark theme for eye comfort

---

## Supported Elements

| Category | Modifiable Items |
|:---|:---|
| **Global Styles** | Background Image, Top Navigation Bar, Sidebar, Global Card Color |
| **AI Reply Area** | AI Reply Bubble, Copy Button (Hover), AI Bubble (Hover), File Operation Box, Tool Card, Tool Card (Hover) |
| **User Area** | User Bubble, User Bubble (Hover), User Avatar, AI Avatar |
| **Input Area** | Input Area Background, Input Box, Action Buttons |

Supports modification of **17** interface elements.

---

## How to Use

### 1. Preparation

Locate the OpenClaw CSS file at:

```
C:\Users\<Your Username>\AppData\Roaming\npm\node_modules\openclaw-cn\dist\control-ui\assets\index-*.css
```

> ⚠️ **Note**: It is recommended to backup the original file before modifying.

### 2. Import CSS File

1. Click the **📁 Import CSS** button at the top of the tool
2. Select the CSS file from the path above
3. After successful import, the left panel will display all modifiable items

### 3. Select Element to Modify

1. Click on the item you want to modify in the left category list
2. The right panel will show the current configuration of that element
3. Color-editable items will display the color editing area
4. Image-supporting items will display the image selection area

### 4. Modify Colors

1. **Color Picker**: Click the 🎨 Color Picker button and select a color from the color chooser
2. **Preset Colors**: Click preset color buttons for quick selection (Pink, Blue, Red, etc. - 10 colors in total)
3. **Transparency**: Drag the transparency slider to adjust transparency (0%-100%)

### 5. Modify Images

1. Click the **📁 Select Image** button
2. Select an image file (supports PNG, JPG, WebP, GIF, SVG formats)
3. The selected image filename will be displayed in the input field

### 6. Apply and Save

1. Click the **✅ Apply Changes** button to apply modifications
2. Click the **💾 Save CSS** button to save the file
3. Replace the original CSS file with the saved file

### 7. Reset

If you are not satisfied with the modifications, click the **🔄 Reset** button to restore to the original state when imported.

---

## Preset Color Reference

| Color | Hex Value |
|:---|:---|
| Pink | #FFC0CB |
| Blue | #0078FF |
| Red | #EE0505 |
| Green | #05EE24 |
| Purple | #5E05EE |
| Yellow | #ECE906 |
| Dark Red | #D8092C |
| Orange | #FF8C00 |
| Cyan | #00CED1 |
| White | #FFFFFF |

---

## Transparency Guide

- `0.1` = 10% transparency (very light)
- `0.3` = 30% transparency (moderate, recommended)
- `0.5` = 50% transparency (semi-transparent)
- `0.7` = 70% transparency (more noticeable)
- `0.9` = 90% transparency (close to solid color)

---

## How to Run

### Method 1: Run Python Script Directly

```bash
python main.py
```

Requires Python 3.7+ environment and tkinter (usually installed with Python).

### Method 2: Run Packaged EXE

Double-click to run `dist/OpenClaw-CSS-Customization-Tool.exe`

---

## Project Info

- **Version**: v2.1
- **Author**: TsangHaotian
- **GitHub**: https://github.com/TsangHaotian/openclaw-css-tweaker

---

## FAQ

### Q: Changes have no effect?

1. Confirm that the CSS file was saved
2. Confirm that the correct CSS file was replaced
3. Refresh the browser (Ctrl+F5 for hard refresh)
4. Check if `!important` is being overridden by other styles

### Q: Want to restore original styles?

1. Use the tool's **🔄 Reset** function
2. Or restore from backup file

---

## Changelog

### v2.1
- Added "About" dialog, showing author and GitHub link
- UI optimization, all buttons changed to rounded modern style
- Fixed color preview compatibility issues

### v2.0
- Supports modification of 17 interface elements
- Supports color picker and transparency adjustment
- Supports image modification (background, avatars)
- Real-time CSS code preview
- Supports reset and save functions

---

Happy customizing! 🎉

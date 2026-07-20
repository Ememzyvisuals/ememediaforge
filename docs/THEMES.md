# EmemediaForge — Theme Guide

Four built-in themes ship with EmemediaForge. Set in `project.yaml`:

```yaml
theme: dark   # modern | light | dark | minimal
```

---

## `modern` — White + Purple

| Property  | Value                     |
|-----------|---------------------------|
| Background | `#FFFFFF` — pure white   |
| Accent     | `#7C3AED` — deep purple  |
| Text       | `#111827` — near-black   |
| Waveform   | Purple animated bars     |

Best for: HuggingFace model pages, professional LinkedIn posts, general demos.

---

## `light` — White + Electric Blue  *(NEW)*

| Property  | Value                         |
|-----------|-------------------------------|
| Background | `#FFFFFF` — pure white       |
| Surface    | `#F0F4FF` — blue-tinted card |
| Accent     | `#2563EB` — electric blue    |
| Text       | `#0F172A` — Slate-900        |
| Waveform   | Blue animated bars           |

Best for: Academic demos, paper releases, clean professional content.
Matches HuggingFace's white UI perfectly.

---

## `dark` — Near-Black + Neon Green

| Property  | Value                        |
|-----------|------------------------------|
| Background | `#08080C` — near-black      |
| Accent     | `#00FF88` — neon green      |
| Text       | `#FFFFFF` — white           |
| Waveform   | Glowing green bars          |

Best for: AI model launches, tech Twitter/X, NaijaVox, Africlaude demos.
The highest visual impact theme — great for viral content.

---

## `minimal` — Off-White + Black

| Property  | Value                        |
|-----------|------------------------------|
| Background | `#FAFAFA` — off-white       |
| Accent     | `#000000` — pure black      |
| Text       | `#000000` — black           |
| Waveform   | Black animated bars         |

Best for: Academic content, conservative audiences, print-adjacent demos.

---

## Custom Themes (Programmatic)

```python
from ememediaforge.themes.base import Theme
from ememediaforge.core.pipeline import run_pipeline

MY_THEME = Theme(
    name="axiveri",
    bg_color=(5, 5, 20),
    surface_color=(15, 15, 35),
    accent_color=(255, 100, 0),       # orange accent
    accent_dim=(180, 60, 0),
    text_primary=(255, 255, 255),
    text_secondary=(160, 160, 180),
    word_active=(255, 100, 0),
    word_past=(80, 80, 100),
    word_future=(40, 40, 60),
    waveform_color=(255, 100, 0),
    progress_color=(200, 80, 0),
    overlay_color=(5, 5, 20, 200),
)

# Pass directly to pipeline (bypasses theme name validation)
from ememediaforge.config.loader import load_config
config = load_config("project.yaml")
run_pipeline(config, theme_override=MY_THEME)
```

*(Custom theme YAML support coming in v1.1)*

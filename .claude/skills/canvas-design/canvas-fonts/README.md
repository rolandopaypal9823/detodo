# canvas-fonts

Tipografías locales para el skill `canvas-design`. Todas OFL (Google Fonts).

| Familia | Pesos | Uso sugerido |
|---|---|---|
| Inter | 200 / 300 / 400 / 600 / 700 | etiquetas clínicas, sans neutra |
| Space Grotesk | 300 / 500 / 700 | titulares, gestos tipográficos |
| EB Garamond | 400 / 500 / 400 italic | serif de contrapunto, notas al pie |
| JetBrains Mono | 200 / 400 | marcadores de referencia, coordenadas, datos |

Cargar en matplotlib:

```python
from matplotlib import font_manager
for f in Path("canvas-fonts").glob("*.ttf"):
    font_manager.fontManager.addfont(str(f))
```

# GitHub Pages Deployment Architecture

## Deployment Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     Developer Push to GitHub                     │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   GitHub Actions Triggered                       │
│  (.github/workflows/deploy.yml)                                 │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Build Job                                  │
│  1. Checkout code                                               │
│  2. Setup Python 3.11                                           │
│  3. Install Pygbag                                              │
│  4. Run: pygbag --build .                                       │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Pygbag Build Process                          │
│                                                                  │
│  Python/Pygame Code                                             │
│         │                                                        │
│         ├──> Emscripten (Python to WASM)                       │
│         ├──> Bundle Assets                                      │
│         ├──> Generate Web HTML/JS                               │
│         └──> Output: ./build/web/                               │
│                                                                  │
│  Result: Browser-ready WebAssembly package                      │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Upload to Pages                               │
│  ./build/web/ → GitHub Pages Artifact                           │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Deploy Job                                  │
│  Deploy artifact to GitHub Pages                                │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   GitHub Pages (Live!)                           │
│  https://username.github.io/repo/                               │
│                                                                  │
│  Files served:                                                   │
│  - index.html (landing page)                                    │
│  - *.wasm (game code)                                           │
│  - *.js (Pygame/Emscripten runtime)                            │
│  - *.data (game assets)                                         │
└─────────────────────────────────────────────────────────────────┘
```

## File Structure After Build

```
Repository Root
├── main.py (async version)
├── config.py
├── core/
├── systems/
├── content/
├── ui/
├── index.html (landing page)
└── .github/
    └── workflows/
        └── deploy.yml

After Pygbag Build (not in repo):
└── build/
    └── web/
        ├── index.html (game iframe)
        ├── main.wasm (compiled game)
        ├── pygame.js (runtime)
        ├── python*.wasm (Python interpreter)
        └── *.data (game files)
```

## Browser Loading Process

```
User visits URL
      │
      ▼
Landing Page (index.html) loads
      │
      ├─> Shows game info
      ├─> Shows controls
      └─> Loads game in iframe
            │
            ▼
      Game index.html loads
            │
            ├─> Load WASM modules
            ├─> Initialize Python interpreter
            ├─> Load Pygame
            ├─> Run main() coroutine
            └─> Game starts!
```

## Key Technologies

- **Pygbag**: Python to WebAssembly compiler for Pygame
- **Emscripten**: C/C++/Python to WebAssembly toolchain
- **WebAssembly (WASM)**: Binary instruction format for web
- **GitHub Actions**: CI/CD automation
- **GitHub Pages**: Static site hosting

## Async Requirement

```python
# Desktop version (old):
def main():
    while running:
        # game loop
        pass

# Web version (new):
async def main():
    while running:
        # game loop
        await asyncio.sleep(0)  # Yield to browser
```

The `await asyncio.sleep(0)` is crucial - it yields control back to the browser event loop, preventing the page from freezing.

## Performance Notes

- First load: ~10-30 seconds (downloading WASM modules)
- Subsequent loads: Fast (cached)
- Runtime: ~60 FPS (same as desktop)
- File size: ~20-30 MB total (Python + Pygame + game)

## Browser Compatibility

| Browser | Support | Notes |
|---------|---------|-------|
| Chrome  | ✅ Excellent | Recommended |
| Firefox | ✅ Excellent | Recommended |
| Safari  | ✅ Good | May be slower |
| Edge    | ✅ Excellent | Chromium-based |
| Mobile  | ⚠️ Limited | Touch controls differ |

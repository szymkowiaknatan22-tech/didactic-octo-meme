# GitHub Pages Setup Guide

This guide will help you enable GitHub Pages for the Fractured Depths game.

## Quick Setup (3 Steps)

### 1. Enable GitHub Pages

1. Go to your repository on GitHub: https://github.com/szymkowiaknatan22-tech/didactic-octo-meme
2. Click on **Settings** (top menu)
3. In the left sidebar, click **Pages**
4. Under "Build and deployment":
   - **Source**: Select **GitHub Actions** (not "Deploy from a branch")
5. Click **Save** if prompted

### 2. Trigger the Deployment

The workflow will automatically run when:
- You push to the `main` or `copilot/add-complete-fractured-depths-game` branch
- You can also manually trigger it:
  1. Go to **Actions** tab
  2. Click on "Deploy to GitHub Pages" workflow
  3. Click "Run workflow" button

### 3. Wait for Build to Complete

1. Go to the **Actions** tab to watch the build progress
2. Wait for the green checkmark (typically 2-3 minutes)
3. Your game will be live at: **https://szymkowiaknatan22-tech.github.io/didactic-octo-meme/**

## Verification

Once deployed, you should see:
- ✅ Green checkmark in Actions tab
- ✅ "github-pages" deployment in the deployment section
- ✅ Game accessible at the URL above

## Troubleshooting

### Build Fails
- Check the Actions logs for specific errors
- Ensure Python dependencies are correct
- Verify Pygbag is compatible with the code

### 404 Error
- Wait a few minutes after deployment
- Check that GitHub Pages is set to "GitHub Actions" mode (not branch)
- Verify the workflow completed successfully

### Game Doesn't Load
- Check browser console for errors (F12)
- Try a different browser (Chrome recommended)
- Clear browser cache and reload

## How It Works

1. **GitHub Actions Workflow** (`/.github/workflows/deploy.yml`):
   - Checks out the code
   - Installs Python and Pygbag
   - Builds the game to WebAssembly
   - Uploads to GitHub Pages

2. **Pygbag Build**:
   - Converts Python/Pygame code to WebAssembly
   - Creates browser-compatible game package
   - Includes all assets and dependencies

3. **Landing Page** (`/index.html`):
   - Provides game information
   - Embeds the game in an iframe
   - Shows controls and instructions

## Manual Build (Optional)

To build locally:

```bash
# Install Pygbag
pip install pygbag

# Build the game
pygbag --build .

# Output will be in: ./build/web/
# Open ./build/web/index.html in a browser to test
```

## Updating the Game

Just push changes to your branch - the workflow will automatically rebuild and redeploy!

## Links

- **Live Game**: https://szymkowiaknatan22-tech.github.io/didactic-octo-meme/
- **Repository**: https://github.com/szymkowiaknatan22-tech/didactic-octo-meme
- **Pygbag Documentation**: https://github.com/pygame-web/pygbag

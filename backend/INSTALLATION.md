# Installation Guide

## Python Version Requirements

- **Python 3.9+**: Core features work (task management, charts, metrics)
- **Python 3.10+**: Full features including LLM integration (aisuite)

## Installation Steps

### Step 1: Check Python Version

```bash
python3 --version
```

**Current System**: Python 3.9.6
- ✅ Core features available
- ⚠️ LLM features require Python 3.10+ (optional)

### Step 2: Install Core Dependencies

For Python 3.9 (current system):
```bash
pip3 install -r requirements.txt
```

This installs:
- pandas (data manipulation)
- matplotlib (chart generation)
- python-dotenv (environment variables)
- python-dateutil (date parsing)
- pytest (testing)
- pytest-cov (coverage)

**Note**: `aisuite` is NOT included (requires Python 3.10+)

### Step 3: Install Full Dependencies (Python 3.10+ only)

If you have Python 3.10+ and want LLM features:
```bash
pip3 install -r requirements-full.txt
```

This includes `aisuite` for LLM integration.

## What Works Without aisuite

✅ **All Core Features Work:**
- Task creation, listing, updating, deletion
- Productivity metrics calculation
- Chart generation (priority, completion rate)
- Email tools (if configured)
- CLI interface
- Data persistence

⚠️ **LLM Features Require Python 3.10+:**
- Natural language agent requests
- Code-as-plan generation
- Chart reflection
- These can be used via direct tool calls instead

## Verification

After installation, verify everything works:

```bash
# Check system status
python3 cli.py status

# Should show:
# - Database: ✓
# - LLM: ✗ (expected on Python 3.9)
# - Email: ✗ (optional, configure if needed)
```

## Troubleshooting

### Issue: aisuite installation fails

**Solution**: This is expected on Python 3.9. Use `requirements.txt` instead of `requirements-full.txt`.

The project works perfectly without aisuite - all core features are functional.

### Issue: Module not found errors

```bash
# Reinstall dependencies
pip3 install -r requirements.txt --upgrade
```

### Issue: Permission errors

```bash
# Use user installation (default)
pip3 install -r requirements.txt --user
```

## Current Installation Status

✅ **Installed and Working:**
- pandas
- matplotlib
- python-dotenv
- python-dateutil
- pytest
- pytest-cov

⚠️ **Not Installed (Optional):**
- aisuite (requires Python 3.10+)

**Project Status**: ✅ Fully functional without aisuite

## Next Steps

1. **Test the installation:**
   ```bash
   python3 cli.py status
   ```

2. **Create a task:**
   ```bash
   python3 cli.py create -t "Test task" -p high
   ```

3. **List tasks:**
   ```bash
   python3 cli.py list
   ```

All core features are ready to use!


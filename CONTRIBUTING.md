# Contributing to Student Subscription Waste Detector

First off, thanks for taking the time to contribute! 🎉

## How Can I Contribute?

### Reporting Bugs

- Check if the bug has already been reported in [Issues](../../issues)
- If not, open a new issue with:
  - A clear title
  - Steps to reproduce
  - Expected vs actual behavior
  - Screenshots if applicable

### Suggesting Features

We welcome feature suggestions! Please open an issue with:
- A clear description of the feature
- Why it would be useful for students
- Any implementation ideas you have

### Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Make your changes** with clear, descriptive commits
3. **Test your changes** locally with `streamlit run app.py`
4. **Submit a PR** with a clear description of what you changed

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/student-subscription-detector.git
cd student-subscription-detector

# Install dependencies
pip install -r requirements.txt

# Run the app locally
streamlit run app.py
```

## Code Style

- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small
- Follow PEP 8 guidelines for Python

## Adding New Subscriptions

To add a new subscription to the database, edit the `SUBSCRIPTIONS_DB` dictionary in `app.py`:

```python
'new_service': {
    'name': 'New Service Name',
    'category': 'Category',  # Streaming, Music, Education, etc.
    'student_discount': True,  # or False
    'avg_monthly': 9.99
},
```

## Priority Areas for Contribution

We especially welcome contributions in these areas:

- [ ] Adding more subscription services to the database
- [ ] Supporting additional CSV formats (OFX, QFX)
- [ ] Improving subscription detection accuracy
- [ ] Adding new investment comparison options
- [ ] UI/UX improvements
- [ ] Documentation improvements
- [ ] Writing tests

## Questions?

Feel free to open an issue with the `question` label if you need help!

## Code of Conduct

Be respectful and inclusive. We're all here to learn and build something useful for students.

---

Built with ❤️ for students, by students.

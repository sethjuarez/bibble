# Contributing to Bibble

Thank you for your interest in contributing to Bibble! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/bibble.git
   cd bibble
   ```
3. **Set up your development environment**:
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   # Configure your .env file with Azure OpenAI credentials
   ```
4. **Run the setup check**:
   ```bash
   python setup_check.py
   ```

## 🛠️ Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Include docstrings for all functions and classes
- Maintain consistency with existing code patterns

### Testing
- Test your changes with both video and image modules
- Verify that imports work correctly
- Run the setup check script to ensure no regressions
- Test with various input types and edge cases

### Documentation
- Update README.md if you add new features
- Include docstrings for new functions
- Add inline comments for complex logic
- Update examples if the API changes

## 📝 Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Keep commits atomic and well-described
   - Include tests for new functionality
   - Update documentation as needed

3. **Test thoroughly**:
   - Verify your changes work as expected
   - Check that existing functionality still works
   - Run the setup check script

4. **Submit a pull request**:
   - Use a clear and descriptive title
   - Explain what your changes do and why
   - Reference any related issues
   - Include screenshots for UI changes

## 🐛 Bug Reports

When reporting bugs, please include:

- **Environment details**: Python version, operating system
- **Steps to reproduce**: Clear steps to trigger the issue
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Error messages**: Full error output if applicable
- **Configuration**: Relevant parts of your setup (without API keys)

## 💡 Feature Requests

For new features:

- **Use case**: Explain why this feature would be useful
- **Proposed solution**: Describe your ideal implementation
- **Alternatives**: Any alternative approaches you considered
- **Additional context**: Screenshots, mockups, or examples

## 🔧 Development Setup

### Environment Variables
For development, you'll need Azure OpenAI access:

```env
AZURE_SORA_ENDPOINT=https://your-sora-endpoint.openai.azure.com
AZURE_SORA_API_KEY=your-api-key
AZURE_IMAGE_ENDPOINT=https://your-image-endpoint.openai.azure.com  
AZURE_IMAGE_API_KEY=your-api-key
```

### Directory Structure
```
bibble/
├── src/
│   ├── video.py           # Video generation
│   ├── design.py          # Image editing
│   ├── images/            # Sample images
│   ├── scene/             # Scene assets
│   └── generated/         # Output directory
├── tests/                 # Test files (future)
├── docs/                  # Additional documentation (future)
└── examples/              # Usage examples (future)
```

## 📦 Submitting Changes

### Commit Message Format
Use clear, descriptive commit messages:

```
feat: add batch video processing capability
fix: resolve mask loading issue in design.py
docs: update README with new configuration options
refactor: improve error handling in video generation
```

### Pull Request Checklist
- [ ] Code follows project style guidelines
- [ ] Changes are tested and working
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No API keys or secrets in code
- [ ] Setup check script passes

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on the best outcome for the project

## 📞 Questions?

If you have questions about contributing:

- Check existing issues and discussions
- Create a new issue with the "question" label
- Reach out to maintainers

Thank you for contributing to Bibble! 🎉
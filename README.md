# Harmony Teacher API 🧑‍🏫

**Educator-first planning, awareness, and collaboration — consent-first, teacher-in-the-loop**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## Overview

The Harmony Teacher API is an **ethically-designed, privacy-first** tool for educators. It provides AI-assisted lesson planning, grading support, student awareness, and teacher collaboration — all with **built-in safeguards** that make harmful outputs impossible by construction.

### Core Principles

🔐 **Privacy by Default** — Minimal data collection, encrypted storage, short retention  
🤝 **Consent-Gated Access** — Every data access requires explicit permission  
✋ **Teacher Override Always Wins** — All AI outputs are drafts requiring approval  
🚫 **No Diagnostic Outputs** — Descriptive patterns only, never labels or classifications  
📜 **Audit-Grade Provenance** — Tamper-evident logging of all operations  

---

## What Makes This Different

### Ethical Constraints by Design

Unlike typical EdTech tools, the Harmony Teacher API **cannot** (by construction):

- ❌ Generate diagnostic labels for students
- ❌ Classify emotional states or moods
- ❌ Automatically submit final grades
- ❌ Build longitudinal student profiles
- ❌ Predict student outcomes

These aren't just policy — they're **architectural impossibilities**. Violations are blocked at runtime by `EthicsGuard` and tested in CI/CD.

### Teacher Authority

All AI-generated content is:
- Marked as **DRAFT** by default
- Requires **explicit teacher approval**
- Tracks **teacher edits** in audit trail
- **Never auto-submitted** without review

---

## Features

### 📚 Lesson Planning
- Generate draft lesson plans from topics
- Differentiation strategy suggestions
- Standards alignment helpers
- **All outputs editable** — teacher has final say

### ✏️ Grading Assistance
- Feedback comment suggestions (drafts only)
- Rubric-based scoring helpers
- **Hard rule:** No automated final grades

### 🔔 Awareness Flags
- Detects participation pattern changes
- Descriptive (not diagnostic) outputs
- Suggests teacher check-ins
- **Never student-visible** without approval

### 🤝 Teacher Collaboration
- Cross-teacher coordination channels
- Grade transition notes
- Workload balancing support
- **Permission-based**, audit-logged

---

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/FractalFuryan/harmony-teacher-api.git
cd harmony-teacher-api

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

### Run API Server

```bash
# Start development server
python teacher_api/api.py

# Or with uvicorn
uvicorn teacher_api.api:app --reload
```

API will be available at `http://localhost:8000`

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=teacher_api --cov-report=html

# Run only ethics tests (critical)
pytest tests/test_ethics.py -v
```

**Ethics tests must pass** before any merge to main.

---

## Architecture

```
harmony-teacher-api/
├── teacher_api/
│   ├── planner/          # Lesson planning engine
│   ├── grading/          # Grading assistance (no automation)
│   ├── support/          # Awareness flags (descriptive only)
│   ├── collaboration/    # Teacher coordination
│   ├── signals/          # Pattern detection math
│   ├── context/          # Ephemeral classroom memory
│   ├── security/         # Encryption, key management
│   ├── provenance/       # Audit logging, hashing
│   ├── ethics/           # Constraint enforcement
│   ├── consent/          # Permission management
│   └── api.py            # FastAPI application
├── tests/                # Comprehensive test suite
├── docs/                 # Documentation
│   ├── ETHICS.md         # Ethical framework
│   ├── CONSENT.md        # Consent management
│   ├── ARCHITECTURE.md   # System design
│   └── THREAT_MODEL.md   # Security analysis
└── pyproject.toml        # Project configuration
```

---

## Documentation

- **[Ethics Framework](docs/ETHICS.md)** — Core principles and enforcement
- **[Consent Management](docs/CONSENT.md)** — Permission system details
- **[Architecture](docs/ARCHITECTURE.md)** — System design and data flow
- **[Threat Model](docs/THREAT_MODEL.md)** — Security and privacy analysis

---

## Development

### Code Quality

```bash
# Format code
black teacher_api/ tests/

# Lint
ruff check teacher_api/ tests/

# Type check
mypy teacher_api/
```

### Pre-commit Hooks

```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Adding New Features

1. **Ethics review first** — Can this harm students? Block it.
2. **Write tests** — Including ethics constraint tests
3. **Document** — Update relevant .md files
4. **Audit log** — Log all sensitive operations
5. **Consent gate** — Require consent if accessing student data

---

## Relationship to Tutor API

The Harmony Teacher API is a **companion** to the Harmony Tutor API, not a fork:

**Shared (via API interface):**
- Hashed signals (opt-in only)
- Aggregated classroom patterns
- Security & ethics modules

**NOT Shared:**
- Raw student interaction data
- Individual student profiles
- Real-time activity streams

See [ARCHITECTURE.md](docs/ARCHITECTURE.md#interface-with-tutor-api) for details.

---

## Security

### Reporting Vulnerabilities

**Ethical violations are security bugs.** If you find a way to:
- Bypass ethics constraints
- Generate diagnostic outputs
- Access data without consent
- Tamper with audit logs

Please report immediately to: [security@example.com](mailto:security@example.com)

### Security Features

- 🔐 AES-256-GCM encryption at rest
- 🔒 TLS 1.3 in transit
- 🔑 Regular key rotation (90-day default)
- 📋 Tamper-evident audit trail
- 🛡️ Input validation & sanitization

---

## License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) file.

---

## Contributing

Contributions welcome! Please:

1. Read [ETHICS.md](docs/ETHICS.md) first
2. Ensure ethics tests pass
3. Add tests for new features
4. Document changes
5. Submit PR with clear description

**Ethics violations** will not be merged, even if technically clever.

---

## Roadmap

### v0.2.0 (Q1 2026)
- [ ] LLM integration for lesson generation
- [ ] Teacher review UI
- [ ] Parent consent portal

### v0.3.0 (Q2 2026)
- [ ] Advanced differentiation strategies
- [ ] Multi-language support
- [ ] LMS integrations

### v1.0.0 (Q3 2026)
- [ ] Production-ready deployment
- [ ] Third-party security audit
- [ ] Formal ethics certification

---

## Acknowledgments

Built with inspiration from:
- **Privacy-first design** principles
- **Value-sensitive design** methodology
- **Ethical AI** research community
- **Educator feedback** and lived experience

---

## Contact

- **Issues:** [GitHub Issues](https://github.com/FractalFuryan/harmony-teacher-api/issues)
- **Discussions:** [GitHub Discussions](https://github.com/FractalFuryan/harmony-teacher-api/discussions)
- **Ethics concerns:** ethics@example.com
- **Security:** security@example.com

---

**Remember:** The goal is to **support teachers**, not replace judgment. Every feature exists to make teaching better, never to reduce students to data points.

🧠 Built with care for educators and students 🎓

# Ethics Framework

**Harmony Teacher API — Ethical Constraints by Design**

---

## Core Principle

> **Harm prevention must be impossible by construction, not just discouraged.**

This API is architected so that ethical violations cannot occur accidentally. Safeguards are structural, not optional.

---

## Hard Non-Goals (Enforced at Runtime)

The following are **architecturally prohibited** — attempting these operations will fail:

### ❌ No Diagnostic Labels

- **Prohibited:** Any output that labels, diagnoses, or classifies students medically or psychologically
- **Examples:** "ADHD symptoms", "autistic traits", "learning disability"
- **Why:** Teachers are educators, not clinicians. Diagnosis requires medical professionals.
- **Enforcement:** `EthicsGuard` blocks outputs containing diagnostic terminology

### ❌ No Emotional Classification

- **Prohibited:** Automated emotional state classification or mood labeling
- **Examples:** "Student is depressed", "anxious behavior detected"
- **Why:** Emotional assessment requires human judgment and therapeutic training
- **Enforcement:** Pattern detection is descriptive only ("participation decreased"), never interpretive

### ❌ No Automated Final Grades

- **Prohibited:** AI-generated final grades without explicit teacher review and approval
- **Examples:** Auto-submitting grades to gradebook
- **Why:** Grading requires human judgment, context, and fairness assessment
- **Enforcement:** All grading outputs marked as `requires_teacher_review=True`; no auto-submission endpoint exists

### ❌ No Longitudinal Student Profiling

- **Prohibited:** Building persistent individual student profiles across years
- **Examples:** "Student risk trajectory", "likelihood of future outcomes"
- **Why:** Students change and grow; labeling limits potential
- **Enforcement:** Context retention limited to 90 days max; classroom-scoped not individual-scoped

### ❌ No Predictive Outcomes

- **Prohibited:** Predicting student life outcomes or future performance
- **Examples:** "College readiness score", "career path prediction"
- **Why:** Reduces students to data points; ignores agency and growth
- **Enforcement:** `ProhibitedOutputType` enum blocks predictive output types

---

## Affirmative Goals (What We Do)

### ✅ Teacher Awareness, Not Automation

- **Goal:** Surface patterns that may warrant teacher attention
- **Approach:** "Consider checking in" not "Student has problem X"
- **Output:** Descriptive flags requiring teacher judgment

### ✅ Consent-First Access

- **Goal:** Every data access requires explicit, informed consent
- **Default:** DENY unless specifically granted
- **Withdrawal:** Consent can be withdrawn instantly with immediate effect
- **Audit:** Every access is logged in tamper-evident audit trail

### ✅ Teacher Override Always Wins

- **Goal:** Teachers have final authority on all decisions
- **Implementation:** All AI outputs are suggestions/drafts requiring approval
- **Example:** Lesson plans marked `status=DRAFT` until teacher approves

### ✅ Privacy by Default

- **Goal:** Minimize data collection and retention
- **Encryption:** All sensitive data encrypted at rest and in transit
- **Retention:** Classroom context expires after 30-90 days
- **Anonymization:** Student IDs hashed when possible

### ✅ Audit-Grade Provenance

- **Goal:** Complete transparency in data handling
- **Audit Log:** Cryptographically chained, tamper-evident
- **Tracking:** Every read, write, update logged with actor and timestamp
- **Verification:** Chain integrity verifiable at any time

---

## Enforcement Mechanisms

### 1. Runtime Validation

**EthicsGuard** validates all outputs before they leave the system:

```python
EthicsGuard.validate_output(output, context="lesson_planning")
```

Raises `ConstraintViolation` if rules broken.

### 2. Type System Constraints

Prohibited outputs are typed as errors:

```python
class ProhibitedOutputType(Enum):
    DIAGNOSTIC_LABEL = "diagnostic_label"
    EMOTIONAL_CLASSIFICATION = "emotional_classification"
    # etc.
```

### 3. Structural Safeguards

Some violations are impossible by design:

- **No auto-grade submission endpoint** — doesn't exist in API
- **Consent gates** — data access requires `consent_manager.require_consent()`
- **Mandatory review flags** — `requires_teacher_review` enforced at dataclass level

### 4. Test-Driven Ethics

Ethics are **tested** like any critical feature:

```python
def test_blocks_diagnostic_labels():
    output = {"output_type": "diagnostic_label"}
    with pytest.raises(ConstraintViolation):
        EthicsGuard.validate_output(output)
```

See [tests/test_ethics.py](../tests/test_ethics.py) for full suite.

---

## Decision Framework

When designing new features, ask:

1. **Could this reduce a student to a label?** → Block it
2. **Could this bypass teacher judgment?** → Require explicit review
3. **Could this be used to predict life outcomes?** → Prohibit
4. **Does this collect unnecessary data?** → Minimize
5. **Is consent clear and withdrawable?** → Enforce gates

---

## Accountability

### For Developers

- Ethics tests must pass before merge
- New features require ethics review
- Violations are treated as security bugs

### For Users (Teachers/Schools)

- Audit logs available for review
- Consent status transparent to families
- Ethical concerns escalated to steering committee

---

## Continuous Improvement

This is a living document. As we learn, we strengthen:

- **Monitoring:** Track attempted violations
- **Review:** Quarterly ethics audits
- **Community:** Educator feedback shapes policy
- **Transparency:** Changes documented in version control

---

## Questions or Concerns?

Ethics is not optional — it's the foundation.

If you see a way to violate these principles, **please report it as a bug**.

---

*Last updated: January 5, 2026*

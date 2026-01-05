# Consent Management

**Privacy by Default, Access by Permission**

---

## Core Principle

> **No student data access without explicit, informed consent.**

Default policy: **DENY** unless specifically granted.

---

## Consent Scopes

Different types of data require different consent levels:

### 1. Basic Info
**Scope:** `ConsentScope.BASIC_INFO`

- Student name, grade level
- Minimal demographic info
- **Default:** Required for any system use

### 2. Academic Patterns
**Scope:** `ConsentScope.ACADEMIC_PATTERNS`

- Learning pattern analysis (anonymized)
- Participation trends
- Engagement metrics
- **Purpose:** Improve teaching strategies

### 3. Classroom Signals
**Scope:** `ConsentScope.CLASSROOM_SIGNALS`

- Aggregated classroom data
- Group-level patterns
- **Note:** Individual students not identifiable

### 4. Collaboration
**Scope:** `ConsentScope.COLLABORATION`

- Cross-teacher coordination
- Grade-level team sharing
- **Purpose:** Smoother transitions, better support

### 5. Support Routing
**Scope:** `ConsentScope.SUPPORT_ROUTING`

- Referrals to counselors/specialists
- Awareness flags shared with support staff
- **Purpose:** Connect students to appropriate resources

---

## Consent Lifecycle

### 1. Granting Consent

**Who can grant:**
- Parent/guardian (required for minors)
- Student (if 18+ or emancipated)
- Legal guardian with documentation

**Process:**
```python
consent_manager.grant_consent(
    student_id="student_123",
    scope=ConsentScope.ACADEMIC_PATTERNS,
    granted_by="parent_456",
    expires_at=datetime.utcnow() + timedelta(days=365),
)
```

**Requirements:**
- Clear explanation of what data is accessed
- Specific purpose statement
- Optional expiration date
- Revocable at any time

### 2. Checking Consent

**Before every data access:**

```python
if not consent_manager.check_consent(student_id, ConsentScope.ACADEMIC_PATTERNS):
    raise PermissionError("Consent required")
```

**Automatic enforcement:**
```python
consent_manager.require_consent(student_id, scope)  # Raises if not granted
```

### 3. Withdrawing Consent

**Who can withdraw:**
- Same person who granted consent
- Student upon reaching majority age
- Legal guardian

**Effect:**
- **Immediate** — takes effect instantly
- All related data access blocked
- Existing insights flagged for review
- Context data can be purged on request

**Process:**
```python
consent_manager.withdraw_consent(
    student_id="student_123",
    scope=ConsentScope.ACADEMIC_PATTERNS,
)
```

### 4. Expiration

Consent can have expiration dates:

- **Default:** Annual renewal recommended
- **Maximum:** 2 years (configurable by district)
- **Automatic:** Expires at grade transition unless renewed

---

## Consent States

### GRANTED
- Active and valid
- Data access permitted
- Logged in audit trail

### DENIED
- Explicitly refused
- No data access
- Cannot be overridden

### WITHDRAWN
- Previously granted, now revoked
- Immediate effect
- Timestamp recorded

### EXPIRED
- Time-limited consent has lapsed
- Treated same as DENIED
- Renewal available

---

## Data Access Matrix

| Feature | Required Scope | Fallback if Denied |
|---------|---------------|-------------------|
| Lesson planning | None | Full access (teacher tool) |
| Grading assistance | `BASIC_INFO` | Manual grading only |
| Awareness flags | `ACADEMIC_PATTERNS` | No pattern detection |
| Support routing | `SUPPORT_ROUTING` | Manual referrals only |
| Teacher collaboration | `COLLABORATION` | Individual teacher only |

---

## Audit Trail

Every consent action is logged:

```python
audit_log.log(
    actor="parent_456",
    action="grant_consent",
    resource="student:123:academic_patterns",
    details={
        "scope": "academic_patterns",
        "expires_at": "2027-01-01",
    }
)
```

**Logged events:**
- Consent granted
- Consent checked (data access)
- Consent withdrawn
- Consent expired
- Access denied (no consent)

---

## Privacy Guarantees

### What We Do NOT Do

❌ **No blanket consent** — each scope requires separate consent  
❌ **No implied consent** — silence is not permission  
❌ **No consent by enrollment** — using the school doesn't mean consent to data use  
❌ **No unchangeable consent** — always revocable  

### What We DO

✅ **Granular scopes** — consent to X doesn't mean consent to Y  
✅ **Clear purpose** — families know exactly what data is used for  
✅ **Transparent access** — audit logs show who accessed what when  
✅ **Immediate revocation** — withdrawal takes effect instantly  
✅ **Data minimization** — only collect what's consented  

---

## For Families

### Your Rights

1. **Know what's collected** — request data access report
2. **Control access** — grant or deny any scope
3. **Withdraw anytime** — no questions asked
4. **See the history** — audit logs available
5. **Request deletion** — beyond consent withdrawal

### How to Manage Consent

**Via school portal:**
- Review current consent status
- Grant/withdraw scopes
- Set expiration dates
- View access history

**Via direct contact:**
- Email: privacy@harmony-teacher-api.example
- Phone: Contact school privacy coordinator

---

## For Teachers

### Before Using Student Data

1. **Check consent status** in system
2. **Request consent** if not granted (via family portal)
3. **Use alternatives** if consent denied (manual methods)
4. **Respect withdrawals** — system enforces automatically

### If Consent is Withdrawn

- System blocks future access
- Existing insights flagged
- Fall back to non-data-driven methods
- **Do not** pressure families to re-consent

---

## Compliance

### Legal Framework

- **FERPA** (Family Educational Rights and Privacy Act)
- **COPPA** (Children's Online Privacy Protection Act)
- **State privacy laws** (varies by jurisdiction)
- **District policies**

### Consent as Legal Requirement

Consent in this system serves dual purpose:
1. **Ethical imperative** — respect for autonomy
2. **Legal compliance** — meeting regulatory requirements

---

## Technical Implementation

### Consent Enforcement

**At API level:**
```python
@require_consent(ConsentScope.ACADEMIC_PATTERNS)
def get_learning_patterns(student_id: str):
    # Automatically blocked if consent not granted
    pass
```

**In data queries:**
```python
# Only return data for students with consent
students_with_consent = filter(
    lambda s: consent_manager.check_consent(s.id, scope),
    all_students
)
```

### Consent Metadata

Every consent grant includes:
- `student_id` (hashed when stored)
- `scope` (enum)
- `granted_by` (parent/guardian ID)
- `granted_at` (timestamp)
- `expires_at` (optional)
- `withdrawn_at` (if applicable)

---

## Future Enhancements

Planned improvements:

- **Tiered consent** — more granular sub-scopes
- **Temporary consent** — "grant for this week only"
- **Delegate consent** — guardian delegates to student at threshold age
- **Consent templates** — district-wide defaults with opt-out

---

## Questions?

**Families:** Contact your school's privacy coordinator  
**Teachers:** See Teacher Handbook > Privacy & Consent  
**Developers:** Review [consent/manager.py](../teacher_api/consent/manager.py)

---

*Last updated: January 5, 2026*

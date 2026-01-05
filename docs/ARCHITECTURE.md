# Architecture

**Harmony Teacher API — System Design**

---

## Design Principles

### 1. **Ethics by Construction**
Harmful outputs are impossible to generate, not just discouraged.

### 2. **Teacher Authority**
All AI outputs are drafts requiring explicit teacher approval.

### 3. **Consent Gates**
Every data access passes through consent verification.

### 4. **Audit First**
Every operation is logged in tamper-evident audit trail.

### 5. **Privacy by Default**
Minimal data collection, encrypted storage, short retention.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Teacher API Layer                        │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │   Planner   │  │   Grading    │  │  Collaboration  │   │
│  │   Engine    │  │  Assistant   │  │    Manager      │   │
│  └─────────────┘  └──────────────┘  └─────────────────┘   │
│         │                 │                   │              │
│         └─────────────────┼───────────────────┘              │
│                           │                                  │
│  ┌────────────────────────▼──────────────────────────────┐  │
│  │           Ethics & Consent Enforcement                │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────┐  │  │
│  │  │ EthicsGuard │  │   Consent    │  │  Audit Log │  │  │
│  │  │  (runtime)  │  │   Manager    │  │  (chained) │  │  │
│  │  └─────────────┘  └──────────────┘  └────────────┘  │  │
│  └────────────────────────────────────────────────────────┘  │
│                           │                                  │
│  ┌────────────────────────▼──────────────────────────────┐  │
│  │           Data & Security Layer                       │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────┐  │  │
│  │  │ Encryption  │  │     Key      │  │  Hashing   │  │  │
│  │  │  (AES-GCM)  │  │  Management  │  │ (SHA-256)  │  │  │
│  │  └─────────────┘  └──────────────┘  └────────────┘  │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
   ┌──────────┐    ┌──────────────┐   ┌────────────┐
   │ Teacher  │    │ Tutor API    │   │  Storage   │
   │   UI     │    │ (signals)    │   │ (encrypted)│
   └──────────┘    └──────────────┘   └────────────┘
```

---

## Module Breakdown

### Core Modules

#### 1. **Planner** (`teacher_api/planner/`)

**Purpose:** Generate lesson plans, pacing guides, differentiation strategies

**Key Components:**
- `lesson_generator.py` — Draft lesson plans
- Status tracking (DRAFT → TEACHER_REVIEW → APPROVED)
- Teacher edit history

**Safeguards:**
- All plans marked `requires_teacher_approval=True`
- `ai_generated=True` flag for transparency
- Teacher edits tracked in audit trail

#### 2. **Grading** (`teacher_api/grading/`)

**Purpose:** Assist with grading workflow (NOT automate it)

**Key Components:**
- `feedback_drafts.py` — Suggest feedback comments
- Rubric scoring helpers (suggestions only)
- `GradingSafeguards` — Enforce review requirements

**Hard Rules:**
- `requires_teacher_review=True` (enforced at construction)
- `is_draft=True` (always)
- No automated grade submission endpoint exists

#### 3. **Support** (`teacher_api/support/`)

**Purpose:** Flag patterns for teacher awareness

**Key Components:**
- `awareness_flags.py` — Pattern detection
- Support routing suggestions
- Descriptive (not diagnostic) outputs

**Constraints:**
- `is_diagnostic=False` (enforced)
- `requires_teacher_judgment=True` (always)
- `visible_to_student=False` (default)

#### 4. **Collaboration** (`teacher_api/collaboration/`)

**Purpose:** Teacher-to-teacher coordination

**Key Components:**
- `channels.py` — Communication channels
- Transition notes for grade handoffs
- Permission-based access

**Privacy:**
- Channel membership required
- Student mentions require consent verification
- All messages audit-logged

### Cross-Cutting Modules

#### 5. **Ethics** (`teacher_api/ethics/`)

**Purpose:** Runtime constraint enforcement

**Key Components:**
- `constraints.py` — `EthicsGuard` validator
- Prohibited output type enum
- Prohibited term detection

**Operation:**
- Validates all outputs before return
- Raises `ConstraintViolation` on breach
- Tested in `tests/test_ethics.py`

#### 6. **Consent** (`teacher_api/consent/`)

**Purpose:** Manage data access permissions

**Key Components:**
- `manager.py` — Consent lifecycle
- Scope-based permissions
- Grant/withdraw/check operations

**Default Policy:**
- DENY unless explicitly granted
- Immediate withdrawal effect
- Audit logging of all consent changes

#### 7. **Security** (`teacher_api/security/`)

**Purpose:** Cryptographic operations

**Key Components:**
- `encryption.py` — AES-256-GCM encryption
- `key_management.py` — Key rotation
- Authenticated encryption (AEAD)

**Standards:**
- Modern algorithms only
- Keys never logged
- Regular rotation (90-day default)

#### 8. **Provenance** (`teacher_api/provenance/`)

**Purpose:** Audit trail and tamper evidence

**Key Components:**
- `audit_log.py` — Chained audit entries
- `hashing.py` — Data integrity
- Genesis hash for chain start

**Guarantees:**
- Every entry links to previous
- Tampering detection via chain verification
- SHA-256 hashing

#### 9. **Signals** (`teacher_api/signals/`)

**Purpose:** Pattern detection math (NO interpretation)

**Key Components:**
- `core_math.py` — Statistical functions
- Deviation detection
- Trend analysis

**Scope:**
- Pure math only
- No domain interpretation at this layer
- Reused from Tutor API

#### 10. **Context** (`teacher_api/context/`)

**Purpose:** Ephemeral memory for classroom patterns

**Key Components:**
- Classroom-scoped (not individual)
- 30-90 day retention max
- Automatic expiration

**Privacy:**
- No longitudinal student profiles
- Aggregated patterns only
- Consent-gated access

---

## Data Flow

### Example: Generating a Lesson Plan

```
1. Teacher requests lesson plan
   └─> API receives request

2. Planner Engine generates draft
   └─> LLM creates lesson structure
   └─> Status set to DRAFT
   └─> requires_teacher_approval=True

3. Ethics Guard validates output
   └─> Check for prohibited terms
   └─> Verify review flag set
   └─> No violations → proceed

4. Audit Log records action
   └─> Actor: teacher_id
   └─> Action: generate_lesson_plan
   └─> Resource: lesson_plan:{id}

5. Return draft to teacher
   └─> Clearly marked as DRAFT
   └─> Edit interface provided

6. Teacher reviews and approves
   └─> Status → APPROVED
   └─> Edits tracked in audit trail
```

### Example: Awareness Flag

```
1. Pattern detected in classroom data
   └─> Participation decrease observed

2. Consent check
   └─> Does student have ACADEMIC_PATTERNS consent?
   └─> If NO → stop, no flag created
   └─> If YES → proceed

3. Flag created (descriptive only)
   └─> "Participation pattern has decreased"
   └─> Suggested action: "Consider check-in"
   └─> is_diagnostic=False (enforced)

4. Ethics Guard validates
   └─> No diagnostic terms
   └─> No emotional classification
   └─> Approved

5. Audit Log records
   └─> Action: create_awareness_flag
   └─> Student ID (hashed)

6. Teacher receives flag
   └─> Uses professional judgment
   └─> May check in, may ignore, may refer
```

---

## Interface with Tutor API

**Relationship:** Companion APIs, not integrated

### What's Shared

**Via API Interface (not database):**
- Hashed signals (opt-in only)
- Aggregated patterns (no raw data)
- Consent status (read-only)

### What's NOT Shared

- Raw student interaction data
- Individual student profiles
- Real-time activity streams
- Personally identifiable information

### Contract

```python
# Tutor API → Teacher API
class SignalTransfer:
    classroom_id: str  # Aggregation scope
    signal_type: str   # "participation", "engagement"
    aggregated_value: float  # Pre-aggregated
    timestamp: datetime
    student_ids: List[str]  # Hashed
    consent_verified: bool  # Must be True
```

**Constraints:**
- No transfer without consent
- Aggregated data only
- Time-limited (signals expire)
- Audit-logged

---

## Deployment Architecture

### Production Setup

```
┌─────────────────────────────────────┐
│         Load Balancer               │
└────────────┬────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼────┐      ┌────▼───┐
│ API    │      │  API   │
│ Server │      │ Server │
│   1    │      │   2    │
└───┬────┘      └────┬───┘
    │                │
    └────────┬───────┘
             │
    ┌────────▼────────┐
    │   Database      │
    │  (encrypted)    │
    └─────────────────┘
```

**Security:**
- TLS 1.3 for all connections
- Database encryption at rest
- Key management service for encryption keys
- Regular security audits

---

## Error Handling

### Ethical Violations

```python
try:
    EthicsGuard.validate_output(output)
except ConstraintViolation as e:
    # Log violation attempt
    audit_log.log(
        actor="system",
        action="ethics_violation_blocked",
        resource=output_id,
        details={"violation": str(e)}
    )
    # Return error to client
    raise HTTPException(status_code=400, detail="Output violates ethical constraints")
```

### Consent Denials

```python
try:
    consent_manager.require_consent(student_id, scope)
except PermissionError:
    # Log denial
    audit_log.log(
        actor=teacher_id,
        action="access_denied_no_consent",
        resource=f"student:{student_id}",
    )
    # Fail gracefully
    return fallback_response()
```

---

## Testing Strategy

### Unit Tests
- Individual module functionality
- Security operations (encryption, hashing)
- Math operations (signals)

### Integration Tests
- Ethics enforcement across modules
- Consent flow end-to-end
- Audit log chaining

### Ethics Tests
- **CRITICAL:** Run on every PR
- Test every prohibited scenario
- Ensure violations are blocked

### Performance Tests
- API response times
- Database query optimization
- Encryption overhead

---

## Monitoring

### Metrics to Track

**Ethical Health:**
- Ethics violations attempted (should be 0)
- Consent denials (expected, track trends)
- Audit chain verifications (should always pass)

**Operational:**
- API latency
- Error rates
- Consent check overhead

**Privacy:**
- Data retention compliance
- Encryption key rotation status
- Audit log completeness

---

## Future Enhancements

### Short-term
- LLM integration for lesson generation
- UI for teacher review workflow
- Parent consent portal

### Medium-term
- Multi-language support
- Advanced differentiation strategies
- Integration with learning management systems

### Long-term
- Federated learning for privacy-preserving patterns
- Blockchain-based audit trail
- Zero-knowledge proof consent verification

---

*Last updated: January 5, 2026*

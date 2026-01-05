# Threat Model

**Harmony Teacher API — Security & Privacy Threat Analysis**

---

## Threat Modeling Approach

**Framework:** STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)

**Scope:** All components that handle student data, teacher workflows, and ethical constraints

---

## Trust Boundaries

```
┌─────────────────────────────────────────────────┐
│  External Zone (Untrusted)                      │
│  - Public Internet                              │
│  - Teacher browsers                             │
│  - External APIs                                │
└──────────────┬──────────────────────────────────┘
               │ TLS 1.3
┌──────────────▼──────────────────────────────────┐
│  DMZ (Semi-Trusted)                             │
│  - Load Balancer                                │
│  - API Gateway                                  │
└──────────────┬──────────────────────────────────┘
               │ Internal network
┌──────────────▼──────────────────────────────────┐
│  Application Zone (Trusted)                     │
│  - Teacher API servers                          │
│  - Ethics Guard                                 │
│  - Consent Manager                              │
└──────────────┬──────────────────────────────────┘
               │ Encrypted connection
┌──────────────▼──────────────────────────────────┐
│  Data Zone (Highly Restricted)                  │
│  - Encrypted database                           │
│  - Key management service                       │
│  - Audit logs                                   │
└─────────────────────────────────────────────────┘
```

---

## Asset Classification

### Critical Assets

**Student Data:**
- Names, IDs (PII)
- Learning patterns
- Participation data
- Risk Level: **CRITICAL**

**Consent Records:**
- Who consented, when, to what
- Withdrawal history
- Risk Level: **CRITICAL**

**Audit Logs:**
- Complete access history
- Ethical violation attempts
- Risk Level: **HIGH**

**Encryption Keys:**
- Master keys
- Data encryption keys
- Risk Level: **CRITICAL**

### Important Assets

**Teacher Data:**
- Lesson plans
- Grading rubrics
- Collaboration messages
- Risk Level: **HIGH**

**System Integrity:**
- API code
- Ethics constraints
- Configuration
- Risk Level: **HIGH**

---

## Threat Scenarios

### 1. SPOOFING

#### T1.1: Teacher Impersonation

**Threat:** Attacker impersonates a teacher to access student data

**Attack Vector:**
- Stolen credentials
- Session hijacking
- Social engineering

**Impact:**
- Unauthorized student data access
- FERPA violation
- Loss of trust

**Mitigations:**
- ✅ Multi-factor authentication (MFA) required
- ✅ Session timeout (30 minutes idle)
- ✅ IP allowlisting for schools
- ✅ Audit logging of all access
- 🔄 Anomaly detection on access patterns (planned)

**Residual Risk:** MEDIUM

---

#### T1.2: Parent Consent Spoofing

**Threat:** Attacker grants consent without parental authority

**Attack Vector:**
- Forged consent forms
- Compromised parent account
- Insider threat (school staff)

**Impact:**
- Unauthorized data processing
- Legal liability
- Privacy violation

**Mitigations:**
- ✅ Email verification for consent grants
- ✅ Consent records audit-logged
- 🔄 Two-factor consent for sensitive scopes (planned)
- 🔄 Manual verification for high-risk students (planned)

**Residual Risk:** MEDIUM

---

### 2. TAMPERING

#### T2.1: Audit Log Tampering

**Threat:** Attacker modifies audit logs to hide malicious activity

**Attack Vector:**
- Database compromise
- Privileged access abuse
- SQL injection

**Impact:**
- Loss of accountability
- Unable to detect breaches
- Regulatory non-compliance

**Mitigations:**
- ✅ Cryptographic chaining (tamper-evident)
- ✅ Hash verification on every read
- ✅ Append-only log structure
- ✅ Regular integrity checks
- 🔄 Write logs to immutable storage (planned)

**Residual Risk:** LOW

---

#### T2.2: Ethics Bypass

**Threat:** Attacker modifies code to bypass ethical constraints

**Attack Vector:**
- Compromised developer account
- Malicious PR merged
- Runtime code injection

**Impact:**
- Diagnostic labels generated
- Automated grading without review
- Catastrophic ethical failure

**Mitigations:**
- ✅ Ethics tests in CI/CD (must pass to merge)
- ✅ Code review required for ethics module
- ✅ Runtime validation (EthicsGuard)
- ✅ Immutable constraint definitions
- 🔄 Formal verification of constraints (research)

**Residual Risk:** LOW (but high impact if occurs)

---

#### T2.3: Consent Record Modification

**Threat:** Attacker changes consent records to grant unauthorized access

**Attack Vector:**
- Database injection
- Compromised admin account
- Logic bug exploitation

**Impact:**
- Data accessed without consent
- FERPA/COPPA violation
- Loss of family trust

**Mitigations:**
- ✅ Consent changes audit-logged
- ✅ Database access controls (least privilege)
- ✅ Input validation on all consent operations
- 🔄 Consent hash signatures (planned)

**Residual Risk:** MEDIUM

---

### 3. REPUDIATION

#### T3.1: Teacher Denies Action

**Threat:** Teacher claims they didn't perform an action (e.g., access student data)

**Attack Vector:**
- Shared credentials
- Inadequate logging
- Log deletion

**Impact:**
- Cannot prove who accessed data
- Legal vulnerability
- Accountability failure

**Mitigations:**
- ✅ Comprehensive audit logging
- ✅ Non-repudiable timestamps
- ✅ Cryptographic chain prevents deletion
- ✅ User attribution on all actions

**Residual Risk:** LOW

---

#### T3.2: Consent Repudiation

**Threat:** Parent claims they didn't grant consent

**Attack Vector:**
- Consent granted by someone else
- System error in recording
- UI confusion

**Impact:**
- Legal dispute
- Data processing questioned
- Compliance audit failure

**Mitigations:**
- ✅ Email confirmation of consent
- ✅ Detailed consent records (IP, timestamp, details)
- ✅ Audit trail of consent lifecycle
- 🔄 Digital signatures for consent (planned)

**Residual Risk:** MEDIUM

---

### 4. INFORMATION DISCLOSURE

#### T4.1: Student Data Leakage

**Threat:** Unauthorized access to student information

**Attack Vector:**
- API vulnerability (e.g., IDOR)
- Database breach
- Insider threat
- Misconfigured permissions

**Impact:**
- Privacy violation
- Regulatory penalties
- Reputational damage

**Mitigations:**
- ✅ Encryption at rest (AES-256)
- ✅ Encryption in transit (TLS 1.3)
- ✅ Consent gates on all access
- ✅ Principle of least privilege
- ✅ No student IDs in URLs/logs
- 🔄 Data loss prevention (DLP) tools (planned)

**Residual Risk:** MEDIUM

---

#### T4.2: Audit Log Exposure

**Threat:** Audit logs leaked, revealing sensitive access patterns

**Attack Vector:**
- Misconfigured storage
- Backup exposure
- Insider access

**Impact:**
- Activity patterns revealed
- Teacher behavior exposed
- Potential targeting of individuals

**Mitigations:**
- ✅ Access controls on audit logs
- ✅ Encrypted storage
- ✅ Audit log access is itself logged
- 🔄 Anonymization of non-critical details (planned)

**Residual Risk:** LOW

---

#### T4.3: Collaboration Channel Leaks

**Threat:** Cross-teacher communications exposed

**Attack Vector:**
- Permission misconfiguration
- Compromised teacher account
- Channel membership error

**Impact:**
- Sensitive student discussions revealed
- Teacher coordination compromised
- Trust breakdown

**Mitigations:**
- ✅ Channel membership verification
- ✅ Consent required for student mentions
- ✅ Access logging
- 🔄 End-to-end encryption for channels (planned)

**Residual Risk:** MEDIUM

---

### 5. DENIAL OF SERVICE

#### T5.1: API Overload

**Threat:** Attacker floods API to deny service to teachers

**Attack Vector:**
- Volumetric attack
- Slowloris-style attack
- Resource exhaustion

**Impact:**
- Teachers cannot access system
- Lesson planning disrupted
- Grading workflow blocked

**Mitigations:**
- ✅ Rate limiting per user
- ✅ Load balancing
- 🔄 DDoS protection (CDN/WAF) (planned)
- 🔄 Auto-scaling infrastructure (planned)

**Residual Risk:** MEDIUM

---

#### T5.2: Consent Check Overhead

**Threat:** Consent verification slows system to unusability

**Attack Vector:**
- Poor implementation
- N+1 query problem
- Database overload

**Impact:**
- System too slow to use
- Teachers bypass system
- Ethical controls ineffective

**Mitigations:**
- ✅ Consent caching (short TTL)
- ✅ Indexed consent lookups
- 🔄 Performance testing in CI (planned)

**Residual Risk:** LOW

---

### 6. ELEVATION OF PRIVILEGE

#### T6.1: Teacher Access Escalation

**Threat:** Teacher gains access to students outside their scope

**Attack Vector:**
- IDOR vulnerabilities
- Missing authorization checks
- Session fixation

**Impact:**
- Unauthorized student data access
- Privacy violation
- Accountability failure

**Mitigations:**
- ✅ Authorization checks on every request
- ✅ Classroom/student scoping enforced
- ✅ No global student queries
- ✅ Audit logging of access attempts

**Residual Risk:** MEDIUM

---

#### T6.2: Bypass Ethics Constraints

**Threat:** Attacker gains ability to generate prohibited outputs

**Attack Vector:**
- Privilege escalation to admin
- Direct database access
- Exploit in EthicsGuard

**Impact:**
- Diagnostic labels generated
- Emotional classification produced
- Catastrophic ethical failure

**Mitigations:**
- ✅ EthicsGuard runs on all code paths
- ✅ No "admin override" for ethics
- ✅ Database constraints mirror code constraints
- ✅ Immutable ethical rules

**Residual Risk:** LOW (but catastrophic impact)

---

## Privacy-Specific Threats

### P1: Longitudinal Profiling

**Threat:** System accumulates data to create persistent student profiles

**Attack Vector:**
- Long retention periods
- Cross-year data correlation
- Inadequate anonymization

**Impact:**
- Students reduced to labels
- Privacy erosion over time
- Discriminatory outcomes

**Mitigations:**
- ✅ Maximum 90-day retention enforced
- ✅ No cross-year identity linkage
- ✅ Automatic data expiration
- ✅ Classroom-scoped, not individual-scoped

**Residual Risk:** LOW

---

### P2: Consent Fatigue

**Threat:** Families over-consent due to confusion or pressure

**Attack Vector:**
- Complex consent UI
- Social pressure
- Bundled consent requests

**Impact:**
- Consent not truly informed
- Over-collection of data
- Violation of intent

**Mitigations:**
- ✅ Granular consent scopes (not bundled)
- ✅ Clear, simple language
- ✅ Easy withdrawal process
- 🔄 Annual consent review reminder (planned)

**Residual Risk:** MEDIUM

---

### P3: Re-identification

**Threat:** Anonymized student data re-identified through correlation

**Attack Vector:**
- Small classroom sizes
- Unique behavior patterns
- External data sources

**Impact:**
- Privacy claims invalidated
- Individual students identified
- Sensitive info exposed

**Mitigations:**
- ✅ Aggregation threshold (min 5 students)
- ✅ Noise injection in small groups
- ✅ No raw individual data in reports
- 🔄 Differential privacy techniques (research)

**Residual Risk:** MEDIUM

---

## Supply Chain Threats

### S1: Compromised Dependencies

**Threat:** Malicious code in third-party libraries

**Attack Vector:**
- Dependency confusion
- Typosquatting
- Upstream compromise

**Impact:**
- Data exfiltration
- Backdoor insertion
- System compromise

**Mitigations:**
- ✅ Dependency pinning
- ✅ SCA (Software Composition Analysis) scanning
- 🔄 Automated vulnerability alerts (planned)
- 🔄 Private package mirror (planned)

**Residual Risk:** MEDIUM

---

### S2: LLM Prompt Injection

**Threat:** Malicious prompts manipulate lesson generation

**Attack Vector:**
- Injected content in lesson requests
- Crafted student data
- Bypass ethical constraints

**Impact:**
- Inappropriate content generated
- Ethics bypass
- Misinformation in lessons

**Mitigations:**
- ✅ EthicsGuard validates all outputs
- ✅ Input sanitization
- 🔄 Prompt hardening techniques (planned)
- 🔄 LLM output monitoring (planned)

**Residual Risk:** MEDIUM-HIGH

---

## Insider Threats

### I1: Malicious Developer

**Threat:** Developer intentionally introduces vulnerability

**Attack Vector:**
- Code changes in PR
- Direct commit to main
- Subtle logic bugs

**Impact:**
- Ethics bypass
- Data exfiltration
- System compromise

**Mitigations:**
- ✅ Code review required (2+ reviewers for ethics module)
- ✅ Automated testing (ethics tests must pass)
- ✅ Audit logging of code changes
- 🔄 Background checks for contributors (process)

**Residual Risk:** MEDIUM

---

### I2: Curious School Admin

**Threat:** Admin with database access snoops on student data

**Attack Vector:**
- Direct database queries
- Backup file access
- Log file examination

**Impact:**
- Privacy violation
- Consent bypass
- Loss of trust

**Mitigations:**
- ✅ Database access audit-logged
- ✅ Encryption at rest
- ✅ Need-to-know access controls
- 🔄 Database activity monitoring (planned)

**Residual Risk:** MEDIUM

---

## Risk Prioritization

### Critical (Address Immediately)

1. **T2.2: Ethics Bypass** — Catastrophic ethical failure
2. **T4.1: Student Data Leakage** — Privacy violation, regulatory
3. **P1: Longitudinal Profiling** — Violates core principle

### High (Address Soon)

4. **T1.1: Teacher Impersonation** — Unauthorized access
5. **T2.3: Consent Record Modification** — Consent integrity
6. **T6.2: Bypass Ethics Constraints** — Core safeguard

### Medium (Monitor and Improve)

7. **T3.2: Consent Repudiation** — Legal clarity
8. **S2: LLM Prompt Injection** — Output integrity
9. **I1: Malicious Developer** — Supply chain

---

## Monitoring & Detection

### Alerts

**Immediate (Page On-Call):**
- Audit chain verification failure
- Ethics constraint violation attempt
- Multiple failed consent checks
- Unauthorized admin access

**High Priority (Alert Within 1 Hour):**
- Unusual data access patterns
- Mass consent withdrawals
- API error spike
- Database performance degradation

**Low Priority (Daily Digest):**
- Failed login attempts
- Rate limit hits
- Slow query warnings

---

## Incident Response

### Ethical Violation Response

1. **Detect:** EthicsGuard raises ConstraintViolation
2. **Log:** Audit log records attempt
3. **Block:** Request denied, no output returned
4. **Alert:** Security team notified
5. **Investigate:** Review logs, code, assess if bypass attempt
6. **Remediate:** Fix vulnerability if found
7. **Report:** Document in incident log

### Data Breach Response

1. **Contain:** Revoke credentials, isolate systems
2. **Assess:** Determine scope (how many students affected)
3. **Notify:** Families within 72 hours (GDPR), districts immediately
4. **Remediate:** Fix vulnerability
5. **Audit:** Review all access logs
6. **Report:** Regulatory reporting as required

---

## Security Roadmap

### Q1 2026
- [ ] Penetration testing
- [ ] Security audit by third party
- [ ] Implement DDoS protection

### Q2 2026
- [ ] Formal verification of ethics constraints
- [ ] End-to-end encryption for collaboration
- [ ] Advanced anomaly detection

### Q3 2026
- [ ] Differential privacy research
- [ ] Zero-knowledge consent proofs
- [ ] Blockchain audit trail (evaluation)

---

*Last updated: January 5, 2026*

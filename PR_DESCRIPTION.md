# 📝 Homework Submission - Homework 3

> **Student Name**: Mykhailo Bestiuk  
> **Date Submitted**: February 10, 2026  
> **Assignment**: Homework 3: Specification-Driven Design

---

## ✅ Summary of Submission

This PR submits a **specification package** (no code) for a **Virtual Card Lifecycle Management** microservice in a regulated FinTech environment. The package provides complete guidance for AI-driven implementation of a PCI-DSS compliant system.

### 📦 Deliverables

| File | Lines | Purpose |
|------|-------|---------|
| `specification.md` | 620 | High/mid/low-level objectives + 18 implementation tasks |
| `agents.md` | 159 | AI coding partner guidelines for FinTech domain |
| `.github/copilot-instructions.md` | 94 | Editor-specific ALWAYS/NEVER rules |
| `README.md` | 88 | Rationale and industry best practices mapping |

### 🎯 Domain: Virtual Card Lifecycle Management

**Why this domain?** Maximizes demonstration of FinTech best practices:
- State machine complexity (4 states, 5 transitions, strict invariants)
- Compliance frameworks (PCI-DSS, PSD2, GDPR)
- Security requirements (tokenization, encryption, masking, audit)
- Real-world production patterns (Stripe, Privacy.com, Revolut)

### 🏗️ System Design Overview

**High-Level Objective**: Build a microservice enabling virtual card creation, lifecycle management (activate/freeze/unfreeze/close), spending limits, transaction visibility, immutable audit trails, and GDPR compliance.

**Mid-Level Objectives (7)**:
1. PCI-DSS Compliant Data Storage (tokenized PANs, AES-256 encryption, masking)
2. Immutable Audit Trail (append-only events, complete actor tracking)
3. Card Lifecycle State Machine (CREATED → ACTIVE ↔ FROZEN → CLOSED)
4. Spending Limits & Controls (per-transaction/daily/monthly, Decimal precision)
5. Transaction Visibility (filterable logs, pagination, masked responses)
6. Role-Based Access Control (cardholder vs ops_compliance, JWT auth)
7. GDPR Compliance (right to erasure, data portability, retention policies)

**Low-Level Tasks (18)**: Each with prompt template, target files, functions, and detailed acceptance criteria.

### 🛠️ Technology Stack Specified

```yaml
Language: Python 3.11+
Framework: FastAPI 0.110+
ORM: SQLAlchemy 2.0 (async)
Database: PostgreSQL 16
Cache: Redis 7
Testing: pytest + httpx (72 tests specified)
Linting: Ruff + mypy (strict)
```

---

### 🤖 AI Agent Configuration Highlights

**agents.md** — Comprehensive guidelines covering:
- Domain rules (Decimal for money, PAN tokenization, state machine validation)
- Code style (naming conventions, structure patterns, error handling)
- Testing expectations (72 tests across 10 suites, compliance tests)
- Security/compliance constraints (PCI-DSS, GDPR, audit requirements)

**copilot-instructions.md** — Editor-level rules:
- **ALWAYS Do**: Use Decimal, UUID, async def, mask PANs, emit audit events, type hints
- **NEVER Do**: Use float for money, store raw PANs, log sensitive data, skip validation

### 📊 Testing Strategy (72 Tests Specified)

| Test Suite | Tests | Focus |
|------------|-------|-------|
| Models & Services | 34 | PAN masking, state transitions, limit validation |
| RBAC & GDPR | 14 | JWT auth, role enforcement, erasure, export |
| Integration | 10 | Full lifecycle workflows, concurrent operations |
| Compliance | 8 | PAN leak detection, security headers, immutability |
| Performance | 6 | Latency benchmarks (p95 thresholds) |

---

## 🛠️ AI Tools Used

### Primary AI Tools
- [x] **Claude Code** (Primary specification architect)
- [x] **GitHub Copilot** (Markdown formatting assistance)

### How AI Tools Were Used

**Claude Code:**
- Structuring specification from high-level to low-level tasks
- Defining compliance requirements (PCI-DSS, GDPR, PSD2)
- Creating comprehensive agent guidelines with domain rules
- Designing 18 implementation tasks with detailed acceptance criteria

**GitHub Copilot:**
- Auto-completing Markdown tables and formatting
- Suggesting consistent terminology
- Code block syntax for examples

**Effectiveness**: Claude Code excelled at domain-specific specification design; Copilot useful for formatting consistency.

---

## 💡 Key Insights & Best Practices

### Specification Quality
- **Granularity**: Each of 18 tasks includes prompt template, target files, functions, and acceptance criteria
- **Compliance-first**: Security/audit requirements embedded throughout (not bolted on)
- **AI-ready**: Structured format enables autonomous AI implementation

### FinTech Best Practices Demonstrated

| Practice | Location in Spec | Industry Standard |
|----------|-----------------|-------------------|
| PAN tokenization | Task 3, MO-1 | PCI-DSS Req 3.4 |
| Immutable audit trail | Task 4, MO-2 | SOX, PSD2 |
| State machine validation | Task 9, MO-3 | Domain-driven design |
| Decimal precision for money | agents.md Domain Rules | FinTech standard |
| Right to erasure | Task 12, MO-7 | GDPR Art 17 |
| Security headers | Task 15 | OWASP best practice |
| Rate limiting | Task 10 | API security standard |

### Design Decisions Rationale

**Why Python 3.11+?** Type hints, performance, async/await support, mature FinTech ecosystem.

**Why PostgreSQL over MySQL?** Better JSONB support for metadata, row-level security, stronger ACID guarantees.

**Why append-only audit?** Regulatory compliance (SOX, PCI-DSS), forensic integrity, simpler reasoning about system state.

**Why 72 tests?** Comprehensive coverage across functional, security, compliance, and performance dimensions.

---

## 📋 Submission Checklist

### Required Files
- [x] `specification.md` — Complete system specification (620 lines)
- [x] `agents.md` — AI guidelines for FinTech domain (159 lines)
- [x] `.github/copilot-instructions.md` — Editor rules (94 lines)
- [x] `README.md` — Rationale and best practices (88 lines)

### Quality Standards
- [x] High-level objective clearly stated
- [x] 7 mid-level objectives with compliance mappings
- [x] 18 low-level tasks with prompt templates
- [x] Technology stack choices justified
- [x] Security/compliance constraints documented
- [x] Testing strategy specified (72 tests)
- [x] AI agent guidelines comprehensive
- [x] Editor rules actionable (ALWAYS/NEVER)

### Documentation Completeness
- [x] Domain rationale explained
- [x] Architecture decisions justified
- [x] Industry best practices mapped to spec locations
- [x] All compliance frameworks referenced (PCI-DSS, GDPR, PSD2)

---

## 🎓 Reflection

### What Went Well
- **Specification depth**: 18 tasks with line-by-line implementation guidance
- **Compliance integration**: Security/audit requirements woven throughout design
- **AI-readiness**: Structured format with explicit prompts for each task
- **Real-world relevance**: Virtual cards are used by millions in production systems

### Learning About Specification-Driven Design
- **Granularity matters**: Detailed acceptance criteria reduce AI interpretation errors
- **Compliance upfront**: Easier to design-in than retrofit security requirements
- **Agent guidelines critical**: Domain-specific rules (Decimal, PAN masking) prevent common FinTech bugs
- **Testing as specification**: 72 specified tests clarify expected system behavior

### Time Spent
- **Research**: ~2 hours (PCI-DSS requirements, state machine patterns)
- **Specification writing**: ~3 hours (specification.md structure and tasks)
- **Agent configuration**: ~1 hour (agents.md, copilot-instructions.md)
- **Documentation**: ~1 hour (README.md rationale and best practices)

**Total**: ~7 hours for comprehensive specification package

---

## 📚 References

- **PCI-DSS v4.0**: Requirements 3.3, 3.4, 10.2
- **GDPR**: Articles 17 (erasure), 20 (portability)
- **PSD2**: Strong Customer Authentication (SCA)
- **OWASP**: Security Headers Best Practices
- **Real-world systems**: Stripe, Privacy.com, Revolut virtual card implementations
- **Documentation**: ~15 minutes
- **Total**: ~100 minutes

---

## 🔗 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [pytest Documentation](https://docs.pytest.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

## ✨ Bonus Features (Optional)

- Mermaid diagrams in architecture documentation
- 5 Architecture Decision Records (ADRs)
- Performance benchmark suite with timing thresholds
- Manual testing checklist for pre-deployment verification

---

**Ready for review!** 🚀

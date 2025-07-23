# Sample Checklists for Ethical AI Checklist Feature

This document provides sample checklists for testing the Ethical AI Checklist feature.

## Positive Scenario Samples

### Sample Checklist for Upload (EAC-P1)
```
No political content
No religious discussions
Age-appropriate language only
No complex terminology
No controversial topics
```

### Sample Manual Entry (EAC-P2)
```
No biased language
No stereotypes
Factually accurate content only
```

### Sample Safe Content Evaluation (EAC-P3)
- **Checklist:**
  ```
  No political content
  No religious discussions
  ```
- **Text to evaluate:** "Photosynthesis is the process by which plants convert sunlight into energy."
- **Expected result:** No issues detected

### Sample Multiple Guidelines (EAC-P4)
```
No political content
No religious discussions
Age-appropriate language only
No complex terminology
No controversial topics
No biased language
No stereotypes
```

## Negative Scenario Samples

### Sample Content Violating Checklist (EAC-N1)
- **Checklist:**
  ```
  No political content
  No religious discussions
  ```
- **Text to evaluate:** "The president's policy on religious freedom has been controversial among voters."
- **Expected result:** Issues detected for both "political content" and "religious discussions"

### Sample Empty Checklist (EAC-N2)
- **Checklist:** (empty)
- **Text to evaluate:** "Any text"
- **Expected result:** Warning to provide a checklist

### Sample Empty Text (EAC-N3)
- **Checklist:**
  ```
  No political content
  ```
- **Text to evaluate:** (empty)
- **Expected result:** Warning to provide text

### Sample Malformed Checklist (EAC-N5)
```
No political content!!!!
@#$%^&*
Don't use complex terminology
```
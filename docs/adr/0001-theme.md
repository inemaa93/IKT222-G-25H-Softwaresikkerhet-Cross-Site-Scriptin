# ADR 0001: Choose application theme

## Context
We need a simple full-stack app to demonstrate stored XSS with clear input→storage→render flow.

## Options
1) Mini-blog with comments
2) Product reviews

## Decision
Choose **Mini-blog with comments**.

## Rationale
- Fast to implement, fewer screens.
- Clear XSS surface (comments + post body).
- Easy to demonstrate “before/after” mitigation.

## Consequences
- Simpler data model; less breadth of features.

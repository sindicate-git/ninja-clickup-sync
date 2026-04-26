
## `docs/architecture.md`

```md
> **Portfolio Sample Notice**  
> This document describes a **sanitized architecture** of an internal automation concept.  
> Implementation details have been generalized to protect sensitive and proprietary information.

# Architecture Overview

## Problem

NinjaOne and ClickUp do not natively synchronize ticket and task data in the desired workflow.

Without automation, staff may need to manually duplicate ticket information into a project management system, which can lead to:

- Duplicate effort
- Missed tickets
- Inconsistent task tracking
- Delayed visibility across teams

## Solution

This project uses a Python-based sync engine that acts as a bridge between both platforms.

The script:

1. Authenticates with NinjaOne
2. Retrieves ticket data
3. Checks a local mapping file
4. Creates new ClickUp tasks when needed
5. Stores the relationship between Ninja ticket IDs and ClickUp task IDs

## High-Level Flow

```text

NinjaOne Tickets
      │
      ▼
NinjaOne API
      │
      ▼
Python Sync Engine
      │
      ├── Reads config.local.json
      ├── Reads mapping.json
      ├── Prevents duplicate task creation
      │
      ▼
ClickUp API
      │
      ▼
ClickUp Tasks

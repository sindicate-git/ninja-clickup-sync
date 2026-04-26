# ninja-clickup-sync
Python-based integration service syncing NinjaOne tickets to ClickUp via REST APIs with duplicate prevention and mapping logic.
> **Portfolio Sample Notice**  
> This repository contains a **sanitized and simplified version** of an internal automation project.  
> All sensitive data, credentials, and proprietary implementation details have been removed or replaced.  
>  
> The purpose of this version is to demonstrate architecture, API integration, and automation design patterns.

![Portfolio Sample](https://img.shields.io/badge/status-portfolio--sample-blue)

# NinjaOne → ClickUp Ticket Sync

A Python-based automation tool that synchronizes IT support tickets from NinjaOne into ClickUp tasks.

## Overview

This project was built to solve a real-world problem in an MSP environment: bridging the gap between an RMM ticketing system (NinjaOne) and a project/task management platform (ClickUp).

The script acts as a lightweight integration service that:
- Pulls tickets from NinjaOne via API
- Creates corresponding tasks in ClickUp
- Maintains a mapping to prevent duplicate entries

## Architecture
The system uses a lightweight Python sync engine to bridge two platforms:
See full breakdown: [Architecture Documentation](docs/architecture.md)

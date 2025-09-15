# Flowchart Module
``` mermaid
flowchart TD
    A[Start] --> B{Select mode}
    B -->|Offline| C[Offline Mode]
    B -->|Online| D[Online Mode]
    B --> |Formula| E[Formula Mode]
    C --> F[Easy UI] 
    D --> F[Easy UI]
    E --> G[Formula UI]

```

## Tree for Easy UI

```bash
Formula Mode
├── History
│   ├── Show all History
├── Label
│   ├── Show all Labels
├── Formula
├── Formula Task
├── Weigh
├── Settings
│   ├── Calibrate
│   ├── Cap/Resolution
│   ├── Unit
│   ├── Auto-Zero ?
│   ├── Filter Grade ?
│   ├── Stability Level
│   ├── Zero Params ?
│   ├── Zero booting ?
│   ├── Simple Rate ?
│   ├── Zero setting ?
│   ├── Sound effect
├── Devices
│   ├── Scale
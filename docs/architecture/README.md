# System Architecture

## High-Level Architecture
`mermaid
graph TD
    UI[User Interface] --> DH[Device Handlers]
    UI --> VIS[Visualization System]
    UI --> REC[Recording System]

    DH --> |Motion Data| VIS
    DH --> |Motion Data| REC

    subgraph Device Handlers
        XS[XSens Handler] --> DP[Data Processor]
        SS[StretchSense Handler] --> DP
        LL[LiveLink Handler] --> DP
    end

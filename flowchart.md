graph TB
    subgraph Frontend
        UI[Web Interface]
        WS[WebSocket Client]
    end

    subgraph FastAPI_Server
        API[FastAPI Server]
        WSH[WebSocket Handler]
        Queue[Packet Queue]
    end

    subgraph Packet_Capture
        PC[PacketCapture Class]
        Sniff[Scapy Sniffer]
        Process[Packet Processor]
    end

    subgraph ML_System
        Pred[NetworkPredictor]
        Model[ML Model]
        History[Prediction History]
    end

    subgraph Features
        RT[Real-time Analysis]
        CSV[CSV Analysis]
        Rep[Report Generation]
    end

    %% Real-time Flow
    UI -->|1. Start Capture| API
    API -->|2. Initialize| PC
    PC -->|3. Start Thread| Sniff
    Sniff -->|4. Capture Packets| Process
    Process -->|5. Queue Packets| Queue
    Queue -->|6. Get Packets| WSH
    WSH -->|7. Request Prediction| Pred
    Pred -->|8. Use Model| Model
    Model -->|9. Return Prediction| Pred
    Pred -->|10. Store| History
    WSH -->|11. Send Results| WS
    WS -->|12. Update| UI

    %% CSV Analysis Flow
    UI -->|1. Upload CSV| API
    API -->|2. Process CSV| Pred
    Pred -->|3. Batch Predict| Model
    Model -->|4. Return Results| API
    API -->|5. Send Response| UI

    %% Report Generation Flow
    UI -->|1. Request Report| API
    API -->|2. Generate Report| Pred
    Pred -->|3. Analyze History| History
    History -->|4. Create Summary| Pred
    Pred -->|5. Save Report| API
    API -->|6. Return Report| UI

    %% Styling
    classDef primary fill:#2374ab,stroke:#2374ab,color:#fff
    classDef secondary fill:#ff7e67,stroke:#ff7e67,color:#fff
    classDef feature fill:#78a042,stroke:#78a042,color:#fff

    class UI,API,PC,Pred,Model primary
    class WS,WSH,Queue,Process,History secondary
    class RT,CSV,Rep feature

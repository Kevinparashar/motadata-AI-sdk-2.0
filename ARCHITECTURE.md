# Metadata Python SDK - Architecture & Workflow Visualization

## Table of Contents
- [System Architecture Overview](#system-architecture-overview)
- [Component Interaction Diagram](#component-interaction-diagram)
- [Data Flow Architecture](#data-flow-architecture)
- [Module Dependencies](#module-dependencies)
- [Workflow Diagrams](#workflow-diagrams)
- [Sequence Diagrams](#sequence-diagrams)
- [Observability Architecture](#observability-architecture)
- [Deployment Architecture](#deployment-architecture)

---

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Metadata Python SDK                               │
│                         (Unified Interface)                              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
            ┌───────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
            │   Core       │ │   Agents    │ │  AI Gateway │
            │  Foundation  │ │   Module    │ │   Module    │
            └───────┬──────┘ └──────┬──────┘ └──────┬──────┘
                    │               │               │
            ┌───────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
            │   Database   │ │     API      │ │   Codecs    │
            │   Module     │ │   Module     │ │   Module    │
            └───────┬──────┘ └──────┬──────┘ └──────┬──────┘
                    │               │               │
                    └───────────────┼───────────────┘
                                    │
                            ┌───────▼───────┐
                            │    Config     │
                            │    Module     │
                            │  (Settings,   │
                            │   Logging,    │
                            │ Observability)│
                            └───────────────┘
                                    │
                            ┌───────▼───────┐
                            │ Observability │
                            │  (Metrics,    │
                            │   Tracing,    │
                            │  Monitoring)  │
                            └───────────────┘
```

---

## Component Interaction Diagram

```mermaid
graph TB
    subgraph "Application Layer"
        APP[Application Code]
    end
    
    subgraph "SDK Core Layer"
        CORE[Core Module]
        VALID[Validators]
        EXCEPT[Exceptions]
        DATA[Data Structures]
        CONCUR[Concurrency]
        EVENT[Event Handler]
        UTILS[Utilities]
    end
    
    subgraph "Functional Modules"
        AGENT[Agents Module<br/>Agno Framework]
        AI[AI Gateway<br/>LiteLLM]
        DB[Database Module<br/>PostgreSQL]
        API[API Module]
        CODEC[Codecs Module]
        CONFIG[Config Module]
        OBS[Observability<br/>Metrics, Tracing,<br/>Health Checks]
    end
    
    subgraph "External Services"
        LITELLM[LiteLLM<br/>Unified AI Gateway<br/>OpenAI, Anthropic, Gemini]
        POSTGRES[PostgreSQL<br/>Database]
        EXT_API[External APIs]
        MSG[Message Queue<br/>NATS]
        MONITOR[Monitoring Tools<br/>Prometheus, Datadog,<br/>Jaeger]
    end
    
    APP --> AGENT
    APP --> AI
    APP --> DB
    APP --> API
    
    AGENT --> CORE
    AGENT --> API
    AGENT --> MSG
    AGENT --> LITELLM
    
    AI --> CORE
    AI --> API
    AI --> CODEC
    AI --> LITELLM
    
    DB --> CORE
    DB --> POSTGRES
    
    API --> CORE
    API --> CODEC
    API --> EXT_API
    
    CORE --> VALID
    CORE --> EXCEPT
    CORE --> DATA
    CORE --> CONCUR
    CORE --> EVENT
    CORE --> UTILS
    
    CONFIG --> CORE
    CONFIG --> UTILS
    
    OBS --> CORE
    OBS --> CONFIG
    OBS --> EVENT
    
    AGENT --> OBS
    AI --> OBS
    DB --> OBS
    API --> OBS
    
    OBS --> MONITOR
    
    style CORE fill:#e1f5ff
    style VALID fill:#fff4e1
    style EXCEPT fill:#ffe1e1
    style AGENT fill:#e1ffe1
    style AI fill:#f0e1ff
    style DB fill:#ffe1f0
    style API fill:#e1ffff
    style OBS fill:#ffe1ff
    style MONITOR fill:#e1e1ff
```

---

## Data Flow Architecture

```mermaid
flowchart LR
    subgraph "Input Layer"
        USER[User Input]
        CONFIG_IN[Configuration]
    end
    
    subgraph "Validation Layer"
        VALIDATE[Input Validators]
        CHECK{Validation<br/>Pass?}
    end
    
    subgraph "Processing Layer"
        AGENT_PROC[Agent Processing]
        AI_PROC[AI Processing]
        DB_PROC[Database Operations]
        API_PROC[API Communication]
    end
    
    subgraph "Transformation Layer"
        CODEC_PROC[Encoding/Decoding]
        FORMAT[Data Formatting]
    end
    
    subgraph "Output Layer"
        RESPONSE[Response Model]
        EVENTS[Event Emission]
        LOGS[Logging]
        METRICS[Metrics Collection]
        TRACES[Distributed Traces]
    end
    
    USER --> VALIDATE
    CONFIG_IN --> VALIDATE
    VALIDATE --> CHECK
    CHECK -->|Pass| AGENT_PROC
    CHECK -->|Pass| AI_PROC
    CHECK -->|Pass| DB_PROC
    CHECK -->|Pass| API_PROC
    CHECK -->|Fail| EXCEPT[Exception Handler]
    
    AGENT_PROC --> CODEC_PROC
    AI_PROC --> CODEC_PROC
    DB_PROC --> FORMAT
    API_PROC --> CODEC_PROC
    
    CODEC_PROC --> RESPONSE
    FORMAT --> RESPONSE
    RESPONSE --> EVENTS
    RESPONSE --> LOGS
    RESPONSE --> METRICS
    RESPONSE --> TRACES
    
    EXCEPT --> EVENTS
    EXCEPT --> LOGS
    EXCEPT --> METRICS
```

---

## Module Dependencies

```mermaid
graph TD
    subgraph "Layer 1: Foundation"
        CORE[Core Module]
    end
    
    subgraph "Layer 2: Base Modules"
        CONFIG[Config Module]
        CODEC[Codecs Module]
    end
    
    subgraph "Layer 3: Functional Modules"
        API[API Module]
        DB[Database Module]
        AI[AI Gateway Module]
        AGENT[Agents Module]
    end
    
    subgraph "Layer 4: Application"
        APP[Application Code]
    end
    
    CONFIG --> CORE
    CODEC --> CORE
    
    API --> CORE
    API --> CONFIG
    API --> CODEC
    
    DB --> CORE
    DB --> CONFIG
    
    AI --> CORE
    AI --> API
    AI --> CODEC
    AI --> CONFIG
    
    AGENT --> CORE
    AGENT --> API
    AGENT --> CONFIG
    
    APP --> AGENT
    APP --> AI
    APP --> DB
    APP --> API
    
    style CORE fill:#4a90e2,color:#fff
    style CONFIG fill:#7b68ee,color:#fff
    style CODEC fill:#7b68ee,color:#fff
    style API fill:#50c878,color:#fff
    style DB fill:#50c878,color:#fff
    style AI fill:#50c878,color:#fff
    style AGENT fill:#50c878,color:#fff
```

---

## Workflow Diagrams

### 1. Agent Task Execution Workflow (Agno)

```mermaid
sequenceDiagram
    participant App as Application
    participant Agent as Agent Module<br/>(Agno)
    participant Validator as Validators
    participant Agno as Agno Framework
    participant LiteLLM as LiteLLM Gateway
    participant DB as PostgreSQL
    participant Event as Event Handler
    
    App->>Agent: execute_task(task)
    Agent->>Validator: validate_task(task)
    alt Validation Success
        Validator-->>Agent: Validated Task
        Agent->>Event: emit("task_started")
        Agent->>Agno: process_task(prompt)
        Agno->>LiteLLM: generate_response()
        LiteLLM-->>Agno: AI Response
        Agno-->>Agent: Processed Result
        Agent->>DB: save_result(data)
        DB-->>Agent: Success
        Agent->>Event: emit("task_completed")
        Agent-->>App: Task Result
    else Validation Failed
        Validator-->>Agent: ValidationError
        Agent->>Event: emit("task_error")
        Agent-->>App: Exception
    end
```

### 2. AI Gateway Request Workflow (LiteLLM)

```mermaid
sequenceDiagram
    participant App as Application
    participant Gateway as AI Gateway
    participant Validator as Validators
    participant LiteLLM as LiteLLM Provider
    participant AI_API as AI Provider APIs<br/>(OpenAI, Anthropic, etc.)
    participant Codec as Codecs
    
    App->>Gateway: generate(prompt, model)
    Gateway->>Validator: validate_string(prompt)
    Gateway->>Validator: validate_string(model)
    alt Validation Success
        Gateway->>Codec: preprocess_input(prompt)
        Codec-->>Gateway: Processed Input
        Gateway->>LiteLLM: completion(model, messages)
        LiteLLM->>AI_API: Unified API Request
        AI_API-->>LiteLLM: Provider Response
        LiteLLM-->>Gateway: Unified Response
        Gateway->>Codec: postprocess_output(response)
        Codec-->>Gateway: Processed Output
        Gateway-->>App: Final Response
    else Validation Failed
        Validator-->>Gateway: ValidationError
        Gateway-->>App: Exception
    end
```

### 3. PostgreSQL Database Operation Workflow

```mermaid
sequenceDiagram
    participant App as Application
    participant DB as PostgreSQL Module
    participant Validator as Validators
    participant Pool as Connection Pool<br/>(psycopg2)
    participant PG as PostgreSQL Server
    participant Event as Event Handler
    
    App->>DB: execute_query(query, params)
    DB->>Validator: validate_string(query)
    DB->>Validator: validate_list(params)
    alt Validation Success
        DB->>DB: check_connection()
        alt Connected
            DB->>Pool: get_connection()
            Pool-->>DB: Connection
            DB->>PG: execute(query, params)
            PG-->>DB: Query Results
            DB->>Pool: return_connection()
            DB->>Event: emit("query_success")
            DB-->>App: Results
        else Not Connected
            DB-->>App: ConnectionError
        end
    else Validation Failed
        Validator-->>DB: ValidationError
        DB-->>App: Exception
    end
```

### 4. API Communication Workflow

```mermaid
sequenceDiagram
    participant App as Application
    participant API as API Communicator
    participant Auth as Authenticator
    participant Validator as Validators
    participant ExtAPI as External API
    participant Codec as Codecs
    
    App->>API: get(endpoint, params)
    API->>Validator: validate_string(endpoint)
    API->>Validator: validate_dict(params)
    alt Validation Success
        API->>Auth: get_access_token()
        Auth-->>API: Token
        API->>Codec: encode_data(params)
        Codec-->>API: Encoded Data
        API->>ExtAPI: HTTP GET Request
        ExtAPI-->>API: HTTP Response
        API->>Codec: decode_data(response)
        Codec-->>API: Decoded Data
        API-->>App: ResponseModel
    else Validation Failed
        Validator-->>API: ValidationError
        API-->>App: Exception
    end
```

---

## Detailed Component Communication

### Core Module Internal Structure

```
┌─────────────────────────────────────────────────────────────┐
│                      Core Module                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Data       │  │  Concurrency │  │    Event     │    │
│  │ Structures  │  │   Utilities  │  │   Handler     │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
│         │                 │                 │             │
│         └─────────────────┼─────────────────┘             │
│                           │                               │
│  ┌──────────────┐  ┌──────▼───────┐  ┌──────────────┐   │
│  │  Validators  │  │   Utilities  │  │  Exceptions  │   │
│  └──────┬───────┘  └──────────────┘  └──────┬───────┘   │
│         │                                    │            │
│         └────────────────────────────────────┘            │
│                                                           │
│              All modules depend on Core                   │
└───────────────────────────────────────────────────────────┘
```

### Agent Module Architecture (Agno Framework)

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Module (Agno)                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              Agent Class                            │  │
│  │  - Lifecycle Management (start, stop)              │  │
│  │  - Task Execution via Agno                        │  │
│  │  - Event Handling                                    │  │
│  │  - Status Management                                 │  │
│  └──────────────┬──────────────────────────────────────┘  │
│                 │                                          │
│  ┌──────────────▼──────────────────────────────────────┐  │
│  │        Agno Framework Integration                   │  │
│  │  - AgnoAgent (from agno package)                   │  │
│  │  - LLM Integration                                  │  │
│  │  - Intelligent Task Processing                     │  │
│  └──────────────┬──────────────────────────────────────┘  │
│                 │                                          │
│  ┌──────────────▼──────────────────────────────────────┐  │
│  │        Agent Communicator                           │  │
│  │  - Message Sending/Receiving                         │  │
│  │  - Topic Subscription                               │  │
│  │  - Protocol Handling (NATS, etc.)                   │  │
│  └──────────────┬──────────────────────────────────────┘  │
│                 │                                          │
│                 ├──────────────┐                          │
│                 │              │                          │
│  ┌──────────────▼──┐  ┌────────▼──────────┐              │
│  │  Event Emitter  │  │  LiteLLM Gateway  │              │
│  │  (from Core)    │  │  (for AI tasks)   │              │
│  └─────────────────┘  └──────────────────┘              │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### AI Gateway Module Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  AI Gateway Module                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              AIGateway (Main Interface)              │  │
│  │  - generate()                                       │  │
│  │  - chat()                                           │  │
│  │  - embed()                                          │  │
│  └──────────────┬──────────────────────────────────────┘  │
│                 │                                          │
│  ┌──────────────▼──────────────────────────────────────┐  │
│  │        Model Integration Factory                    │  │
│  │  - LiteLLMProvider                                  │  │
│  │  (Unified interface for OpenAI, Anthropic,          │  │
│  │   Gemini, and other providers)                     │  │
│  └──────────────┬──────────────────────────────────────┘  │
│                 │                                          │
│  ┌──────────────▼──────────────────────────────────────┐  │
│  │        Prompt Manager                               │  │
│  │  - Template Management                              │  │
│  │  - Dynamic Prompt Generation                        │  │
│  └──────────────┬──────────────────────────────────────┘  │
│                 │                                          │
│  ┌──────────────▼──────────────────────────────────────┐  │
│  │        Input/Output Processing                      │  │
│  │  - preprocess_input()                               │  │
│  │  - postprocess_output()                             │  │
│  │  - normalize_text()                                 │  │
│  │  - chunk_text()                                     │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

---

## Complete System Workflow

```mermaid
graph TB
    subgraph "User Application"
        START([User Request])
    end
    
    subgraph "SDK Entry Points"
        AGENT_ENTRY[Agent Module]
        AI_ENTRY[AI Gateway]
        DB_ENTRY[Database Module]
        API_ENTRY[API Module]
    end
    
    subgraph "Core Processing"
        VALIDATE[Input Validation]
        EXCEPT_HANDLE[Exception Handling]
        EVENT_EMIT[Event Emission]
    end
    
    subgraph "External Services"
        AI_SERV[AI Providers]
        DB_SERV[Databases]
        EXT_API[External APIs]
    end
    
    subgraph "Response Processing"
        CODEC_PROC[Encoding/Decoding]
        FORMAT[Response Formatting]
        LOG[Logging]
    end
    
    subgraph "Output"
        RESPONSE([Response to User])
    end
    
    START --> AGENT_ENTRY
    START --> AI_ENTRY
    START --> DB_ENTRY
    START --> API_ENTRY
    
    AGENT_ENTRY --> VALIDATE
    AI_ENTRY --> VALIDATE
    DB_ENTRY --> VALIDATE
    API_ENTRY --> VALIDATE
    
    VALIDATE -->|Success| EVENT_EMIT
    VALIDATE -->|Failure| EXCEPT_HANDLE
    
    EVENT_EMIT --> AI_SERV
    EVENT_EMIT --> DB_SERV
    EVENT_EMIT --> EXT_API
    
    AI_SERV --> CODEC_PROC
    DB_SERV --> FORMAT
    EXT_API --> CODEC_PROC
    
    CODEC_PROC --> LOG
    FORMAT --> LOG
    EXCEPT_HANDLE --> LOG
    
    LOG --> RESPONSE
    
    style START fill:#90EE90
    style RESPONSE fill:#90EE90
    style VALIDATE fill:#FFD700
    style EXCEPT_HANDLE fill:#FF6B6B
    style EVENT_EMIT fill:#4ECDC4
```

---

## Error Handling Flow

```mermaid
flowchart TD
    START([Operation Starts])
    VALIDATE{Input<br/>Validation}
    VALIDATE -->|Pass| PROCESS[Process Request]
    VALIDATE -->|Fail| VALID_ERROR[ValidationError]
    
    PROCESS --> OPERATION{Operation<br/>Type}
    OPERATION -->|API| API_CALL[API Call]
    OPERATION -->|Database| DB_CALL[Database Query]
    OPERATION -->|AI| AI_CALL[AI Request]
    
    API_CALL --> API_RESULT{Result}
    DB_CALL --> DB_RESULT{Result}
    AI_CALL --> AI_RESULT{Result}
    
    API_RESULT -->|Success| SUCCESS[Success Response]
    API_RESULT -->|Failure| API_ERROR[APIError]
    
    DB_RESULT -->|Success| SUCCESS
    DB_RESULT -->|Failure| DB_ERROR[DatabaseError]
    
    AI_RESULT -->|Success| SUCCESS
    AI_RESULT -->|Failure| MODEL_ERROR[ModelError]
    
    VALID_ERROR --> EXCEPT_HANDLER[Exception Handler]
    API_ERROR --> EXCEPT_HANDLER
    DB_ERROR --> EXCEPT_HANDLER
    MODEL_ERROR --> EXCEPT_HANDLER
    
    EXCEPT_HANDLER --> LOG_ERROR[Log Error]
    EXCEPT_HANDLER --> EMIT_EVENT[Emit Error Event]
    EXCEPT_HANDLER --> RETURN_ERROR[Return Error to User]
    
    SUCCESS --> LOG_SUCCESS[Log Success]
    SUCCESS --> EMIT_SUCCESS[Emit Success Event]
    SUCCESS --> RETURN_SUCCESS[Return Response]
    
    style VALID_ERROR fill:#FF6B6B
    style API_ERROR fill:#FF6B6B
    style DB_ERROR fill:#FF6B6B
    style MODEL_ERROR fill:#FF6B6B
    style SUCCESS fill:#90EE90
```

---

## Authentication Flow

```mermaid
sequenceDiagram
    participant App as Application
    participant API as API Module
    participant Auth as Authenticator
    participant Validator as Validators
    participant TokenStore as Token Storage
    participant ExtAPI as External API
    
    App->>API: make_request(endpoint)
    API->>Auth: get_access_token()
    
    alt Token Exists & Valid
        Auth->>TokenStore: check_token()
        TokenStore-->>Auth: Valid Token
        Auth-->>API: Return Token
    else Token Missing or Expired
        Auth->>Validator: validate_credentials()
        alt OAuth2
            Auth->>ExtAPI: Request Token
            ExtAPI-->>Auth: New Token
            Auth->>TokenStore: Store Token
            Auth-->>API: Return Token
        else JWT
            Auth->>Auth: Generate JWT
            Auth->>TokenStore: Store Token
            Auth-->>API: Return Token
        else API Key
            Auth->>Auth: Return API Key
            Auth-->>API: Return Key
        end
    end
    
    API->>ExtAPI: Request with Auth
    ExtAPI-->>API: Response
    API-->>App: Response
```

---

## Configuration Management Flow

```
┌─────────────────────────────────────────────────────────────┐
│              Configuration Management                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  File Config │  │  Env Config  │  │  Code Config │    │
│  │  (JSON/YAML) │  │  Variables   │  │  (Dict)      │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
│         │                 │                 │             │
│         └─────────────────┼─────────────────┘             │
│                           │                               │
│                  ┌────────▼────────┐                      │
│                  │  Settings Class │                      │
│                  │  - Merge Config │                      │
│                  │  - Validate     │                      │
│                  │  - Cache        │                      │
│                  └────────┬────────┘                      │
│                           │                               │
│         ┌─────────────────┼─────────────────┐            │
│         │                 │                 │            │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐     │
│  │   Agents    │  │  AI Gateway │  │  Database   │     │
│  │   Module    │  │   Module    │  │   Module    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

---

## Data Transformation Pipeline

```mermaid
graph LR
    subgraph "Input"
        RAW[Raw Input Data]
    end
    
    subgraph "Validation"
        VAL[Validators]
    end
    
    subgraph "Preprocessing"
        PRE[Preprocess Input]
        NORM[Normalize Text]
        CHUNK[Chunk Text]
    end
    
    subgraph "Encoding"
        ENCODE[Codec Encode]
    end
    
    subgraph "Processing"
        PROC[Process Data]
    end
    
    subgraph "Decoding"
        DECODE[Codec Decode]
    end
    
    subgraph "Postprocessing"
        POST[Postprocess Output]
        FORMAT[Format Response]
    end
    
    subgraph "Output"
        OUT[Structured Output]
    end
    
    RAW --> VAL
    VAL --> PRE
    PRE --> NORM
    NORM --> CHUNK
    CHUNK --> ENCODE
    ENCODE --> PROC
    PROC --> DECODE
    DECODE --> POST
    POST --> FORMAT
    FORMAT --> OUT
```

---

## Module Interaction Matrix

| Module | Depends On | Used By |
|--------|-----------|---------|
| **Core** | None (Foundation) | All Modules |
| **Config** | Core | All Modules |
| **Codecs** | Core | API, AI Gateway |
| **API** | Core, Config, Codecs | Agents, AI Gateway |
| **Database** | Core, Config | Agents, Applications |
| **AI Gateway** | Core, API, Codecs, Config | Agents, Applications |
| **Agents** | Core, API, Config | Applications |
| **Observability** | Core, Config, Event Handler | All Modules, Monitoring Tools |

---

## Key Design Principles

### 1. **Layered Architecture**
- **Layer 1**: Core foundation (data structures, utilities, exceptions)
- **Layer 2**: Base modules (config, codecs, observability)
- **Layer 3**: Functional modules (agents, AI, database, API)
- **Layer 4**: Application code

### 2. **Dependency Flow**
- All modules depend on Core
- No circular dependencies
- Clear separation of concerns

### 3. **Error Handling**
- Centralized exception hierarchy
- Validation at entry points
- Detailed error context

### 4. **Event-Driven**
- Event emission for important operations
- Asynchronous event handling
- Decoupled component communication

### 5. **Type Safety**
- Full type hints throughout
- Input validation on all public methods
- Runtime type checking

### 6. **Observability**
- Comprehensive metrics collection (counters, gauges, histograms)
- Distributed tracing across services
- Performance monitoring (latency, throughput)
- Health checks for system components
- Integration with monitoring tools (Prometheus, Datadog, Jaeger)

---

## Observability Architecture

### Observability Component Structure

```mermaid
graph TB
    subgraph "Observability Module"
        OBS_MAIN[Observability<br/>Main Class]
        
        subgraph "Metrics"
            METRICS_REG[Metrics Registry]
            COUNTER[Counter Metrics]
            GAUGE[Gauge Metrics]
            HISTOGRAM[Histogram Metrics]
        end
        
        subgraph "Tracing"
            TRACER[Tracer]
            SPAN[Trace Span]
            TRACE_ID[Trace IDs]
        end
        
        subgraph "Performance"
            PERF_MON[Performance Monitor]
            LATENCY[Latency Tracking]
            THROUGHPUT[Throughput Monitoring]
        end
        
        subgraph "Health"
            HEALTH_CHECKER[Health Checker]
            HEALTH_CHECK[Health Check]
            STATUS[Status Reporting]
        end
    end
    
    subgraph "SDK Modules"
        AGENT_MOD[Agents]
        AI_MOD[AI Gateway]
        DB_MOD[Database]
        API_MOD[API]
    end
    
    subgraph "External Monitoring"
        PROM[Prometheus]
        DD[Datadog]
        JAEGER[Jaeger]
    end
    
    OBS_MAIN --> METRICS_REG
    OBS_MAIN --> TRACER
    OBS_MAIN --> PERF_MON
    OBS_MAIN --> HEALTH_CHECKER
    
    METRICS_REG --> COUNTER
    METRICS_REG --> GAUGE
    METRICS_REG --> HISTOGRAM
    
    TRACER --> SPAN
    TRACER --> TRACE_ID
    
    PERF_MON --> LATENCY
    PERF_MON --> THROUGHPUT
    
    HEALTH_CHECKER --> HEALTH_CHECK
    HEALTH_CHECKER --> STATUS
    
    AGENT_MOD --> OBS_MAIN
    AI_MOD --> OBS_MAIN
    DB_MOD --> OBS_MAIN
    API_MOD --> OBS_MAIN
    
    OBS_MAIN --> PROM
    OBS_MAIN --> DD
    OBS_MAIN --> JAEGER
    
    style OBS_MAIN fill:#ffe1ff
    style METRICS_REG fill:#e1ffe1
    style TRACER fill:#e1f5ff
    style PERF_MON fill:#fff4e1
    style HEALTH_CHECKER fill:#ffe1e1
```

### Observability Data Flow

```mermaid
flowchart LR
    subgraph "SDK Operations"
        OP1[Agent Task]
        OP2[AI Request]
        OP3[DB Query]
        OP4[API Call]
    end
    
    subgraph "Observability Collection"
        MET[Collect Metrics]
        TRACE[Create Spans]
        PERF[Measure Performance]
        HEALTH[Run Health Checks]
    end
    
    subgraph "Observability Storage"
        MET_STORE[Metrics Registry]
        TRACE_STORE[Trace Store]
        PERF_STORE[Performance Data]
        HEALTH_STORE[Health Status]
    end
    
    subgraph "Export & Integration"
        EXPORT[Export Data]
        PROM_EXP[Prometheus Format]
        DD_EXP[Datadog Format]
        JAEGER_EXP[Jaeger Format]
    end
    
    OP1 --> MET
    OP1 --> TRACE
    OP1 --> PERF
    
    OP2 --> MET
    OP2 --> TRACE
    OP2 --> PERF
    
    OP3 --> MET
    OP3 --> TRACE
    OP3 --> PERF
    OP3 --> HEALTH
    
    OP4 --> MET
    OP4 --> TRACE
    OP4 --> PERF
    OP4 --> HEALTH
    
    MET --> MET_STORE
    TRACE --> TRACE_STORE
    PERF --> PERF_STORE
    HEALTH --> HEALTH_STORE
    
    MET_STORE --> EXPORT
    TRACE_STORE --> EXPORT
    PERF_STORE --> EXPORT
    HEALTH_STORE --> EXPORT
    
    EXPORT --> PROM_EXP
    EXPORT --> DD_EXP
    EXPORT --> JAEGER_EXP
```

### Observability Integration Workflow

```mermaid
sequenceDiagram
    participant App as Application
    participant SDK as SDK Module
    participant Obs as Observability
    participant Metrics as Metrics Registry
    participant Tracer as Tracer
    participant Monitor as Performance Monitor
    participant Health as Health Checker
    participant Ext as External Tools
    
    App->>SDK: Execute Operation
    SDK->>Obs: Start Monitoring
    
    Obs->>Tracer: Start Span
    Obs->>Monitor: Start Measurement
    Obs->>Metrics: Record Counter
    
    SDK->>SDK: Process Operation
    
    SDK->>Obs: End Monitoring
    Obs->>Tracer: Finish Span
    Obs->>Monitor: End Measurement
    Obs->>Metrics: Update Metrics
    
    Obs->>Health: Check Health
    Health-->>Obs: Health Status
    
    Obs->>Ext: Export Metrics
    Obs->>Ext: Export Traces
    Obs->>Ext: Export Performance Data
    
    Ext-->>App: Monitoring Dashboard
```

### Metrics Collection Flow

```mermaid
graph TD
    START([Operation Starts])
    START --> VALIDATE{Input<br/>Validation}
    
    VALIDATE -->|Pass| OP_START[Operation Start]
    VALIDATE -->|Fail| METRIC_ERROR[Record Error Metric]
    
    OP_START --> METRIC_START[Record Start Metric]
    METRIC_START --> TRACE_START[Start Trace Span]
    TRACE_START --> PERF_START[Start Performance Timer]
    
    PERF_START --> EXECUTE[Execute Operation]
    
    EXECUTE -->|Success| METRIC_SUCCESS[Increment Success Counter]
    EXECUTE -->|Error| METRIC_FAIL[Increment Error Counter]
    
    METRIC_SUCCESS --> PERF_END[End Performance Timer]
    METRIC_FAIL --> PERF_END
    
    PERF_END --> HISTOGRAM[Record Latency Histogram]
    HISTOGRAM --> TRACE_END[End Trace Span]
    TRACE_END --> METRIC_END[Record End Metric]
    
    METRIC_ERROR --> END([End])
    METRIC_END --> END
    
    style METRIC_ERROR fill:#FF6B6B
    style METRIC_FAIL fill:#FF6B6B
    style METRIC_SUCCESS fill:#90EE90
```

### Health Check Architecture

```mermaid
graph TB
    subgraph "Health Check System"
        HC_REGISTRY[Health Checker Registry]
        
        subgraph "Component Checks"
            DB_CHECK[Database Health]
            API_CHECK[API Health]
            AI_CHECK[AI Gateway Health]
            AGENT_CHECK[Agent Health]
        end
        
        subgraph "System Checks"
            MEM_CHECK[Memory Health]
            CPU_CHECK[CPU Health]
            DISK_CHECK[Disk Health]
        end
    end
    
    subgraph "Health Status"
        STATUS_AGG[Aggregated Status]
        DETAILS[Detailed Results]
        TIMESTAMPS[Check Timestamps]
    end
    
    subgraph "Integration"
        API_ENDPOINT[Health API Endpoint]
        MONITORING[Monitoring Tools]
        ALERTS[Alert System]
    end
    
    HC_REGISTRY --> DB_CHECK
    HC_REGISTRY --> API_CHECK
    HC_REGISTRY --> AI_CHECK
    HC_REGISTRY --> AGENT_CHECK
    HC_REGISTRY --> MEM_CHECK
    HC_REGISTRY --> CPU_CHECK
    HC_REGISTRY --> DISK_CHECK
    
    DB_CHECK --> STATUS_AGG
    API_CHECK --> STATUS_AGG
    AI_CHECK --> STATUS_AGG
    AGENT_CHECK --> STATUS_AGG
    MEM_CHECK --> STATUS_AGG
    CPU_CHECK --> STATUS_AGG
    DISK_CHECK --> STATUS_AGG
    
    STATUS_AGG --> DETAILS
    STATUS_AGG --> TIMESTAMPS
    
    STATUS_AGG --> API_ENDPOINT
    STATUS_AGG --> MONITORING
    STATUS_AGG --> ALERTS
```

### Observability Integration Points

```
┌─────────────────────────────────────────────────────────────┐
│              SDK Module (Agent/AI/DB/API)                    │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ Observability Hooks
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
│   Metrics    │ │   Tracing   │ │ Performance │
│  Collection  │ │   System    │ │  Monitoring │
└───────┬──────┘ └──────┬──────┘ └──────┬──────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
                ┌───────▼───────┐
                │ Observability │
                │   Main Class  │
                └───────┬───────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
│  Prometheus  │ │   Datadog   │ │   Jaeger    │
│   Exporter   │ │   Adapter   │ │   Adapter   │
└──────────────┘ └─────────────┘ └─────────────┘
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│              (User's Application Code)                       │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                  Metadata Python SDK                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Agents   │  │    AI    │  │ Database │  │   API    │   │
│  │ Module   │  │ Gateway  │  │  Module  │  │  Module  │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │              │             │          │
│       └─────────────┼──────────────┼─────────────┘          │
│                     │              │                        │
│              ┌──────▼──────────────▼──────┐                │
│              │      Core Module           │                │
│              │  (Foundation & Utilities) │                │
│              └──────────────┬─────────────┘                │
│                             │                              │
│              ┌──────────────▼──────────────┐              │
│              │   Config & Observability    │              │
│              │  (Settings, Logging,        │              │
│              │   Metrics, Tracing)        │              │
│              └─────────────────────────────┘              │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
│   LiteLLM    │ │ PostgreSQL  │ │ External    │
│ (AI Gateway) │ │  Database   │ │ APIs        │
│ OpenAI,      │ │             │ │             │
│ Anthropic,   │ │             │ │             │
│ Gemini, etc. │ │             │ │             │
└──────────────┘ └─────────────┘ └─────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
│ Prometheus   │ │   Datadog   │ │   Jaeger    │
│ (Metrics)    │ │   (APM)     │ │  (Tracing)  │
└──────────────┘ └─────────────┘ └─────────────┘
```

---

## Summary

This architecture visualization demonstrates:

1. **Clear Separation of Concerns**: Each module has a specific responsibility
2. **Dependency Management**: Core module provides foundation for all others
3. **Data Flow**: Clear paths from input to output with validation and transformation
4. **Error Handling**: Comprehensive exception handling at every layer
5. **Scalability**: Modular design allows easy extension and modification
6. **Type Safety**: Validation ensures data integrity throughout the system
7. **Event-Driven**: Asynchronous event handling for decoupled communication
8. **Observability**: Comprehensive monitoring with metrics, tracing, performance tracking, and health checks

The SDK is designed to be:
- **Modular**: Use only what you need
- **Extensible**: Easy to add new providers, databases, or features
- **Reliable**: Comprehensive error handling and validation
- **Performant**: Async support and efficient data processing
- **Maintainable**: Clear architecture and documentation
- **Observable**: Full visibility into system behavior with metrics, traces, and health monitoring


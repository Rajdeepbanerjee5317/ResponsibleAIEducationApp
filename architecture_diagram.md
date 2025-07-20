# Responsible AI Education App - Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                FRONTEND LAYER                               │
│                              (Streamlit UI)                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │  streamlit_app  │    │     pages/      │    │     Static      │        │
│  │      .py        │    │                 │    │   Resources     │        │
│  │                 │    │ • Personalized │    │                 │        │
│  │ • Main Entry    │    │   Q&A.py        │    │ • Config        │        │
│  │ • Navigation    │    │ • Free_Text_    │    │ • Styling       │        │
│  │ • Layout        │    │   Generation.py │    │ • Assets        │        │
│  │                 │    │ • Evaluate_     │    │                 │        │
│  │                 │    │   Outputs.py    │    │                 │        │
│  │                 │    │ • Ethical_AI_   │    │                 │        │
│  │                 │    │   Checklist.py  │    │                 │        │
│  │                 │    │ • Responsible_  │    │                 │        │
│  │                 │    │   Prompting.py  │    │                 │        │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       │ API Calls
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                               BACKEND LAYER                                 │
│                            (Business Logic)                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────┐    ┌─────────────────────────────────┐ │
│  │      services/                  │    │         Data Layer              │ │
│  │                                 │    │                                 │ │
│  │  ┌─────────────────────────────┐ │    │  ┌─────────────────────────────┐ │ │
│  │  │   evaluation_service.py     │ │    │  │       Constants             │ │ │
│  │  │                             │ │    │  │                             │ │ │
│  │  │ • generate_safe_text()      │ │    │  │ • UNSAFE_KEYWORDS           │ │ │
│  │  │ • evaluate_text()           │ │    │  │ • DEFAULT_PRINCIPLES        │ │ │
│  │  │ • load_checklist_from_file()│ │    │  │ • Safety Guidelines         │ │ │
│  │  └─────────────────────────────┘ │    │  └─────────────────────────────┘ │ │
│  │                                 │    │                                 │ │
│  │  ┌─────────────────────────────┐ │    │  ┌─────────────────────────────┐ │ │
│  │  │    prompt_service.py        │ │    │  │       Scenarios             │ │ │
│  │  │                             │ │    │  │                             │ │ │
│  │  │ • get_scenario()            │ │    │  │ • Educational Templates    │ │ │
│  │  │ • analyze_prompt_quality()  │ │    │  │ • Simulated Responses       │ │ │
│  │  │ • get_simulated_response()  │ │    │  │ • Prompt Keywords           │ │ │
│  │  └─────────────────────────────┘ │    │  └─────────────────────────────┘ │ │
│  └─────────────────────────────────┘    └─────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       │ External Dependencies
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            EXTERNAL LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │   Streamlit     │    │   LangChain     │    │   File System   │        │
│  │   Framework     │    │   Templates     │    │                 │        │
│  │                 │    │                 │    │ • User Uploads  │        │
│  │ • UI Components │    │ • PromptTemplate│    │ • Checklists    │        │
│  │ • State Mgmt    │    │ • Text Processing│    │ • Config Files  │        │
│  │ • Routing       │    │                 │    │                 │        │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

## Component Responsibilities

### Frontend Layer (Streamlit UI)
- **streamlit_app.py**: Main application entry point, navigation, and layout
- **pages/**: Individual page components for different features
  - User interface and interaction handling
  - Form validation and user input processing
  - Display of results and feedback

### Backend Layer (Business Logic)
- **evaluation_service.py**: Core safety and evaluation logic
  - Content safety filtering
  - Text evaluation against AI principles
  - Custom checklist processing
- **prompt_service.py**: Prompt analysis and educational scenarios
  - Prompt quality assessment
  - Educational scenario management
  - Simulated AI response generation

### Data Flow
1. User interacts with Frontend (Streamlit pages)
2. Frontend calls Backend services for processing
3. Backend processes data using business logic
4. Backend returns results to Frontend
5. Frontend displays results to user

### Key Architectural Principles
- **Separation of Concerns**: UI logic separated from business logic
- **Modularity**: Services are independent and reusable
- **Safety First**: Built-in content filtering and evaluation
- **Educational Focus**: Simulated responses for learning purposes
```
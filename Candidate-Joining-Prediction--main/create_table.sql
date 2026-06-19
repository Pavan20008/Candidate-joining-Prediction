CREATE TABLE interviews (
    interview_id SERIAL PRIMARY KEY,
    candidate_id INTEGER,
    interview_date DATE,
    interview_score FLOAT,
    technical_score FLOAT,
    behavioral_score FLOAT,
    education_level VARCHAR(50),
    years_of_experience INTEGER,
    skills JSONB,
    enthusiasm_level VARCHAR(20),
    response_to_offer VARCHAR(20),
    salary_offered INTEGER,
    benefits JSONB,
    job_title VARCHAR(100),
    number_of_rounds INTEGER,
    interview_type VARCHAR(50),
    questions_answers JSONB,
    interviewer_feedback TEXT,
    job_market_conditions VARCHAR(20),
    candidate_options INTEGER,
    joined BOOLEAN,
    employee_info TEXT,              -- General employee details
    notice_period INTEGER,           -- Notice period in days
    no_of_companies_changed INTEGER, -- Number of previous job changes
    search_engine_activity TEXT,     -- Simulated search engine data
    linkedin_open_network BOOLEAN,   -- Whether LinkedIn is in open network
    applied_to_other_companies BOOLEAN, -- Whether applied elsewhere
    joining_date DATE,               -- Proposed joining date
    notice_period_manageable BOOLEAN -- Whether notice period is manageable
);
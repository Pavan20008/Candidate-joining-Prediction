Candidate Joining Prediction
This project predicts the probability that a candidate will join a company after an interview, using structured and NLP features from interview data.

Project Overview
Goal: Predict whether a candidate will join after an interview based on interview data.
Tech Stack: Python, PostgreSQL, scikit-learn, pandas, VADER Sentiment, TF-IDF
Features:
Structured data (scores, experience, etc.)
Candidate and offer info (notice period, job changes, LinkedIn, etc.)
NLP features (sentiment, TF-IDF from answers)
Project Structure
generate_data.py: Generate synthetic candidate data (now includes new offer/candidate info).
candidate_interview_data.json: Generated data file.
create_table.sql: SQL to create the interviews table (with new columns).
insert_data.py: Insert data into PostgreSQL.
prepare_data.py: Prepare and encode data for modeling (with new features).
nlp_features.py: Add NLP features and save enhanced datasets (with new features).
train_model.py: Train and save ML models.
tune_model.py: Hyperparameter tuning for Random Forest.
evaluate_model.py: Evaluate model and save metrics/plots.
test_model.py: Test model with hardcoded sample (with new features).
predict.py: Interactive prediction for new candidates (with new features).
verify_data.py: Verify data in the database.
X_train.csv, X_test.csv, y_train.csv, y_test.csv: Processed datasets.
random_forest_model.pkl, tuned_random_forest_model.pkl: Saved models.
feature_names.txt: List of features used in modeling.
confusion_matrix.png, roc_curve.png: Evaluation plots.
Setup Instructions
Clone the repository and navigate to the project folder.
Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Linux/Mac
Install dependencies:
pip install -r requirements.txt
If requirements.txt is missing, install manually:
pip install pandas numpy scikit-learn psycopg2-binary vaderSentiment faker matplotlib seaborn joblib
Set up PostgreSQL:
Install PostgreSQL and create a database named interview_db.
Update database credentials in scripts if needed.
Run create_table.sql to create the table.
Usage
Generate Data:
python generate_data.py
Insert Data into Database:
python insert_data.py
Prepare Data:
python prepare_data.py
# or for NLP features
python nlp_features.py
Train Model:
python train_model.py
# or for hyperparameter tuning
python tune_model.py
Evaluate Model:
python evaluate_model.py
Predict for New Candidates:
python predict.py
Feature Encoding Reference
education_level_encoded: 0 = Bachelor's, 1 = Master's, 2 = PhD
enthusiasm_level_encoded: 0 = High, 1 = Medium, 2 = Low
response_to_offer_encoded: 0 = Negative, 1 = Neutral, 2 = Positive
job_market_conditions_encoded: 0 = Competitive, 1 = Stable
job_title_encoded, interview_type_encoded: See label encoding in data
notice_period_encoded: 1 = short (≤30 days), 0 = long (>30 days)
linkedin_open_network, applied_to_other_companies, notice_period_manageable: 1 = Yes/True, 0 = No/False
Requirements
Python 3.7+
PostgreSQL
See dependencies above
Authors
Kuruva Pavan sai krishna

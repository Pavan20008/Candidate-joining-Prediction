import psycopg2
import os
import json
import decimal
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report, roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# --- DATABASE CONNECTION DETAILS ---
DB_NAME = "interview_db"
DB_USER = "postgres"
DB_PASSWORD = "UAEy@@$$11"
DB_HOST = "localhost"
DB_PORT = "5432"

CREATE_TABLE_SQL = open("create_table.sql").read()

# 1. Check if table exists and has data
def table_has_data():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'interviews');")
        exists = cur.fetchone()[0]
        if not exists:
            cur.close()
            conn.close()
            return False
        cur.execute("SELECT COUNT(*) FROM interviews;")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count > 0
    except Exception as e:
        print(f"Error checking table: {e}")
        return False

# 2. Create table
def create_table():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()
        cur.execute(CREATE_TABLE_SQL)
        conn.commit()
        cur.close()
        conn.close()
        print("Table 'interviews' created or already exists.")
    except Exception as e:
        print(f"Error creating table: {e}")

# 3. Generate data
def generate_data():
    fake = Faker()
    records = []
    for i in range(1, 101):
        interview_score = round(np.random.normal(7, 2), 2)
        technical_score = round(np.random.normal(7, 2), 2)
        behavioral_score = round(np.random.normal(7, 2), 2)
        years_of_experience = max(0, int(np.random.normal(7, 5)))
        salary_offered = int(np.random.lognormal(mean=11, sigma=0.5))
        candidate_options = random.randint(0, 10)
        notice_period = random.randint(0, 365)
        no_of_companies_changed = random.randint(0, 20)
        noise = np.random.normal(0, 0.5)
        z = (
            0.5 * interview_score +
            0.4 * technical_score +
            0.3 * behavioral_score +
            0.000015 * salary_offered +
            0.12 * years_of_experience -
            0.18 * candidate_options -
            0.012 * notice_period -
            0.06 * no_of_companies_changed +
            noise - 6.5
        )
        join_prob = 1 / (1 + np.exp(-z))
        joined = random.random() < join_prob
        record = {
            "interview_id": i,
            "candidate_id": 100 + i,
            "interview_date": fake.date_between(start_date="-5y", end_date="today").strftime("%Y-%m-%d"),
            "interview_score": interview_score,
            "technical_score": technical_score,
            "behavioral_score": behavioral_score,
            "education_level": fake.job(),
            "years_of_experience": years_of_experience,
            "skills": [fake.word() for _ in range(random.randint(0, 15))],
            "enthusiasm_level": fake.word(),
            "response_to_offer": fake.word(),
            "salary_offered": salary_offered,
            "benefits": [fake.word() for _ in range(random.randint(0, 10))],
            "job_title": fake.job(),
            "number_of_rounds": random.randint(1, 10),
            "interview_type": fake.word(),
            "questions_answers": [
                {"question": fake.sentence(), "answer": fake.sentence()}
                for _ in range(random.randint(1, 10))
            ],
            "interviewer_feedback": fake.sentence(),
            "job_market_conditions": fake.word(),
            "candidate_options": candidate_options,
            "joined": joined,
            "employee_info": fake.profile(),
            "notice_period": notice_period,
            "no_of_companies_changed": no_of_companies_changed,
            "search_engine_activity": fake.sentence(),
            "linkedin_open_network": random.choice([True, False]),
            "applied_to_other_companies": random.choice([True, False]),
            "joining_date": (datetime.now() + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
            "notice_period_manageable": random.choice([True, False])
        }
        records.append(record)
    def default_serializer(obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        return str(obj)
    with open("candidate_interview_data.json", "w") as f:
        json.dump(records, f, indent=2, default=default_serializer)
    print("Successfully generated and saved 100 records to candidate_interview_data.json")

# 4. Insert data
def insert_data():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()
        with open("candidate_interview_data.json", "r") as f:
            data = json.load(f)
        for record in data:
            cur.execute(
                """
                INSERT INTO interviews (
                    candidate_id, interview_date, interview_score, technical_score, behavioral_score,
                    education_level, years_of_experience, skills, enthusiasm_level, response_to_offer,
                    salary_offered, benefits, job_title, number_of_rounds, interview_type,
                    questions_answers, interviewer_feedback, job_market_conditions, candidate_options, joined,
                    employee_info, notice_period, no_of_companies_changed, search_engine_activity,
                    linkedin_open_network, applied_to_other_companies, joining_date, notice_period_manageable
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                          %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    record["candidate_id"], record["interview_date"], float(record["interview_score"]),
                    float(record["technical_score"]), float(record["behavioral_score"]), record["education_level"],
                    record["years_of_experience"], json.dumps(record["skills"]), record["enthusiasm_level"],
                    record["response_to_offer"], float(record["salary_offered"]), json.dumps(record["benefits"]),
                    record["job_title"], record["number_of_rounds"], record["interview_type"],
                    json.dumps(record["questions_answers"]), record["interviewer_feedback"],
                    record["job_market_conditions"], record["candidate_options"], record["joined"],
                    json.dumps(record["employee_info"]) if isinstance(record["employee_info"], dict) else record["employee_info"],
                    record["notice_period"], record["no_of_companies_changed"],
                    record["search_engine_activity"], record["linkedin_open_network"],
                    record["applied_to_other_companies"], record["joining_date"], record["notice_period_manageable"]
                )
            )
        conn.commit()
        cur.close()
        conn.close()
        print(f"{len(data)} records inserted successfully into 'interviews' table.")
    except Exception as e:
        print(f"Error inserting data: {e}")

# 5. Prepare data
def prepare_data():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("SELECT * FROM interviews")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows, columns=columns)
        cur.close()
        conn.close()
        # Convert JSONB fields to Python objects
        for col in ['skills', 'benefits', 'questions_answers']:
            df[col] = df[col].apply(
                lambda x: json.loads(x) if isinstance(x, str) and x else (x if isinstance(x, list) else [])
            )
        df['interviewer_feedback'].fillna('No feedback provided', inplace=True)
        le_education = LabelEncoder()
        df['education_level_encoded'] = le_education.fit_transform(df['education_level'])
        le_enthusiasm = LabelEncoder()
        df['enthusiasm_level_encoded'] = le_enthusiasm.fit_transform(df['enthusiasm_level'])
        le_response = LabelEncoder()
        df['response_to_offer_encoded'] = le_response.fit_transform(df['response_to_offer'])
        le_market = LabelEncoder()
        df['job_market_conditions_encoded'] = le_market.fit_transform(df['job_market_conditions'])
        le_job_title = LabelEncoder()
        df['job_title_encoded'] = le_job_title.fit_transform(df['job_title'])
        le_interview_type = LabelEncoder()
        df['interview_type_encoded'] = le_interview_type.fit_transform(df['interview_type'])
        df['num_skills'] = df['skills'].apply(len)
        df['num_benefits'] = df['benefits'].apply(len)
        df['total_answer_length'] = df['questions_answers'].apply(
            lambda x: sum(len(item['answer']) for item in x if isinstance(x, list))
        )
        df['notice_period_encoded'] = df['notice_period'].apply(lambda x: 1 if x <= 30 else 0)
        df['joining_date_diff'] = (pd.to_datetime(df['joining_date']) - pd.to_datetime(df['interview_date'])).dt.days
        features = [
            'interview_score', 'technical_score', 'behavioral_score', 'years_of_experience',
            'salary_offered', 'number_of_rounds', 'candidate_options', 'num_skills',
            'num_benefits', 'total_answer_length', 'education_level_encoded',
            'enthusiasm_level_encoded', 'response_to_offer_encoded',
            'job_market_conditions_encoded', 'job_title_encoded', 'interview_type_encoded',
            'notice_period_encoded', 'joining_date_diff', 'no_of_companies_changed',
            'linkedin_open_network', 'applied_to_other_companies', 'notice_period_manageable'
        ]
        X = df[features]
        y = df['joined'].astype(int)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        X_train.to_csv('X_train.csv', index=False)
        X_test.to_csv('X_test.csv', index=False)
        y_train.to_csv('y_train.csv', index=False)
        y_test.to_csv('y_test.csv', index=False)
        print("Processed data saved to CSV files")
    except Exception as e:
        print(f"Error preparing data: {e}")

# 6. Train and save model
def train_and_save_model():
    try:
        X_train = pd.read_csv('X_train.csv')
        X_test = pd.read_csv('X_test.csv')
        y_train = pd.read_csv('y_train.csv').values.ravel()
        y_test = pd.read_csv('y_test.csv').values.ravel()
        log_reg = LogisticRegression(random_state=42, max_iter=1000)
        rf_clf = RandomForestClassifier(random_state=42, n_estimators=100)
        log_reg.fit(X_train, y_train)
        print("Logistic Regression model trained")
        rf_clf.fit(X_train, y_train)
        print("Random Forest model trained")
        def evaluate_model(model, X_test, y_test, model_name):
            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test)[:, 1]
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            roc_auc = roc_auc_score(y_test, y_proba)
            print(f"\n{model_name} Evaluation:")
            print(f"Accuracy: {accuracy:.4f}")
            print(f"Precision: {precision:.4f}")
            print(f"Recall: {recall:.4f}")
            print(f"F1-Score: {f1:.4f}")
            print(f"ROC-AUC: {roc_auc:.4f}")
            return y_proba
        log_reg_proba = evaluate_model(log_reg, X_test, y_test, "Logistic Regression")
        rf_proba = evaluate_model(rf_clf, X_test, y_test, "Random Forest")
        log_reg_roc_auc = roc_auc_score(y_test, log_reg_proba)
        rf_roc_auc = roc_auc_score(y_test, rf_proba)
        if rf_roc_auc >= log_reg_roc_auc:
            best_model = rf_clf
            model_name = "random_forest_model.pkl"
            print("\nRandom Forest selected as best model")
        else:
            best_model = log_reg
            model_name = "logistic_regression_model.pkl"
            print("\nLogistic Regression selected as best model")
        joblib.dump(best_model, model_name)
        print(f"Best model saved as {model_name}")
        feature_names = X_train.columns.tolist()
        with open("feature_names.txt", "w") as f:
            f.write("\n".join(feature_names))
        print("Feature names saved to feature_names.txt")
    except Exception as e:
        print(f"Error training/saving model: {e}")

# 7. Evaluate model
def evaluate_model_performance():
    try:
        X_test = pd.read_csv('X_test.csv')
        y_test = pd.read_csv('y_test.csv').values.ravel()
        model = joblib.load('random_forest_model.pkl')
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Not Joined', 'Joined'], yticklabels=['Not Joined', 'Joined'])
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig('confusion_matrix.png')
        plt.close()
        print("Confusion matrix saved as confusion_matrix.png")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Not Joined', 'Joined']))
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        roc_auc = auc(fpr, tpr)
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f}')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc="lower right")
        plt.savefig('roc_curve.png')
        plt.close()
        print("ROC curve saved as roc_curve.png")
    except Exception as e:
        print(f"Error evaluating model: {e}")

# 8. Prompt user and predict
def prompt_and_predict():
    try:
        # Try both model files
        model = None
        if os.path.exists('random_forest_model.pkl'):
            model = joblib.load('random_forest_model.pkl')
        elif os.path.exists('logistic_regression_model.pkl'):
            model = joblib.load('logistic_regression_model.pkl')
        else:
            print("No trained model found.")
            return
        with open('feature_names.txt', 'r') as f:
            feature_names = f.read().splitlines()
        print("\nEnter candidate details (press Enter for default values):")
        data = {}
        for feature in feature_names:
            value = input(f"{feature} (e.g., 8.0 for scores, 4 for years, 1/0 for yes/no): ") or None
            data[feature] = float(value) if value else 0.0
        new_data = pd.DataFrame([data], columns=feature_names)
        proba = model.predict_proba(new_data)[:, 1]
        print(f"\nProbability of joining: {proba[0]*100:.2f}%")
        print("\nPrediction complete.")
    except Exception as e:
        print(f"Error predicting: {e}")

# --- Main pipeline logic ---
def main():
    if not table_has_data():
        print("No data found in 'interviews' table. Running full pipeline...")
        create_table()
        generate_data()
        insert_data()
        prepare_data()
        train_and_save_model()
        evaluate_model_performance()
        prompt_and_predict()
    else:
        print("Data found in 'interviews' table. Skipping to prediction...")
        prompt_and_predict()

if __name__ == "__main__":
    main() 
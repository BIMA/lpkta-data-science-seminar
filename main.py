import pickle

import functions_framework
from google.cloud import bigquery, storage
import json

bq = bigquery.Client("my-local-sandbox-355006")
gcs = storage.Client("my-local-sandbox-355006")

pkl_file = gcs.bucket("lpkta-data-science").blob("seminar-data-science/dataset/cm_model_v1.pkl").download_as_bytes()
model = pickle.loads(pkl_file)


@functions_framework.http
def main(request):
    data = request.json
    user_id = int(data.get("user_id"))

    # PROHIBITTED!!!!
    features = bq.query(
        f"SELECT * FROM `my-local-sandbox-355006.lpkta.credit_scoring_features` WHERE id = {user_id}").result().to_dataframe()
    # RECOMMENDED WAY
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "INTEGER", user_id)
        ]
    )
    features = bq.query("SELECT * FROM `my-local-sandbox-355006.lpkta.credit_scoring_features` WHERE id = @user_id",
                        job_config=job_config).result().to_dataframe()

    features = features[['annual_income',
                         'monthly_inhand_salary',
                         'num_bank_accounts',
                         'num_credit_card',
                         'interest_rate',
                         'num_of_loan',
                         'delay_from_due_date',
                         'num_of_delayed_payment',
                         'credit_mix',
                         'outstanding_debt',
                         'credit_history_age',
                         'monthly_balance']]

    prediction = model.predict(features)

    return json.dumps({"message": "success", "user_id": user_id, "prediction": str(prediction)})


if __name__ == "__main__":
    main()

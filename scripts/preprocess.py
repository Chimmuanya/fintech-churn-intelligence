"""
preprocess.py
Simple preprocessing pipeline to:
- read raw user-level dataset (e.g., telco_churn.csv)
- read synthetic events
- compute per-user aggregates (e.g., events_count, days_active, time_to_first_event)
- merge into a single processed file for modeling: data/processed/users_features.csv
"""

import pandas as pd
import numpy as np

def compute_user_aggregates(events_df):
    """
    Compute simple per-user aggregates useful for churn modeling:
    - events_count: total events in period
    - days_active: distinct days with events
    - time_to_first_action_days: days between signup and first event (if available)
    """
    # ensure timestamp is datetime
    events_df['timestamp'] = pd.to_datetime(events_df['timestamp'])
    # events per user
    events_count = events_df.groupby('user_id').agg(events_count=('event_type','count')).reset_index()
    # distinct active days per user
    events_df['active_day'] = events_df['timestamp'].dt.date
    days_active = events_df.groupby('user_id').agg(days_active=('active_day', 'nunique')).reset_index()
    # first event timestamp per user
    first_event = events_df.groupby('user_id').agg(first_event_ts=('timestamp', 'min')).reset_index()
    # join
    agg = events_count.merge(days_active, on='user_id', how='left').merge(first_event, on='user_id', how='left')
    return agg

def main():
    # load raw users if present
    try:
        users = pd.read_csv("data/raw/telco_churn.csv", parse_dates=['start_date', 'churn_date'])
    except FileNotFoundError:
        # fall back to creating a minimal users table from synthetic events
        users = None

    # load synthetic events (required)
    events = pd.read_csv("data/synthetic/events.csv", parse_dates=['timestamp', 'signup_date'])
    # compute aggregates
    agg = compute_user_aggregates(events)
    # if users table exists, merge features into it
    if users is not None:
        # ensure user_id is same type
        if 'user_id' not in users.columns:
            # maybe our users table uses 'customerID' or similar; leave this as a manual mapping step
            raise ValueError("Expected 'user_id' column in raw users file.")
        users_features = users.merge(agg, on='user_id', how='left')
    else:
        # create a minimal processed file with user_id + features
        users_features = agg.copy()

    # fillna for numeric features with zeros (conservative)
    numeric_cols = users_features.select_dtypes(include=[np.number]).columns
    users_features[numeric_cols] = users_features[numeric_cols].fillna(0)

    # persist processed dataset
    users_features.to_csv("data/processed/users_features.csv", index=False)
    print("Processed user features written to data/processed/users_features.csv")

if __name__ == "__main__":
    main()

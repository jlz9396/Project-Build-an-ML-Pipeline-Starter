#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()

# DO NOT MODIFY
def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    
    run = wandb.init(project="nyc_airbnb", group="cleaning", save_code=True)
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)
    # Drop outliers
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    # Drop rows in the dataset that are not in the proper geolocation
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()
    # Save the cleaned file
    df.to_csv('clean_sample.csv',index=False)

    # log the new data.
    artifact = wandb.Artifact(
     args.output_artifact,
     type=args.output_type,
     description=args.output_description,
 )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")
  
    parser.add_argument(
        "--input_artifact", 
        type =str,
        help = "Filename of the input artifact",
        required = True
    )

    parser.add_argument(
        "--output_artifact", 
        type =str,
        help = "Filename of the output artifact",
        required = True
    )

    parser.add_argument(
        "--output_type", 
        type =str,
        help = "Type of output artifact",
        required = True
    )

    parser.add_argument(
        "--output_description", 
        type =str,
        help = "Description of the output artifact",
        required = True
    )

    parser.add_argument(
        "--min_price", 
        type =float,
        help = "Minimum price in USD allowed in the dataset",
        required = True
    )

    parser.add_argument(
        "--max_price",
        type =float,
        help = "Maximum price in USD allowed in the dataset",
        required = True
    )


    args = parser.parse_args()

    go(args)
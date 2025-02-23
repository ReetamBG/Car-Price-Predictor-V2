# Car Price Predictor V2
### End to End Machine Learning Project implementing MLOPS

### Setup DVC with Supabase S3
dvc remote add -d {storage_name} s3://{bucket name}/{folder name (if any)} -f                      # create remote storage (Storage name set by us. Can be anything)
dvc remote modify {storage_name} endpointurl {endpoint url}                 # add endpoint url
dvc remote modify {storage_name} access_key_id {access key id}              # add access key id
dvc remote modify {storage_name} secret_access_key {secret access key}      # add secret access key

All done just dvc add dvc push now 

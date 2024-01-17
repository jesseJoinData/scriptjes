import os
import json

def check_conditions(file_path, target_value, target_dataset_id):
    with open(file_path, 'r') as file:
        data = json.load(file)
        for item in data.get('data', []):
            for dataset in item.get('datasets', []):
                if dataset.get('datasetId') != target_dataset_id:
                    for client in dataset.get('clients', []):
                        if client.get('companyValue') == target_value:
                            return True
    return False

def main():
    folder_path = 'json_files'
    match_file = 'matching_files.txt'
    non_match_file = 'non_matching_files.txt'

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            if check_conditions(file_path, "12035790", "2eaa4c1f-e755-4217-b2db-7696e332a48e"):
                with open(match_file, 'a') as f:
                    f.write(file_name[:-5][-8:] + '\n')  # Exclude '.json' and get last 8 characters
            else:
                with open(non_match_file, 'a') as f:
                    f.write(file_name[:-5][-8:] + '\n')  # Exclude '.json' and get last 8 characters

if __name__ == "__main__":
    main()

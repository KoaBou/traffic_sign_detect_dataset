def analyze_unknown_format(file_path):
    data_summary = {
        'line_count': 0,
        'structure_summary': {},
        'data_types': {}
    }

    with open(file_path, 'r') as file:
        for line in file:
            data_summary['line_count'] += 1
            # Perform analysis for each line and update data_summary

    return data_summary


file_path = 'dataset_13k_folder/dataset_13k/annotations/val.json'
summary = analyze_unknown_format(file_path)
print(summary)

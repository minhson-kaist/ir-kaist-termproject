import jsonlines
import config

dict_golden_label = []

with jsonlines.open(config.train_folder, 'r') as jsl_file:
    # load json object
    for obj in jsl_file:
        dict_obj = {'id': obj['example_id'], 
                    'query': obj['question_text'], 
                    'query_tokens': obj['question_tokens']}
        
        for a_id in obj['annotations']:
            long_answer_token = []
            if a_id['long_answer']['start_token'] != -1:
                # get gold label paragraph and merge tokens
                long_answer_start_token = a_id['long_answer']['start_token']
                long_answer_end_token = a_id['long_answer']['end_token']
                long_answer_tokens = obj['document_tokens'][long_answer_start_token:long_answer_end_token]
                
                for token in long_answer_tokens:
                    if token['html_token']:
                        continue
                    else:
                        long_answer_token.append(token['token'])
            dict_obj['long_answer'] = ' '.join(long_answer_token)
                
        dict_obj['long_answer_candidates'] = list()
        
        # get paragraph candidates
        for i in range(len(obj['long_answer_candidates'])):
            start_token = obj['long_answer_candidates'][i]['start_token']
            end_token = obj['long_answer_candidates'][i]['end_token']
            
            paragraph = obj['document_tokens'][start_token:end_token]
            paragraph_token = []
            for token in paragraph:
                if token['html_token']:
                    continue
                else:
                    paragraph_token.append(token['token'])
            dict_obj['long_answer_candidates'].append(' '.join(paragraph_token))
        
        dict_golden_label.append(dict_obj)
        #break
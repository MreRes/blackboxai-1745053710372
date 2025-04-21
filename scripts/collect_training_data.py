import json
import os

def collect_conversation_logs(log_dir='logs', output_file='training_data.jsonl'):
    """
    Collect conversation logs from log files and format them for AI fine-tuning.
    Assumes logs are JSON lines with 'user_message' and 'bot_response' fields.
    """
    training_data = []
    for filename in os.listdir(log_dir):
        if filename.endswith('.log') or filename.endswith('.jsonl'):
            filepath = os.path.join(log_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line.strip())
                        user_msg = record.get('user_message')
                        bot_resp = record.get('bot_response')
                        if user_msg and bot_resp:
                            training_data.append({
                                "prompt": user_msg,
                                "completion": bot_resp
                            })
                    except json.JSONDecodeError:
                        continue

    with open(output_file, 'w', encoding='utf-8') as out_f:
        for item in training_data:
            out_f.write(json.dumps(item, ensure_ascii=False) + '\n')

    print(f"Collected {len(training_data)} training samples into {output_file}")

if __name__ == '__main__':
    collect_conversation_logs()

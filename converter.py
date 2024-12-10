import csv

def convert_raw_text_to_csv(raw_text, output_csv):
    lines = raw_text.strip().split('\n')
    questions = []
    current_question = None

    i = 0
    while i < len(lines):
        if lines[i].strip().isdigit():
            if current_question:
                questions.append(current_question)
            current_question = {'question': '', 'options': [], 'answer': '', 'image': 'NULL'}
            if i + 2 < len(lines):
                current_question['question'] = lines[i + 2].strip()
            if i + 4 < len(lines) and i + 7 < len(lines):
                current_question['options'] = [
                    lines[i + 4].strip(),
                    lines[i + 5].strip(),
                    lines[i + 6].strip(),
                    lines[i + 7].strip()
                ]
            i += 9  # Move to the next question block
        else:
            i += 1

    if current_question:
        questions.append(current_question)

    # Debugging: Print the extracted questions and options
    for q in questions:
        print(f"Question: {q['question']}")
        print(f"Options: {q['options']}")

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['question', 'option1', 'option2', 'option3', 'option4', 'answer', 'image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for q in questions:
            writer.writerow({
                'question': q['question'],
                'option1': q['options'][0] if len(q['options']) > 0 else '',
                'option2': q['options'][1] if len(q['options']) > 1 else '',
                'option3': q['options'][2] if len(q['options']) > 2 else '',
                'option4': q['options'][3] if len(q['options']) > 3 else '',
                'answer': q['answer'],
                'image': q['image']
            })

raw_text = """
1
Below is your most recent answer to this question.
กรณีใดบ้างที่ควรใช้ supervised learning แทน time series modeling

โมเดลปริมาณน้ำฝน PM2.5 และอุณหภูมิในแต่ละวันของกรุงเทพ
มีข้อมูลน้อย เช่น มีรอบ seasonal เพียงหนึ่งรอบ
ต้องการศึกษา seasonal effect ในข้อมูล
ควรใช้ time series modeling กับข้อมูลที่มีความสัมพันธ์ระหว่างเวลาเสมอ

2
Below is your most recent answer to this question.
ข้อใดไม่ถูกต้องเกี่ยวกับการโมเดล time series

ควรมีการ transform ข้อมูลเพื่อทำให้โมเดล stationary มากขึ้นก่อนนำมาเทรนกับโมเดล
ถ้า time series เป็น multiplicative time series สามารถทำ log transform เพื่อใช้กับ additive model ได้
การทำsmoothingก่อนเทรนโมเดลสามารถช่วยให้โมเดลรับมือกับ outlier ได้ดีขึ้น
ควรใช้โมเดลที่ซับซ้อนที่สุดเพื่อจะได้รับมือกับข้อมูลทุกรูปแบบ

3	
Below is your most recent answer to this question.
ข้อใดไม่ถูกต้องเกี่ยวกับการประยุกต์ใช้ time series modeling

สามารถนำ time series มา decompose เพื่อแสดง trend ของข้อมูลในการประกอบการตัดสินใจได้
สามารถนำ Confidence interval ของการทำนายใช้บอกจุดสูงสุดและต่ำสุดของความเป็นไปได้ของข้อมูลได้
เป็นการประยุกต์ใช้ที่ถูกต้องทุกข้อ
สามารถนำมาทำโมเดลเพื่อแจ้งเตือนในช่วงเวลาที่ผิดปกติ
"""

convert_raw_text_to_csv(raw_text, 'questions_converted.csv')
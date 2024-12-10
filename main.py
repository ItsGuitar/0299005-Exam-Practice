import csv
import random
import pygame
import sys
import os
import time

def load_questions(filename):
    questions = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            questions.append(row)
    random.shuffle(questions)
    return questions

questions = load_questions('questions.csv')

pygame.init()

screen = pygame.display.set_mode((1200, 600), pygame.RESIZABLE)
pygame.display.set_caption('0299005 Exam')

font = pygame.font.Font('NotoSansThai-Regular.ttf', 16)
big_font = pygame.font.Font('NotoSansThai-Regular.ttf', 72)

def display_question(question, selected_option=None, correct_option=None):
    screen.fill((255, 255, 255))
    y_offset = 50
    question_text = font.render(question['question'], True, (0, 0, 0))
    screen.blit(question_text, (50, y_offset))
    y_offset += 50

    if question['image'] and question['image'] != "NULL":
        image_path = os.path.join('res', question['image'])
        image = pygame.image.load(image_path)
        max_height = int(screen.get_height() * 0.3)
        if image.get_height() > max_height:
            scale_factor = max_height / image.get_height()
            new_size = (int(image.get_width() * scale_factor), max_height)
            image = pygame.transform.scale(image, new_size)
        screen.blit(image, (50, y_offset))
        y_offset += image.get_height() + 20

    for i, option in enumerate(['option1', 'option2', 'option3', 'option4']):
        color = (0, 0, 0)
        if selected_option is not None:
            if i + 1 == selected_option:
                color = (0, 255, 0) if selected_option == correct_option else (255, 0, 0)
            elif i + 1 == correct_option:
                color = (0, 255, 0)
        option_text = font.render(f"{i+1}. {question[option]}", True, color)
        screen.blit(option_text, (50, y_offset))
        y_offset += 50
    pygame.display.flip()

def display_feedback(is_correct):
    message = "เก่งจังว" if is_correct else "SKILL ISSUE"
    color = (0, 255, 0) if is_correct else (255, 0, 0)
    feedback_text = big_font.render(message, True, color)
    feedback_rect = feedback_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    start_time = time.time()
    while time.time() - start_time < 0.7:
        screen.blit(feedback_text, feedback_rect)
        pygame.display.flip()
        pygame.time.delay(10)
        alpha = int(255 * (1 - (time.time() - start_time) / 0.7))
        feedback_text.set_alpha(alpha)

current_question = 0
display_question(questions[current_question])

waiting_for_feedback = False

key_to_option = {
    pygame.K_1: 1,
    pygame.K_2: 2,
    pygame.K_3: 3,
    pygame.K_4: 4,
    pygame.K_KP1: 1,
    pygame.K_KP2: 2,
    pygame.K_KP3: 3,
    pygame.K_KP4: 4
}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            display_question(questions[current_question])
        elif event.type == pygame.KEYDOWN:
            if waiting_for_feedback:
                current_question += 1
                if current_question < len(questions):
                    display_question(questions[current_question])
                    waiting_for_feedback = False
                else:
                    print("จบละ")
                    pygame.quit()
                    sys.exit()
            else:
                if event.key in key_to_option:
                    selected_option = key_to_option[event.key]
                    correct_option = int(questions[current_question]['answer'])
                    correct_option_text = questions[current_question][f'option{correct_option}']
                    is_correct = selected_option == correct_option
                    display_question(questions[current_question], selected_option, correct_option)
                    display_feedback(is_correct)
                    waiting_for_feedback = True
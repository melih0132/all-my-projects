import json
import random
import os
from datetime import datetime
import time

class QuizGame:
    def __init__(self):
        self.questions = []
        self.high_scores = []
        self.load_questions()
        self.load_scores()
        
    def load_questions(self):
        """Load questions from JSON file."""
        try:
            with open('quiz_data.json', 'r') as file:
                data = json.load(file)
                self.questions = data['questions']
        except FileNotFoundError:
            print("Error: Questions file not found!")
            exit(1)
            
    def load_scores(self):
        """Load high scores from file."""
        try:
            with open('high_scores.json', 'r') as file:
                self.high_scores = json.load(file)
        except FileNotFoundError:
            self.high_scores = []
            
    def save_score(self, player_name, score, time_taken):
        """Save player's score to high scores."""
        score_entry = {
            'player': player_name,
            'score': score,
            'time': time_taken,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.high_scores.append(score_entry)
        self.high_scores.sort(key=lambda x: (-x['score'], x['time']))
        self.high_scores = self.high_scores[:10]  # Keep only top 10
        
        with open('high_scores.json', 'w') as file:
            json.dump(self.high_scores, file, indent=4)
            
    def display_question(self, question, number):
        """Display a question and its options."""
        print(f"\nQuestion {number}:")
        print(question['question'])
        print("\nOptions:")
        for i, option in enumerate(question['options'], 1):
            print(f"{i}. {option}")
            
    def get_player_answer(self):
        """Get and validate player's answer."""
        while True:
            try:
                answer = int(input("\nEnter your answer (1-4): "))
                if 1 <= answer <= 4:
                    return answer - 1
                print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Please enter a valid number.")
                
    def display_high_scores(self):
        """Display the high scores table."""
        print("\n=== HIGH SCORES ===")
        print("Rank  Player  Score  Time(s)  Date")
        print("-" * 50)
        
        for i, score in enumerate(self.high_scores, 1):
            print(f"{i:4d}  {score['player']:6s}  {score['score']:5d}  {score['time']:7.1f}  {score['date']}")
            
    def show_statistics(self):
        """Display game statistics."""
        if not self.high_scores:
            print("\nNo games played yet!")
            return
            
        scores = [score['score'] for score in self.high_scores]
        times = [score['time'] for score in self.high_scores]
        
        print("\n=== STATISTICS ===")
        print(f"Average Score: {sum(scores)/len(scores):.1f}")
        print(f"Average Time: {sum(times)/len(times):.1f} seconds")
        print(f"Highest Score: {max(scores)}")
        print(f"Fastest Time: {min(times):.1f} seconds")
        
    def play_game(self):
        """Main game loop."""
        print("=== PROGRAMMING QUIZ GAME ===")
        player_name = input("Enter your name: ")
        
        # Shuffle questions
        game_questions = random.sample(self.questions, min(5, len(self.questions)))
        score = 0
        start_time = time.time()
        
        for i, question in enumerate(game_questions, 1):
            self.display_question(question, i)
            answer = self.get_player_answer()
            
            if answer == question['correct']:
                print("Correct!")
                score += 1
            else:
                correct_option = question['options'][question['correct']]
                print(f"Wrong! The correct answer was: {correct_option}")
                
        end_time = time.time()
        time_taken = end_time - start_time
        
        print(f"\nGame Over! {player_name}")
        print(f"Score: {score}/{len(game_questions)}")
        print(f"Time taken: {time_taken:.1f} seconds")
        
        self.save_score(player_name, score, time_taken)
        
    def main_menu(self):
        """Display and handle main menu."""
        while True:
            print("\n=== MAIN MENU ===")
            print("1. Play Game")
            print("2. View High Scores")
            print("3. View Statistics")
            print("4. Exit")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == '1':
                self.play_game()
            elif choice == '2':
                self.display_high_scores()
            elif choice == '3':
                self.show_statistics()
            elif choice == '4':
                print("Thanks for playing!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    game = QuizGame()
    game.main_menu()
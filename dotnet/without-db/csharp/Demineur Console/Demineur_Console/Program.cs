namespace Demineur_Console
{
    internal class Program
    {
        // The size of the board
        const int rows = 10;
        const int cols = 10;

        // The number of mines on the board
        const int mines = 10;

        // The board, represented by a two-dimensional array of cells
        static Cell[,] board = new Cell[rows, cols];

        // A random number generator
        static Random random = new Random();

        // The game state, indicating whether the game is over or not
        static bool gameOver = false;

        // The number of cells that are revealed
        static int revealed = 0;

        static void Main(string[] args)
        {
            // Initialize the board
            InitializeBoard();

            // Place the mines randomly on the board
            PlaceMines();

            // Calculate the numbers for each cell
            CalculateNumbers();

            // Print the board
            PrintBoard();

            // Start the game loop
            while (!gameOver)
            {
                // Get the user input
                Console.WriteLine("Enter the row and column of the cell you want to reveal (separated by a space):");
                string input = Console.ReadLine();
                string[] parts = input.Split(' ');
                int row = int.Parse(parts[0]);
                int col = int.Parse(parts[1]);

                // Check if the input is valid
                if (row < 0 || row >= rows || col < 0 || col >= cols)
                {
                    Console.WriteLine("Invalid input. Please try again.");
                    continue;
                }

                // Reveal the cell
                RevealCell(row, col);

                // Print the board
                PrintBoard();

                // Check if the user won or lost
                CheckGameState();
            }

            // End the game
            Console.WriteLine("Game over.");
            Console.ReadLine();
        }

        // A method to initialize the board with empty cells
        static void InitializeBoard()
        {
            for (int i = 0; i < rows; i++)
            {
                for (int j = 0; j < cols; j++)
                {
                    board[i, j] = new Cell();
                }
            }
        }

        // A method to place the mines randomly on the board
        static void PlaceMines()
        {
            int count = 0;
            while (count < mines)
            {
                int i = random.Next(rows);
                int j = random.Next(cols);
                if (!board[i, j].IsMine)
                {
                    board[i, j].IsMine = true;
                    count++;
                }
            }
        }

        // A method to calculate the numbers for each cell
        static void CalculateNumbers()
        {
            for (int i = 0; i < rows; i++)
            {
                for (int j = 0; j < cols; j++)
                {
                    if (!board[i, j].IsMine)
                    {
                        board[i, j].Number = CountMines(i, j);
                    }
                }
            }
        }

        // A method to count the number of mines around a given cell
        static int CountMines(int i, int j)
        {
            int count = 0;
            for (int x = i - 1; x <= i + 1; x++)
            {
                for (int y = j - 1; y <= j + 1; y++)
                {
                    if (x >= 0 && x < rows && y >= 0 && y < cols && board[x, y].IsMine)
                    {
                        count++;
                    }
                }
            }
            return count;
        }

        // A method to print the board
        static void PrintBoard()
        {
            Console.WriteLine("  0 1 2 3 4 5 6 7 8 9");
            Console.WriteLine("  -------------------");
            for (int i = 0; i < rows; i++)
            {
                Console.Write(i + "|");
                for (int j = 0; j < cols; j++)
                {
                    Console.Write(board[i, j] + " ");
                }
                Console.WriteLine("|" + i);
            }
            Console.WriteLine("  -------------------");
            Console.WriteLine("  0 1 2 3 4 5 6 7 8 9");
        }

        // A method to reveal a cell
        static void RevealCell(int i, int j)
        {
            // If the cell is already revealed, do nothing
            if (board[i, j].IsRevealed)
            {
                return;
            }

            // Reveal the cell
            board[i, j].IsRevealed = true;
            revealed++;

            // If the cell is a mine, set the game over flag to true
            if (board[i, j].IsMine)
            {
                gameOver = true;
            }

            // If the cell is empty, reveal the adjacent cells recursively
            if (board[i, j].Number == 0)
            {
                for (int x = i - 1; x <= i + 1; x++)
                {
                    for (int y = j - 1; y <= j + 1; y++)
                    {
                        if (x >= 0 && x < rows && y >= 0 && y < cols)
                        {
                            RevealCell(x, y);
                        }
                    }
                }
            }
        }

        // A method to check the game state
        static void CheckGameState()
        {
            // If the game is over, reveal all the mines
            if (gameOver)
            {
                RevealMines();
            }

            // If the user revealed all the non-mine cells, set the game over flag to true and congratulate the user
            if (revealed == rows * cols - mines)
            {
                gameOver = true;
                Console.WriteLine("Congratulations! You have cleared the board!");
            }
        }

        // A method to reveal all the mines
        static void RevealMines()
        {
            for (int i = 0; i < rows; i++)
            {
                for (int j = 0; j < cols; j++)
                {
                    if (board[i, j].IsMine)
                    {
                        board[i, j].IsRevealed = true;
                    }
                }
            }
        }
    }

    // A class to represent a cell on the board
    class Cell
    {
        // A property to indicate whether the cell is a mine or not
        public bool IsMine { get; set; }

        // A property to indicate whether the cell is revealed or not
        public bool IsRevealed { get; set; }

        // A property to store the number of mines around the cell
        public int Number { get; set; }

        // A constructor to initialize the cell
        public Cell()
        {
            IsMine = false;
            IsRevealed = false;
            Number = 0;
        }

        // A method to override the string representation of the cell
        public override string ToString()
        {
            // If the cell is not revealed, return a dot
            if (!IsRevealed)
            {
                return ".";
            }

            // If the cell is a mine, return an asterisk
            if (IsMine)
            {
                return "*";
            }

            // If the cell is empty, return a space
            if (Number == 0)
            {
                return " ";
            }

            // Otherwise, return the number as a string
            return Number.ToString();
        }
    }
}
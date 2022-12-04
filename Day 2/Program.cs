string[] lines = System.IO.File.ReadAllLines(@".\input.txt");

// Index by difference of your score and opponent's score mod 3
// int[] scores = new int[3] {3, 6, 0};

// Order by score of result X, Y, Z
int[] scores = new int[3] {0, 3, 6};

int sum = 0;

foreach (string line in lines) {
    char c = line[0];
    char d = line[2];
    
//     int opp = c - 'A' + 1;
//     int you = d - 'X' + 1;
//     int ind = (you - opp) % 3;
//     if (ind < 0) ind += 3;
//     sum += you + scores[ind];

    int opp = c - 'A' + 1;
    int result = d - 'X' + 1;
    int you = opp + result + 1;
    if (you > 3) {
        you -= 3;
    }
    if (you > 3) {
        you -= 3;
    }
    sum += you + scores[result-1];
}

Console.WriteLine(sum);
using System.Linq;
string[] lines = System.IO.File.ReadAllLines(@".\input.txt");
// int[] elf1 = Array.ConvertAll(line[0].Split(','), s => Convert.ToInt32(s));

int maxY = lines.Length;
int maxX = lines[0].Length;

bool[,] visible = new bool[maxX,maxY];
int[,] grid = new int[maxX,maxY];
for (int i = 0; i < maxY; i++) {
    string line = lines[i];
    for (int j = 0; j < maxX; j++) {
        grid[j,i] = Convert.ToInt32(line[j] - '0');
    }
}

// Vertical
for (int i = 0; i < maxX; i++) {
    int tallestSeenFromAbove = -1;
    int tallestSeenFromBelow = -1;
    for (int j = 0; j < maxY; j++) {
        if (grid[i,j] > tallestSeenFromAbove) {
            visible[i,j] = true;
            tallestSeenFromAbove = grid[i,j];
        }
        if (grid[i,maxY - j - 1] > tallestSeenFromBelow) {
            visible[i,maxY - j - 1] = true;
            tallestSeenFromBelow = grid[i,maxY - j - 1];
        }
    }
}

/// Horizontal
for (int j = 0; j < maxY; j++) {
    int tallestSeenFromLeft = -1;
    int tallestSeenFromRight = -1;
    for (int i = 0; i < maxX; i++) {
        if (grid[i,j] > tallestSeenFromLeft) {
            visible[i,j] = true;
            tallestSeenFromLeft = grid[i,j];
        }
        if (grid[maxX - i - 1, j] > tallestSeenFromRight) {
            visible[maxX - i - 1,j] = true;
            tallestSeenFromRight = grid[maxX - i - 1,j];
        }
    }
}

// Console.WriteLine(visible.ToList().Where(vis => vis == true).Count());
int count = 0;
foreach(bool vis in visible) {
    if (vis) count++;
}

Console.WriteLine(count);

// Part 2
int scenicScore(int x, int y) {    
    int right = 0;
    for (int i = x; i < maxX; i++) {
        if (i == x) continue;
        right++;
        if (grid[i,y] >= grid[x,y]) break;
    }

    int left = 0;
    for (int i = x; i >= 0; i--) {
        if (i == x) continue;
        left++;
        if (grid[i,y] >= grid[x,y]) break;
    }

    int below = 0;
    for (int j = y; j < maxY; j++) {
        if (j == y) continue;
        below++;
        if (grid[x,j] >= grid[x,y]) break;
    }

    int above = 0;
    for (int j = y; j >= 0; j--) {
        if (j == y) continue;
        above++;
        if (grid[x,j] >= grid[x,y]) break;
    }

    return left * right * above * below;
}

int max = 0;
for (int y = 0; y < maxY; y++) {
    for (int x = 0; x < maxX; x++) {
        int s = scenicScore(x,y);
        if (s > max) {
            max = s;
        }
    }
}
Console.WriteLine(max);

string[] lines = System.IO.File.ReadAllLines(@".\input.txt");

int w = lines[0].Length;
int h = lines.Length;

int[,] grid = new int[w,h];

List<int> startingSteps = new List<int>();
int[] startPos = {0,0};
int[] endPos = {0,0};
for (int x = 0; x < w; x++) {
    for (int y = 0; y < h; y++) {
        if (lines[y][x] == 'S') {
            startPos = new int[] {x, y};
            grid[x,y] = 0;
        } else if (lines[y][x] == 'E') {
            endPos = new int[] {x, y};
            grid[x,y] = 25;
        } else {
            grid[x,y] = lines[y][x] - 'a';
        }
    }
}

int[,] steps = new int[w,h];
for(int i = 0; i < w; i++) {
    for (int j = 0; j < h; j++) {
        steps[i,j] = -1;
    }
}

List<int[]> Q = new List<int[]>();
Q.Add(endPos);

while(Q.Count > 0) {
    int minIndex = 0;
    for (int i = 0; i < Q.Count; i++) {
        if (steps[Q[i][0], Q[i][1]] < steps[Q[minIndex][0], Q[minIndex][1]]) minIndex = i;
    }
    int x = Q[minIndex][0], y = Q[minIndex][1];
    Q.RemoveAt(minIndex);

    // if (startPos.SequenceEqual(new int[] {x, y})) {        
    //     Console.WriteLine(steps[x,y] + 1);
    //     break;
    // }
    if (lines[y][x] == 'a' || lines[y][x] == 'S') {
        startingSteps.Add(steps[x,y]);
    }

    int alt = steps[x,y] + 1;

    if (x < w-1 && (alt < steps[x+1, y] || steps[x+1,y] == -1) && grid[x+1,y] >= grid[x,y] -1) {
        steps[x+1, y] = alt;
        Q.Add(new int[] {x+1, y});
    }
    if (x > 0 && (alt < steps[x-1, y] || steps[x-1, y] == -1) && grid[x-1,y] >= grid[x,y] -1) {
        steps[x-1, y] = alt;
        Q.Add(new int[] {x-1, y});
    }    
    if (y < h-1 && (alt < steps[x, y+1] || steps[x, y+1] == -1) && grid[x,y+1] >= grid[x,y] -1) {
        steps[x, y+1] = alt;
        Q.Add(new int[] {x, y+1});
    }
    if (y > 0 && (alt < steps[x, y-1] || steps[x, y-1] == -1) && grid[x,y-1] >= grid[x,y] -1) {
        steps[x, y-1] = alt;
        Q.Add(new int[] {x, y-1});
    }
}

for (int j = 0; j < h; j++) {
    for (int i = 0; i < w; i++) {
        Console.Write(steps[i,j]);
        Console.Write(" ");
    }
    Console.WriteLine();
}

Console.WriteLine(startingSteps.Min() + 1);
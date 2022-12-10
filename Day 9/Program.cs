string[] lines = System.IO.File.ReadAllLines(@".\input.txt");

List<int[]> knotPositions = new List<int[]>();
List<int[]> tailPositions = new List<int[]>();
for (int i = 0; i < 10; i++) knotPositions.Add(new int[] {0,0}); // Max 1 for Part 1
tailPositions.Add(new int[] {0, 0});

void tailFromHeadMove(int[] headPos, int[] tailPos) {
    if (Math.Abs(headPos[0] - tailPos[0]) > 1) { 
        int Xdiff = headPos[0]-tailPos[0] > 0 ? 1 : -1;
        tailPos[0] += Xdiff;
        if (Math.Abs(headPos[1] - tailPos[1]) > 0) {
            int Ydiff = headPos[1]-tailPos[1] > 0 ? 1 : -1;
            tailPos[1] += Ydiff;
        }
    }
    if (Math.Abs(headPos[1] - tailPos[1]) > 1) {
        int Ydiff = headPos[1]-tailPos[1] > 0 ? 1 : -1;
        tailPos[1] += Ydiff;
        if (Math.Abs(headPos[0] - tailPos[0]) > 0) { 
            int Xdiff = headPos[0]-tailPos[0] > 0 ? 1 : -1;
            tailPos[0] += Xdiff;
        }
    }
}

bool sequenceExists(List<int[]> p, int[] q) {
    foreach (int[] pos in p) {
        bool exists = true;
        for (int i = 0; i < q.Length; i++) {
            if (q[i] != pos[i]) {
                exists = false;
                break;
            }
        }
        if (exists) return true;
    }
    return false;
}

for (int i = 0; i < lines.Length; i++) {
    string[] line = lines[i].Split(' ');
    int steps = Convert.ToInt32(line[1]);
    
    for (int j = 0; j < steps; j++) {
        // Move Head
        string dir = line[0];
        int[] headPos = knotPositions[0];
        if (dir == "R") headPos[0]++;
        if (dir == "L") headPos[0]--;
        if (dir == "U") headPos[1]++;
        if (dir == "D") headPos[1]--;
        // Console.WriteLine(dir + " step " + j);
        for (int k = 1; k < knotPositions.Count; k++) {
            tailFromHeadMove(knotPositions[k-1], knotPositions[k]);
            // Console.WriteLine("{0}, {1}", knotPositions[k][0], knotPositions[k][1]);            
        }
        int[] tailPos = knotPositions.Last();
        if (!sequenceExists(tailPositions, tailPos)) tailPositions.Add(new int[2] {tailPos[0], tailPos[1]});
    }

}

Console.WriteLine(tailPositions.Count());
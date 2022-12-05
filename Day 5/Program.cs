string[] lines = System.IO.File.ReadAllLines(@".\input.txt");
// int[] elf1 = Array.ConvertAll(line[0].Split(','), s => Convert.ToInt32(s));

int N = 9;
List<char>[] stacks = new List<char>[N];
for (int j = 0; j < N; j++) {
    stacks[j] = new List<char>();
}

bool receivedStacks = false;
for (int i = 0; i < lines.Length; i++) {  
    string line = lines[i]; 
    if (line == "") {
        receivedStacks = true;
        continue;
    }

    if (!receivedStacks) {
        for (int j = 0; j < N; j++) {
            int index = 1 + j*4;
            if (line[index] != ' ' && !Char.IsNumber(line[index])) stacks[j].Insert(0, line[index]);
        }
    } else {
        string[] split = line.Split(' ');
        int n = Convert.ToInt32(split[1]);
        int start = Convert.ToInt32(split[3]) - 1;
        int finish = Convert.ToInt32(split[5]) - 1;
        // for(int j = 0; j < n; j++) {
        //     int index = stacks[start].Count - 1;
        //     char move = stacks[start][index];
        //     stacks[start].RemoveAt(index);
        //     stacks[finish].Add(move);            
        // }
        int index = stacks[start].Count - n;
        for(int j = 0; j < n; j++) {
            char move = stacks[start][index];
            stacks[start].RemoveAt(index);
            stacks[finish].Add(move);            
        }
    }
}

for (int j = 0; j < N; j++) {
    Console.Write(stacks[j][stacks[j].Count-1]);
}



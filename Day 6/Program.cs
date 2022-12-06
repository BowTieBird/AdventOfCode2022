string[] lines = System.IO.File.ReadAllLines(@".\input.txt");
// int[] elf1 = Array.ConvertAll(line[0].Split(','), s => Convert.ToInt32(s));

string line = lines[0];
int N = 14; // 4
char[] prev = new char[N];
Array.Copy(line.ToCharArray(), 0, prev, 0, N);
for (int i = 0; i < line.Length; i++) {  
    char c = line[i];
    prev[(i+1) % N] = line[i];
    bool foundMatch = false;
    List<char> soFar = new List<char>();
    for (int j = 0; j < prev.Length; j++) {
        if (soFar.Contains(prev[j])) {
            foundMatch = true;
            break;
        }
        soFar.Add(prev[j]);
    }
    if (!foundMatch) {
        Console.WriteLine(i+1);
        break;
    }
}


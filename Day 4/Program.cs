string[] lines = System.IO.File.ReadAllLines(@".\input.txt");

// int[] x1 = Array.ConvertAll(line[0].Split(','), s => Convert.ToInt32(s));

int count = 0;
int count2 = 0;

for (int i = 0; i < lines.Length; i++) {    
    string[] line = lines[i].Split(',');
    int[] elf1 = Array.ConvertAll(line[0].Split('-'), s => Convert.ToInt32(s));
    int[] elf2 = Array.ConvertAll(line[1].Split('-'), s => Convert.ToInt32(s));

    // Check if one range contains the other
    if (elf1[0] <= elf2[0] && elf1[1] >= elf2[1] ||
        elf1[0] >= elf2[0] && elf1[1] <= elf2[1]) {
        count++;
    } 

    // Check if the ranges overlap
    if (elf1[1] >= elf2[0] && elf1[0] <= elf2[0] ||
        elf2[1] >= elf1[0] && elf2[0] <= elf1[0]) {
        count2++;
    }
}

Console.WriteLine(count);
Console.WriteLine(count2);

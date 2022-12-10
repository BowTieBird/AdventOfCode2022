string[] lines = System.IO.File.ReadAllLines(@".\input.txt");

int X = 1;
int cycle = 0;
int sum = 0;
char[] CRT = new char[40*6];
CRT[0] = '#';

for (int i = 0; i < lines.Length; i++) {
    string[] line = lines[i].Split(' ');
    if (line[0] == "noop") {
        doCycle();
    }
    if (line[0] == "addx") {
        doCycle();
        doCycle();
        X += Int32.Parse(line[1]);
    }

}


void doCycle() {
    cycle++;
    List<int> cyclesToPrint = new List<int> {20, 60, 100, 140, 180, 220};
    if (cyclesToPrint.Contains(cycle)) {
        int signalStrength = cycle * X;
        Console.WriteLine(signalStrength);
        sum += signalStrength;
    }
    int pos = (cycle-1) % 40;
    CRT[cycle-1] = Math.Abs(X - pos) <= 1 ? '#' : '.'; 
}

void drawScreen() {
    for (int i = 0; i < CRT.Length; i++) {
        Console.Write(CRT[i]);
        if ((i + 1) % 40 == 0) Console.WriteLine();
    }
}

Console.WriteLine(sum);
drawScreen();

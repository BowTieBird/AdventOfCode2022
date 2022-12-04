string[] lines = System.IO.File.ReadAllLines(@".\input.txt");

int[] maxcount = new int[3];
int count = 0;

foreach (string line in lines) {
    if (line == "") {
        for (int j = 0; j < maxcount.Length; j++) {
            if (count > maxcount[j]) {
                // Swap count and maxcount[j]
                int temp = maxcount[j];
                maxcount[j] = count;
                count = temp;
            }
        }
        count = 0;
    } else {
        count += Convert.ToInt32(line);
    }
}

Console.WriteLine(maxcount[0]);
Console.WriteLine(maxcount.Sum());
using System.Linq;
string[] lines = System.IO.File.ReadAllLines(@".\input.txt");
// int[] elf1 = Array.ConvertAll(line[0].Split(','), s => Convert.ToInt32(s));

// Array.Copy(line.ToCharArray(), 0, prev, 0, N);
List<string> filePath = new List<string>();
Dictionary<string, double> currentDirs = new Dictionary<string, double>();
Dictionary<string, double> allDirs = new Dictionary<string, double>();
currentDirs.Add("/", 0);

string makeFilePath(string f) {
    string s = "/" + string.Join('/', filePath);
    string t =  "/" + s;
    return t;
}

bool listingMode = false;
for (int i = 1; i < lines.Length; i++) {
    string[] line = lines[i].Split(' ');
    if (line[0] == "$") {
        listingMode = false;
        if (line[1] == "cd") {
            if (line[2] == "..") {
                // Console.WriteLine(currentDirs[string.Join('/', filePath)]);
                string mykey = "/" + string.Join('/', filePath);
                allDirs[mykey] = currentDirs[mykey];            
                currentDirs.Remove(filePath.Last());
                filePath.RemoveAt(filePath.Count-1);    
            } else {
                filePath.Add(line[2]);
                currentDirs.Add("/" + string.Join('/', filePath), 0);
                allDirs.Add("/" + string.Join('/', filePath), 0);
            }
        }
        if (line[1] == "ls") {
            listingMode = true;
        }
    } else if (listingMode) {
        if (line[0] == "dir") continue;
        foreach (string key in currentDirs.Keys) {
            currentDirs[key] += Convert.ToDouble(line[0]);
        }
    }
}

string s = "/" + string.Join('/', filePath);
allDirs[s] = currentDirs[s]; 

double count1 = 0;
foreach(string key in allDirs.Keys) {
    if (allDirs[key] < 100000) {
        count1 += allDirs[key];
    }
    // Console.Write(key + ": ");
    // Console.WriteLine(allDirs[key]);
}
Console.WriteLine(count1);
Console.WriteLine(currentDirs["/"]);

var value = from entry in allDirs
    orderby entry.Value ascending
    where entry.Value > 30000000 - (70000000 - currentDirs["/"])
    select entry;
Console.WriteLine(value.First());
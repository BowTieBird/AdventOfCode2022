string[] lines = System.IO.File.ReadAllLines(@".\input.txt");


int priority = 0;
// foreach (string line in lines) {
//     string first = line.Substring(0, line.Length/2);
//     for (int i = line.Length/2; i<line.Length; i++) {
//         if (first.Contains(line[i])) {
//             int p = line[i] - 'a' + 1;
//             Console.Write(line[i]);
//             Console.WriteLine(p);
//             if (p >= 1) { // lowercase
//                 priority += p;
//             } else {
//                 p = (line[i] - 'A') + 27;
//                 priority += p;
//                 Console.WriteLine(p);
//             }
//             break;
//         }
//     }
// }

for (int j = 0; j < lines.Length; j++) {
    if (j % 3 != 0) {
        continue;
    }

    string line  = lines[j]; 
    string nextline = lines[j+1];
    string nnextline = lines[j+2];
    
    for (int i = 0; i<line.Length; i++) {
        if (nextline.Contains(line[i])) {
            if (nnextline.Contains(line[i])) {
                int p = line[i] - 'a' + 1;
                if (p >= 1) { // lowercase
                    priority += p;
                } else {
                    p = (line[i] - 'A') + 27;
                    priority += p;
                }
                break;
            }
        }
    }
}

Console.WriteLine(priority);
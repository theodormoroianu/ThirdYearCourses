#include <bits/stdc++.h>
using namespace std;


int main()
{
    int n;
    cout << "Nr of shifts: ";
    cin >> n;

    vector <int> c(n), s(n);

    cout << "coeficients:\n";
    for (int i = 0; i < n; i++) {
        cout << "  c[" << i + 1 << "] = ";
        cin >> c[i];
    }

    cout << "initial state:\n";
    for (int i = 0; i < n; i++) {
        cout << "  s[" << i << "] = ";
        cin >> s[i];
    }

    for (int t = 0; t < 100; t++) {
        cout << s[t] << ' ';
        int v = 0;
        for (int i = 0; i < n; i++)
            v ^= c[i] * s[t + n - i - 1];
        s.push_back(v);
    }
    
}
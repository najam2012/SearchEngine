#include<iostream> 
using namespace std;

int main() {
    freopen("input.txt", "r", stdin);
    freopen("output.txt", "w", stdout);

    int n;
    bool trans = true;
    cin >> n;

    int **m = new int*[n];
    for (int i = 0; i < n; i++) {
        m[i] = new int[n];
    }

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cin >> m[i][j];
        }
    }

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; i < n; i++)
            {
                if (!(m[i][j] == 1 && m[j][k] == 1 && m[k][i] == 1))
                    trans = false;
            }
        }
    }

    if (trans)
        cout << 1;
    else
        cout << 0;
}
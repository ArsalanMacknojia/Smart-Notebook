#include <bits/stdc++.h>
#include<cmath>
using namespace std;

// Fibonacci Sequence
int sequence[1000];
int fibonacci(int n)
{
    // base case
    if (n <= 1) return n;

    // check list
    if (sequence[n] != 0) return sequence[n];

    // calculate value if it's not in the list
    sequence[n] = fibonacci(n - 1) + fibonacci(n - 2);
    return sequence[n];
}

// Quadratic Roots
float *findRoots(int a, int b, int c)
{
    static float result[2];
    float discriminant, realPart, imaginaryPart, x1, x2;

    if (a == 0){
       cout << "This is not a quadratic equation" << endl;
       return result;
    }

     discriminant = b*b - 4*a*c;

     if (discriminant > 0)
     {
         cout << "Roots are real and different." << endl;
         result[0] = (-b + sqrt(discriminant)) / (2*a);
         result[1] = (-b - sqrt(discriminant)) / (2*a);
     }
     else if (discriminant == 0)
     {
         cout << "Roots are real and same." << endl;
         result[0] = (-b + sqrt(discriminant)) / (2*a);
         result[1] = (-b + sqrt(discriminant)) / (2*a);
     }
     else // discriminant < 0
     {
              cout << "Roots are complex and different." << endl;

         result[0] = (float) -b/(2*a);
         result[1] = sqrt(-discriminant)/(2*a);
     }
     return result;
}


extern "C" {
    int fib(int n) {return fibonacci(n);}
}

extern "C" {
    float *quadRoots(int a, int b, int c) {return findRoots(a, b, c);}
}
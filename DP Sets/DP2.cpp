#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;

int main()
{
    int n;cin>>n;

    vector<int> memo1(n+1,0);
    vector<char> input(n),memo2(n+1,'\0');

    for(int i=0;i<n;i++)
        cin>>input[i];

    for(int i=n-1;i>=0;i--)
    {
        int record1=1;
        char record2=input[i];
        for(int j=i+1;j<=n;j++)
        {
            if(memo2[j]=='\0' or input[i]<memo2[j])
            {
                int temp=memo1[j]+1;
                if(temp>record1)
                {
                    record1=temp;
                    record2=input[i];
                }
            }
        }
        memo1[i]=record1;
        memo2[i]=record2;
    }

    int Max=0;
    for(int i=0;i<=n;i++)
        Max=max(Max,memo1[i]);

    cout<<Max<<'\n';
    return 0;
}
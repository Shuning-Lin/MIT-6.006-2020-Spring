#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;

int main()
{
    int n;cin>>n;
    vector<int> temp(n+3,0);
    vector<int> record(n+3,0);
    for(int i=0;i<n;i++)
        cin>>temp[i];

    for(int i=n-1;i>=0;i--)
    {
        int s1=record[i+1];
        int s2=temp[i]+record[i+2];
        int s3=temp[i]+temp[i+1]+record[i+3];
        record[i]=max(max(s1,s2),s3);
    }
    
    cout<<record[0];
    return 0;
}
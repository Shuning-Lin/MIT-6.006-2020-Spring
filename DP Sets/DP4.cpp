#include<iostream>
#include<string>
#include<algorithm>
#include<vector>
using namespace std;

string s1,s2;
vector<vector<int>> memo; 

int dp(int index1,int index2)
{
    if(index1==-1 or index2==-1)
        return 0;

    if(memo[index1][index2]!=-1) 
        return memo[index1][index2];

    if(s1[index1]==s2[index2])
        return memo[index1][index2]=dp(index1-1,index2-1)+1;
    else
        return memo[index1][index2]=max(dp(index1-1,index2),dp(index1,index2-1));
}

int main()
{
    cin>>s1;
    cin>>s2;

    memo.assign(s1.length(),vector<int>(s2.length(),-1));  

    cout<<dp(s1.length()-1,s2.length()-1);

    return 0;

}